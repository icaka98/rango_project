from django.contrib import admin
from django.urls import path, re_path, include

from rango import views

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$', views.index, name='index'),
    re_path(r'^rango/', include('rango.urls')),
    re_path(r'accounts/', include('registration.backends.simple.urls'))
]
