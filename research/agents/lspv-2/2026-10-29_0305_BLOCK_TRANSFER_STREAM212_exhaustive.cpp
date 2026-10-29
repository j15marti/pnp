#include <array>
#include <vector>
#include <iostream>
#include <algorithm>
#include <cstdint>
using namespace std;
struct Occ {int clause,pos;};
int main(){
  for(int n:{3,6}){
    vector<array<int,3>> scopes;
    for(int j=0;j<n/3;j++){
      int x=3*j;
      scopes.push_back({x,x+1,x+2});
      scopes.push_back({(x+1)%n,(x+2)%n,(x+3)%n});
      scopes.push_back({(x+2)%n,(x+3)%n,(x+4)%n});
      scopes.push_back({x,x+1,x+2});
    }
    vector<vector<Occ>> occ(n);
    for(int ci=0;ci<(int)scopes.size();ci++)
      for(int pi=0;pi<3;pi++)occ[scopes[ci][pi]].push_back({ci,pi});
    for(auto &v:occ)if(v.size()!=4)return 2;
    vector<array<int,2>> masks;
    for(int a=0;a<4;a++)for(int b=a+1;b<4;b++)masks.push_back({a,b});
    vector<int> literal_sign(scopes.size()*3,0);
    long long count=0,unsat=0,min_sat=1LL<<30;
    auto rec=[&](auto&& self,int v)->void{
      if(v<n){
        for(auto pair:masks){
          for(int p=0;p<4;p++){
            Occ slot=occ[v][p];
            literal_sign[3*slot.clause+slot.pos] = (p==pair[0]||p==pair[1]);
          }
          self(self,v+1);
        }
        return;
      }
      count++;
      int sat_count=0;
      for(int a=0;a<(1<<n);a++){
        bool formula_true=true;
        for(int ci=0;ci<(int)scopes.size()&&formula_true;ci++){
          bool clause_true=false;
          for(int pi=0;pi<3;pi++){
            int bit=(a>>scopes[ci][pi])&1;
            clause_true|=(bit==literal_sign[3*ci+pi]);
          }
          if(!clause_true)formula_true=false;
        }
        if(formula_true)sat_count++;
      }
      if(sat_count==0)unsat++;
      min_sat=min<long long>(min_sat,sat_count);
    };
    rec(rec,0);
    cout<<"n="<<n<<" balanced_signings="<<count<<" unsat="<<unsat<<" minimum_satisfying_assignments="<<min_sat<<"\n";
  }
}
