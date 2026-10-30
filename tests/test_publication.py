"""Bounded publication checks: no backend or paid services are used."""
import importlib.util
import hashlib
import json
from pathlib import Path
import unittest
import shutil
import tempfile
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("build_site", ROOT / "scripts/build_site.py")
publisher = importlib.util.module_from_spec(spec)
spec.loader.exec_module(publisher)


class PublicationTests(unittest.TestCase):
    def test_no_unexpected_files_or_symlinks_are_published(self):
        source = ROOT / "site"
        self.assertEqual({p.name for p in source.iterdir()}, publisher.ALLOWED)
        self.assertTrue(all(p.is_file() and not p.is_symlink() for p in source.iterdir()))

    def test_only_review_branch_can_publish(self):
        with self.assertRaisesRegex(ValueError, "Only the review"):
            publisher.build("a" * 40, "main", ROOT / "dist")

    def test_commit_is_not_an_arbitrary_url_or_shell_value(self):
        for value in ["main", "abc", "https://example.com", "$(echo bad)", "A" * 40]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                publisher.build(value, "review", ROOT / "dist")

    def test_output_cannot_escape_the_repository(self):
        with self.assertRaisesRegex(ValueError, "Output must"):
            publisher.build("a" * 40, "review", ROOT.parent / "somewhere-else")

    def test_widget_appears_once_and_after_its_configuration(self):
        html = (ROOT / "site/index.html").read_text()
        loader = 'src="https://app.voicedot.ai/widget/v1/voicedot.js"'
        self.assertEqual(html.count(loader), 1)
        self.assertEqual(html.count("window.VOICEDOT_CONFIG ="), 1)
        self.assertLess(html.index("window.VOICEDOT_CONFIG ="), html.index(loader))
        self.assertNotIn("{{", html)
        self.assertNotIn("{%", html)

    def test_each_html_uses_matching_assets_and_revision_manifest(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            shutil.copytree(ROOT / "site", root / "site")
            with patch.object(publisher, "ROOT", root):
                publisher.build("a" * 40, "review", root / "dist")
                html = (root / "dist/index.html").read_text()
                for name in ("styles.css", "deployment.js"):
                    digest = hashlib.sha256((root / "site" / name).read_bytes()).hexdigest()[:16]
                    versioned = f"{Path(name).stem}.{digest}{Path(name).suffix}"
                    self.assertIn(f'./{versioned}"', html)
                    self.assertEqual((root / "dist" / versioned).read_bytes(),
                                     (root / "site" / name).read_bytes())
                manifest = f"deployment.{'a' * 40}.json"
                self.assertIn(f'data-manifest="./{manifest}"', html)
                self.assertEqual(json.loads((root / "dist" / manifest).read_text())["commit"], "a" * 40)
                (root / "site/styles.css").write_text(".button { color: green; }")
                publisher.build("b" * 40, "review", root / "dist")
                changed = (root / "dist/index.html").read_text()
                self.assertNotEqual(html, changed)
                self.assertIn(f"deployment.{'b' * 40}.json", changed)
                self.assertFalse((root / "dist" / manifest).exists())
                self.assertEqual(json.loads((root / "dist/deployment.json").read_text())["commit"], "b" * 40)

    def test_export_example_uses_versioned_assets_and_same_public_widget(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            shutil.copytree(ROOT / "site", root / "site")
            with patch.object(publisher, "ROOT", root):
                publisher.build("a" * 40, "review", root / "dist")
            html = (root / "dist/needs-fix.html").read_text()
            self.assertIn(f'data-manifest="./deployment.{"a" * 40}.json"', html)
            self.assertNotIn('href="./styles.css"', html)
            self.assertNotIn('src="./deployment.js"', html)
            self.assertEqual(html.count("window.VOICEDOT_CONFIG ="), 1)
            self.assertEqual(html.count('src="https://app.voicedot.ai/widget/v1/voicedot.js"'), 1)
            self.assertIn('download="weekly-sync.md"', html)
            self.assertIn("Download Markdown", html)

    def test_binding_is_only_a_public_project_reference(self):
        self.assertEqual(json.loads((ROOT / ".voicedot.json").read_text()),
                         {"version": 1, "projectId": "vd_project_50"})


if __name__ == "__main__":
    unittest.main()
