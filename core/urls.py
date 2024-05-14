from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('secret-admin/', admin.site.urls),

    # chat urls
    path('', include('mainApp.urls')),

    # auth urls
    path('auth/', include('users.urls')),

    # add friend urls
    path('add_friend/', include('add_friend_app.urls')),

    # chat urls
    path('chat/', include('chat.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)