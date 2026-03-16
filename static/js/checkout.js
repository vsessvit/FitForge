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

function getTrimmedFieldValue(fieldName) {
    return form[fieldName] ? $.trim(form[fieldName].value) : '';
}

function buildBillingDetails() {
    var billingDetails = {
        name: getTrimmedFieldValue('full_name'),
        email: getTrimmedFieldValue('email')
    };

    var phoneNumber = getTrimmedFieldValue('phone_number');
    if (phoneNumber) {
        billingDetails.phone = phoneNumber;
    }

    var address = {};
    var line1 = getTrimmedFieldValue('street_address1');
    var line2 = getTrimmedFieldValue('street_address2');
    var city = getTrimmedFieldValue('town_or_city');
    var state = getTrimmedFieldValue('county');
    var postalCode = getTrimmedFieldValue('postcode');
    var country = getTrimmedFieldValue('country');

    if (line1) {
        address.line1 = line1;
    }
    if (line2) {
        address.line2 = line2;
    }
    if (city) {
        address.city = city;
    }
    if (state) {
        address.state = state;
    }
    if (postalCode) {
        address.postal_code = postalCode;
    }
    if (country) {
        address.country = country;
    }

    if (Object.keys(address).length > 0) {
        billingDetails.address = address;
    }

    return billingDetails;
}

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
                // eslint-disable-next-line no-unused-vars
                success: function(_cacheResponse) {
                    // Finally, confirm card payment with Stripe
                    stripe.confirmCardPayment(clientSecret, {
                        payment_method: {
                            card: card,
                            billing_details: buildBillingDetails()
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
                // eslint-disable-next-line no-unused-vars
                error: function(_cacheError) {
                    // Reload page, error will be shown in messages
                    location.reload();
                }
            });
        },
        // eslint-disable-next-line no-unused-vars
        error: function(_error) {
            // Show error
            var errorDiv = document.getElementById('card-errors');
            $(errorDiv).html('<span>Error creating payment. Please try again.</span>');
            
            // Hide loading overlay
            $('.loading-overlay').fadeOut();
            
            // Re-enable elements
            card.update({ 'disabled': false});
            $('#submit-button').attr('disabled', false);
        }
    });
});
