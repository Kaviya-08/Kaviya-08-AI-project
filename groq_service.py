import requests
import json

class GroqService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.groq.com/openai/v1/chat/completions'
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
    
    def get_summary(self, content, is_email=True):
        """Get a summary of content using the Groq API."""
        if not self.api_key:
            return "Error: Groq API key not configured. Please set the GROQ_API_KEY environment variable."
            
        try:
            content_type = "email" if is_email else "news article"
            
            # Create the prompt for summarization
            system_prompt = f"You are an expert summarizer. Provide a concise summary of the following {content_type}. Focus on the key points and actionable information."
            
            if is_email:
                user_prompt = f"Summarize this email in 2-3 bullet points highlighting the most important information:\n\n{content}"
            else:
                user_prompt = f"Summarize this news article in 3-4 bullet points highlighting the main points:\n\n{content}"
            print("content : " ,content , user_prompt) 
            payload = {
                'model': 'llama-3.1-8b-instant',  # Use an appropriate model
                'messages': [
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': user_prompt}
                ],
                'temperature': 0.3,  # Lower temperature for more focused summaries
                'max_tokens': 300
            }
            
            response = requests.post(self.base_url, headers=self.headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            summary = result['choices'][0]['message']['content']
            
            return summary
            
        except Exception as e:
            print(f"Error in Groq API call: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return f"Error generating summary: {str(e)}"
