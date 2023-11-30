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
