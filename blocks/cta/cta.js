/**
 * Call-to-action panels. Variants: image (photo left, text right),
 * banner (text over a full-width photo), dual (two side-by-side cards).
 * @param {Element} block The cta block
 */
export default function decorate(block) {
  const rows = [...block.children];
  const decorateButtons = (root) => root.querySelectorAll('p > a:only-child').forEach((a) => {
    a.classList.add('button');
  });
  if (block.classList.contains('dual')) {
    const inner = document.createElement('div');
    inner.className = 'cta-cards';
    rows.forEach((row) => {
      const card = document.createElement('div');
      card.className = 'cta-card';
      card.append(...row.firstElementChild.childNodes);
      decorateButtons(card);
      inner.append(card);
    });
    block.textContent = '';
    block.append(inner);
    return;
  }
  const [imageRow, contentRow] = rows;
  const media = document.createElement('div');
  media.className = 'cta-media';
  const img = imageRow?.querySelector('img');
  if (img) {
    // the photo is painted as a CSS background (no img element), like the source
    media.style.backgroundImage = `url("${img.currentSrc || img.src}")`;
  }
  const text = document.createElement('div');
  text.className = 'cta-text';
  const inner = document.createElement('div');
  inner.className = 'cta-inner';
  if (contentRow) inner.append(...contentRow.firstElementChild.childNodes);
  decorateButtons(inner);
  if (block.classList.contains('banner')) inner.querySelectorAll('a.button').forEach((a) => a.classList.add('alt'));
  text.append(inner);
  block.textContent = '';
  block.append(media, text);
}
