from django.urls import path
import authentication.views as auth

app_name = 'auth'

urlpatterns = [
    path('login/', auth.login, name='login'),
    path('logout/', auth.logout, name='logout'),
    path('registration/', auth.registration, name='registration'),
    path('change_password/', auth.change_password, name='change_password'),
    path('delete_account/', auth.delete_account, name='delete_account'),
    path('verify/<str:email>/<str:key>/', auth.verify, name='verify'),
    path('renew_verification_key/', auth.renew_verification_key, name='renew_verification_key'),
]