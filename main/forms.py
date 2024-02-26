from django.forms import ModelForm
from main.models import Game

class GameForm(ModelForm):
    class Meta:
        model = Game
        fields = ["title", "price", "description"]