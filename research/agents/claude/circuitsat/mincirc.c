// Exact min #gates (fan-in-2, full binary basis B2) for all n-var Boolean functions, n<=4.
// Iterative deepening DFS over normal circuits (op(0,0)=0), canonical gate ordering.
// usage: mincirc n maxdepth ; prints cost histogram and per-function costs (file out)
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef unsigned int u32;
int n, NF, K; u32 full; u32 tt[16]; int ia[16], ib[16];
signed char *cost; long nodes=0; int found;
// normal nondegenerate ops on (a,b): and, a&~b, ~a&b, or, xor
static inline u32 op(int o,u32 a,u32 b){switch(o){case 0:return a&b;case 1:return a&~b;case 2:return ~a&b;case 3:return a|b;default:return a^b;}}
int cur_budget;
void dfs(int m,int k){ // m = #nodes so far (inputs+gates), k gates used
  // record all current gates' functions
  nodes++;
  if(k==cur_budget) return;
  int last_i = (k>0)? ia[m-1]:-1, last_j = (k>0)? ib[m-1]:-1;
  for(int j=1;j<m;j++)for(int i=0;i<j;i++){
    if(k>0 && !(j==m-1) ){ // gate doesn't use previous gate => keys must be nondecreasing
      if(j<last_j || (j==last_j && i<last_i)) continue;
    }
    for(int o=0;o<5;o++){
      u32 f=op(o,tt[i],tt[j])&full;
      if(f==0) continue;
      int dup=0; for(int t=0;t<m;t++) if(tt[t]==f){dup=1;break;}
      if(dup) continue;
      tt[m]=f; ia[m]=i; ib[m]=j;
      int c=k+1;
      unsigned idx=f; // normal fn index (bit0 = 0 always)
      if(cost[idx]<0||cost[idx]>c) cost[idx]=c;
      dfs(m+1,k+1);
    }
  }
}
int main(int argc,char**argv){
  n=atoi(argv[1]); K=atoi(argv[2]); int bits=1<<n; full=(bits==32)?0xffffffffu:((1u<<bits)-1);
  // truth tables with bit x = value on input x; normal => bit0=0
  for(int v=0;v<n;v++){u32 t=0;for(int x=0;x<bits;x++) if((x>>v)&1) t|=1u<<x; tt[v]=t;}
  NF=1<<bits; cost=malloc(NF); memset(cost,-1,NF);
  for(int v=0;v<n;v++) cost[tt[v]]=0; cost[0]=0;
  for(int b=1;b<=K;b++){cur_budget=b; dfs(n,0);} // note: IDDFS redundant but gives min via cost[] update
  int hist[20]={0},unk=0;
  for(u32 f=0;f<(u32)NF;f+=2){ // normal functions: bit0=0 -> even index
    int c=cost[f]; if(c<0) unk++; else hist[c]++; }
  printf("n=%d normal functions=%d nodes=%ld unknown(>%d)=%d\n",n,NF/2,nodes,K,unk);
  for(int c=0;c<20;c++) if(hist[c]) printf("  cost %d: %d functions (x2 with output negation=%d)\n",c,hist[c],2*hist[c]);
  return 0;}
