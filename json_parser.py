def next(i, json):
    # Get next token
    # TODO: Copying the JSON string every call is slow
    # Loop prevents excess calls to next() if lots of whitespace is found
    while i < len(json):
        orig_i = i
        if json[i] in ("[", "]", "{", "}", ":", ","):
            i += 1
            return (i, json[i-1])
        elif json[i] == '"':
            i += 1
            while json[i] != '"':
                i += 1
            i += 1
            # Omit quotation marks from returned string
            return (i, json[orig_i + 1:i - 1])
        elif json[i].isalpha():
            if json[i:i + 4] in ("true", "null"):
                i += 4
                return (i, json[i - 4: i])
            elif json[i:i + 5] == "false":
                i += 5
                return (i, "false")
            else:
                i += 1
        elif json[i].isdigit():
            # TODO: add floats, scientific notation
            while json[i].isdigit():
                i += 1
            return (i, json[orig_i:i])
        else:
            i += 1

def lex(json):
    i = 0
    if json[0] != "{":
        exit("error: JSON must begin with '{'")
    tokens = []
    while i < len(json):
        i, token = next(i, json)
        if token is None:
            continue
        tokens.append(token)
    return tokens

def parse_array(i, tokens):
    values = []
    while i < len(tokens):
        if tokens[i] == "]":
            i += 1
            return i, values
        elif tokens[i].isalnum():
            values.append(tokens[i])
            i += 1
        elif tokens[i] == "[":
            i += 1
            values.append(parse_array(i, tokens))
        elif tokens[i] == "{":
            i += 1
            values.append(parse_obj(i, tokens))
        else:
            i += 1
    if i >= len(tokens):
        raise ValueError("parse_array() did not find end of array")

def parse_obj(i, tokens):
    obj = {}
    i = 0
    while i < len(tokens):
        if token == "{":
            x = parse_obj()
        elif token == "}":
            return obj
        elif token == "[":
            x = parse_array(i, tokens)
        #elif token == "]":
            # Should only be found in build_array()
            #pass #assert False
        elif token == ":":
            # expect value or array
            #val = next()
            #obj[key] = val
            pass
        elif token == ",":
            pass
        elif token in ("null", "true", "false"):
            pass
        i += 1

if __name__ == "__main__":
    json = """{"status":"SpaceTraders is currently online and available to play","version":"v2.1.2","resetDate":"2023-11-18","description":"SpaceTraders is a headless API and fleet-management game where players can work together or against each other to trade, explore, expand, and conquer in a dynamic and growing universe. Build your own UI, write automated scripts, or just play the game from the comfort of your terminal. The game is currently in alpha and is under active development.","stats":{"agents":981,"ships":2593,"systems":8498,"waypoints":171410},"leaderboards":{"mostCredits":[{"agentSymbol":"WHYANDO","credits":49033063},{"agentSymbol":"SG-1-DEVX","credits":23554646},{"agentSymbol":"WHYAIR","credits":23447152},{"agentSymbol":"EMBERCOM","credits":19870328},{"agentSymbol":"SAFPLUSPLUS","credits":16114234},{"agentSymbol":"SIKAYN","credits":14400580},{"agentSymbol":"SG-1-DEVX2","credits":11074824},{"agentSymbol":"CTRI-U-","credits":10381460},{"agentSymbol":"ESEIDEL","credits":4143143},{"agentSymbol":"RDTST1","credits":3011010},{"agentSymbol":"RDTST3","credits":3000019},{"agentSymbol":"RUTHLESSDUCK","credits":2986999},{"agentSymbol":"PHANTASM","credits":2838114},{"agentSymbol":"BLACKRAT","credits":1904066},{"agentSymbol":"CTRI-V-","credits":890783}],"mostSubmittedCharts":[]},"serverResets":{"next":"2023-12-02T16:00:00.000Z","frequency":"fortnightly"},"announcements":[{"title":"Server Resets","body":"We will be doing complete server resets frequently during the alpha to deploy fixes, add new features, and balance the game. Resets will typically be conducted on Saturday mornings. Previous access tokens will no longer be valid after the reset and you will need to re-register your agent. Take this as an opportunity to try and make it to the top of the leaderboards!"},{"title":"Support Us","body":"Supporters of SpaceTraders can reserve their agent call sign between resets. Consider donating to support our development: https://donate.stripe.com/28o29m5vxcri6OccMM"},{"title":"Discord","body":"Our Discord community is very active and helpful. Share what you're working on, ask questions, and get help from other players and the developers: https://discord.com/invite/jh6zurdWk5"}],"links":[{"name":"Website","url":"https://spacetraders.io/"},{"name":"Documentation","url":"https://docs.spacetraders.io/"},{"name":"Playground","url":"https://docs.spacetraders.io/playground"},{"name":"API Reference","url":"https://spacetraders.stoplight.io/docs/spacetraders/"},{"name":"OpenAPI Spec - Bundled","url":"https://stoplight.io/api/v1/projects/spacetraders/spacetraders/nodes/reference/SpaceTraders.json?fromExportButton=true&snapshotType=http_service&deref=optimizedBundle"},{"name":"OpenAPI Spec - Source","url":"https://github.com/SpaceTradersAPI/api-docs/blob/main/reference/SpaceTraders.json"},{"name":"Discord","url":"https://discord.com/invite/jh6zurdWk5"},{"name":"Support Us","url":"https://donate.stripe.com/28o29m5vxcri6OccMM"},{"name":"Report Issues","url":"https://github.com/SpaceTradersAPI/api-docs/issues"},{"name":"Wiki","url":"https://github.com/SpaceTradersAPI/api-docs/wiki"},{"name":"Account Portal (Coming Soon)","url":"https://my.spacetraders.io/"},{"name":"Twitter","url":"https://twitter.com/SpaceTradersAPI"}]}"""
    tokens = lex(json)
