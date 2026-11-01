// ARC-TRIPLE-MOMENT-SELECTOR-GATE289: exhaustive original-clause U/S triples.
// C++17: g++ -O3 -std=c++17 triple_moments289.cpp -o triple_moments289
// stdin: n m then m signed triples; stdout: mode/histogram counts.
// Restriction: n<=256 only for this computational diagnostic (NOT an all-input solver).
#include <bits/stdc++.h>
using namespace std;
using U=unsigned long long;
struct Bits { array<U,4> w{}; };
struct Clause { Bits supp; bool positive; };
struct HistKey {int k,v,h; bool operator<(const HistKey&o)const{return tie(k,v,h)<tie(o.k,o.v,o.h);} };
int main(){ios::sync_with_stdio(false);cin.tie(nullptr);
 int n,m; if(!(cin>>n>>m))return 1; if(n>256)return 2;
 vector<Clause> cs(m);map<int,int> occ; set<array<int,3>> seen;
 for(int j=0;j<m;j++){int x[3]; for(int t=0;t<3;t++)if(!(cin>>x[t]))return 3;
  if((x[0]>0)!=(x[1]>0)||(x[1]>0)!=(x[2]>0))return 4;
  cs[j].positive=(x[0]>0);
  array<int,3> key{x[0],x[1],x[2]}; sort(key.begin(),key.end());
  if(!seen.insert(key).second)return 5;
  for(int t=0;t<3;t++){int a=abs(x[t]);if(a<1||a>n)return 6;cs[j].supp.w[(a-1)>>6]|=1ULL<<((a-1)&63);occ[x[t]]++;}
  int cardinality=0;for(U q:cs[j].supp.w)cardinality+=__builtin_popcountll(q);
  if(cardinality!=3)return 7;
 }
 if(n%3||3*m!=4*n)return 8;
 for(int x=1;x<=n;x++)if(occ[x]!=2||occ[-x]!=2)return 9;
 map<HistKey,long long> hist;
 long long triple=0, mode_trials=0, compatible=0, inconsistent=0;
 for(int i=0;i<m;i++)for(int j=i+1;j<m;j++)for(int k=j+1;k<m;k++){
  const auto &a=cs[i], &b=cs[j], &c=cs[k]; ++triple;
  Bits union_all; int v=0;
  for(int t=0;t<4;t++){union_all.w[t]=a.supp.w[t]|b.supp.w[t]|c.supp.w[t];v+=__builtin_popcountll(union_all.w[t]);}
  for(int mode=0;mode<8;mode++){++mode_trials; // bit 1 means U (all false); bit 0 means S (all true).
   bool oneA=a.positive? !(mode&1): bool(mode&1);
   bool oneB=b.positive? !(mode&2): bool(mode&2);
   bool oneC=c.positive? !(mode&4): bool(mode&4);
   bool ok=true;int h=0;
   for(int t=0;t<4;t++){
    U ones=(oneA?a.supp.w[t]:0)|(oneB?b.supp.w[t]:0)|(oneC?c.supp.w[t]:0);
    U zeros=(!oneA?a.supp.w[t]:0)|(!oneB?b.supp.w[t]:0)|(!oneC?c.supp.w[t]:0);
    if((ones&zeros)!=0){ok=false;break;}
    h+=__builtin_popcountll(ones);
   }
   if(!ok){++inconsistent;continue;}++compatible;
   hist[{__builtin_popcount((unsigned)mode),v,h}]++;
  }
 }
 cout<<"TRIPLES "<<triple<<" MODE_TRIALS "<<mode_trials<<" COMPATIBLE "<<compatible<<" INCONSISTENT "<<inconsistent<<"\n";
 for(auto [key,count]:hist)cout<<key.k<<' '<<key.v<<' '<<key.h<<' '<<count<<"\n";
}
