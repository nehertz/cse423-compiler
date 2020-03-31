int main()
{
        int a;
        int b;
        int c = a + b;

        if ((a < b) || (a > b) && c) {
                a++;
                b++;
                return 1;
        } else if (!c) {
                return -1;
        } else {
                a = a - b;
                return 0;
        }
}