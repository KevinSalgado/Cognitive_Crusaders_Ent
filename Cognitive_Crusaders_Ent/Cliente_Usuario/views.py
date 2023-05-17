from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def Inicio(Request):
    return render(Request, 'Inicio.html', {'request': Request})
    # template = loader.get_template("Inicio.html")
    # return HttpResponse(template.render())

@login_required()
def Servicios(Request):
    template = loader.get_template("servicios.html")
    return HttpResponse(template.render())

def Salir(Request):
    logout(Request)
    template = loader.get_template("Inicio.html")
    return HttpResponse(template.render()) 
