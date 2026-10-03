#include <bits/stdc++.h>
using namespace std;
using U128=__uint128_t;

struct Bits{ uint64_t w[5]={0,0,0,0,0}; };
inline bool test(const Bits&b,int i){ return (b.w[i>>6]>>(i&63))&1ULL; }
inline void setb(Bits&b,int i){ b.w[i>>6]|=1ULL<<(i&63); }
inline int popc(const Bits&b){ int s=0; for(int i=0;i<5;i++) s+=__builtin_popcountll(b.w[i]); return s; }
inline int pc(U128 x){ return __builtin_popcountll((uint64_t)x)+__builtin_popcountll((uint64_t)(x>>64)); }

vector<U128> cm;
vector<vector<int>> ca;
U128 FULL;
unsigned long long Cb[281][10];
const int M=280,SEL=9;

unsigned long long rec(U128 cov,int k,Bits forb){
  int r=SEL-k;
  if(cov==FULL){
    int av=M-popc(forb);
    return (r>=0&&r<=av)?Cb[av][r]:0;
  }
  if(r<=0) return 0;
  if(128-pc(cov)>16*r) return 0;

  U128 rem=FULL^cov;
  uint64_t lo=(uint64_t)rem;
  int a=lo?__builtin_ctzll(lo):64+__builtin_ctzll((uint64_t)(rem>>64));

  Bits run=forb;
  unsigned long long tot=0;
  for(int ci:ca[a]){
    if(test(run,ci)) continue;
    Bits child=run;
    setb(child,ci);
    tot+=rec(cov|cm[ci],k+1,child);
    setb(run,ci);
  }
  return tot;
}

int main(){
  for(int n=0;n<=M;n++){
    Cb[n][0]=1;
    for(int k=1;k<=9&&k<=n;k++) Cb[n][k]=Cb[n-1][k-1]+Cb[n-1][k];
  }

  vector<array<int,3>> tr;
  for(int i=0;i<7;i++) for(int j=i+1;j<7;j++) for(int k=j+1;k<7;k++)
    tr.push_back({i,j,k});

  ca.assign(128,{});
  for(auto T:tr) for(int pat=0;pat<8;pat++){
    U128 m=0;
    int ci=cm.size();
    for(int a=0;a<128;a++){
      bool ok=true;
      for(int z=0;z<3;z++) if(((a>>T[z])&1)!=((pat>>z)&1)){ ok=false; break; }
      if(ok){ m|=(U128(1)<<a); ca[a].push_back(ci); }
    }
    cm.push_back(m);
  }

  FULL=~U128(0);
  vector<int> roots=ca[0];
  vector<unsigned long long> vals(roots.size());
  auto st=chrono::steady_clock::now();

  #pragma omp parallel for schedule(dynamic,1) num_threads(5)
  for(int q=0;q<(int)roots.size();q++){
    Bits forb;
    for(int z=0;z<=q;z++) setb(forb,roots[z]);
    vals[q]=rec(cm[roots[q]],1,forb);
  }

  unsigned long long ans=0;
  for(auto x:vals) ans+=x;
  double sec=chrono::duration<double>(chrono::steady_clock::now()-st).count();
  cout<<"D(7,9) unsat "<<ans<<" sec "<<sec<<"\n";
}
