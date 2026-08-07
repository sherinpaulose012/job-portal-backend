from django.http import JsonResponse


class SubscriptionMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        print("SUBSCRIPTION MIDDLEWARE RUNNING")
        print("PATH:", request.path)
        print("USER:", request.user)
        print("AUTHENTICATED:", request.user.is_authenticated)

        if request.path == "/analytics/dashboard/":

            return JsonResponse({
                "test": "Subscription middleware is working"
            }, status=403)

        return self.get_response(request)