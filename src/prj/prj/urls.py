from django.urls import path, include

urlpatterns = [
    path('', include('myapp.urls')),  # Inclut les routes de votre application
]
