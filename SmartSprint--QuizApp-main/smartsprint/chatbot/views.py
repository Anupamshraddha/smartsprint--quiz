
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
import uuid

from .models import Conversation, Message
from .services import OllamaService

def chat_view(request):
    """View for the chat interface"""
    # Get or create a session ID for anonymous users
    if request.user.is_authenticated:
        user = request.user
        session_id = None
    else:
        user = None
        session_id = request.session.get('chat_session_id')
        if not session_id:
            session_id = str(uuid.uuid4())
            request.session['chat_session_id'] = session_id
    
    # Get or create a conversation
    conversation_id = request.GET.get('conversation_id')
    if conversation_id:
        try:
            conversation = Conversation.objects.get(id=conversation_id)
            # Verify the conversation belongs to the user/session
            if (user and conversation.user == user) or (session_id and conversation.session_id == session_id):
                pass
            else:
                # Create a new conversation if the requested one doesn't belong to the user
                conversation = Conversation.objects.create(
                    user=user,
                    session_id=session_id
                )
        except Conversation.DoesNotExist:
            conversation = Conversation.objects.create(
                user=user,
                session_id=session_id
            )
    else:
        conversation = Conversation.objects.create(
            user=user,
            session_id=session_id
        )
    
    # Get conversation history
    messages = conversation.messages.all()
    
    context = {
        'conversation': conversation,
        'messages': messages,
    }
    
    return render(request, 'chat.html', context)

@csrf_exempt
@require_POST
def chat_message(request):
    """API endpoint for sending/receiving chat messages"""
    try:
        data = json.loads(request.body)
        message = data.get('message', '').strip()
        conversation_id = data.get('conversation_id')
        
        if not message or not conversation_id:
            return JsonResponse({'error': 'Message and conversation ID are required'}, status=400)
        
        # Get the conversation
        try:
            conversation = Conversation.objects.get(id=conversation_id)
            
            # Verify the conversation belongs to the user/session
            if request.user.is_authenticated:
                if conversation.user != request.user:
                    return JsonResponse({'error': 'Unauthorized'}, status=403)
            else:
                session_id = request.session.get('chat_session_id')
                if conversation.session_id != session_id:
                    return JsonResponse({'error': 'Unauthorized'}, status=403)
        except Conversation.DoesNotExist:
            return JsonResponse({'error': 'Conversation not found'}, status=404)
        
        # Save the user message
        user_message = Message.objects.create(
            conversation=conversation,
            role='user',
            content=message
        )
        
        # Get the conversation history for context
        history = []
        for msg in conversation.messages.all():
            if msg.role in ['user', 'assistant']:
                history.append({
                    'role': msg.role,
                    'content': msg.content
                })
        
        # Generate response with Ollama
        ollama_service = OllamaService()
        system_prompt = "You are a helpful AI assistant integrated in a Django application."
        response = ollama_service.generate_response(
            prompt=message,
            system_prompt=system_prompt,
            conversation_history=history[:-1]  # Exclude the current message
        )
        
        # Save the assistant's response
        assistant_message = Message.objects.create(
            conversation=conversation,
            role='assistant',
            content=response
        )
        
        # Update the conversation's last modified time
        conversation.save()
        
        return JsonResponse({
            'response': response,
            'conversation_id': conversation.id,
        })
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)