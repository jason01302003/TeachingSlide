/* 簡報：把每張投影片的 Markdown 顯示出來，並處理縮放與換頁。 */
(function () {
  const stage = document.getElementById('stage');
  const slides = [...document.querySelectorAll('.slide')];
  const bar = document.querySelector('#progress i');
  let current = 0;

  slides.forEach(sl => {
    const src = sl.querySelector('script[type="text/markdown"]');
    const body = sl.querySelector('.body');
    body.innerHTML = window.renderMarkdown(src.textContent.replace(/<\\\/script/g, '</script'), {
      link: t => '../wiki.html#' + t,
      cite: id => '../wiki.html#sources/' + id.toLowerCase(),
    });
    body.querySelectorAll('a').forEach(a => { a.target = a.classList.contains('wikilink') || a.classList.contains('cite') ? 'wiki' : '_blank'; a.rel = 'noopener'; });
  });

  function fit() {
    const scale = Math.min(window.innerWidth / 1280, (window.innerHeight - 44) / 720);
    stage.style.transform = `translate(-50%, -50%) scale(${scale})`;
  }

  function show(i) {
    current = Math.max(0, Math.min(slides.length - 1, i));
    slides.forEach((s, k) => s.classList.toggle('on', k === current));
    bar.style.width = ((current + 1) / slides.length * 100) + '%';
    if (location.hash !== '#' + (current + 1)) history.replaceState(null, '', '#' + (current + 1));
  }

  document.getElementById('prev').onclick = () => show(current - 1);
  document.getElementById('next').onclick = () => show(current + 1);
  document.addEventListener('keydown', e => {
    if (['ArrowRight', 'PageDown', ' ', 'Enter'].includes(e.key)) { show(current + 1); e.preventDefault(); }
    else if (['ArrowLeft', 'PageUp', 'Backspace'].includes(e.key)) { show(current - 1); e.preventDefault(); }
    else if (e.key === 'Home') show(0);
    else if (e.key === 'End') show(slides.length - 1);
  });
  let touchX = null;
  document.addEventListener('touchstart', e => { touchX = e.touches[0].clientX; }, { passive: true });
  document.addEventListener('touchend', e => {
    if (touchX === null) return;
    const dx = e.changedTouches[0].clientX - touchX;
    if (Math.abs(dx) > 50) show(current + (dx < 0 ? 1 : -1));
    touchX = null;
  });
  window.addEventListener('resize', fit);
  window.addEventListener('hashchange', () => show((parseInt(location.hash.slice(1), 10) || 1) - 1));

  /* 給檢查用：回報內容超出版面的投影片編號 */
  window.deckOverflow = () => slides.map((s, i) => {
    const was = s.classList.contains('on');
    s.classList.add('on');
    const b = s.querySelector('.body');
    const over = b.scrollHeight > b.clientHeight + 2 || b.scrollWidth > b.clientWidth + 2;
    if (!was) s.classList.remove('on');
    return over ? i + 1 : null;
  }).filter(Boolean);

  fit();
  show((parseInt(location.hash.slice(1), 10) || 1) - 1);
})();
