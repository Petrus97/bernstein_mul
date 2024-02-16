# R. Bernstein's algorithm for integer constant multiplication
Python implementation of the Bernstein algorithm for constant integer multiplication[[1]](#1). The implementation follows the final version developed by Briggs and Harvey in [[2]](#2).

## Example output
```zsh
 ~/bernstein_mul  python3 src/bernstein.py -c -82    
8 = 1 << 3; // SHIFT 3 times
7 = 8 - 1; // SHIFT_SUB
28 = 7 << 2; // SHIFT 2 times
21 = 28 - 7; // FACTOR_SUB
42 = 21 << 1; // SHIFT 1 times
-41 = 1 - 42; // SHIFT_REV
-82 = -41 << 1; // SHIFT 1 times
Number of operations: 7
GENERATED CODE:
---------------
// Multiply by -82 using the fewest operations
int multiply(int n)
{
        int t1, t2, t3, t4, t5, t6, t7;
        t1 = n << 3;
        t2 = t1 - n;
        t3 = t2 << 2;
        t4 = t3 - t2;
        t5 = t4 << 1;
        t6 = n - t5;
        t7 = t6 << 1;
        return t7;
}

---------------
```


## References
<a id="1">[1]</a> Bernstein, R., 1986. Multiplication by integer constants. Software: practice and experience, 16(7), pp.641-652.

<a id="2">[2]</a> Briggs, P. and Harvey, T., 1994. Multiplication by Integer Constants.