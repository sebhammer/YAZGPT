import os

def zoomsh(args):
    command_string = "zoomsh"
    for command in args:
        command_string += " '" + command['verb'] + " " + command['arguments'] + "'"
    command_string += " quit"
    print("My command is", command_string)
    stream = os.popen(command_string)
    lines = stream.readlines()
    print("done")

def zoom_search(query):
    query_string = ""

    if query["title"]:
        query_string += "@attr 1=4 " + query["title"]
    if query["author"]:
        if query_string != "": query_string = "@and " + query_string
        query_string += "@attr 1=1003 " + query["author"]

    print("My query string is ", query_string)


def main():
    zoom_search({"title": "zen and the art of motorcycle maintenance", "author": "pirsig"})
    zoomsh([{"verb": "connect", "arguments": "z3950.loc.gov:7090/Voyager"},
            {"verb": "set", "arguments": "preferredRecordSyntax marc21"},
            {"verb": "set", "arguments": "charset utf8"},
            {"verb": "find", "arguments": "xxfgdfgdfgdfg"},
            {"verb": "show", "arguments": "18 1 xml;charset=marc8,utf8"}])

if __name__ == "__main__":
    main()