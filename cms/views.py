from django.shortcuts import render
from django.http import HttpResponse
from models import Pages
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
import urllib
# Create your views here.

class myContentHandler(ContentHandler):
    def __init__ (self):
            self.inItem = False
            self.inContent = False
            self.theContent = ""
            self.titulo = ""
            self.line = ""

    def startElement (self, name, attrs):
        if name == 'item':
            self.inItem = True
        elif self.inItem:
            if name == 'title':
                self.inContent = True
            elif name == 'link':
                self.inContent = True

    def endElement (self, name):
        if name == 'item':
            self.inItem = False
        elif self.inItem:
            if name == 'title':
                # To avoid Unicode trouble
                self.titulo = self.theContent
                self.inContent = False
                self.theContent = ""
            elif name == 'link':
                self.line +=  "<a href=" + self.theContent  + ">" + self.titulo + "</a></br>"
                self.inContent = False
                self.theContent = ""

    def characters (self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars


def mostrar (request, key):
    try:
        valor = Pages.objects.get(id=key)
        respuesta = "<p>El valor es " + valor.page + "</p>"

        theParser = make_parser()
        theHandler = myContentHandler()
        theParser.setContentHandler(theHandler)
        url_original = "http://barrapunto.com/index.rss"
        f = urllib.urlopen (url_original)
        theParser.parse(f)
        respuesta += theHandler.line
    except Pages.DoesNotExist:
        respuesta = "Esta clave no existe"

    return HttpResponse(respuesta)

def add(request, key, valor):
    nuevo = Pages(name=key,page=valor)
    nuevo.save()
    return HttpResponse("Nuevo elemento almacenado")
def listar(request):
    listado = Pages.objects.all()
    respuesta = "<ul>"
    for elemento in listado:
        respuesta += '<li><a href ="'+ str(elemento.id) + '">'
        respuesta += str(elemento.name) + '</a>'
    respuesta += "</ul>"
    return HttpResponse(respuesta)
def notFound(request):
    return HttpResponse("Not Found: Argumentos invalidos")
