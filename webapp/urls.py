from django.urls import path
from . import views 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # login,register & logout urls
    path('',views.homepage,name='home'),
    path('login',views.login_page,name='login'),
    path('register',views.register_page,name='register'),
    path('logout',views.logout_page,name='logout'),
    path('delete',views.delete,name='delete'),

    #Bols urls
    path('postlist', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),

   
    #Api Urls
    path('api/',views.PostList.as_view()),
    path('<int:pk>/',views.PostDetail.as_view()),

    
    #media files static setting
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)