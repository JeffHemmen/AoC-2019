#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>

#define SIG_REP 10000
#define PHASES  100
#define OFFSET  5977737

void apply_phase(int* signal, int* new_sig, int sig_len) {
    int i, j, sum;
    for(int pos = 1; pos <= sig_len; pos++) { // in new_sig
        if(pos % 1000 == 1)
            printf("Processing position %7d of %d.\n", pos, sig_len);
        sum = 0;
        i = -1;
        i += pos;
        while(i < sig_len) {
            // add <pos> terms
            for(j=0; j<pos && i<sig_len; j++, i++) {
                sum += signal[i];
            }
            // skip next <pos>
            i += pos;
            if(i >= sig_len - 1)
                break;
            // sub <pos> terms
            for(j=0; j<pos && i<sig_len; j++, i++) {
                sum -= signal[i];
            }
            // skip next <pos>
            i += pos;
            if(i >= sig_len - 1)
                break;
        }
        new_sig[pos - 1] = abs(sum) % 10;
    }
}

void apply_phase_smart(int* signal, int* new_sig, int offset, int sig_len) {
    int i, j, sum;
    new_sig[sig_len - 1] = signal[sig_len - 1];
    for(int pos = sig_len - 1; pos >= offset; pos--) { // in new_sig
        sum = new_sig[pos] + signal[pos - 1];
        new_sig[pos - 1] = abs(sum) % 10;
    }
}

int main(int argc, char **argv) {
    FILE *fp;

    char filetext[1024];
    int short_sig[1024];
    char* filename = "input.txt";
    if(argc >= 2) {
        filename = argv[1];
    }

    fp = fopen(filename, "r");
    if (!fp) {
        printf("Error opening file \"%s\".\n", filename);
        return 1;
    }

    fgets(filetext, 1024, fp);
    int i;
    for(i = 0; filetext[i]; i++) {
        short_sig[i] = filetext[i] - '0';
    }
    int short_sig_len = i;
    int short_sig_bytes = i * sizeof(int);
//    printf("Short signal has %d characters, i.e. %d bytes.\n", short_sig_len, short_sig_bytes);

    int sig_len = short_sig_len * SIG_REP;
    int sig_bytes = short_sig_bytes * SIG_REP;
//    printf("Real signal has %d characters, i.e. %d bytes.\n", sig_len, sig_bytes);

    assert(sig_bytes == sig_len * sizeof(int)); // sanity check
    int *signal = malloc(sig_bytes);
    int *new_sig = malloc(sig_bytes);
//    printf("Allocated two int arrays with %d bytes each.\n", sig_bytes);
//    printf("Address of signal : %d\n", (int)signal);
//    printf("Address of new_sig: %d\n", (int)new_sig);


    for(i=0; i<SIG_REP; i++) {
//        if(!(i%1000)) {
//            printf("%d\n", i);
//            printf("[%5d]: Copying %d bytes from <short_sig> to <signal> + %d\n", i, short_sig_bytes, i * short_sig_bytes);
//        }
        memcpy(signal + (i * short_sig_len), short_sig, short_sig_bytes);
    }

//    printf("OK\n");

    for(int phase=0; phase < PHASES; phase++) {
//        printf("Applying phase %3d...\n", phase);
        apply_phase_smart(signal, new_sig, OFFSET, sig_len);
        int *tmp = signal;
        signal = new_sig;
        new_sig = tmp;
        memset(new_sig, 0, sig_bytes);
    }

    for(int offset = OFFSET; offset < OFFSET + 8; offset++) {
        printf("%d", signal[offset]);
    }
    printf("\n");

}
