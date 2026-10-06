__attribute__((noinline)) static void crash_here(void) { volatile int *p = (int *)0; *p = 7; }
__attribute__((noinline)) static void middle(void) { crash_here(); }
int main(void) { middle(); return 0; }
