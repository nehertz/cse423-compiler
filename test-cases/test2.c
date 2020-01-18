int main()
{
        unsigned int a = 2;
        auto b = 99;
        extern double c = 32.2;
        struct d;
        char e = 'e';
        union f;
        register short g = 1;
        long h = 99999999;
        static volatile enum i;
        const float j = 3.14;

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

        label:
                printf("label");

        

        return 0;
}

void func(int param1, int param2) {
        int aa = 1;
        int bb = 2;
        int cc = 3;

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

        cc++;
        cc--;

        int check == aa == 3 ? aa > 3 : return;

        dd = cc >> 3;
        ee = dd << 1;
        ff = ~ee;
        gg = ff & 1;
        hh = gg | 0;
        ii = gg ^ 1;

        int size = sizeof(aa);

        char *apple = "apple!";
        int where = &apple;

        return;
}