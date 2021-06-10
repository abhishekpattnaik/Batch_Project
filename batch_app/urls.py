from django.urls import path

from . import views

urlpatterns = [
    # path('dashboard/', views.view1, name='index'),
	# path('login/', views.loginPage, name="login"),  
	# path('logout/', views.logoutUser, name="logout"),
	path('home/', views.Home, name="home"),
]