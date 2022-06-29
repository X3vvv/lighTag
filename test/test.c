#include <stdio.h>
int main() {
    int dis = 1234;
    int dis2 = dis/10;
    printf("%x\n", (dis2)&0xFF);
    return 0;
}