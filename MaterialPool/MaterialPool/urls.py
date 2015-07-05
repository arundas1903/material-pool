from django.conf.urls import include, url, patterns
from django.contrib import admin

urlpatterns = patterns(
    url(r'^api/', include('rest_framework.urls',
                          namespace='rest_framework')),
    url(r'^auth/', include('auth_user.urls')),
    url(r'^admin/', include(admin.site.urls))
)
