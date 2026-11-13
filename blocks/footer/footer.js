import { getMetadata } from '../../scripts/aem.js';
import { loadFragment } from '../fragment/fragment.js';

/**
 * loads and decorates the footer
 * @param {Element} block The footer block element
 */
export default async function decorate(block) {
  const footerMeta = getMetadata('footer');
  const footerPath = footerMeta ? new URL(footerMeta, window.location).pathname : '/footer';
  const fragment = await loadFragment(footerPath);

  block.textContent = '';
  const nav = document.createElement('nav');
  nav.className = 'footer-nav';
  const copy = fragment.querySelector('p');
  const list = fragment.querySelector('ul');
  if (copy) {
    const span = document.createElement('span');
    span.textContent = copy.textContent;
    nav.append(span);
  }
  if (list) {
    list.querySelectorAll('li > p').forEach((p) => p.replaceWith(...p.childNodes));
    const links = document.createElement('div');
    links.className = 'footer-links';
    links.append(list);
    nav.append(links);
  }
  block.append(nav);
}
