from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .dspy_logic import get_chemistry_response

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

            if not user_message:
                return JsonResponse({
                    'error': 'No message provided',
                    'status': 'error'
                }, status=400)

            # Use DSPy Chemistry QA module
            bot_response = get_chemistry_response(user_message)

            return JsonResponse({
                'response': bot_response,
                'status': 'success'
            })
        except Exception as e:
            print(f"[ERROR] Exception in chat_api: {str(e)}")
            import traceback
            traceback.print_exc()
            return JsonResponse({
                'error': 'Failed to generate response',
                'status': 'error'
            }, status=500)

    return JsonResponse({
        'error': 'Method not allowed',
        'status': 'error'
    }, status=405)
