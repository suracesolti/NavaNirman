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

// Password validation on signup page
const passwordInput = document.getElementById('password-input');
if (passwordInput) {
  const requirements = {
    length: document.getElementById('req-length'),
    number: document.getElementById('req-number'),
    special: document.getElementById('req-special')
  };

  function updatePasswordRequirements() {
    const password = passwordInput.value;

    // Check each requirement
    const meetsLength = password.length >= 8;
    const meetsNumber = /\d/.test(password);
    const meetsSpecial = /[^A-Za-z0-9]/.test(password);

    // Update UI
    updateRequirement(requirements.length, meetsLength);
    updateRequirement(requirements.number, meetsNumber);
    updateRequirement(requirements.special, meetsSpecial);
  }

  function updateRequirement(element, isMet) {
    const icon = element.querySelector('.requirement-icon');
    if (isMet) {
      element.classList.add('met');
      icon.textContent = '✓';
    } else {
      element.classList.remove('met');
      icon.textContent = '✗';
    }
  }

  // Listen for input changes
  passwordInput.addEventListener('input', updatePasswordRequirements);
  
  // Initial update
  updatePasswordRequirements();
}

