from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponseRedirect
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from django.shortcuts import render, redirect

from .serializers import LoginSerializer
from .forms import RegisterForm, LoginForm


def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'register_page.html', {'form': form})
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)

            return redirect('/')
        else:
            return render(request, 'register_page.html', {'form': form})


class LoginView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'login_page.html'

    def get(self, request):
        form = LoginForm()
        return Response({'form': form}, template_name=self.template_name)

    @staticmethod
    def post(request):
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('/')
            else:
                error_msg = {'error': "Authentication error. Wrong password or username", "status": 403}
                status_code = status.HTTP_403_FORBIDDEN
                return JsonResponse(data=error_msg, status=status_code)


class LogoutView(APIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        logout(request)
        return redirect('/login')
