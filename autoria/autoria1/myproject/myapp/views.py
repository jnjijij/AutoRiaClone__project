from django.http import HttpResponse

def index():
    return HttpResponse("Hello, world. You're at the my_app index.")
