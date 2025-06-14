from django.http import HttpResponse
from django.shortcuts import render
def homePage(request):
    # return HttpResponse("Hello, world. You're at the home page.")
    return render(request, 'home.html')


def aboutPage(request):
    # return HttpResponse("Hello, world. You're at the about page.")
    return render(request, 'about.html')