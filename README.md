# Harbor Notes — Voicedot Review Demo

A small, fictitious website for testing the complete Voicedot workflow:

**Leave page feedback → ask a coding agent for a fix → inspect and authorize the
change → deploy it → personally review the result.**

Maintained by **Good Sheet Sp z o.o.**, the company behind Voicedot. This
repository is the editable sample website. The plugin package lives in
[voicedot/voicedot-agent-plugin](https://github.com/voicedot/voicedot-agent-plugin).

| Start here | Link |
| --- | --- |
| Live coding demo | [review.voicedot.ai](https://review.voicedot.ai/) |
| Source and working branch | [voicedot/voicedot-review-demo · review](https://github.com/voicedot/voicedot-review-demo/tree/review) |
| Plugin package | [voicedot/voicedot-agent-plugin](https://github.com/voicedot/voicedot-agent-plugin) |
| Dedicated demo-account sign-in | [Reviewer login](https://app.voicedot.ai/reviewer/login/) |
| Public deployment revision | [deployment.json](https://review.voicedot.ai/deployment.json) |
| Product and integration guide | [Voicedot MCP guide](https://voicedot.ai/en/docs/mcp) |

## Before you start

- Anyone can open the website and download or clone this public source.
- To read feedback through the plugin, connect the dedicated demo account using
  the private reviewer sign-in instructions supplied with the submission.
- To publish a code change to this shared website, use the separately supplied,
  repository-limited GitHub access. A Voicedot connection alone does not grant
  GitHub write access. A push to your own fork does not update this preview.
- The `.voicedot.json` file selects Harbor Notes; it does not authorize access.
  Repository-write and account credentials belong in secure credential storage,
  never in this repository, remote URLs, commands, screenshots or chat messages.

The shared website may already contain a fix from an earlier rehearsal. Check
its current state before choosing a comment. The repeatable contrast example is
described below; a previous Checked item is not a new request.

## 1. Open the working repository

```sh
git clone --branch review https://github.com/voicedot/voicedot-review-demo.git
cd voicedot-review-demo
git status
```

For an existing checkout, fetch and inspect the current `review` branch before
editing. Preserve another reviewer's work.

| Branch | Role |
| --- | --- |
| **`review`** | Default branch, current shared website source, and the only branch the publishing workflow deploys |
| **`main`** | Locked original website baseline; do not push or merge changes into it |

No npm install, paid service, application backend or local secrets file is
needed. The checks and publisher use Python 3's standard library.

## 2. Leave one real comment on the live page

Open **https://review.voicedot.ai/**, open the feedback widget, select the element
you mean and send a comment. For a contrast rehearsal, pin the primary button
and write:

> Please make the Start a workspace button easier to read by using a darker green.

Send the first feedback yourself. Opening the page only verifies installation;
it does not create a feedback message.

## 3. Ask your coding agent to inspect it

Use a coding agent with this repository open and the dedicated Voicedot account
connected. A suitable request is:

> Read the new Harbor Notes feedback from https://review.voicedot.ai about the
> Start a workspace button. Show the page context and propose the smallest fix.
> Do not edit or publish yet.

The exact address matters. The separate fixtures
[Harbor Notes](https://app.voicedot.ai/reviewer/demo/harbor-notes/) and
[Fieldwork Notes](https://app.voicedot.ai/reviewer/demo/fieldwork-notes/) are used
for conversation and team-handover cases; this repository does not publish
changes to those pages.

## 4. Authorize, inspect and test the code change

After reviewing the proposal, explicitly authorize the change **and publication
to this demo repository**. For the contrast example, change only the primary
button background in `site/styles.css`; preserve its label and layout.

Inspect the diff, check the affected page in a real browser, and run:

```sh
python3 -m unittest discover -s tests -v
git diff --check
git diff
```

These checks cover the publication boundary, one-time widget installation,
public project binding and revision-specific assets. They do not replace
checking the deployed page.

## 5. Publish and verify the exact revision

With authorized GitHub access, commit the reviewed files and push:

```sh
git push origin review
git rev-parse HEAD
```

1. Open [GitHub Actions](https://github.com/voicedot/voicedot-review-demo/actions)
   and wait for **Publish review website** to succeed for that commit.
2. Open [deployment.json](https://review.voicedot.ai/deployment.json). Its full
   `commit` must equal `git rev-parse HEAD`; its `branch` must be `review`.
3. Open the actual HTTPS website and inspect the changed element. The footer
   shows the deployed revision and links to its commit in this repository.

A successful push, local screenshot or green test alone does not establish
that the public site contains the change. If the revision differs, wait for the
matching deployment and check again before preparing a review round.

## 6. Review the deployed change as a person

Ask the agent to prepare a review round for the exact changed feedback thread,
including the public page address, deployed commit and what to check. Review
the preview and explicitly confirm creation of that round.

Open the returned Voicedot review link, use **Open this place**, inspect the
actual result, and personally choose **Checked** or **Needs fix**. The agent
must not manufacture the first feedback, mark your review decision, or resolve
unrelated discussions just to make the demonstration look complete.

## Repeat the contrast example without rewriting history

The original primary button background is `#b8c6bb`; the example fix uses
`#23523f`. If the shared preview is already dark, the person authorizing the
rehearsal can authorize a new commit on `review` restoring **only that button's
background** to `#b8c6bb`.

Run the same checks, publish and verify that baseline commit first. Then send
a fresh, identifiable human comment and start the cycle above. Preserve the
existing fixes, publisher, history, feedback and previous human decisions.
Do not reset the branch to `main`, force-push, delete feedback, or pretend the
same completed item is still open. Check that no other reviewer is using the
shared branch before starting another rehearsal.

## Repository and publication design

| Path | Purpose |
| --- | --- |
| `site/index.html` | Fictitious Harbor Notes page and single widget installation |
| `site/styles.css` | Website styles and the button-contrast example |
| `site/deployment.js` | Reads the page's revision manifest and displays its commit |
| `.voicedot.json` | Public project reference for the coding agent |
| `scripts/build_site.py` | Builds the bounded static output and exact revision manifests |
| `tests/test_publication.py` | Lightweight publication-boundary tests |
| `.github/workflows/publish.yml` | Pinned GitHub Pages actions, restricted to `review` |
| `AGENTS.md` | Instructions and authorization boundaries for coding agents |

Only four explicit static sources and generated deployment manifests are
published. Styles and scripts have content-hashed names; the HTML refers to a
revision-specific manifest so cached assets cannot claim a newer deployment.
The publisher contains no Voicedot or Cloudflare credential. Deployment uses
short-lived GitHub permissions scoped to this Pages repository.

For an optional local layout check:

```sh
python3 -m http.server 4391 --directory site
```

Open http://localhost:4391. This HTTP preview checks layout only; widget
collection must be verified on the exact authorized public HTTPS origin.

## Access and support

Reviewer write access is limited to **this repository**, with Contents
read/write and Metadata read. It does not include Workflows, Administration or
other repositories. The locked baseline branch remains protected. Provide and
renew the credential through the private reviewer channel; never add it here.

This is a sample website, not the Voicedot backend or MCP server. New-account
registration uses the separate official CLI workflow described in
[Agent setup](https://voicedot.ai/en/docs/agents). The plugin does not perform
purchases or choose the person's plan.

For integration, reviewer-access or reproducible page problems, use
[Voicedot support](https://voicedot.ai/en/support). Include the page URL and
deployed commit; omit credentials and private visitor content.

## License

[MIT](LICENSE).
