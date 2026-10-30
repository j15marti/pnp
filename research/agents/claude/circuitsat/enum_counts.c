// Exhaustive enumeration of fan-in-2 B2 circuits (10 non-degenerate binary ops, sharing allowed)
// usage: enum_counts n g ; prints for each #sat value k whether some g-gate circuit (output = last gate) attains it
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static int n,G; static unsigned tt[16]; static unsigned mask; static char seen[1<<17];
static int ops[10]={0x8,0x4,0x2,0x1,0x7,0xB,0xD,0xE,0x6,0x9}; // AND, a&~b, ~a&b, NOR, NAND, a|~b.. (see apply)
static unsigned ap(int op,unsigned a,unsigned b){unsigned r=0;
 if(op&8)r|=a&b; if(op&4)r|=a&~b; if(op&2)r|=~a&b; if(op&1)r|=~a&~b; return r&mask;}
static void rec(int i){
  if(i==G){ seen[__builtin_popcount(tt[n+G-1])]=1; return; }
  int m=n+i;
  for(int a=0;a<m;a++)for(int b=a+1;b<m;b++)for(int o=0;o<10;o++){
    tt[m]=ap(ops[o],tt[a],tt[b]); rec(i+1);} }
int main(int c,char**v){n=atoi(v[1]);G=atoi(v[2]);int N=1<<n;mask=(N==32)?0xffffffffu:((1u<<N)-1);
 for(int j=0;j<n;j++){unsigned t=0;for(int x=0;x<N;x++)if(x>>j&1)t|=1u<<x;tt[j]=t;}
 rec(0); printf("n=%d g=%d achievable #sat:",n,G);for(int k=0;k<=N;k++)if(seen[k])printf(" %d",k);printf("\n");}
