from django.urls import path
from main.views import show_main, create_game, show_xml, show_json, show_xml_by_id, show_json_by_id
from main.views import register
from main.views import login_user
from main.views import logout_user
app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('create-game', create_game, name='create_game'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<int:game_id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<int:game_id>/', show_json_by_id, name='show_json_by_id'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
]