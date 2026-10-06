#include <stdio.h>
#include <stddef.h>
__attribute__((noinline)) static void demo_decode(unsigned char *p, size_t n, unsigned char key){ for(size_t i=0;i<n;i++) p[i]^=key; }
int main(void){ unsigned char s[]={0x3b,0x2f,0x2e,0x32,0x35,0x28,0x33,0x20,0x3f,0x3e,0}; demo_decode(s,10,0x5a); puts((char*)s); return 0; }
