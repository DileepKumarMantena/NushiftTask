from django.urls import path
from .views import *

urlpatterns = [
    path("Adminregistration", AdminRegistrationApi.as_view()),
    path('AdminLoginApi', AdminLoginApi.as_view()),
    path('MoviesPostApi', MoviesPostApi.as_view()),
    path('GetAllMovies', GetAllMovies.as_view()),
    path('GetAllCustomers', GetAllCustomers.as_view()),
    path('GetAllMoviesInDescendingOrder', GetAllMoviesInDescendingOrder.as_view()),
    path('GetAllMoviesInAssendingOrder', GetAllMoviesInAssendingOrder.as_view()),
    path('GetMovieByDay', GetMovieByDay.as_view()),
    path('MovieNotificationApi',MovieNotificationApi.as_view())

]
