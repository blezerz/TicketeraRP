from django.shortcuts import render

# Create your views here.


def index(request):
    data = {
        "titulo": 'Electronica',
        "producto1": 'Camara Fotografica',
        "producto2": "FonosBluethoo",
        "producto3": "Televisor"
    }

    return render(request, 'index.html',data)

