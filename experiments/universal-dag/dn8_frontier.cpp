#include <bits/stdc++.h>
using namespace std;

// DN8-FRONTIER1
// Exhaustive finite verifier for D(n,8), n=3..9.
// For n<=7, also verifies the singleton intersection property used for
// the all-pairs clause-query lower-bound certificate.
// For n=8,9, directly enumerates exact covers and checks that no new
// full-support UNSAT core appears.
//
// Genuine 3-clauses: exactly 3 distinct variables.
// Input encoding: one presence bit per possible signed 3-clause.
// Promise: exactly 8 clause bits are 1.

static const int MAXA=512;
struct Clause { array<int,3> T; int pat; bitset<MAXA> mask; };

vector<Clause> clauses_for(int n, vector<vector<int>>& contains) {
  int A=1<<n;
  vector<Clause> C;
  contains.assign(A,{});
  for(int i=0;i<n;i++) for(int j=i+1;j<n;j++) for(int k=j+1;k<n;k++){
    array<int,3> T={i,j,k};
    for(int pat=0;pat<8;pat++){
      bitset<MAXA> m;
      for(int a=0;a<A;a++){
        bool ok=true;
        for(int z=0;z<3;z++) if(((a>>T[z])&1)!=((pat>>z)&1)){ok=false;break;}
        if(ok)m.set(a);
      }
      int ci=C.size();
      C.push_back({T,pat,m});
      for(int a=0;a<A;a++) if(m.test(a)) contains[a].push_back(ci);
    }
  }
  return C;
}

long long binomll(int n,int k){
  if(k<0||k>n)return 0;
  __int128 r=1;
  for(int i=1;i<=k;i++)r=r*(n-k+i)/i;
  return (long long)r;
}

int main(){
  const long long core[8]={0,0,0,1,268,3030,7800,5040};

  for(int n=3;n<=9;n++){
    vector<vector<int>> contains;
    auto C=clauses_for(n,contains);
    int A=1<<n, M=C.size();
    bitset<MAXA> FULL;
    for(int a=0;a<A;a++)FULL.set(a);

    long long covers=0;
    map<int,long long> support;
    vector<int> chosen;

    vector< bitset<280> > inter;
    vector<long long> appear;
    if(n<=7){
      inter.resize(M); appear.assign(M,0);
      for(int i=0;i<M;i++) for(int j=0;j<M;j++) inter[i].set(j);
    }

    function<void(bitset<MAXA> const&)> rec = [&](bitset<MAXA> const& cov){
      if(cov==FULL){
        if(chosen.size()==8){
          covers++;
          set<int> vars;
          for(int ci:chosen) for(int v:C[ci].T) vars.insert(v);
          support[vars.size()]++;
          if(n<=7){
            bitset<280> F;
            for(int ci:chosen)F.set(ci);
            for(int ci:chosen){ appear[ci]++; inter[ci]&=F; }
          }
        }
        return;
      }
      if(chosen.size()>=8)return;
      int a=0; while(a<A && cov.test(a))a++;
      for(int ci:contains[a]){
        if((C[ci].mask&cov).any())continue;
        chosen.push_back(ci);
        auto nc=cov|C[ci].mask;
        rec(nc);
        chosen.pop_back();
      }
    };

    bitset<MAXA> zero;
    rec(zero);

    long long predicted=0;
    for(int k=3;k<=7;k++) predicted += binomll(n,k)*core[k];

    cout<<"n "<<n<<" clause_bits "<<M<<" unsat "<<covers
        <<" predicted "<<predicted<<" support";
    for(auto [k,v]:support) cout<<" "<<k<<":"<<v;

    if(n<=7 && n>=4){
      bool singleton=true;
      long long mn=LLONG_MAX,mx=0;
      for(int i=0;i<M;i++){
        int cnt=0;
        for(int j=0;j<M;j++) if(inter[i].test(j))cnt++;
        singleton &= (cnt==1 && inter[i].test(i));
        mn=min(mn,appear[i]); mx=max(mx,appear[i]);
      }
      cout<<" singleton_intersections "<<singleton
          <<" min_clause_appear "<<mn<<" max_clause_appear "<<mx
          <<" certified_query_lb "<<M-1;
    }
    cout<<"\n";

    if(covers!=predicted){ cerr<<"prediction mismatch n="<<n<<"\n"; return 2; }
    if(n>=8 && support.rbegin()->first>7){ cerr<<"new support core n="<<n<<"\n"; return 3; }
  }
  cout<<"verification PASS\n";
}
