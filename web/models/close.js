// "Close" button for full-screen interactive models: back to where the visitor came from.
(function () {
  if (window.self !== window.top) return; // embedded in an iframe on the site: no close button
  var b = document.createElement('a');
  b.className = 'model-close'; b.textContent = '✕ Close'; b.href = '/insights/#models';
  b.setAttribute('aria-label', 'Close the model and go back');
  b.style.cssText = 'position:fixed;bottom:16px;right:16px;z-index:9999;background:#111;color:#f4f1ea;font:700 13px/1 Inter,Arial,sans-serif;letter-spacing:.06em;padding:11px 14px;border-radius:22px;text-decoration:none;box-shadow:0 2px 10px rgba(0,0,0,.25)';
  b.addEventListener('click', function (e) {
    if (document.referrer && document.referrer.indexOf(location.origin) === 0 && history.length > 1) { e.preventDefault(); history.back(); }
  });
  document.body.appendChild(b);
})();
