from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html')

def party_room(request):
    return render(request, 'party_room.html')
