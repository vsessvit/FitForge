// Bookings JavaScript for FitForge

// Cancel booking functionality (placeholder for future implementation)
document.addEventListener('DOMContentLoaded', function() {
    const cancelButtons = document.querySelectorAll('.cancel-booking-btn');
    
    cancelButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const bookingId = this.dataset.bookingId;
            if (confirm('Are you sure you want to cancel this booking?')) {
                alert('Cancel booking functionality will be implemented in the next phase.');
                // Future: AJAX request to cancel booking endpoint
                // cancelBooking(bookingId);
            }
        });
    });
});

// Future function for AJAX cancel booking
// function cancelBooking(bookingId) {
//     fetch(`/bookings/cancel/${bookingId}/`, {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//             'X-CSRFToken': getCookie('csrftoken')
//         },
//     })
//     .then(response => response.json())
//     .then(data => {
//         if (data.success) {
//             location.reload();
//         }
//     })
//     .catch(error => console.error('Error:', error));
// }
