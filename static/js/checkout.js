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
    
    // Show loading overlay
    $('.loading-overlay').fadeIn();
    
    // Get CSRF token
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    
    // First, get the client secret from server
    $.ajax({
        url: '/checkout/create_payment_intent/',
        type: 'POST',
        headers: {'X-CSRFToken': csrfToken},
        success: function(paymentResponse) {
            var clientSecret = paymentResponse.clientSecret;
            
            // Then cache checkout data in the payment intent
            var saveInfo = Boolean($('#id-save-info').attr('checked'));
            var postData = {
                'csrfmiddlewaretoken': csrfToken,
                'client_secret': clientSecret,
                'save_info': saveInfo,
            };
            
            $.ajax({
                url: '/checkout/cache_checkout_data/',
                type: 'POST',
                data: postData,
                success: function(cacheResponse) {
                    // Finally, confirm card payment with Stripe
                    stripe.confirmCardPayment(clientSecret, {
                        payment_method: {
                            card: card,
                            billing_details: {
                                name: $.trim(form.full_name.value),
                                phone: $.trim(form.phone_number.value),
                                email: $.trim(form.email.value),
                                address: {
                                    line1: $.trim(form.street_address1.value),
                                    line2: $.trim(form.street_address2.value),
                                    city: $.trim(form.town_or_city.value),
                                    state: $.trim(form.county.value),
                                    postal_code: $.trim(form.postcode.value),
                                    country: $.trim(form.country.value),
                                }
                            }
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
                            
                            // Hide loading overlay
                            $('.loading-overlay').fadeOut();
                            
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
                error: function(cacheError) {
                    // Reload page, error will be shown in messages
                    location.reload();
                }
            });
        },
        error: function(error) {
            // Show error
            var errorDiv = document.getElementById('card-errors');
            $(errorDiv).html(`<span>Error creating payment. Please try again.</span>`);
            
            // Hide loading overlay
            $('.loading-overlay').fadeOut();
            
            // Re-enable elements
            card.update({ 'disabled': false});
            $('#submit-button').attr('disabled', false);
        }
    });
});
