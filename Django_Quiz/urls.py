from django.utils.translation import gettext_lazy as _
from django.conf.urls.i18n import i18n_patterns
from home import execute
from django.contrib import admin
from django.urls import path, include, re_path


from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    prefix_default_language=False
)

handler404='home.views.outside_404_not_found'
handler500='home.views.request_500'
handler502='home.views.request_502_error'

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT,}),]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
