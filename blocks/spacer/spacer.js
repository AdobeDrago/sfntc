/**
 * Empty vertical gap, one paragraph high.
 * @param {Element} block The spacer block
 */
export default function decorate(block) {
  block.setAttribute('aria-hidden', 'true');
  block.textContent = '';
}
