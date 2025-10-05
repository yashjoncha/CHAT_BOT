from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

def home(request):
    """Basic home view"""
    return JsonResponse({
        'status': 'success',
        'message': 'Welcome to ChatBot API',
        'version': '1.0.0'
    })

def health_check(request):
    """Health check endpoint for deployment"""
    return JsonResponse({
        'status': 'healthy',
        'service': 'chatbot'
    })
