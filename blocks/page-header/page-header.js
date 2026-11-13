/**
 * Page title band with a breadcrumb line.
 * Row 1: the page title. Row 2 (optional): breadcrumb text.
 * @param {Element} block The page-header block
 */
export default function decorate(block) {
  const [titleRow, crumbRow] = [...block.children];
  const h1 = titleRow?.querySelector('h1, h2');
  const title = document.createElement('h1');
  title.textContent = h1 ? h1.textContent : titleRow?.textContent.trim();
  const crumbs = crumbRow ? crumbRow.firstElementChild?.innerHTML : '';
  block.textContent = '';
  block.append(title);
  if (crumbs) {
    const wrap = document.createElement('div');
    wrap.className = 'page-header-crumbs';
    const p = document.createElement('p');
    // keep the source's nested span structure: links, then the current page
    const outer = document.createElement('span');
    const parts = crumbs.replace(/^<p>|<\/p>$/g, '').split(/(?<=<\/a>)\s+/);
    parts.forEach((part, i) => {
      const span = document.createElement('span');
      span.innerHTML = part;
      if (i === parts.length - 1) span.setAttribute('aria-current', 'page');
      if (i) outer.append(' ');
      outer.append(span);
    });
    p.append(outer);
    wrap.append(p);
    block.dataset.crumbs = 'true';
    block.after(wrap);
  }
}
