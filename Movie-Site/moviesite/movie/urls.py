from django.urls import path
from .views import *


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register_list'),
    path('login/', CustomLoginView.as_view(), name='login_list'),
    path('logout/', LogoutView.as_view(), name='logout_list'),

    path('', MovieListViewSet.as_view({'get': 'list', 'post': 'create'}), name='movie_list'),
    path('<int:pk>/', MovieDetailViewSet.as_view({'get': 'retrieve', 'put': 'update',
                                              'delete': 'destroy'}), name='movie_detail'),

    path('country', CountryListViewSet.as_view({'get': 'list', 'post': 'create'}), name='country_list'),
    path('country/<int:pk>/', CountryDetailViewSet.as_view({'get': 'retrieve', 'put': 'update',
                                                  'delete': 'destroy'}), name='country_detail'),

    path('profile/', ProfileViewSet.as_view({'get': 'list', 'post': 'create'}), name='profile_list'),
    path('profile/<int:pk>/', ProfileViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='profile_detail'),

    path('director/', DirectorListViewSet.as_view({'get': 'list', 'post': 'create'}), name='director_list'),
    path('director/<int:pk>/', DirectorDetailViewSet.as_view({'get': 'retrieve', 'put': 'update',
                                                  'delete': 'destroy'}), name='director_detail'),

    path('actor/', ActorListViewSet.as_view({'get': 'list', 'post': 'create'}), name='actor_list'),
    path('actor/<int:pk>/', ActorDetailViewSet.as_view({'get': 'retrieve', 'put': 'update',
                                                  'delete': 'destroy'}), name='actor_detail'),

    path('janre/', JanreListViewSet.as_view({'get': 'list', 'post': 'create'}), name='janre_list'),
    path('janre/<int:pk>/', JanreListViewSet.as_view({'get': 'retrieve', 'put': 'update',
                                                  'delete': 'destroy'}), name='janre_detail'),

    path('movie_languages/', MomentsListViewSet.as_view({'get': 'list', 'post': 'create'}), name='movie_languages_list'),
    path('movie_languages/<int:pk>/', MomentsDetailViewSet.as_view({'get': 'retrieve', 'put': 'update',
                                                  'delete': 'destroy'}), name='movie_languages_detail'),

    path('moments/', MomentsListViewSet.as_view({'get': 'list', 'post': 'create'}), name='moments_list'),
    path('moments/<int:pk>/', MomentsDetailViewSet.as_view({'get': 'retrieve', 'put': 'update',
                                                  'delete': 'destroy'}), name='moments_detail'),

    path('rating/', RatingViewSet.as_view({'get': 'list', 'post': 'create'}), name='rating_list'),
    path('rating/<int:pk>/', RatingViewSet.as_view({'get': 'retrieve', 'put': 'update',
                                                  'delete': 'destroy'}), name='rating_detail'),

    path('favorite/', FavoriteViewSet.as_view({'get': 'list', 'post': 'create'}), name='favorite_detail'),

    path('favorite_movie/', FavoriteMovieViewSet.as_view({'get': 'list', 'post': 'create'}), name='favorite_movie_list'),



]