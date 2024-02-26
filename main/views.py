from django.shortcuts import render, redirect
from main.forms import GameForm
from main.models import Game
from django.http import HttpResponse
from django.core import serializers

# Create your views here.
def show_main(request):
    games = Game.objects.all()

    context = {
        'name': 'Nazwa Allysa',
        'class': 'PBP A',
        'games': games
    }

    return render(request, "main.html", context)

def create_game(request):
    form = GameForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_game.html", context)

def show_xml(request):
    data = Game.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Game.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, game_id):
    data = Game.objects.filter(pk=game_id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, game_id):
    data = Game.objects.filter(pk=game_id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")