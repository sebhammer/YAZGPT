import os
import re
import json

def get_subfield(field, sf):
    for s in field['subfields']:
        subfield, value = list(s.items())[0]
        if subfield == sf:
            return value
    return ""

# Parse a dict representation of a MARC record into a compact form suitable for an LLM
# This should be vastly improved to handle more non-book edge cases
def parse_bib(record):
    res = []
    for b in record['fields']:
        field, value = list(b.items())[0] # Unpacking that goofy JSON-MARC thing
        # print(field, value)
        match field:
            case "100":
                res.append({'author': get_subfield(value, 'a')})
            case "700"|"710":
                res.append({'contributor': get_subfield(value, 'a') + " " + get_subfield(value, 'e')})
            case "245":
                res.append({'title': get_subfield(value, 'a')})
            case "260"|"264":
                res.append({'publication': get_subfield(value, 'a') + get_subfield(value, "b") + \
                        get_subfield(value, "c")})
    return res

# Parse the output of zoomsh into a hitcount and records and records parsed into dicts
def zoomsh_results(lines):
    # Grab the hitcount
    first_line =  lines.pop(0)
    results_pattern = re.compile(r'^.*: (\d*) hits')
    r = results_pattern.search(first_line)
    result = { 'hits': r.group(1), 'records': [] }

    # Check if this is the start of a new record
    recordline_pattern = re.compile(r'^(\d*) .*')
    # Outer loop runs through records, as long as it finds a line like
    # 19 database=Voyager syntax=USmarc schema=unknown
    while len(lines):
        recordline = lines[0]
        rm = recordline_pattern.search(recordline)
        tmp = rm.groups(1)
        if not rm or not rm.groups(1):
            break
        lines.pop(0)
        # Grab lines of JSON and add to buffer until we're done (closing bracket in position 0)
        record_text = ''
        while len(lines):
            record_text += lines[0]
            if lines.pop(0) == '}\n':
                break
        record_dict = json.loads(record_text)
        result['records'].append(parse_bib(record_dict))
        if len(lines): # Grab the empty line after a record, if there is one
            lines.pop(0)

    return result

# Grap the fields we care about out of a list of MARC records and add to the result dict
def interpret_records(result):
    return True

# Build a shell command line and call zoomsh, parse results and return results
def zoomsh(args):
    command_string = "zoomsh -a apdulog"
    for command in args:
        command_string += " '" + command['verb'] + " " + command['arguments'] + "'"
    command_string += " quit"
    print("My command is", command_string)
    stream = os.popen(command_string)
    lines = stream.readlines()
    return zoomsh_results(lines)

# Construct a boolean PQF query from a dict with field-term pairs
def zoom_makequery(query):
    query_string = ""
    for field, term in query.items():
        if query_string: query_string = "@and " + query_string + " "
        match field:
            case "title":
                query_string += "@attr 1=4"
            case "author":
                query_string += "@attr 1=1003"
            case "subject":
                query_string += "@attr 1=21"
            case "date":
                query_string += "@attr 1=30"
        query_string += ' "' + term + '"'
    return query_string

def main():
    query = zoom_makequery({"title": "water bottle"})
    r = zoomsh([{"verb": "connect", "arguments": "z3950.loc.gov:7090/Voyager"},
            {"verb": "set", "arguments": "preferredRecordSyntax marc21"},
            {"verb": "set", "arguments": "charset utf8"},
            {"verb": "find", "arguments": query},
            {"verb": "show", "arguments": "1 30 json;charset=marc8,utf8"}])
    print(r)

if __name__ == "__main__":
    main()