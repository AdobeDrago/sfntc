/**
 * Statistic carousel: each row is one slide (heading + sub heading).
 * All slides share one grid cell so the block is as tall as the tallest slide.
 * @param {Element} block The carousel block
 */
export default function decorate(block) {
  const slides = [...block.children];
  const dots = document.createElement('div');
  dots.className = 'carousel-dots';
  const show = (index) => {
    slides.forEach((slide, i) => {
      slide.classList.toggle('is-active', i === index);
      slide.setAttribute('aria-hidden', i === index ? 'false' : 'true');
    });
    [...dots.children].forEach((dot, i) => {
      dot.classList.toggle('is-active', i === index);
      dot.setAttribute('aria-current', i === index ? 'true' : 'false');
    });
  };
  slides.forEach((slide, i) => {
    slide.classList.add('carousel-slide');
    const content = document.createElement('div');
    content.className = 'carousel-content';
    content.append(...slide.firstElementChild.childNodes);
    slide.textContent = '';
    slide.append(content);
    const dot = document.createElement('button');
    dot.type = 'button';
    dot.setAttribute('aria-label', `Go to slide ${i + 1}`);
    dot.addEventListener('click', () => show(i));
    dots.append(dot);
  });
  block.append(dots);
  show(0);
}
