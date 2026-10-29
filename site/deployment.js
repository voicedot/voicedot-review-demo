/* The publisher stamps this manifest after checkout, never from visitor input. */
(async () => {
  const link = document.getElementById('deployment-commit');
  const detail = document.getElementById('deployment-detail');
  try {
    const response = await fetch(link.dataset.manifest || './deployment.json', { cache: 'no-store' });
    if (!response.ok) throw new Error('Manifest unavailable');
    const deployment = await response.json();
    if (!/^[a-f0-9]{40}$/.test(deployment.commit)) throw new Error('Invalid revision');
    link.textContent = deployment.commit.slice(0, 12);
    link.href = `https://github.com/voicedot/voicedot-review-demo/commit/${deployment.commit}`;
    detail.textContent = `Branch: ${deployment.branch} · Published: ${deployment.builtAt}`;
  } catch {
    link.textContent = 'Local preview — no published commit';
    detail.textContent = 'A successful Pages deployment writes the revision manifest.';
  }
})();
