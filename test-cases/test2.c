#include <stdio.h>
struct Name {
        int a;
}name_t;
void func(int param1, int param2);

void func(int param1, int param2) {
        int aa = 1;
        int bb = 2;
        int cc = 3;

        //test assignment operators
        aa += 1;
        bb -= 2;
        cc *= 9;
        cc /= 3;
        aa %= 1;
        bb <<= 1;
        bb >>= 1;
        bb &= 1;
        bb ^= 1;
        bb |= 1;

        //test In/Decrement operators
        cc++;
        cc--;

        //test Conditional operators
        int check == aa == 3 ? aa > 3 : return;

        //test Bitwise operators
        int dd = cc >> 3;
        int ee = dd << 1;
        int ff = ~ee;
        int gg = ff & 1;
        int hh = gg | 0;
        int ii = gg ^ 1;

        //test Special operators
        int size = sizeof(aa);
        //char *apple = "apple!";
        int where = &apple;

        return;
        /* 
        Shah Yash 
        */
}

struct Yash {
        int b
};
int main()
{
        unsigned int a = 2;
        auto int b = 99;
        struct d;
        typedef signed long slong;
        char e = 'e';
        union f;
        register short g = 1;
        long h = 99999999;
        static volatile enum i;
        const float j = 3.14;
        int arr[10];
        a = (int) ++ a;


        if (a + b - c * g / j % h == 42) {
                
        } else if (a != b && a > b || !(a < b)) {
                if (a <= b) {
                        return 1;
                }
                if (a >=  b) {
                        return 2;
                }
        } else {
                return 3;
        }

        for(a = 0; a < 10; a++){
                if(a < 8){
                        continue;
                }        
        }

        switch (a)
        {
                case 9: 
                        a = 1;
                        break;
        
                default:
                        a = 0; 
                        break;
        }



        label:
                printf("label");

        do {
                a = a + 1;

        }while( a < 10);


        return 0;
}



void func2(int param1) {
        if (param1 % 2 == 0){
                goto even;
        } else {
                goto odd;
        }

        even: 
                return;
        odd:
                return;
}