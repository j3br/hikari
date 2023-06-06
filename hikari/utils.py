import json

def format_code_block(string):
    return f"```\n{string}\n```"

def handle_error_response(response, state):
    if response.status_code >= 400 and response.status_code < 500:
        extended_info = response.json().get('error', {}).get('@Message.ExtendedInfo', [])
        message = format_code_block(json.dumps(extended_info, indent=2, sort_keys=True))

    elif response.status_code != 200:
        message = format_code_block(
            f"An error occurred during the HTTP request: {response.status_code}"
        )
    return f"Failed to initiate power {state}" + message
