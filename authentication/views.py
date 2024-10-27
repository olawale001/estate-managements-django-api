from rest_framework.response import Response
from rest_framework.permissions import BasePermission, AllowAny
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from rest_framework import generics
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.parsers import MultiPartParser, FormParser
from .models import CustomUser
from .serializers import CustomUserSerializer
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy
from django.core.mail import send_mail

CustomUser = get_user_model()

class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')
    token_generator = default_token_generator
    subject_template_name = 'password_reset_subject.txt'

    def form_valid(self, form):
        email = form.cleaned_data['email'] 
        try:
            user = CustomUser.objects.get(email=email)
            send_mail(
                subject='Password Reset',
                message='Here is the link to reset your password',
                from_email='olacodeire@gmail.com',
                recipient_list=[user.email],
                fail_silently=False,
            )
        except CustomUser.DoesNotExist:
            pass
        return super().form_valid(form)

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('password_reset_complete')

class CustomUserCreateView(generics.CreateAPIView, generics.ListAPIView, generics.DestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        user = serializer.save()
        user.is_active = False
        user.save() 
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        current_site = get_current_site(self.request)
        mail_subject = 'Activate Your Account'
        message = render_to_string('email_verification.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': uid,
            'token': token,
            'urls': reverse('authentication:verify_email', kwargs={'uidb64': uid, 'token': token})
        })
        send_mail(mail_subject, message, 'olacodeire@gmail.com', [user.email])

# class VerifyEmailView(APIView):  
#     def get(self, request, uidb64, token):
#         try:
#             uid = urlsafe_base64_decode(uidb64).decode()
#             user = CustomUser.objects.get(pk=uid)
#         except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
#             user = None

#         if user is not None and default_token_generator.check_token(user, token):
#             user.is_active = True
#             user.save()        
#             return Response({'message': 'Email successfully verified.'})
#         else:
#             return Response({'message': 'Activate link is invalid'}, status=400)


class VerifyEmailView(APIView):  
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            return Response({'error': 'Invalid UID'}, status=400)

        if user is not None and default_token_generator.check_token(user, token):
            if not user.is_active:
                user.is_active = True
                user.save()
                return Response({'message': 'Email successfully verified.'}, status=200)
            else:
                return Response({'message': 'Email is already verified.'}, status=200)
        else:
            return Response({'error': 'Invalid activation link.'}, status=400)


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin'

class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'manager'

class IsTenant(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'tenant'
