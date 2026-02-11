// Bookings JavaScript for FitForge

// Cancel booking functionality
document.addEventListener('DOMContentLoaded', function() {
    const cancelButtons = document.querySelectorAll('.cancel-booking-btn');
    
    cancelButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const bookingId = this.dataset.bookingId;
            // Redirect to cancel confirmation page
            window.location.href = `/bookings/cancel/${bookingId}/`;
        });
    });
});
