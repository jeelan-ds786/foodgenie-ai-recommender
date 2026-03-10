import requests
from context.context_intents.weather_context import API_KEY

def test_api_key():
    url = f"https://api.openweathermap.org/data/2.5/weather?q=Chennai&appid={API_KEY}"
    
    try:
        response = requests.get(url, timeout=5)
        print(f"Status Code: {response.status_code}")
        
        data = response.json()
        
        if response.status_code == 200:
            print("✓ API Key is VALID!")
            print(f"Weather in Chennai: {data['weather'][0]['main']}")
            print(f"Temperature: {data['main']['temp']} K")
            return True
        elif response.status_code == 401:
            print("✗ API Key is INVALID (401 Unauthorized)")
            return False
        else:
            print(f"✗ Error: {data.get('message', 'Unknown error')}")
            return False
            
    except requests.RequestException as e:
        print(f"✗ Connection error: {e}")
        return False

if __name__ == "__main__":
    test_api_key()
