from django.urls import path
from post import views

app_name = 'post'

urlpatterns = [
    path('', views.index, name='index'),
    path('newpost/', views.NewPost, name='newpost'),
    path('<uuid:post_id>/toggle_like/', views.toggle_like, name='likes'),
    path('<uuid:post_id>/favorite/', views.favorite, name='favorite'),



]
