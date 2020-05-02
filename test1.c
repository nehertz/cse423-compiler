<<<<<<< master
int add3(int a, int b, int c)
{
<<<<<<< master
        int e = 1;
<<<<<<< master
//   return a + b + c;
=======
        return a + b + c;
>>>>>>> fixed bugs
=======
        
        return 1;
>>>>>>> Function Calls are done
}
=======
// int add3(int a, int b, int c)
// {
//         int e = 1;
//   return a + b + c;
// }
<<<<<<< HEAD
>>>>>>> Fixed some bugs in code gen
=======
>>>>>>> assembly_assignment

int main()
{     

        //// Test var decl 
        // int aa;
        // int bb; 
        // int a = 100;
        // int b = 30;
        // float e = 20.2;
        // int c;
        // a = b;
        // int e, f, g;

        //// Test assignment and Arithmetic
        ////assignment = ['=' ,'*=', '/=', '%=', '+=', '-=', '<<=',  '>>=', '&=', '|=', '^=']
        ////arithmetic = ['<<', '>>', '+', '-', '*', '/', '%', '|', '&', '~', '^'] 
        // a =  b << 3;
        // a =  b >> 3;
        // a =  b + 3;
        // a =  b - 3;
        // a = b * 3;
        // a = b / 3;
        // a = b % 3;
        // a = b | 3;
        // a = b & 3;
        // a = b ^ 3;
        // a *=  b >> 3;
        // a /=  b + 3;
        // a %=  b - 3;
        // a += b * 3;
        // a -= b / 3;
        // a <<= b % 3;
        // a >>= b | 3;
        // a &= b & 3;
        // a |= b ^ 3;

        // Test complex arithmetic expression 
        // a = (a + b) * 2;

        //// Unary 
<<<<<<< master
        int a,b;
        // a = (-a + b) * 2;
        // b = sizeof(a);
=======
        // int a,b;
        // b = (-a + b) * 2;
        ///TODO: sizeof not supported;
<<<<<<< HEAD
>>>>>>> Fixed some bugs in code gen
=======
>>>>>>> assembly_assignment

        ////TODO: Type casting not support 
        // float f = 10.5;
        // a = f;
        // a = f + b;

        // // Goto stmt 
        // goto even;
        // even:
        //         a = 1;
        // int a;
        //   while ( a > 3 && a < 1 ) {
        //         // continue;
        //         // break;
        //         // float j = j + 2;
        // }
        // while and do while loop
        // int a;
        // while ( a + 1 > 3 || a < 1 ) {
        //         // continue;
        //         // break;
        //         float j = j + 2;
        // }

        // do {
        //         int i =  10;
        //         // float j = j + 2;
        // } while (a < 3);

        
        ////test for loop 
        // for (int i = 1; i < 5; i++){
        //         i += 10;
        // }
        // a = a + 1;
        ////test return stmt
<<<<<<< HEAD
<<<<<<< master
        // return add(a, b);
=======
        // return add3(a, b, c);
>>>>>>> Fixed some bugs in code gen
=======
        // return add3(a, b, c);
>>>>>>> assembly_assignment
        // return 1 + 2 + a +b;
        // return 1+2;
        // return a = 1 + 2;
        // return 1 + 2 + 3;

        // Samuel Example 1:
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

        //test if-statement 
        if(a > 2){
          ++b;    
        } else if (a > b){
          a = b;
        } else {
          a = 1;
        }

        // return 0;
}