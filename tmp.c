#include <stdio.h>
int main()
{
    unsigned char x = 255;
    char y = (char) x;

    printf("x = %hhu & y = %hhd \n", x, y);
    return 0;
}