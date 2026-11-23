// Tap-to-zoom images open in an overlay with a close button instead of a new tab.
(function () {
  var box;
  function close() { if (box) { box.remove(); box = null; document.body.style.overflow = ''; } }
  function open(src, alt) {
    close();
    box = document.createElement('div');
    box.className = 'lightbox';
    box.setAttribute('role', 'dialog');
    box.setAttribute('aria-label', alt || 'Image');
    box.innerHTML = '<button type="button" class="lb-close" aria-label="Close">✕</button><div class="lb-scroll"><img alt=""></div>';
    box.querySelector('img').src = src;
    box.querySelector('img').alt = alt || '';
    box.addEventListener('click', function (e) { if (e.target === box || e.target.classList.contains('lb-close') || e.target.classList.contains('lb-scroll')) close(); });
    document.body.appendChild(box);
    document.body.style.overflow = 'hidden';
    box.querySelector('.lb-close').focus();
  }
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a.zoom');
    if (!a || e.ctrlKey || e.metaKey || e.shiftKey) return;
    e.preventDefault();
    var img = a.querySelector('img');
    open(a.getAttribute('href'), img ? img.alt : '');
  });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
})();
// Back-to-top button: appears after scrolling down, on every page.
(function () {
  var b = document.createElement('button');
  b.type = 'button'; b.className = 'to-top'; b.setAttribute('aria-label', 'Back to top'); b.textContent = '↑';
  b.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: 'smooth' }); });
  document.body.appendChild(b);
  function upd() { b.classList.toggle('show', window.scrollY > 700); }
  window.addEventListener('scroll', upd, { passive: true }); upd();
})();
