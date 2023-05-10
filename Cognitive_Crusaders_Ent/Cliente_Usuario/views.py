from django.http import HttpResponse
from django.template import loader


def Inicio(request):
    template = loader.get_template("Inicio.html")
    return HttpResponse(template.render())
