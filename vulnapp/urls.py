from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('api/users/<uuid:user_id>/profile/', views.user_profile, name='user_profile'),
    path('posts/', views.post_list, name='post_list'),
    path('posts/create/', views.create_post, name='create_post'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('posts/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('static', views.directory_listing, {'path': ''}),
    path('static/', views.directory_listing, {'path': ''}),
    path('static/<path:path>', views.directory_listing),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 