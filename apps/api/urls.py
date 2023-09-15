from django.urls import path, include


urlpatterns = [
    path('blog/', include(('apps.blog.urls', 'blog'))),
    path('users/', include(('apps.users.urls', 'users'))),
    path('authenticate/', include(('apps.authenticate.urls', 'authenticate'))),
]
