#include <bits/stdc++.h>
using namespace std;

// Exact promised-weight symbolic count + reduced ordered clause-query DAG for D(5,9).
// Input bits indicate presence of the 80 possible genuine 3-clauses.
// Promise: exactly 9 bits are 1. Output 1 means UNSAT.
//
// Order used: sign-pattern round-robin across the 10 variable triples.
// Result is exact for this fixed order, not a global DAG minimum.

struct Key {
  uint32_t cov;
  uint8_t t,k;
  bool operator==(Key const&o) const { return cov==o.cov && t==o.t && k==o.k; }
};
struct KH {
  size_t operator()(Key const&x) const {
    return ((uint64_t)x.cov*0x9e3779b97f4a7c15ULL)^((uint64_t)x.t<<8)^x.k;
  }
};
struct Sig {
  uint32_t lo,hi;
  uint8_t t;
  bool operator==(Sig const&o) const { return lo==o.lo && hi==o.hi && t==o.t; }
};
struct SH {
  size_t operator()(Sig const&x) const {
    return ((uint64_t)x.lo*11995408973635179863ULL)^
           ((uint64_t)x.hi*10150724397891781847ULL)^x.t;
  }
};

unsigned long long Cbin[81][10];

int main(){
  for(int n=0;n<=80;n++){
    Cbin[n][0]=1;
    for(int k=1;k<=min(n,9);k++) Cbin[n][k]=Cbin[n-1][k-1]+Cbin[n-1][k];
  }

  vector<array<int,3>> triples;
  for(int i=0;i<5;i++) for(int j=i+1;j<5;j++) for(int k=j+1;k<5;k++)
    triples.push_back({i,j,k});

  vector<uint32_t> base;
  for(auto vs:triples) for(int pat=0;pat<8;pat++){
    uint32_t fm=0;
    for(int a=0;a<32;a++){
      bool fals=true;
      for(int z=0;z<3;z++){
        int pos=(pat>>z)&1, bit=(a>>vs[z])&1;
        if(pos ? bit : !bit){ fals=false; break; }
      }
      if(fals) fm |= 1u<<a;
    }
    base.push_back(fm);
  }

  vector<int> ord;
  for(int pat=0;pat<8;pat++) for(int tr=0;tr<10;tr++) ord.push_back(tr*8+pat);

  vector<uint32_t> e(80), suff(81,0);
  for(int t=0;t<80;t++) e[t]=base[ord[t]];
  for(int t=79;t>=0;t--) suff[t]=suff[t+1]|e[t];

  const uint32_t FULL=0xffffffffu;

  // Exact UNSAT count.
  unordered_map<Key,unsigned long long,KH> cmemo;
  cmemo.reserve(3000000);
  function<unsigned long long(int,int,uint32_t)> count_unsat =
    [&](int t,int k,uint32_t cov)->unsigned long long{
      int rem=80-t,need=9-k;
      if(need<0||need>rem) return 0;
      if(cov==FULL) return Cbin[rem][need];
      if(t==80||need==0) return 0;
      if(32-__builtin_popcount(cov)>4*need) return 0;
      if((cov|suff[t])!=FULL) return 0;
      Key key{cov,(uint8_t)t,(uint8_t)k};
      auto it=cmemo.find(key); if(it!=cmemo.end()) return it->second;
      auto v=count_unsat(t+1,k,cov)+count_unsat(t+1,k+1,cov|e[t]);
      cmemo.emplace(key,v); return v;
    };

  unsigned long long unsat=count_unsat(0,0,0);

  // Reduced fixed-order DAG.
  unordered_map<Key,uint32_t,KH> memo;
  memo.reserve(3000000);
  vector<unordered_map<Sig,uint32_t,SH>> uniq(80);
  uint32_t next=3; // 0 SAT, 1 UNSAT, 2 invalid promise branch

  function<uint32_t(int,int,uint32_t)> f =
    [&](int t,int k,uint32_t cov)->uint32_t{
      int rem=80-t,need=9-k;
      if(need<0||need>rem) return 2;
      if(cov==FULL) return 1;
      if(t==80) return 0;
      if(32-__builtin_popcount(cov)>4*need) return 0;
      if((cov|suff[t])!=FULL) return 0;
      if(need==0) return 0;
      if(need==rem) return ((cov|suff[t])==FULL)?1:0;

      Key key{cov,(uint8_t)t,(uint8_t)k};
      auto it=memo.find(key); if(it!=memo.end()) return it->second;

      uint32_t lo=f(t+1,k,cov);
      uint32_t hi=f(t+1,k+1,cov|e[t]);
      uint32_t id;
      if(lo==hi) id=lo;
      else {
        Sig s{lo,hi,(uint8_t)t};
        auto jt=uniq[t].find(s);
        if(jt==uniq[t].end()){ id=next++; uniq[t].emplace(s,id); }
        else id=jt->second;
      }
      memo.emplace(key,id);
      return id;
    };

  f(0,0,0);
  uint64_t nodes=0; size_t peak=0; int peak_level=-1;
  for(int t=0;t<80;t++){
    nodes += uniq[t].size();
    if(uniq[t].size()>peak){ peak=uniq[t].size(); peak_level=t; }
  }

  cout << "D(5,9)\n";
  cout << "total_formulas " << Cbin[80][9] << "\n";
  cout << "unsat_formulas " << unsat << "\n";
  cout << "sat_formulas " << (Cbin[80][9]-unsat) << "\n";
  cout << "fixed_order_query_dag_nodes " << nodes << "\n";
  cout << "peak_width " << peak << "\n";
  cout << "peak_level " << peak_level << "\n";
  cout << "memo_states " << memo.size() << "\n";
}
