from django.urls import path, include
from . import views

app_name = "glucose"

urlpatterns = [
    path('levels', views.levels_for_user),
    path('highlow', views.highlow),
    path('levels/<int:id>', views.levels_for_id),
    path('load-data', views.load_data),
    path('users', views.get_users)
]
