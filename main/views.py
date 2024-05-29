from django.shortcuts import render, redirect
from main.forms import GameForm
from main.models import Game
from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import datetime
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse

@login_required(login_url='/login')
def show_main(request):
    games = Game.objects.filter(user=request.user)

    context = {
        'name': request.user.username,
        'games': games,
        'last_login': request.COOKIES['last_login'],
    }

    return render(request, "main.html", context)

def create_game(request):
 form = GameForm(request.POST or None)

 if form.is_valid() and request.method == "POST":
     game = form.save(commit=False)
     game.user = request.user
     game.save()
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

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.info(request, 'Sorry, incorrect username or password. Please try again.')
    context = {}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

def update_game(request, id):
    game = Game.objects.get(pk = id)

    form = GameForm(request.POST or None, instance=game)

    if form.is_valid() and request.method == "POST":
        # Simpan form dan kembali ke halaman awal
        form.save()
        return HttpResponseRedirect(reverse('main:show_main'))

    context = {'form': form}
    return render(request, "update_game.html", context)

def delete_game(request, id):
    # Get data berdasarkan ID
    game = Game.objects.get(pk = id)
    # Hapus data
    game.delete()
    # Kembali ke halaman awal
    return HttpResponseRedirect(reverse('main:show_main'))

@csrf_exempt
def add_game_ajax(request):
    if request.method == 'POST':
        title = request.POST.get("title")
        price = request.POST.get("price")
        description = request.POST.get("description")
        user = request.user

        new_game = Game(title=title, price=price, description=description, user=user)
        new_game.save()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()

@csrf_exempt
def create_game_flutter(request):
    if request.method == 'POST':

        data = json.loads(request.body)

        new_game = Game.objects.create(
            user = request.user,
            title = data["title"],
            price = int(data["price"]),
            description = data["description"]
        )

        new_game.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)