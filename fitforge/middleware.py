from django.contrib import messages
from django.urls import resolve
from django.shortcuts import redirect


class AuthenticatedUserSignupRedirectMiddleware:
    """
    Middleware to redirect authenticated users away from signup/login pages
    and show them a friendly message.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if user is authenticated
        if request.user.is_authenticated:
            # Check which page they're trying to access
            try:
                path = resolve(request.path_info)
                # If trying to access signup or login, redirect with message
                if path.url_name in ['account_signup', 'account_login']:
                    messages.info(
                        request,
                        f'You are already signed in as {request.user.username}. '
                        'Visit your profile to manage your account.'
                    )
                    return redirect('profiles:profile')
            except:
                # If URL doesn't resolve, just continue
                pass

        response = self.get_response(request)
        return response
