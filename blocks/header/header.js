import { getMetadata } from '../../scripts/aem.js';
import { loadFragment } from '../fragment/fragment.js';

const mobile = window.matchMedia('(max-width: 899px)');

function closeAll(list) {
  list.querySelectorAll('li.nav-drop').forEach((li) => li.setAttribute('aria-expanded', 'false'));
}

/**
 * loads and decorates the header
 * @param {Element} block The header block element
 */
export default async function decorate(block) {
  const navMeta = getMetadata('nav');
  const navPath = navMeta ? new URL(navMeta, window.location).pathname : '/nav';
  const fragment = await loadFragment(navPath);

  block.textContent = '';
  const bar = document.createElement('div');
  bar.className = 'header-bar';

  const logo = document.createElement('a');
  logo.href = '/';
  logo.className = 'header-logo';
  logo.innerHTML = '<img src="/images/logo.png" alt="Company Logo" width="172" height="58">';
  bar.append(logo);

  const nav = document.createElement('nav');
  nav.id = 'nav';
  nav.setAttribute('aria-label', 'Main');
  const list = fragment.querySelector('ul');
  if (list) {
    // DA wraps nested list text as <li><p><a>: unwrap the paragraphs
    list.querySelectorAll('li > p').forEach((p) => p.replaceWith(...p.childNodes));
    list.querySelectorAll(':scope > li').forEach((li) => {
      const sub = li.querySelector(':scope > ul');
      if (!sub) return;
      li.classList.add('nav-drop');
      li.setAttribute('aria-expanded', 'false');
      const top = li.querySelector(':scope > a');
      top?.addEventListener('click', (e) => {
        if (top.getAttribute('href') === '#' || mobile.matches) {
          e.preventDefault();
          const open = li.getAttribute('aria-expanded') === 'true';
          closeAll(list);
          li.setAttribute('aria-expanded', open ? 'false' : 'true');
        }
      });
    });
    const current = list.querySelector(`a[href="${window.location.pathname}"]`);
    if (current) current.setAttribute('aria-current', 'page');
    nav.append(list);
  }
  bar.append(nav);

  const toggle = document.createElement('button');
  toggle.type = 'button';
  toggle.className = 'header-toggle';
  toggle.setAttribute('aria-label', 'Menu');
  toggle.setAttribute('aria-expanded', 'false');
  toggle.innerHTML = '<span></span>';
  toggle.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') === 'true';
    toggle.setAttribute('aria-expanded', open ? 'false' : 'true');
    bar.classList.toggle('is-open', !open);
  });
  bar.append(toggle);
  block.append(bar);
}
