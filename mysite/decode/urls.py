from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('', views.mainhome, name='mainhome'),
    path('fun/', views.fun, name='fun'),
    path('streamlit/g1/', views.streamlit_app, kwargs={'app_name': 'g1', 'port': 8501}, name='streamlit_g1'),
    path('streamlit/g3/', views.streamlit_app, kwargs={'app_name': 'g3', 'port': 8502}, name='streamlit_g3'),
    path('streamlit/g4/', views.streamlit_app, kwargs={'app_name': 'g4', 'port': 8503}, name='streamlit_g4'),
    path('streamlit/g5/', views.streamlit_app, kwargs={'app_name': 'g5', 'port': 8504}, name='streamlit_g5'),
    path('streamlit/g6/', views.streamlit_app, kwargs={'app_name': 'g6', 'port': 8505}, name='streamlit_g6'),
    path('streamlit/g7/', views.streamlit_app, kwargs={'app_name': 'g7', 'port': 8506}, name='streamlit_g7'),
    path('streamlit/g8/', views.streamlit_app, kwargs={'app_name': 'g8', 'port': 8507}, name='streamlit_g8'),
]

