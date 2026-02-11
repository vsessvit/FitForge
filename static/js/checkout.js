/*
    Stripe Elements JavaScript
*/

// Get Stripe public key from template
var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();

// Custom styling for card element
var style = {
    base: {
        color: '#000',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};

// Create card element and mount it
var card = elements.create('card', {style: style});
card.mount('#card-element');

// Handle real-time validation errors on the card element
card.addEventListener('change', function (event) {
    var errorDiv = document.getElementById('card-errors');
    if (event.error) {
        var html = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
        `;
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    }
});

// Handle form submit
var form = document.getElementById('payment-form');

form.addEventListener('submit', function(ev) {
    ev.preventDefault();
    
    // Disable card element and submit button
    card.update({ 'disabled': true});
    $('#submit-button').attr('disabled', true);
    
    // Get CSRF token
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    
    // Get client secret from server
    $.ajax({
        url: '/checkout/create_payment_intent/',
        type: 'POST',
        headers: {'X-CSRFToken': csrfToken},
        success: function(response) {
            // Confirm card payment with Stripe
            stripe.confirmCardPayment(response.clientSecret, {
                payment_method: {
                    card: card,
                }
            }).then(function(result) {
                if (result.error) {
                    // Show error to customer
                    var errorDiv = document.getElementById('card-errors');
                    var html = `
                        <span class="icon" role="alert">
                            <i class="fas fa-times"></i>
                        </span>
                        <span>${result.error.message}</span>
                    `;
                    $(errorDiv).html(html);
                    
                    // Re-enable card element and submit button
                    card.update({ 'disabled': false});
                    $('#submit-button').attr('disabled', false);
                } else {
                    // Payment succeeded, submit form
                    if (result.paymentIntent.status === 'succeeded') {
                        form.submit();
                    }
                }
            });
        },
        error: function(error) {
            // Show error
            var errorDiv = document.getElementById('card-errors');
            $(errorDiv).html(`<span>Error creating payment. Please try again.</span>`);
            
            // Re-enable elements
            card.update({ 'disabled': false});
            $('#submit-button').attr('disabled', false);
        }
    });
});
