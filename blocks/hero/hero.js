/**
 * Home hero: full-bleed photo with a translucent text card.
 * Row 1: image. Row 2: heading, text, call to action.
 * @param {Element} block The hero block
 */
export default function decorate(block) {
  const [imageRow, contentRow] = [...block.children];
  const picture = imageRow?.querySelector('picture');
  const card = document.createElement('div');
  card.className = 'hero-card';
  if (contentRow) card.append(...contentRow.firstElementChild.childNodes);
  card.querySelectorAll('p > a').forEach((a) => a.classList.add('button'));
  block.textContent = '';
  const img = picture?.querySelector('img');
  if (img) {
    // the photo is painted as a CSS background (no img element), like the source
    const media = document.createElement('div');
    media.className = 'hero-media';
    media.style.backgroundImage = `url("${img.currentSrc || img.src}")`;
    block.append(media);
  }
  block.append(card);
}
