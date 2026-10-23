// Exact minimum B2 (all 2-input gates, free negation) circuit size for functions of n<=4 inputs.
// Iterative deepening over gate sequences; truth tables as bitmasks. Each run is far below 30 s for the listed targets.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static int n, NT; static unsigned MASK;
static unsigned val[32]; static int nn;
static unsigned target;
static int ops[10]={0x8,0x4,0x2,0x1,0xE,0xD,0xB,0x7,0x6,0x9}; // 4-bit gate truth tables (AND-type,OR-type,XOR,XNOR)
static unsigned apply(int op,unsigned a,unsigned b){unsigned r=0;
 if(op&8)r|=a&b; if(op&4)r|=a&~b; if(op&2)r|=~a&b; if(op&1)r|=~a&~b; return r&MASK;}
static int dfs(int left,int lastkey){
 if(left==0) return 0;
 for(int i=0;i<nn;i++)for(int j=i+1;j<nn;j++)for(int o=0;o<10;o++){
  unsigned f=apply(ops[o],val[i],val[j]);
  if(left==1){ if(f==target||f==(~target&MASK)) return 1; continue;}
  int dup=0; for(int k=0;k<nn;k++) if(val[k]==f||val[k]==(~f&MASK)){dup=1;break;}
  if(dup) continue;
  int key=(i*32+j); // canonical order: nondecreasing (j,i) among consecutive independent gates is skipped for simplicity
  val[nn++]=f; int r=dfs(left-1,key); nn--; if(r) return 1;
 }
 return 0;}
static int minsize(unsigned t){target=t&MASK; nn=n;
 for(int v=0;v<n;v++){unsigned m=0;for(unsigned x=0;x<NT;x++) if((x>>v)&1)m|=1u<<x; val[v]=m;}
 for(int i=0;i<n;i++) if(target==val[i]||target==(~val[i]&MASK)) return 0;
 for(int g=1;g<=6;g++) if(dfs(g,-1)) return g; return -1;}
int main(int argc,char**argv){ n=atoi(argv[1]); NT=1<<n; MASK=(NT==32)?0xFFFFFFFFu:((1u<<NT)-1);
 unsigned t=strtoul(argv[2],0,0); printf("%d\n",minsize(t)); }
