#define PY_SSIZE_T_CLEAN
#include <Python.h>

// Wide chars maintain string index equality between Python and C
int lex_num(int i, wchar_t *wc_json, size_t wc_len) {
    if (wc_json[i] == '-') {
        i++;
    }
    assert('0' <= wc_json[i] && wc_json[i] <= '9');
    if (wc_json[i] == '0' && wc_json[i + 1] != '.') {
        fprintf(stderr, "%s", "error: JSON numbers cannot have leading zeroes\n");
        //exit(1);
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

void print_string(size_t len, wchar_t *wchar) {
    printf("starting print\n");
    for (unsigned long i = 0; i < len; i++) {
        printf("%lc", wchar[i]);
    }
    printf("\n");
}
