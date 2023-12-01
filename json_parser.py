"""Convert a JSON string to a python object"""

def next(i, json):
    # Get next token
    # id(json) is the same in lex() and next(), cool pass by reference
    # Loop prevents excess calls to next() if lots of whitespace is found
    while i < len(json):
        orig_i = i
        if json[i] in ("[", "]", "{", "}", ":", ","):
            i += 1
            return (i, json[i-1])
        elif json[i] == '"':
            # TODO: allow escaped quotation marks and other characters
            i += 1
            while json[i] != '"':
                i += 1
            i += 1
            # Omit quotation marks from returned string
            return (i, json[orig_i + 1:i - 1])
        elif json[i].isalpha():
            if json[i:i + 4] == "true":
                i += 4
                return (i, True)
            elif json[i:i + 4] == "null":
                i += 4
                return (i, None)
            elif json[i:i + 5] == "false":
                i += 5
                return (i, False)
            else:
                i += 1
        elif json[i].isdigit():
            while json[i].isdigit():
                i += 1
            # Check for floats
            if json[i] == "." and json[i + 1].isdigit():
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
    i = 0
    if json[0] != "{" or json[-1] != "}":
        exit(f"JSON must begin and end with curly braces. start={json[0]}, end={json[-1]}")
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
        elif tokens[i].isalnum():
            values.append(tokens[i])
            if tokens[i + 1] != "," and tokens[i + 1] != "]":
                raise ValueError(
                        "parse_array() did not find delimiter or end of array"
                )
        elif tokens[i] == "[":
            i, arr = parse_array(i + 1, tokens)
            values.append(arr)
        else:
            # Increment i to prevent infinite loop
            i += 1
    if i >= len(tokens):
        raise ValueError("parse_array() did not find end of array")

def parse_obj(tokens, i=1):
    # TODO: allow first/last character to be [ and ]
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
                if token.isdigit():
                    obj[key] = int(token)
                else:
                    obj[key] = token
                key = ""
        i += 1
    return i, obj

if __name__ == "__main__":
    json = """{"status":"SpaceTraders","version":"v2.1.2","resetDate":"2023-11-18","description":"SpaceTraders","stats":{"agents":981,"ships":2593,"systems":8498,"waypoints":171410},"leaderboards":{"mostCredits":[{"agentSymbol":"WHYANDO","credits":49033063},{"agentSymbol":"SG-1-DEVX","credits":23554646},{"agentSymbol":"WHYAIR","credits":23447152},{"agentSymbol":"EMBERCOM","credits":19870328},{"agentSymbol":"SAFPLUSPLUS","credits":16114234},{"agentSymbol":"SIKAYN","credits":14400580},{"agentSymbol":"SG-1-DEVX2","credits":11074824},{"agentSymbol":"CTRI-U-","credits":10381460},{"agentSymbol":"ESEIDEL","credits":4143143},{"agentSymbol":"RDTST1","credits":3011010},{"agentSymbol":"RDTST3","credits":3000019},{"agentSymbol":"RUTHLESSDUCK","credits":2986999},{"agentSymbol":"PHANTASM","credits":2838114},{"agentSymbol":"BLACKRAT","credits":1904066},{"agentSymbol":"CTRI-V-","credits":890783}],"mostSubmittedCharts":[]},"serverResets":{"next":"2023-12-02T16:00:00.000Z","frequency":"fortnightly"},"announcements":[{"title":"Server Resets","body":"We"},{"title":"Support Us","body":"Supporters"},{"title":"Discord","body":"Our"}],"links":[{"name":"Website","url":"https://spacetraders.io/"},{"name":"Documentation","url":"https://docs.spacetraders.io/"},{"name":"Playground","url":"https://docs.spacetraders.io/playground"},{"name":"API Reference","url":"https"},{"name":"OpenAPI Spec - Bundled","url":"https://s"},{"name":"OpenAPI Spec - Source","url":"https://github.com/SpaceTradersAPI/api-docs/blob/main/reference/SpaceTraders.json"},{"name":"Discord","url":"https://discord.com/invite/jh6zurdWk5"},{"name":"Support Us","url":"https://donate.stripe.com/28o29m5vxcri6OccMM"},{"name":"Report Issues","url":"https://github.com/SpaceTradersAPI/api-docs/issues"},{"name":"Wiki","url":"https://github.com/SpaceTradersAPI/api-docs/wiki"},{"name":"Account Portal (Coming Soon)","url":"https://my.spacetraders.io/"},{"name":"Twitter","url":"https://twitter.com/SpaceTradersAPI"}]}"""

    tokens = lex(json)
    obj = parse_obj(tokens)
    print(obj[1])
