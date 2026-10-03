#include <bits/stdc++.h>
using namespace std;

// D(5,8): exact symbolic count and reduced ordered clause-query DAG.
// Promise: exactly eight of 80 clause-presence bits are 1.
// Order: sign-pattern round-robin across the ten variable triples.
// The DAG size is exact for this order only, not a global minimum.

struct Key{uint32_t cov; uint8_t t,k; bool operator==(Key const&o)const{return cov==o.cov&&t==o.t&&k==o.k;}};
struct KH{size_t operator()(Key const&x)const{return ((uint64_t)x.cov*0x9e3779b97f4a7c15ULL)^((uint64_t)x.t<<8)^x.k;}};
struct Sig{uint32_t lo,hi; uint8_t t; bool operator==(Sig const&o)const{return lo==o.lo&&hi==o.hi&&t==o.t;}};
struct SH{size_t operator()(Sig const&x)const{return ((uint64_t)x.lo*11995408973635179863ULL)^((uint64_t)x.hi*10150724397891781847ULL)^x.t;}};
unsigned long long Cb[81][9];

int main(){
  for(int n=0;n<=80;n++){Cb[n][0]=1;for(int k=1;k<=min(n,8);k++)Cb[n][k]=Cb[n-1][k-1]+Cb[n-1][k];}
  vector<array<int,3>> triples;
  for(int i=0;i<5;i++)for(int j=i+1;j<5;j++)for(int k=j+1;k<5;k++)triples.push_back({i,j,k});
  vector<uint32_t> base;
  for(auto vs:triples)for(int pat=0;pat<8;pat++){
    uint32_t fm=0;
    for(int a=0;a<32;a++){
      bool fals=true;
      for(int z=0;z<3;z++)if(((a>>vs[z])&1)!=((pat>>z)&1)){fals=false;break;}
      if(fals)fm|=1u<<a;
    }
    base.push_back(fm);
  }
  vector<int> ord;
  for(int pat=0;pat<8;pat++)for(int tr=0;tr<10;tr++)ord.push_back(tr*8+pat);
  vector<uint32_t> e(80),suff(81,0);
  for(int t=0;t<80;t++)e[t]=base[ord[t]];
  for(int t=79;t>=0;t--)suff[t]=suff[t+1]|e[t];
  const uint32_t FULL=0xffffffffu;

  unordered_map<Key,unsigned long long,KH> cmemo;
  function<unsigned long long(int,int,uint32_t)> cnt=[&](int t,int k,uint32_t cov)->unsigned long long{
    int rem=80-t,need=8-k;
    if(need<0||need>rem)return 0;
    if(cov==FULL)return Cb[rem][need];
    if(t==80||need==0)return 0;
    if(32-__builtin_popcount(cov)>4*need)return 0;
    if((cov|suff[t])!=FULL)return 0;
    Key key{cov,(uint8_t)t,(uint8_t)k};
    auto it=cmemo.find(key);if(it!=cmemo.end())return it->second;
    auto v=cnt(t+1,k,cov)+cnt(t+1,k+1,cov|e[t]);
    cmemo.emplace(key,v);return v;
  };
  auto uns=cnt(0,0,0);

  unordered_map<Key,uint32_t,KH> memo;
  vector<unordered_map<Sig,uint32_t,SH>> uniq(80);
  uint32_t next=3;
  function<uint32_t(int,int,uint32_t)> f=[&](int t,int k,uint32_t cov)->uint32_t{
    int rem=80-t,need=8-k;
    if(need<0||need>rem)return 2;
    if(cov==FULL)return 1;
    if(t==80)return 0;
    if(32-__builtin_popcount(cov)>4*need)return 0;
    if((cov|suff[t])!=FULL)return 0;
    if(need==0)return 0;
    if(need==rem)return ((cov|suff[t])==FULL)?1:0;
    Key key{cov,(uint8_t)t,(uint8_t)k};
    auto it=memo.find(key);if(it!=memo.end())return it->second;
    uint32_t lo=f(t+1,k,cov),hi=f(t+1,k+1,cov|e[t]),id;
    if(lo==hi)id=lo;
    else{
      Sig s{lo,hi,(uint8_t)t};
      auto jt=uniq[t].find(s);
      if(jt==uniq[t].end()){id=next++;uniq[t].emplace(s,id);}else id=jt->second;
    }
    memo.emplace(key,id);return id;
  };
  f(0,0,0);
  uint64_t nodes=0;size_t peak=0;int peak_level=-1;
  for(int t=0;t<80;t++){nodes+=uniq[t].size();if(uniq[t].size()>peak){peak=uniq[t].size();peak_level=t;}}
  cout<<"total_formulas "<<Cb[80][8]<<"\n";
  cout<<"unsat_formulas "<<uns<<"\n";
  cout<<"sat_formulas "<<Cb[80][8]-uns<<"\n";
  cout<<"fixed_order_query_dag_nodes "<<nodes<<"\n";
  cout<<"peak_width "<<peak<<"\n";
  cout<<"peak_level "<<peak_level<<"\n";
  cout<<"memo_states "<<memo.size()<<"\n";
}
