API_KEY = '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'
MODEL = 'openai/gpt-oss-20b:free'
URL = 'https://openrouter.ai/api/v1/chat/completions'

class Assignment_service:
    def __init__(self, key=API_KEY, model=MODEL, url=URL):
        self.key = key
        self.model = model
        self.url = url
    
    def send_request(self, content):
        try:
            import requests
            import json

            response = requests.post(
                url=self.url,
                headers={
                    'Authorization': f'Bearer {self.key}',
                    'Content-Type': 'application/json', 
                },
                data=json.dumps({
                    'model': self.model,
                    'messages': [
                        {'role': 'user', 'content': content}
                    ],
                    'temperature': 0.7,
                    'max_tokens': 2000
                }),
                timeout=30 
            )

            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                print(f'API error: {response.status_code} {response.text}')
                return None
        except requests.exceptions.Timeout:
            print("Request timed out")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None
        except KeyError as e:
            print(f"Unexpected response format: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
    
    def parse_ai_response(self, response_text):
        import json
        import re
        
        try:
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                analysis = json.loads(json_str)

                if 'understanding_level' not in analysis:
                    analysis['understanding_level'] = 1.0  
                
                if isinstance(analysis['understanding_level'], str):
                    try:
                        analysis['understanding_level'] = float(analysis['understanding_level'])
                    except ValueError:
                        analysis['understanding_level'] = 1.0
                
                return analysis
            else:
                print("No JSON found in response, using fallback")
                return self.get_fallback_analysis()
                
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            return self.get_fallback_analysis()
        except Exception as e:
            print(f"Error parsing AI response: {e}")
            return self.get_fallback_analysis()

    def get_fallback_analysis(self):
        """Provide fallback analysis if AI fails"""
        return {
            "learning_style": "Mixed learning style based on responses",
            "understanding_level": 1.0,
            "cognitive_level": "Analytical and practical thinker",
            "attention_span": "Focused in engaging environments",
            "problem_solving_style": "Systematic problem-solving approach",
            "learning_pace": "Self-directed learning pace",
            "strengths": ["Adaptability", "Willingness to learn", "Curiosity"],
            "improvement_areas": ["Could develop more structured approaches", "May benefit from varied techniques"],
            "recommended_learning_methods": ["Interactive learning", "Practical application", "Structured practice"],
            "motivation_factors": ["Personal growth", "Achievement", "Skill development"]
        }