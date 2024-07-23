from django.urls import path

from .views import GenerateQRCode, QRLogin

urlpatterns = [
    path('generate-qr/<int:user_id>/', GenerateQRCode.as_view(), name='generate_qr_code'),
    path('qr-login/<int:user_id>/<str:token>/', QRLogin.as_view(), name='qr_login'),
]
