from django.urls import path
from .views import Home

app_name="main"

urlpatterns = [
    path('', Home.as_view())
]
