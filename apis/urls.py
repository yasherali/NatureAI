from django.contrib import admin
from django.urls import path
from natureai.views import signup, LoginView, ForgotPasswordAPIView, VerificationAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', signup),
    path('login/', LoginView.as_view()),
    path('forgot-password/', ForgotPasswordAPIView.as_view()),
    path('verification/', VerificationAPIView.as_view()),
]
