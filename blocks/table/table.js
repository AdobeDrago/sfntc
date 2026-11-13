/**
 * Plain data table: first row is the header row.
 * @param {Element} block The table block
 */
export default function decorate(block) {
  const table = document.createElement('table');
  const thead = document.createElement('thead');
  const tbody = document.createElement('tbody');
  [...block.children].forEach((row, i) => {
    const tr = document.createElement('tr');
    [...row.children].forEach((cell) => {
      const el = document.createElement(i === 0 ? 'th' : 'td');
      // cells arrive wrapped in a paragraph: keep only the text/inline content
      const p = cell.querySelector(':scope > p');
      el.append(...(p || cell).childNodes);
      tr.append(el);
    });
    (i === 0 ? thead : tbody).append(tr);
  });
  table.append(thead, tbody);
  block.textContent = '';
  block.append(table);
}
