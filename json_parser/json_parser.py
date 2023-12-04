"""
Convert a JSON file to a Python object.

Use: python json_parser.py json_file.txt
"""
import cProfile
import sys
import time
import ctypes

parse_funcs = ctypes.CDLL('./parse_funcs.so')

def lex(json, wchar_json):
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
        orig_i = i
        if json[i] in "[]{}:,":
            tokens.append(json[i])
            i += 1
        elif json[i] == '"':
            # TODO: refactor lexing escape characters
            paired_backslash = None
            remove_indexes = []
            i += 1
            appended = False
            # The outer loop ignores any escaped "
            while True:
                while json[i] != '"':
                    if json[i] == "\\":
                        if paired_backslash is None:
                            paired_backslash = False
                        else:
                            paired_backslash ^= True
                        if json[i + 1] not in '"\\/bfnrtu' and not paired_backslash:
                            raise ValueError("backslash followed by invalid",
                                             f"character: {json[i + 1]}")
                        if json[i + 1] == 'u':
                            for j in range(2, 6):
                                if json[i + j].lower() not in 'abcdef0123456789':
                                    raise ValueError('invalid escaped Unicode:',
                                                     f'{json[i:i+6]}')
                        if not paired_backslash:
                            remove_indexes.append(i)
                    elif paired_backslash is False:
                       paired_backslash = True
                    i += 1
                assert json[i] == '"'
                # Append token when an unescaped quotation mark is found
                if json[i-1] != "\\" or paired_backslash:
                    token = json[orig_i + 1:i]
                    if remove_indexes:
                        token = list(token)
                        # zip() probably has a higher runtime cost
                        control_chars = (('b', '\b'), ('f', '\f'), ('n', '\n'),
                                         ('r', '\r'), ('t', '\t'))
                    for idx in remove_indexes[::-1]:
                        if json[idx + 1] in '"/\\':
                            # orig_i is index of initial ", orig_i + 1 index is \
                            del token[idx - (orig_i + 1)]
                            continue
                        elif json[idx + 1] == 'u':
                            adj_idx = idx - (orig_i + 1)
                            hex_digits = ''.join(token[adj_idx + 2:adj_idx + 6])
                            unicode_char = chr(int(hex_digits, 16))
                            token[adj_idx] = unicode_char
                            del token[adj_idx + 1:adj_idx + 6]
                            continue

                        for letter, control_char in control_chars:
                            if json[idx + 1] == letter:
                                token[idx - orig_i] = control_char
                                del token[idx - (orig_i + 1)]
                                break

                    if isinstance(token, list):
                        token = ''.join(token)
                    tokens.append(token)
                    appended = True
                i += 1
                if appended:
                    break
        elif json[i].isalpha():
            if json[i:i + 4] == "true":
                i += 4
                tokens.append(True)
            elif json[i:i + 4] == "null":
                i += 4
                tokens.append(None)
            elif json[i:i + 5] == "false":
                i += 5
                tokens.append(False)
            else:
                raise ValueError(f"""invalid string is missing quotation marks:
                                 {json[i:i+10]}""")
        elif json[i].isdigit() or (json[i] == "-" and json[i + 1].isdigit()):
            end_i = parse_funcs.lex_num(i, wchar_json, len(json))
            tokens.append(float(json[i:end_i]))
            i = end_i
        elif json[i].strip() == "":
            i += 1
        else:
            raise ValueError(f"unexpected character={json[i]} in '{json[i:i+10]}'")

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

def parse(json):
    wchar_json = ctypes.c_wchar_p(json)
    tokens = lex(json, wchar_json)
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
    #pr = cProfile.Profile()
    #pr.enable()
    start = time.time()
    for _ in range(100):
        obj = parse(json)
    #pr.disable()
    #pr.print_stats()
    elapsed = time.time() - start
    print(obj)
    print("elapsed:", elapsed)

    # Time per 100 iterations of lexing and parsing (seconds)
    # 1.33 - lots of next() calls
    # 1.18 - combined lex() and next()
    # 1.27 - escaped characters implemented (full JSON spec supported)
    # 1.25 - call C function to lex numbers
