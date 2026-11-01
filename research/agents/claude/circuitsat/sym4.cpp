// Exact min AIG gate count (2-input AND, free edge negation) for all 4-input
// SYMMETRIC functions (32 of them), by iterative-deepening DFS with budget K.
// Reports G if <=K else ">K". Gate order canonical: gate j must use gate j-1 or exceed it in value.
#include <bits/stdc++.h>
using namespace std;
typedef unsigned U; const U M=0xFFFF; U lit[40]; int nl; int K; U target; long long nodes;
bool dfs(int used,U last,bool lastUsedPrev){
  // available literal tables lit[0..nl): inputs(4)+gates
  if(used==K) return false;
  int remaining=K-used;
  for(int i=0;i<nl*2;i++){U a=(i&1)?(M^lit[i>>1]):lit[i>>1];
    for(int j=i;j<nl*2;j++){U b=(j&1)?(M^lit[j>>1]):lit[j>>1];
      U g=a&b; if(g==0||g==M||g==a||g==b) continue;
      bool usesPrev = (used>0)&&(((i>>1)==nl-1)||((j>>1)==nl-1));
      if(used>0 && !usesPrev && g<=last) continue;
      bool dup=false; for(int t=0;t<nl;t++) if(lit[t]==g||lit[t]==(M^g)){dup=true;break;} if(dup) continue;
      nodes++;
      if(g==target||g==(M^target)) return true;
      if(remaining>1){lit[nl++]=g; bool r=dfs(used+1,g,usesPrev); nl--; if(r) return true;}
    }}
  return false;
}
int main(int argc,char**argv){int KM=atoi(argv[1]);
  U in[4]; for(int i=0;i<4;i++){U t=0;for(int x=0;x<16;x++) if((x>>i)&1) t|=1u<<x; in[i]=t;}
  printf("{");
  int s0=argc>2?atoi(argv[2]):0,s1=argc>3?atoi(argv[3]):32;for(int s=s0;s<s1;s++){ // symmetric fn: bit w of s = value at weight w? 5 weights 0..4
    U f=0; for(int x=0;x<16;x++){int w=__builtin_popcount(x); if((s>>w)&1) f|=1u<<x;}
    if(s&1){} // keep all
    target=f; int G=-1;
    if(f==0||f==M){G=0;} else {
      for(int i=0;i<4;i++) if(f==in[i]||f==(M^in[i])) G=0;
      for(int k=1;k<=KM&&G<0;k++){ nl=4; for(int i=0;i<4;i++) lit[i]=in[i]; ::K=k; if(dfs(0,0,false)) G=k; }
    }
    printf("%s\"%02d\":%d",s>s0?",":"",s,G);
    fflush(stdout);
  }
  printf("}\n"); fprintf(stderr,"nodes %lld\n",nodes);
}
