from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^articles/', include('article.urls', namespace='articles')),
    url(r'^accounts/', include('account.urls', namespace='accounts')),
    url(r'^comments/', include('comment.urls', namespace='comments')),
    url(r'^about_me/$', TemplateView.as_view(template_name='about_me.html'), name='about_me'),
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
