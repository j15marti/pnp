// Exact minimum number of fan-in-2 gates (full binary basis B2, free negation) to compute every
// n-variable Boolean function, n<=3, by exhaustive DFS over circuits (gates may share, fan-out unbounded).
// usage: ./a n maxdepth
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int n, maxd, NF; int best[1<<16]; // best cost per truth table (as integer mask)
int f[16]; int key[16]; int total; unsigned mask;
long long nodes=0;
static void dfs(int d){
  // f[0..n-1] inputs, f[n..n+d-1] gates
  int m=n+d;
  if(d==maxd) return;
  for(int a=0;a<m;a++) for(int b=a+1;b<m;b++){
    int k=b*32+a;
    if(d>0 && k<key[d-1] && !(a==m-1||b==m-1)) continue; // canonical order
    for(int op=0;op<16;op++){
      // skip degenerate ops: constants, projections, negated projections
      if(op==0||op==15||op==3||op==12||op==5||op==10) continue;
      unsigned x=f[a],y=f[b],r=0;
      if(op&1) r|=~x&~y; if(op&2) r|=~x&y; if(op&4) r|=x&~y; if(op&8) r|=x&y;
      r&=mask;
      int dup=0; for(int i=0;i<m;i++) if(f[i]==r||f[i]==(int)(~r&mask)){dup=1;break;}
      if(dup) continue;
      nodes++;
      unsigned nr=r, c=~r&mask;
      if(best[nr]>d+1) best[nr]=d+1;
      if(best[c]>d+1) best[c]=d+1;
      f[m]=r; key[d]=k; dfs(d+1);
    }
  }
}
int main(int argc,char**argv){
  n=atoi(argv[1]); maxd=atoi(argv[2]); NF=1<<n; mask=(NF==32)?0xffffffffu:((1u<<(1<<n))-1);
  for(int i=0;i<(1<<16);i++) best[i]=99;
  for(int i=0;i<n;i++){ unsigned t=0; for(int x=0;x<NF;x++) if((x>>i)&1) t|=1u<<x; f[i]=t; best[t]=0; best[~t&mask]=0; }
  best[0]=0; best[mask]=0;
  dfs(0);
  int hist[20]={0}; int unk=0; for(unsigned t=0;t<=mask;t++){ if(best[t]==99) unk++; else hist[best[t]]++; }
  printf("n=%d maxdepth=%d nodes=%lld\n",n,maxd,nodes);
  for(int k=0;k<20;k++) if(hist[k]) printf("cost %d: %d functions\n",k,hist[k]);
  printf("unresolved(cost>%d): %d\n",maxd,unk);
  if(argc>3){ for(unsigned t=0;t<=mask;t++) printf("%u %d\n",t,best[t]); }
}
