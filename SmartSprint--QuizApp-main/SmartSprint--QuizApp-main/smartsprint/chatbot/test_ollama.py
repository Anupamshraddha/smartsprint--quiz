import requests
import sys

def test_ollama_connection(model_name="llama3"):
    """Test the connection to Ollama API"""
    try:
        print(f"Testing connection to Ollama API with model {model_name}...")
        
        # Test the connection to Ollama API
        url = "http://localhost:11434/api/chat"
        payload = {
            "model": model_name,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello, is Ollama working?"}
            ],
            "stream": False
        }
        
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        
        if "message" in result and "content" in result["message"]:
            print("✅ Successfully connected to Ollama!")
            print(f"Ollama response: {result['message']['content'][:100]}...")
            return True
        else:
            print("❌ Connected to Ollama API but received an unexpected response format.")
            print(f"Response: {result}")
            return False
        
    except requests.exceptions.ConnectionError:
        print("❌ Failed to connect to Ollama API. Is Ollama running?")
        print("Try starting Ollama with: ollama serve")
        return False
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error communicating with Ollama API: {str(e)}")
        return False
    
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False

if __name__ == "__main__":
    # Get model name from command line argument, if provided
    model_name = "llama3"
    if len(sys.argv) > 1:
        model_name = sys.argv[1]
    
    test_ollama_connection(model_name)