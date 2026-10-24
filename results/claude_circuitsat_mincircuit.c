// exact min #fan-in-2 gates (B2, output complement free) for all n-var functions, n<=3, via exhaustive DFS
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int n,T,maxk; unsigned tab[16]; int best[1<<16]; long long leaves=0;
unsigned mask;
void dfs(int cnt,int k){
  if(k>0){ unsigned f=tab[cnt-1]; if(best[f]>k)best[f]=k; }
  if(k==maxk) return;
  for(int i=0;i<cnt;i++)for(int j=i+1;j<cnt;j++){
    unsigned a=tab[i],b=tab[j];
    unsigned g[5]={a&b,a&~b&mask,~a&b&mask,a|b,a^b};
    for(int t=0;t<5;t++){ tab[cnt]=g[t]; dfs(cnt+1,k+1);} }
}
int main(int c,char**v){ n=atoi(v[1]); maxk=atoi(v[2]); T=1<<n; mask=(T==32)?0xffffffffu:((1u<<T)-1);
  for(int i=0;i<n;i++){unsigned t=0;for(int x=0;x<T;x++)if(x>>i&1)t|=1u<<x;tab[i]=t;}
  int NF=1<<T; for(int f=0;f<NF;f++)best[f]=99;
  for(int i=0;i<n;i++)best[tab[i]]=0; best[0]=0;
  dfs(n,0);
  // normal functions f(0)=0 ; complement pairs share cost
  int hist[12]={0}, histdep[12]={0}, un=0;
  for(int f=0;f<NF;f++){ int cst=best[f]; int cf=best[(~f)&mask]; if(cf<cst)cst=cf; 
    int dep=1; for(int i=0;i<n;i++){ unsigned sh=1u<<i,m=0; for(int x=0;x<T;x++)if(!(x>>i&1))m|=1u<<x; if((((unsigned)f&m)<<sh)==((unsigned)f&~m&mask)) dep=0; }
    // note: dep computed as "all variables essential"
    int d=cst>=99?11:cst; hist[d]++; if(dep)histdep[d]++; 
    // unique-sat functions: popcount==1
    if(__builtin_popcount(f)==1){ if(cst>un)un=cst; }
  }
  printf("n=%d maxgates=%d\n",n,maxk);
  for(int d=0;d<12;d++)if(hist[d])printf("  size %d: all=%d fully_dependent=%d\n",d,hist[d],histdep[d]);
  printf("  max cost over single-minterm (unique-SAT) functions: %d\n",un);
}
