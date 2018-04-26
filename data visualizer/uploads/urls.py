from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from uploads.core import views


urlpatterns = [
    # url(r'^$', views.home, name='home'),
    url(r'^software/display/$', views.display_data, name='simple_upload'),
    # url(r'^software/visualize/$',views.form_fill, name='form_fill'),
    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
