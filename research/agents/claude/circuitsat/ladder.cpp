// Exhaustive minimum-gate ladder for fan-in-2 AND circuits with free negation
// (equivalently AND/OR/NOT with negation absorbed into wires). Wires = 2*gates.
// usage: ladder n maxgates   (maxgates<=6; level maxgates is found by a last-gate sweep, not stored)
#include <bits/stdc++.h>
using namespace std;
typedef uint32_t F; typedef array<uint16_t,6> St;
int n; F MASK; int T;
F norm(F f){ return (f&1)? (~f)&MASK : f; }
int main(int argc,char**argv){
  n=atoi(argv[1]); int G=atoi(argv[2]); T=1<<n; MASK=(T==32)?0xffffffffu:((1u<<T)-1);
  vector<F> in;
  for(int i=0;i<n;i++){F f=0;for(int a=0;a<T;a++) if((a>>i)&1) f|=1u<<a; in.push_back(norm(f));}
  map<F,int> best; // normalized function -> min gates
  best[0]=0; for(F f:in) best[f]=0;
  vector<St> cur(1); cur[0].fill(0);
  for(int k=1;k<=G;k++){
    bool last=(k==G);
    vector<St> nxt;
    for(auto&s:cur){
      vector<F> av=in; for(int j=0;j<k-1;j++) av.push_back(s[j]);
      int m=av.size();
      for(int i=0;i<m;i++)for(int j=i+1;j<m;j++)for(int p=0;p<4;p++){
        F a=av[i]^((p&1)?MASK:0), b=av[j]^((p&2)?MASK:0);
        F r=norm(a&b);
        if(r==0) continue;
        if(!best.count(r)) best[r]=k;
        if(last) continue;
        bool dup=false; for(int t=0;t<m;t++) if(av[t]==r) dup=true;
        if(dup) continue;
        St ns=s; ns[k-1]=r; sort(ns.begin(),ns.begin()+k);
        nxt.push_back(ns);
      }
    }
    if(!last){sort(nxt.begin(),nxt.end()); nxt.erase(unique(nxt.begin(),nxt.end()),nxt.end()); cur.swap(nxt);}
    fprintf(stderr,"level %d states %zu funcs %zu\n",k,cur.size(),best.size());
  }
  // histogram, and minterm/ one-sat functions
  map<int,int> h; for(auto&p:best) h[p.second]++;
  printf("n=%d total normalized functions found=%zu of %u\n",n,best.size(),(T==32)?(1u<<31):(1u<<(T-1)));
  for(auto&p:h) printf("gates=%d count=%d\n",p.first,p.second);
  // min gates for functions with exactly one satisfying assignment (either polarity class) 
  int mn1=1e9; for(auto&p:best){int w=__builtin_popcount(p.first); if(w==1||w==T-1) mn1=min(mn1,p.second);}
  printf("min gates for exactly-one-sat function: %d\n",mn1);
  // parity
  F par=0; for(int a=0;a<T;a++) if(__builtin_popcount(a)&1) par|=1u<<a; par=norm(par);
  printf("parity gates: %d\n", best.count(par)?best[par]:-1);
}
