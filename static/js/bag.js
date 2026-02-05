// Handle quantity input increment and decrement
document.addEventListener('DOMContentLoaded', function() {
    // Increment quantity
    const incrementButtons = document.querySelectorAll('.increment-qty');
    incrementButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const input = this.closest('.quantity-control').querySelector('.qty_input');
            const currentValue = parseInt(input.value);
            const maxValue = parseInt(input.getAttribute('max'));
            
            if (currentValue < maxValue) {
                input.value = currentValue + 1;
            }
        });
    });

    // Decrement quantity
    const decrementButtons = document.querySelectorAll('.decrement-qty');
    decrementButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const input = this.closest('.quantity-control').querySelector('.qty_input');
            const currentValue = parseInt(input.value);
            const minValue = parseInt(input.getAttribute('min'));
            
            if (currentValue > minValue) {
                input.value = currentValue - 1;
            }
        });
    });

    // Update quantity on form submit
    const updateForms = document.querySelectorAll('.update-form');
    updateForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            this.submit();
        });
    });

    // Remove item button
    const removeButtons = document.querySelectorAll('.remove-item');
    removeButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const url = this.getAttribute('data-url');
            window.location.href = url;
        });
    });
});
