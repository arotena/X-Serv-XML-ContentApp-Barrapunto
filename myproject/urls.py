from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'myproject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^(\d+)$' , 'cms.views.mostrar'),
    url(r'(.+)/(.+)' , 'cms.views.add'),
    url(r'^$' , 'cms.views.listar'),
    url(r'.*' , 'cms.views.notFound')
)
