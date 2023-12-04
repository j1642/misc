#define PY_SSIZE_T_CLEAN
#include <Python.h>

int parse_num(int i, char *json) {
    int len = strlen(json);
    //printf("i=%d, json=%s\n", i, json); // prints sigma correctly
    wchar_t wc_json[len * 2];
    // Count characters in a string, accounting for multi-bytes
    size_t wc_len = mbstowcs(wc_json, json, len * 2);

    if (wc_json[i] == '-') {
        assert('0' <= wc_json[i + 1] && wc_json[i + 1] <= '9');
        i++;
    } else {
        assert('0' <= wc_json[i] && wc_json[i] <= '9');
    }
    if (wc_json[i] == '0' && wc_json[i + 1] != '.') {
        fprintf(stderr, "%s", "error: JSON numbers cannot have leading zeroes\n");
        exit(1);
    }
    while ('0' <= wc_json[i] && wc_json[i] <= '9') {
        i++;
    }
    if (wc_json[i] == '.') {
        if (wc_json[i + 1] < '0' || '9' < wc_json[i + 1]) {
            fprintf(stderr, "%s", "error: decimal point not followed by digits\n");
            exit(1);
        }
        i++;
        while ('0' <= wc_json[i] && wc_json[i] <= '9') {
            i++;
        }
        if (wc_json[i] == 'e' || wc_json[i] == 'E') {
            //printf("entered exponent if\n");
            i++;
            if (wc_json[i] == '+' || wc_json[i] == '-') {
                i++;
                while ('0' <= wc_json[i] && wc_json[i] <= '9') {
                    i++;
                }
            }
        }
    }
    if ((unsigned long)i > wc_len) {
        fprintf(stderr, "%s", "error: escaped end of JSON string\n");
        exit(1);
    }
    return i;
}
