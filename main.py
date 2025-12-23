import os
#import sys
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    # Load and prepare API key for use
    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")

    # Validate api key
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    client = genai.Client(api_key=api_key)

    # Get message contents from a command line argument
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")

    # Set verbose option
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    # list containing conversation context
    messages = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)]),
    ]

    # Prepare content generation response
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
    )

    if not response.usage_metadata:
        raise RuntimeError("Gemini API response is none")
    
    # Set response metadata
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    # Print verbose option
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}\n")
    
    # Generate content and print metadata
    print(f"{response.text}")

if __name__ == "__main__":
    main()