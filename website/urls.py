from django.contrib.auth.views import LogoutView
from django.urls import path

from LookBook import settings
from website.views import MainView, StyleDetailView, SignUpView, SignInView

urlpatterns = [
    path('', MainView.as_view(), name='index'),
    path('style/<slug>/', StyleDetailView.as_view(), name='style_detail'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('signout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='signout', ),
]
