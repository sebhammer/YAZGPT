import openai
import zoomsh_wrapper

chat_history = [
    {
        "role": "system",
        "content": "You are a library metadata assistant, providing help with various technical metadata tasks"
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
                    "description": "Searches the title index"
                },
                "author": {
                    "type": "string",
                    "description": "Searches the author index"
                },
                "subject": {
                    "type": "string",
                    "description": "Searches for books about this subject matter"
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
    query = zoom_makequery(parameters)


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
