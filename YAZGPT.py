import openai
import json
import argparse

import zoomsh_wrapper
import zlog

# This list represents the history of the conversation. We bootstrap it with an initial prompt to give
# the LLM background and direction. Prompt is read from a file.
chat_history = [
    {
        "role": "system",
        "content": None
    }
]

# Maximum number of records to retrieve
max_records = 50;

functions_definition = [
    {
        "name": "search",
        "description": "Search a database of bibliographic information",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Searches the title field"
                },
                "author": {
                    "type": "string",
                    "description": "Searches the author field. IMPORTANT: Personal names should be \
                                   given as Surname, First Name like King, Stephen"
                },
                "subject": {
                    "type": "string",
                    "description": "Searches the subject field",
                },
                "date": {
                    "type": "string",
                    "description": "The date of publication"
                },
                "isbn": {
                    "type": "string",
                    "description": "Search for a specific ISBN. If you get zero hits, try again with or \
                    without the dashes"
                }
            }
        }
    }
]


def search_function(parameters):
    query = zoomsh_wrapper.zoom_makequery(parameters)
    r = zoomsh_wrapper.zoomsh([{"verb": "connect", "arguments": "z3950.loc.gov:7090/Voyager"},
            {"verb": "set", "arguments": "preferredRecordSyntax marc21"},
            {"verb": "set", "arguments": "charset utf8"},
            {"verb": "find", "arguments": query},
            {"verb": "show", "arguments": "0 " + str(max_records) + " json;charset=marc8,utf8"}])
    if r.get('result_count'):
        print("Hitcount: ", r['result_count'])
    return json.dumps(r)

def chatline(line):
    zlog.log("User: " + line)
    chat_history.append({"role": "user", "content": line})
    response=openai.ChatCompletion.create(model="gpt-3.5-turbo-16k",
                                          messages=chat_history,
                                          functions=functions_definition,
                                          function_call="auto")
    message = response['choices'][0].message
    chat_history.append(message)
    while message.get("function_call"):
        # The LLM wants to call a function
        print("Function Call", message['function_call']["name"],
              message['function_call']["arguments"])
        if message['function_call']['name'] == 'search':
            result = search_function(message['function_call']['arguments'])

            chat_history.append(
                {
                    'role': 'function',
                    'name': 'search',
                    'content': result
                }
            )
            response = openai.ChatCompletion.create(model="gpt-3.5-turbo-16k",
                                                    messages=chat_history,
                                                    functions=functions_definition,
                                                    function_call="auto")
            message = response['choices'][0].message
            chat_history.append(message)
        else:
            print("Unknown function!")
    if message.content:
        print(message.content)

# TODO:  -t -l
def main():
    parser = argparse.ArgumentParser(description="A simple GPT-powered Z39.50 client")
    parser.add_argument('-p', '--prompt', help="path to initial setup prompt, default etc/prompts/default.txt",
                        default='etc/prompts/default.txt')
    parser.add_argument('-t', '--temperature',
                        help="temperature parameter for the LLM. 0 is predictable, 1 is creative",
                        default=1)
    parser.add_argument('-l', '--log', help='a logfile for background protocol actions and data retrieved')
    parser.add_argument('-n', '--max_records', help='Maximum number of records to fetch', default=50)
    args = parser.parse_args()
    with open(args.prompt) as pfile:
        chat_history[0]['content'] = pfile.read()
    max_records = args.max_records;
    zlog.logfile = args.log

    zlog.log("New session\n------------------------\n")

    print("Welcome to the YAZGPT AI-powered Z39.50 client")

    while True:
        print("\nYAZGPT>> ", end="")
        inputl = input()
        print()
        chatline(inputl)

if __name__ == "__main__":
    main()
