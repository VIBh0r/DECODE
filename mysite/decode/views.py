from django.shortcuts import render

def home(request):
    return render(request, 'decode/home.html')

def mainhome(request):
    return render(request, 'decode/mainhome.html', {'title': 'Home'})

def fun(request):
    return render(request, 'decode/fun.html', {'title': '<..>'})

def streamlit_app(request, app_name, port):
    return render(request, 'decode/streamlit_app.html', {'app_name': app_name, 'port': port})
