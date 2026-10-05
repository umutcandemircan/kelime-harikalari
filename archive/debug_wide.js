
  const wide = [];
  document.querySelectorAll('*').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.right > 360) {
      wide.push({ tag: el.tagName, id: el.id, class: el.className, right: r.right, width: r.width });
    }
  });
  console.log('WIDE_ELEMENTS:' + JSON.stringify(wide));
