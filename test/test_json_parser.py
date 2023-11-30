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
    _, obj = json_parser.parse_obj(tokens)
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

def test_full_parsing():
    json = """{"status":"SpaceTraders","version":"v2.1.2","resetDate":"2023-11-18","description":"SpaceTraders","stats":{"agents":1000,"ships":2637,"systems":8498,"waypoints":171410},"leaderboards":{"mostCredits":[{"agentSymbol":"WHYANDO","credits":54773386},{"agentSymbol":"SG-1-DEVX","credits":27622741},{"agentSymbol":"WHYAIR","credits":26829125},{"agentSymbol":"EMBERCOM","credits":19870328},{"agentSymbol":"SAFPLUSPLUS","credits":18308138},{"agentSymbol":"SIKAYN","credits":14398264},{"agentSymbol":"CTRI-U-","credits":12363331},{"agentSymbol":"SG-1-DEVX2","credits":11278192},{"agentSymbol":"ESEIDEL","credits":9314458},{"agentSymbol":"PHANTASM","credits":5593649},{"agentSymbol":"RDTST3","credits":2990498},{"agentSymbol":"RDTST1","credits":2965963},{"agentSymbol":"RUTHLESSDUCK","credits":2888722},{"agentSymbol":"CTRI-V-","credits":929640},{"agentSymbol":"RD-SAT-LOL","credits":522327}],"mostSubmittedCharts":[]},"serverResets":{"next":"2023-12-02T16:00:00.000Z","frequency":"fortnightly"},"announcements":[{"title":"Server Resets","body":"We"},{"title":"Support Us","body":"Supporters"},{"title":"Discord","body":"Our"}],"links":[{"name":"Website","url":"https://spacetraders.io/"},{"name":"Documentation","url":"https://docs.spacetraders.io/"},{"name":"Playground","url":"https://docs.spacetraders.io/playground"},{"name":"API Reference","url":"https://spacetraders.stoplight.io/docs/spacetraders/"},{"name":"OpenAPI Spec - Bundled","url":"https"},{"name":"OpenAPI Spec - Source","url":"https://"},{"name":"Discord","url":"https://discord.com/invite/jh6zurdWk5"},{"name":"Support Us","url":"https://donate"},{"name":"Report Issues","url":"https://github.com/SpaceTradersAPI/api-docs/issues"},{"name":"Wiki","url":"https://github.com/SpaceTradersAPI/api-docs/wiki"},{"name":"Account Portal (Coming Soon)","url":"https://my.spacetraders.io/"},{"name":"Twitter","url":"https://twitter.com/SpaceTradersAPI"}]}"""
    tokens = json_parser.lex(json)
    _, obj = json_parser.parse_obj(tokens)
    print(obj)
    assert obj == {"status": "SpaceTraders", "version": "v2.1.2",
                   "resetDate":"2023-11-18","description":"SpaceTraders",
                   "stats":{
                       "agents":1000,"ships":2637,"systems":8498,
                       "waypoints":171410
                    },
                   "leaderboards":{
                       "mostCredits":[
                           {"agentSymbol":"WHYANDO","credits":54773386},
                           {"agentSymbol":"SG-1-DEVX","credits":27622741},
                           {"agentSymbol":"WHYAIR","credits":26829125},
                           {"agentSymbol":"EMBERCOM","credits":19870328},
                           {"agentSymbol":"SAFPLUSPLUS","credits":18308138},
                           {"agentSymbol":"SIKAYN","credits":14398264},
                           {"agentSymbol":"CTRI-U-","credits":12363331},
                           {"agentSymbol":"SG-1-DEVX2","credits":11278192},
                           {"agentSymbol":"ESEIDEL","credits":9314458},
                           {"agentSymbol":"PHANTASM","credits":5593649},
                           {"agentSymbol":"RDTST3","credits":2990498},
                           {"agentSymbol":"RDTST1","credits":2965963},
                           {"agentSymbol":"RUTHLESSDUCK","credits":2888722},
                           {"agentSymbol":"CTRI-V-","credits":929640},
                           {"agentSymbol":"RD-SAT-LOL","credits":522327}
                        ],
                       "mostSubmittedCharts":[]
                    },
                   "serverResets":{
                       "next":"2023-12-02T16:00:00.000Z",
                       "frequency":"fortnightly"
                    },
                   "announcements":[
                       {"title":"Server Resets","body":"We"},
                       {"title":"Support Us","body":"Supporters"},
                       {"title":"Discord","body":"Our"}
                    ],
                   "links":[
                       {"name":"Website","url":"https://spacetraders.io/"},
                       {"name":"Documentation","url":"https://docs.spacetraders.io/"},
                       {"name":"Playground","url":"https://docs.spacetraders.io/playground"},
                       {"name":"API Reference","url":"https://spacetraders.stoplight.io/docs/spacetraders/"},
                       {"name":"OpenAPI Spec - Bundled","url":"https"},
                       {"name":"OpenAPI Spec - Source","url":"https://"},
                       {"name":"Discord","url":"https://discord.com/invite/jh6zurdWk5"},
                       {"name":"Support Us","url":"https://donate"},
                       {"name":"Report Issues","url":"https://github.com/SpaceTradersAPI/api-docs/issues"},
                       {"name":"Wiki","url":"https://github.com/SpaceTradersAPI/api-docs/wiki"},
                       {"name":"Account Portal (Coming Soon)","url":"https://my.spacetraders.io/"},
                       {"name":"Twitter","url":"https://twitter.com/SpaceTradersAPI"}]
    }
