from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from django.shortcuts import HttpResponseRedirect, render, redirect

from .serializers import LoginSerializer
from .forms import RegisterForm


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
            return redirect('/home')
        else:
            return render(request, 'register_page.html', {'form': form})


class LoginView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'login_page.html'

    @staticmethod
    def get(request):
        serializer = LoginSerializer()
        return Response({'serializer': serializer})

    @staticmethod
    def post(request):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return HttpResponseRedirect('/home')
        else:
            error_msg = {'error': "Authentication error. Wrong password or username"}
            status_code = status.HTTP_403_FORBIDDEN
            return Response(data=error_msg, status=status_code, template_name='403.html')


class LogoutView(APIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        logout(request)
        return redirect('/login')
