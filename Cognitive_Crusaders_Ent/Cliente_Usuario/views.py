from django.http import HttpResponse
from django.template import loader


def Inicio(request):
    template = loader.get_template("Inicio.html")
    return HttpResponse(template.render())

def Servicios(request):
    template = loader.get_template("servicios.html")
    return HttpResponse(template.render())
