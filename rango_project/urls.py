from django.contrib import admin
from django.urls import path, re_path, include
from registration.backends.simple.views import RegistrationView

from rango import views


class MyRegistrationView(RegistrationView):
    def get_success_url(self, user=None):
        return '/rango/'


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$', views.index, name='index'),
    re_path(r'^rango/', include('rango.urls')),
    re_path(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
    re_path(r'^accounts/', include('registration.backends.simple.urls'))
]
