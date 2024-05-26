from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.views.generic import RedirectView


urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('login')), name='home'),
    path('admin/', admin.site.urls),
    path('api/', include('library.urls')),  # This includes the `library` app URLs under `api/`
]
