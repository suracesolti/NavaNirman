const toggleButtons = document.querySelectorAll('.nav-toggle');

toggleButtons.forEach((button) => {
  const targetId = button.dataset.target;
  if (!targetId) return;
  const nav = document.getElementById(targetId);
  if (!nav) return;

  button.addEventListener('click', () => {
    nav.classList.toggle('active');
  });
});
