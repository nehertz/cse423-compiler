// int add3(int a, int b, int c)
// {
//   return a + b + c;
// }
// enum week{Mon = 10, Tue, Wed, Thur = 20, Fri, Sat, Sun};

int main()
{     
        // Test enum 
        // enum week day; 
        // day = Mon; 
        // day = Tue; 
        // day = Wed; 
        // day = Thur; 
        // day = Fri; 
        // day = Sat; 
        // day = Sun;
        // day = Mon + 10; 

        //// Test var decl 
        int aa;
        int bb; 
        int a = 100;
        int b = 30;
        float e = 20.2;
        int c = 10 / e;
        return aa;
        // int c; 
        // float d;
        // int e, f, g;

        //// Test assignment and Arithmetic
        ////assignment = ['=' ,'*=', '/=', '%=', '+=', '-=', '<<=',  '>>=', '&=', '|=', '^=']
        ////arithmetic = ['<<', '>>', '+', '-', '*', '/', '%', '|', '&', '~', '^'] 
        // a =  b << 3;
        // a =  b >> 3;
        // a =  b + 3;
        // a =  b - 3;
        // a = b * 3;
        a = b / 3;
        a = b % 3;
        // a = b | 3;
        // a = b & 3;
        // a = b ^ 3;
        // a *=  b >> 3;
        // a /=  b + 3;
        // a %=  b - 3;
        // a += b * 3;
        a -= b / 3;
        // a <<= b % 3;
        // a >>= b | 3;
        // a &= b & 3;
        // a |= b ^ 3;

        // Test complex arithmetic expression 
        // a = (a + b) * 2;

        //// Unary 
        // int a,b;
        // b = (-a + b) * 2;
        // b = sizeof(a);

        //// Type casting
        // float f = 10.5;
        // a = f;
        // a = f + b;

        //// Goto stmt 
        // goto even;
        // even:
        //         a = 1;
         
        // while and do while loop
        // int a;
        // while ( a + 1 > 3 || a < 1 ) {
        //         //continue;
        //         // break;
        //         float j = j + 2;
        // }

        // do {
        //         int i = i + 1;
        //         float j = j + 2;
        // } while (a < 3);

        
        ////test for loop 
        // for (int i = 1; i < 5; i++){
        //         i += 10;
        // }
        // a = a + 1;
        ////test return stmt
        //return add(a, b);
        // return 1 + 2 + a +b;
        // return 1+2;
        // return a = 1 + 2;
        // return 1 + 2 + 3;

        // //Samuel Example 1:
        // int i, j, k;
        // i = 1;
        // j = 3;
        // k = 5;
        // i = i * add3(i,j,k);
        // return i;

        // Samuel Example 2:
        // int i, j;
        // j = 0;
        // for(i = 0; i < 10; ++i)
        // {
        // if(i%2 == 0){
        //         ++j;    
        // }
        // }
        // return j;

        ////test if-statement 
        // if(a%2 == 0){
        //   ++b;    
        // } else if (a > b){
        //   a = b;
        // } else if (a > b){
        //   a = b;
        // } else {
        //   a = 1;
        // }

        return 0;
}