#include <stdio.h>
#include <stdlib.h>
#include <string.h>
// exact min B2 circuit size (fan-in 2, all 16 ops, free negation) for all n-var functions, DFS up to depth D
int n,D,TT; unsigned mask; unsigned val[16]; signed char best[65536]; long found=0;
void rec(int k,int g){ // k nodes, g gates used
  if(k>n){ unsigned f=val[k-1]; if(best[f]<0||best[f]>g){ if(best[f]<0)found++; best[f]=g;} }
  if(g==D) return;
  for(int i=0;i<k;i++)for(int j=i+1;j<k;j++)for(int op=1;op<15;op++){
    unsigned a=val[i],b=val[j],r=0;
    if(op&1)r|=~a&~b; if(op&2)r|=~a&b; if(op&4)r|=a&~b; if(op&8)r|=a&b;
    r&=mask; if(op==0||op==15)continue;
    int dup=0; for(int t=0;t<k;t++) if(val[t]==r||(~val[t]&mask)==r){dup=1;break;}
    if(dup)continue;
    val[k]=r; rec(k+1,g+1);
  }
}
int main(int c,char**v){ n=atoi(v[1]);D=atoi(v[2]); TT=1<<n; mask=(n==4)?0xFFFF:((1u<<TT)-1);
  memset(best,-1,sizeof best);
  for(int i=0;i<n;i++){unsigned x=0;for(int m=0;m<TT;m++)if(m>>i&1)x|=1u<<m;val[i]=x;}
  rec(n,0);
  // histogram over all functions
  int hist[20]={0},un=0; for(unsigned f=0;f<=mask;f++){ if(best[f]<0)un++; else hist[(int)best[f]]++; }
  // functions of 0 gates: constants and literals not recorded; count separately
  if(n==3){unsigned q[]={232,150,216,128,226,126,22};for(int i=0;i<7;i++)printf("tt%u:%d\n",q[i],best[q[i]]);} printf("n=%d D=%d unresolved(incl trivial)=%d\n",n,D,un);
  for(int g=1;g<=D;g++)printf("gates=%d count=%d\n",g,hist[g]);
  return 0;}
