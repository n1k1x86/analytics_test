from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from django.shortcuts import render, redirect

from mixpanel import Mixpanel

from .serializers import LoginSerializer
from .forms import RegisterForm
from mixpanel_tracking import event_to_track


def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
        event_to_track(request, 'Register Page View', properties={})
        return render(request, 'register_page.html', {'form': form})
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)

            event_to_track(request, 'Signed Up', properties={})

            return redirect('/')
        else:
            return render(request, 'register_page.html', {'form': form})


class LoginView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'login_page.html'

    def get(self, request):
        event_to_track(request, 'Login Page View', properties={})

        return Response({}, template_name=self.template_name)

    @staticmethod
    def post(request):
        username = request.data['username']
        password = request.data['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            event_to_track(request, 'Signed In', properties={})

            return JsonResponse(data={'username': username, "status": 200}, status=status.HTTP_200_OK)
        else:
            error_msg = {'error': "Authentication error. Wrong password or username", "status": 403}
            status_code = status.HTTP_403_FORBIDDEN
            return JsonResponse(data=error_msg, status=status_code)


class LogoutView(APIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        event_to_track(request, 'Logout', properties={})
        logout(request)
        return redirect('/login')
