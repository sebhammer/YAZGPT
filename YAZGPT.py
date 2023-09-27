import openai
import zoomsh_wrapper
import json

chat_history = [
    {
        "role": "system",
        "content": "You are a library metadata assistant, providing help with various \
        technical metadata tasks. You have access to a search API. When using the API, group \
        results by work, followed by individual editions of that work. List all available editions \
        for each work. List the original work first followed by any derived works like movie versions, etc."
    }
]

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
            {"verb": "show", "arguments": "1 30 json;charset=marc8,utf8"}])
    print("Hitcount: ", r['result_count'])
    return json.dumps(r)

def chatline(line):
    chat_history.append({"role": "user", "content": line})
    response=openai.ChatCompletion.create(model="gpt-3.5-turbo-16k",
                                          messages=chat_history,
                                          functions=functions_definition,
                                          function_call="auto")
    message = response['choices'][0].message
    chat_history.append(message)
    if (message.get("function_call")):
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

def main():
    print("Welcome to the YAZGPT AI-powered Z39.50 client")

    while True:
        print("\nYAZGPT>> ", end="")
        inputl = input()
        chatline(inputl)

if __name__ == "__main__":
    main()
