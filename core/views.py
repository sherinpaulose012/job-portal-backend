from django.http import JsonResponse

def home(request):
    return JsonResponse({
        "message": "Zecpath AI job portal"
    })