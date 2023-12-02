"""
Convert a JSON file to a Python object.

Use: python json_parser.py json_file.txt
"""

import sys

def next(i, json):
    # Get next token
    # id(json) is the same in lex() and next(), cool pass by reference
    # Loop prevents excess calls to next() if lots of whitespace is found
    while i < len(json):
        orig_i = i
        if json[i] in ("[", "]", "{", "}", ":", ","):
            return (i + 1, json[i])
        elif json[i] == '"':
            # TODO: refactor lexing escape characters
            paired_backslash = True
            remove_indexes = []
            i += 1
            while True:
                while json[i] != '"':
                    if json[i] == "\\":
                        paired_backslash ^= True
                        if json[i + 1] not in '"\\/bfnrtu':
                            raise ValueError("invalid JSON backslash found")
                        remove_indexes.append(i)
                    i += 1
                assert json[i] == '"'
                # Return token when an unescaped quotation mark is found
                # TODO: check escaped unicode values \uABCD
                if paired_backslash or json[i-1] != "\\":
                    token = json[orig_i + 1:i]
                    if remove_indexes:
                        token = list(token)
                        # zip() probably has a higher runtime cost
                        control_chars = (('b', '\b'), ('f', '\f'), ('n', '\n'),
                                         ('r', '\r'), ('t', '\t'))
                    # orig_i is index of initial ", so use orig_i + 1
                    for idx in remove_indexes:
                        if json[idx + 1] == '"' or json[idx + 1] == "/":
                            del token[idx - (orig_i + 1)]
                            continue
                        for letter, control_char in control_chars:
                            if json[idx + 1] == letter:
                                token[idx - orig_i] = control_char
                                del token[idx - (orig_i + 1)]
                    if isinstance(token, list):
                        token = ''.join(token)
                    # remove \ from token?
                    return (i + 1, token)
                i += 1
            # Omit quotation marks from returned string
            return (i + 1, json[orig_i + 1:i])
        elif json[i].isalpha():
            if json[i:i + 4] == "true":
                return (i + 4, True)
            elif json[i:i + 4] == "null":
                return (i + 4, None)
            elif json[i:i + 5] == "false":
                return (i + 5, False)
            else:
                raise ValueError(f"""invalid string is missing quotation marks:
                                 {json[i:i+10]}""")
        elif json[i].isdigit() or (json[i] == "-" and json[i + 1].isdigit()):
            if json[i] == "-":
                i += 1
            # Allow floats like 0.1
            if json[i] == "0" and json[i + 1] != ".":
                raise ValueError("JSON numbers cannot have leading zeroes")
            while json[i].isdigit():
                i += 1
            # Check for floats
            if json[i] == "." and json[i + 1].isdigit():
                i += 1
                while json[i].isdigit():
                    i += 1
                # Check for scientific notation
                if json[i] == "e" or json[i] == "E":
                    i += 1
                    if json[i] == "+" or json[i] == "-":
                        i += 1
                    while json[i].isdigit():
                        i += 1

            return (i, float(json[orig_i:i]))
        else:
            i += 1
    if i >= len(json):
        return ValueError("next() did not return")

def lex(json):
    # Convert a JSON string to a 'tokens' iterable
    if json[0] == "{" and json[-1] == "}":
        pass
    elif json[0] == "[" and json[-1] == "]":
        pass
    else:
        raise ValueError(f"""JSON must begin and end with curly braces or
                         brackets. start={json[0]}, end={json[-1]}""")
    i = 0
    tokens = []
    while i < len(json):
        i, token = next(i, json)
        tokens.append(token)
    return tokens

def parse_array(i, tokens):
    # Convert the 'tokens' iterable to Python object
    values = []
    while i < len(tokens):
        # Do not increment i here, increment at end of the parse_obj() loop
        if tokens[i] == "]":
            return i, values
        elif tokens[i] == "{":
            i, obj = parse_obj(tokens, i + 1)
            values.append(obj)
        elif tokens[i] == "[":
            i, arr = parse_array(i + 1, tokens)
            values.append(arr)
        elif tokens[i] != ",":
            values.append(tokens[i])
            if tokens[i + 1] != "," and tokens[i + 1] != "]":
                raise ValueError(
                        "parse_array() did not find delimiter or end of array"
                )
            i += 1
        elif tokens[i] == ",":
            if tokens[i + 1] == "]":
                raise ValueError("JSON spec disallows trailing comma in arrays")
            i += 1
        else:
            raise ValueError("unexpected value:", tokens[i])

    if i >= len(tokens):
        raise ValueError("parse_array() did not find end of array")

def parse_obj(tokens, i=1):
    obj = {}
    key = ""
    while i < len(tokens):
        token = tokens[i]
        if token == "{":
            i, child_obj = parse_obj(tokens, i + 1)
            assert key
            obj[key] = child_obj
            key = ""
        elif token == "}":
            return i + 1, obj
        elif token == "[":
            i, arr = parse_array(i + 1, tokens)
            assert key
            obj[key] = arr
            key = ""
        elif token == ":":
            assert key
        elif token == ",":
            assert key == ""
        elif token in (None, True, False):
            assert key
            obj[key] = token
            key = ""
        else:
            if key == "":
                key = token
            else:
                obj[key] = token
                key = ""
        i += 1
    return i, obj

def parse(tokens):
    if tokens[0] == "{":
        return parse_obj(tokens)
    elif tokens[0] == "[":
        return parse_array(1, tokens)
    raise ValueError(f"""invalid JSON beginning or end char: begin={tokens[0]},
                     end={tokens[-1]}""")

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        json = f.read()
    # multiple files end in Unicode 10 control code
    json = json[:-1]
    tokens = lex(json)
    obj = parse(tokens)
    print(obj[1])
