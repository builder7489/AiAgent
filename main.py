import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load and prepare API key for use
load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

# Get contents from a command line argument
try:
    user_prompt = str(sys.argv[1])
except Exception as e:
    print(f"Error no argument found")
    sys.exit(1)

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

# Prepare content generation response
response = client.models.generate_content(
    model='gemini-2.0-flash-001', 
    contents=messages,
) 

def main():
    # Generate content and print metadata
    print(f"{response.text}")

    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()