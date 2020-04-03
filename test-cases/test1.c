int main()
{
        int a;
        int b;
        int c = a + b;

        if ((a < b) && (a > b)) {
                a++;
                b++;
                return 1;
        } else if (!c && !a) {
                return -1;
        } else {
                a = a - b;
                return 0;
        }
}