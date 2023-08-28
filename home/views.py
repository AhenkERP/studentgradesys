from django.shortcuts import render
from django.views import View

# home page
class Home(View):
    def get(self, request):
        return render(request, 'home/index.html')


def error404(request, *args, **kwargs):
    """ 404 Error Page """
    return render(request, 'home/404.html')


def error403(request, *args, **kwargs):
    """ 403 Error Page """
    return render(request, 'home/403.html')


def error500(request, *args, **kwargs):
    """ 500 Error Page """
    return render(request, 'home/500.html')


def csrf_failure(request, reason="CSRF Error"):
    """ 403 CSRF Error Page """
    return render(request, 'home/403_csrf.html')