import ctypes

parse_funcs = ctypes.CDLL('./parse_funcs.so')
s = "Σ json -1.234e-5x"
actual = parse_funcs.parse_num(7, s.encode('utf-8'))
print("actual:", actual, f"({s[actual]})")
print("expected:", len(s) - 1)
