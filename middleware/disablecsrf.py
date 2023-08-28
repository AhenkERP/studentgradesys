from django.middleware.csrf import CsrfViewMiddleware

class DisableCsrfMiddleware(CsrfViewMiddleware):
    def process_view(self, request, callback, callback_args, callback_kwargs):
        # Disable CSRF protection for OAuth Toolkit endpoints
        if "oauth2_provider" in request.path:
            return None
        return super().process_view(request, callback, callback_args, callback_kwargs)
