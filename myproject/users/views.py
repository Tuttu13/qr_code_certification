import io

import qrcode
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class GenerateQRCode(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        token = default_token_generator.make_token(user)
        
        qr_data = f"http://127.0.0.1:8000/api/qr-login/{user_id}/{token}/"
        qr = qrcode.make(qr_data)
        
        buf = io.BytesIO()
        qr.save(buf, format='PNG')
        buf.seek(0)
        
        return HttpResponse(buf.getvalue(), content_type="image/png")

class QRLogin(APIView):
    def get(self, request, user_id, token):
        user = get_object_or_404(User, pk=user_id)
        
        if default_token_generator.check_token(user, token):
            login(request, user)
            return Response({"detail": "Login successful"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
