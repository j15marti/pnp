// Independent exhaustive 2positive/2negative signings of cycle+block 3-uniform scope.
// For n=9 there are exactly 6^9 sign patterns; count UNSAT via 2^n truth-table bitset.
#include <array>
#include <vector>
#include <iostream>
#include <cstdint>
#include <cstdlib>
#include <chrono>
using namespace std;
struct Occ{int clause,slot;};
int n, words, nc;
vector<array<int,3>> scope;
vector<vector<Occ>> positions;
vector<array<vector<uint64_t>,8>> forbidden;
vector<int> clauseSigns;
unsigned long long tested=0, unsat=0;
vector<int> firstUnsat;
vector<int> chosen;
vector<uint64_t> full;
void rec(int v) {
  if(v==n){
    tested++;
    vector<uint64_t> cov(words,0);
    for(int c=0;c<nc;c++){
      const auto &bits=forbidden[c][clauseSigns[c]];
      for(int w=0;w<words;w++)cov[w]|=bits[w];
    }
    bool any=false;
    for(int w=0;w<words;w++)if(cov[w]!=full[w]){any=true;break;}
    if(!any){
      unsat++;
      if(firstUnsat.empty())firstUnsat=chosen;
    }
    return;
  }
  for(int a=0;a<4;a++)for(int b=a+1;b<4;b++){
    chosen[v]=((1<<a)|(1<<b));
    for(int idx:{a,b}){const auto &o=positions[v][idx];clauseSigns[o.clause]|=1<<o.slot;}
    rec(v+1);
    for(int idx:{a,b}){const auto &o=positions[v][idx];clauseSigns[o.clause]&=~(1<<o.slot);}
  }
}
int main(int argc,char**argv){
  n=argc>1?atoi(argv[1]):9;
  if(n<3||n%3||n>12)return 1;
  for(int i=0;i<n;i++)scope.push_back({i,(i+1)%n,(i+2)%n});
  for(int j=0;j<n;j+=3)scope.push_back({j,j+1,j+2});
  nc=scope.size();positions.resize(n);
  for(int c=0;c<nc;c++)for(int j=0;j<3;j++)positions[scope[c][j]].push_back({c,j});
  for(auto &p:positions)if(p.size()!=4)return 2;
  words=((1<<n)+63)/64;forbidden.resize(nc);clauseSigns.assign(nc,0);
  full.assign(words,~0ull);if((1<<n)%64)full.back()=(1ull<<((1<<n)%64))-1;
  for(int c=0;c<nc;c++)for(int s=0;s<8;s++){
    forbidden[c][s].assign(words,0);
    for(int a=0;a<(1<<n);a++){
      bool f=true;
      for(int j=0;j<3;j++)if(((a>>scope[c][j])&1)==((s>>j)&1)){f=false;break;}
      if(f)forbidden[c][s][a/64]|=1ull<<(a%64);
    }
  }
  chosen.assign(n,0);
  auto start=chrono::steady_clock::now();rec(0);
  double sec=chrono::duration<double>(chrono::steady_clock::now()-start).count();
  cout<<"n="<<n<<" m="<<nc<<" balanced_signings="<<tested<<" unsat="<<unsat<<" elapsed_seconds="<<sec<<"\n";
  if(unsat){cout<<"first_unsat_sign_choices=";for(int x:firstUnsat)cout<<x<<",";cout<<"\n";}
  return 0;
}
