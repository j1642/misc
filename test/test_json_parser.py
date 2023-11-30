import json_parser

def test_lex_simple():
    # Lex the simplest JSON case
    json = """{"status":"SpaceTraders"}"""
    tokens = json_parser.lex(json)
    assert tokens == ["{", "status", ":", "SpaceTraders", "}"] 

def test_lex_array():
    # Lex array of booleans, null, and integer
    json = """{"list":[true, false, null, 21]}"""
    tokens = json_parser.lex(json)
    assert tokens == ["{", "list", ":",
        "[", "true", ",", "false", ",", "null", ",", "21", "]", "}"] 

def test_parsing():
    json = """{"status":"SpaceTraders","version":"v2.1.2","resetDate":
"2023-11-18","description":"SpaceTraders","stats":{"agents":1000,"ships":2637,
"systems":8498,"waypoints":171410}"""
    tokens = json_parser.lex(json)
    _, obj = json_parser.parse_obj(0, tokens)
    assert obj == {"status": "SpaceTraders",
                   "version": "v2.1.2",
                   "resetDate": "2023-11-18",
                   "description": "SpaceTraders",
                   "stats": {
                       "agents": 1000,
                       "ships": 2637,
                       "systems": 8498,
                       "waypoints": 171410
                   }
   }
