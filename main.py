import os
import sys
from dotenv import load_dotenv
from google import genai

# Load and prepare API key for use
load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

# Get contents from a command line argument
try:
    cli_argument = str(sys.argv[1])
except Exception as e:
    print(f"Error no argument found")
    sys.exit(1)

# Prepare content generation response
response = client.models.generate_content(
    model='gemini-2.0-flash-001', 
    contents=cli_argument
) 

def main():
    # Generate content and print metadata
    print(f"{response.text}")

    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()