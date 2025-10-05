from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

def home(request):
    """Render the chat interface"""
    return render(request, 'chat/index.html')

def health_check(request):
    """Health check endpoint for deployment"""
    return JsonResponse({
        'status': 'healthy',
        'service': 'chatbot'
    })

def chat_api(request):
    """Handle chat messages and return response"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')

            # Simple response - just say "let's go"
            bot_response = "let's go"

            return JsonResponse({
                'response': bot_response,
                'status': 'success'
            })
        except Exception as e:
            return JsonResponse({
                'error': str(e),
                'status': 'error'
            }, status=400)

    return JsonResponse({
        'error': 'Method not allowed',
        'status': 'error'
    }, status=405)
