#define PY_SSIZE_T_CLEAN
#include <Python.h>
//#include <stdio.h>

void parse_num(int i, char *json) {
    char len = 14;
    printf("i=%d, json=%s\n", i, json);
    printf("sizeof(json)=%lu\n", sizeof(json));
    fprintf(stderr, "%s", "error: error text\n"); // does not exit by itself
    printf("json bytes = ");
    for (int i = 0; i < len; i++) {
        printf("%d ", json[i]);
    }
    printf("\n");
    //char s[3];
    for (int i = 0; i < len; i++) {
//snprintf(s, 3, "%d", json[i]);
        //printf("%s ", s);
        //printf("%d ", json[i] + '0');
        //printf("%d ", (char)json[i]);
        printf("%c ", (char)json[i]);
    }
    printf("\n");
}

//        elif json[i].isdigit() or (json[i] == "-" and json[i + 1].isdigit()):
//            if json[i] == "-":
//                i += 1
//            # Allow floats like 0.1
//            if json[i] == "0" and json[i + 1] != ".":
//                raise ValueError("JSON numbers cannot have leading zeroes")
//            while json[i].isdigit():
//                i += 1
//            # Check for floats
//            if json[i] == ".":
//                if not json[i + 1].isdigit():
//                    raise ValueError(f"decimal point not followed by digits: idx={i}")
//                i += 1
//                while json[i].isdigit():
//                    i += 1
//                # Check for scientific notation
//                if json[i] == "e" or json[i] == "E":
//                    i += 1
//                    if json[i] == "+" or json[i] == "-":
//                        i += 1
//                    while json[i].isdigit():
//                        i += 1
//            tokens.append(float(json[orig_i:i]))
