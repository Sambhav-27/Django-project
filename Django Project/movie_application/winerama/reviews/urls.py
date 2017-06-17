from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /
    url(r'^$', views.review_list, name='review_list'),
    # ex: /review/5/
    url(r'^review/(?P<review_id>[0-9]+)/$', views.review_detail, name='review_detail'),
    # ex: /wine/
    url(r'^wine$', views.wine_list, name='wine_list'),
    url(r'^wine/add_search/$', views.add_search, name='add_search'),
    # ex: /wine/5/
    url(r'^wine/(?P<wine_id>[0-9]+)/$', views.wine_detail, name='wine_detail'),
    url(r'^wine/(?P<wine_id>[0-9]+)/add_review/$', views.add_review, name='add_review'),
    # ex: /review/user - get reviews for the logged user
    url(r'^review/user/(?P<username>\w+)/$', views.user_review_list, name='user_review_list'),
    # ex: /review/user - get reviews for the user passed in the url
    url(r'^review/user/$', views.user_review_list, name='user_review_list'),
    # ex: /recommendation - get wine recommendations for the logged user
    url(r'^recommendation/$', views.user_recommendation_list, name='user_recommendation_list'),
    url(r'^wine/shopping_cart/$', views.shopping_cart, name='shopping_cart'),
    url(r'^wine/add_movie/(?P<wine_id>[0-9]+)/$', views.add_movie, name='add_movie'),
    url(r'^wine/recently_bought/(?P<wine_id>[0-9]+)/$', views.recently_bought, name='recently_bought'),
    url(r'^wine/already_bought/(?P<wine_id>[0-9]+)/$', views.already_bought, name='already_bought'),
    url(r'^wine/already_added_to_cart/(?P<wine_id>[0-9]+)/$', views.already_added_to_cart, name='already_added_to_cart'),
    url(r'^wine/checkout/$', views.checkout, name='checkout'),
    url(r'^wine/my_movies/$', views.my_movies, name='my_movies'),
    url(r'^wine/remove_movie/(?P<wine_id>[0-9]+)/$', views.remove_movie, name='remove_movie'),
]