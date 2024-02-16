#include <assert.h>

// Multiply by -82 using the fewest operations
int multiply(int n) {
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

int main() {
  assert(multiply(1) == -82);
  assert(multiply(2) == -164);
  assert(multiply(3) == -246);
  assert(multiply(4) == -328);
  assert(multiply(5) == -410);
  assert(multiply(6) == -492);
}