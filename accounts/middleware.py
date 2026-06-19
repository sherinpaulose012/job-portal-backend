class RoleLoggingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        if hasattr(request, "user") and request.user.is_authenticated:
            print(
                f"User: {request.user.email} | Role: {request.user.role}"
            )

        return response