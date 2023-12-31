import os
import re
import json

import zlog

def get_subfield(field, sf):
    for s in field['subfields']:
        subfield, value = list(s.items())[0]
        if subfield == sf:
            return value
    return ""


def parse_bib(record):
    # Parse a dict representation of a MARC record into a compact form suitable for an LLM
    # This should be vastly improved to handle more non-book edge cases
    res = []
    for b in record['fields']:
        field, value = list(b.items())[0] # Unpacking that goofy JSON-MARC thing
        # print(field, value)
        match field:
            case "020":
                res.append({'isbn': get_subfield(value, 'a')})
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


def zoomsh_results(format, lines):
    # Parse the output of zoomsh into a hitcount and records and records parsed into dicts

    # Grab the hitcount
    first_line =  lines.pop(0)
    zlog.log(first_line)
    error_pattern = re.compile(r'^.* error: (.*)')
    r = error_pattern.search(first_line)
    if r:
        return { 'error': 'There was an error!', 'message': r.groups(1) }
    results_pattern = re.compile(r'^.*: (\d*) hits')
    r = results_pattern.search(first_line)
    result = { 'result_count': r.group(1), 'records': [] }
    if result['result_count'] == "0":
        result["error"] = "No hits. Try a broader search. If you were searching for an author, did \
        you remember to reverse the first and family name?"

    # Check if this is the start of a new record
    recordline_pattern = re.compile(r'^(\d*) .*')
    if format == "detailed":
        end_of_record = "\n"
    else:
        end_of_record = "}\n"
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
        # Line-formatted records are separated by two newlines
        record_text = ''
        while len(lines):
            record_text += lines[0]
            if lines.pop(0) == end_of_record:
                break
        if format == "brief":
            record_dict = json.loads(record_text)
            result['records'].append(parse_bib(record_dict))
        else:
            result['records'].append(record_text)
        if len(lines): # Grab the empty line after a record, if there is one
            lines.pop(0)

    return result


def zoomsh(format, args):
    # Build a shell command line and call zoomsh, parse results and return results
    command_string = "zoomsh -a apdulog"
    for command in args:
        command_string += " '" + command['verb'] + " " + command['arguments'] + "'"
    command_string += " quit"
    zlog.log(command_string)
    stream = os.popen(command_string)
    lines = stream.readlines()
    return zoomsh_results(format, lines)


def format(parm_string):
    query = json.loads(parm_string)
    if query.get("format"):
        return query["format"]
    else:
        return "brief"

def makequery(parm_string):
    # Construct a boolean PQF query from a dict with field-term pairs
    query = json.loads(parm_string)
    query_string = ""
    for field, term in query.items():
        if field == "format":
            continue
        if query_string: query_string = "@and " + query_string + " "
        match field:
            case "title":
                query_string += "@attr 1=4"
            case "author":
                query_string += "@attr 1=1003"
            case "isbn":
                query_string += "@attr 1=7"
            case "subject":
                query_string += "@attr 1=21"
            case "date":
                query_string += "@attr 1=30"
        query_string += ' "' + term + '"'
    return query_string

def main():
    query = makequery({"title": "water bottle"})
    r = zoomsh([{"verb": "connect", "arguments": "z3950.loc.gov:7090/Voyager"},
            {"verb": "set", "arguments": "preferredRecordSyntax marc21"},
            {"verb": "set", "arguments": "charset utf8"},
            {"verb": "find", "arguments": query},
            {"verb": "show", "arguments": "1 30 json;charset=marc8,utf8"}])
    print(r)

if __name__ == "__main__":
    main()