from django.urls import path
from . import views

app_name = "polls"
urlpatterns = [
    path('', views.index, name="index"),
    path('some_url', views.some_url),
    path('<int:question_id>/', views.detail, name='detail')
]
