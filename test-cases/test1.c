int main()
{
        int a;
        int b;
        int c = a + b;

        if ((a < b) && (a > b) || c) {
                a++;
                b++;
        } else if (!(c && a)) {
                a = 2;
        } else {
                a = a - b;
        }

        return 0;
}