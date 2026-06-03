import os
#import sys
import argparse
#import prompts

from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions
from call_function import call_function

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

    # List containing conversation context
    messages = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)]),
    ]

    #
    # START MODEL-CALLING LOGIC
    #
    for _ in range(20):
        # List containing function calls
        function_results: list = []

        # Prepare content generation response
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            ),
        )

        if not response.usage_metadata:
            raise RuntimeError("Gemini API response is none")
        
        # Set response metadata
        prompt_tokens = response.usage_metadata.prompt_token_count
        response_tokens = response.usage_metadata.candidates_token_count

        # Add previous responses to message content list
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        # Print verbose option
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {response_tokens}\n")
        
        
        # Print any possible function calls with name, args
        if response.function_calls != None:
            for function_call in response.function_calls:
                function_call_result = call_function(function_call, args.verbose)

                if not function_call_result.parts:
                    raise Exception("Empty result...")
                if function_call_result.parts[0].function_response == None:
                    raise Exception("None ...")
                if function_call_result.parts[0].function_response.response == None:
                    raise Exception("None ...")        
                else:
                    function_results.append(function_call_result.parts[0])
                    if args.verbose:
                        print(f"-> {function_call_result.parts[0].function_response.response}")

        # Add list of function calls to messages list contexting
        messages.append(types.Content(role="user", parts=function_results))

        # END model is not request function call and has a final response to the user
        if not response.function_calls and response.text != None:
            print(f"FINAL RESPONSE")
            print(f"{response.text}")
            break

    # END model is requesting more function calls and the loop range has been reached
    else:
        print(f"NO CONCLUSION...")
        exit(1)


if __name__ == "__main__":
    main()