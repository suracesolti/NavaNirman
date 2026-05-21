const toggles = [
  {buttonId: 'navToggle', navId: 'mainNav'},
  {buttonId: 'navToggleAbout', navId: 'mainNavAbout'},
  {buttonId: 'navToggleCategories', navId: 'mainNavCategories'},
  {buttonId: 'navToggleProduct', navId: 'mainNavProduct'},
  {buttonId: 'navToggleContact', navId: 'mainNavContact'},
];

toggles.forEach(({ buttonId, navId }) => {
  const button = document.getElementById(buttonId);
  const nav = document.getElementById(navId);
  if (!button || !nav) return;

  button.addEventListener('click', () => {
    nav.classList.toggle('active');
  });
});
