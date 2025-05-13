import json
import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class OllamaService:
    """Service for interacting with Ollama API"""
    
    def __init__(self, model_name="llama3"):
        # Default to llama3, but you can change this to any model you have in Ollama
        self.model_name = model_name
        self.base_url = getattr(settings, "OLLAMA_API_URL", "http://localhost:11434")
    
    def generate_response(self, prompt, system_prompt=None, conversation_history=None):
        """
        Generate a response from Ollama
        
        Args:
            prompt (str): The user's message
            system_prompt (str, optional): System instructions for the model
            conversation_history (list, optional): Previous conversation messages
            
        Returns:
            str: The model's response
        """
        try:
            url = f"{self.base_url}/api/chat"
            
            # Default system prompt if none provided
            if not system_prompt:
                system_prompt = "You are a helpful AI assistant."
            
            # Format the messages for the Ollama API
            messages = []
            
            # Add system message
            messages.append({"role": "system", "content": system_prompt})
            
            # Add conversation history if provided
            if conversation_history:
                messages.extend(conversation_history)
            
            # Add the current user message
            messages.append({"role": "user", "content": prompt})
            
            # Prepare the request payload
            payload = {
                "model": self.model_name,
                "messages": messages,
                "stream": False
            }
            
            # Make the request to Ollama
            response = requests.post(url, json=payload, timeout=120)
            response.raise_for_status()
            
            # Parse the response
            result = response.json()
            
            # Return the assistant's message
            if "message" in result and "content" in result["message"]:
                return result["message"]["content"]
            
            return "I'm sorry, I couldn't generate a response."
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error connecting to Ollama: {str(e)}")
            return "I'm having trouble connecting to the language model service. Please make sure Ollama is running."
        
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return "An error occurred while generating a response."