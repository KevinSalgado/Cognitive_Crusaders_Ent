from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required

@login_required()
def Inicio(Request):
    template = loader.get_template("Inicio.html")
    return HttpResponse(template.render())

def Servicios(Request):
    template = loader.get_template("servicios.html")
    return HttpResponse(template.render())
