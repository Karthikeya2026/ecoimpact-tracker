// Basic form validation
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', (e) => {
        const inputs = form.querySelectorAll('input[type="number"]');
        inputs.forEach(input => {
            if (input.value < 0) {
                e.preventDefault();
                alert('Please enter non-negative values.');
            }
        });
    });
});