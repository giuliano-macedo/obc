/* Programa para calcular o mdc segundo o algoritmo de Euclides. */

int mdc (int u, int v)
{
  if (v == 0) return u;
  else return gcd(v, u-u/v*v);
  /* u-u/v*v == u mod v */
}

void main(void)
{ int x; int y;
  int z;

  x = 5;
  y = 10;
  z = mdc(x, y);
}