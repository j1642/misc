import ctypes

parse_funcs = ctypes.CDLL('./parse_funcs.so')
print(parse_funcs.parse_num(212, "Σ json text".encode('utf-8')))
