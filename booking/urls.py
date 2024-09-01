from . import views
from django.urls import path

urlpatterns = [
    path('booking/', views.PostList.as_view(), name='home'),
]