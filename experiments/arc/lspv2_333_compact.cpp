// LSPV-2 / COFACTOR-LATTICE-OBDD333. C++17, standalone exact F15 benchmark.
// This is EXPONENTIAL knowledge compilation, not a SAT decision lower bound.
#include <bits/stdc++.h>
using namespace std;
int main(){
 vector<array<int,3>> F={{1,2,7},{1,3,8},{4,5,9},{4,6,10},{2,3,5},
 {6,11,12},{7,11,13},{8,12,14},{9,13,15},{10,14,15}};
 vector<array<int,3>> N={{1,2,11},{2,3,11},{1,3,12},{4,5,13},{5,6,14},
 {4,6,15},{7,8,12},{8,9,13},{9,10,14},{10,7,15}};
 for(auto c:N){for(auto &v:c)v=-v;F.push_back(c);}
 const int n=15,K=1<<n;vector<uint32_t> pow3(n+1,1);
 for(int i=1;i<=n;i++)pow3[i]=3*pow3[i-1];int T=pow3[n];
 vector<uint32_t> ids(T);vector<uint64_t> keys;keys.reserve(T);
 unordered_map<uint64_t,uint32_t> table;uint32_t newID=2;int models=0;
 for(uint32_t p=0;p<(uint32_t)T;p++){
  int q=p,top=-1,mask=0,assigned=0;
  for(int v=0;v<n;v++){
   int digit=q%3;q/=3;
   if(digit==2)top=v;
   else{assigned|=1<<v;if(digit)mask|=1<<v;}
  }
  if(top==-1){
   bool good=true;
   for(auto C:F){bool sat=false;
    for(int l:C)if(bool(mask&(1<<(abs(l)-1)))==(l>0))sat=true;
    if(!sat){good=false;break;}
   }
   models+=good;ids[p]=good?1:0;
  }else{
   int off=pow3[top];uint32_t lo=ids[p-2*off],hi=ids[p-off];
   if(lo==hi)ids[p]=lo;
   else{
    uint64_t key=(uint64_t(top)<<48)|(uint64_t(lo)<<24)|hi;
    auto [it,inserted]=table.emplace(key,newID);
    if(inserted)newID++;
    ids[p]=it->second;
   }
  }
  keys.push_back((uint64_t(assigned)<<48)|(uint64_t(ids[p])<<24)|p);
 }
 sort(keys.begin(),keys.end());vector<int> edge(K*n,0);
 uint64_t previous=UINT64_MAX;
 for(auto z:keys){
  if((z>>24)==previous)continue;previous=z>>24;
  int S=z>>48,p=z&((1<<24)-1);
  for(int v=0;v<n;v++)if(!(S&(1<<v))){
   int o=pow3[v];if(ids[p-2*o]!=ids[p-o])edge[S*n+v]++;
  }
 }
 vector<int> lo(K,1e9),hi(K,0),lchoice(K,-1),hchoice(K,-1);
 lo[K-1]=0;
 for(int S=K-2;S>=0;S--)for(int v=0;v<n;v++)if(!(S&(1<<v))){
  int u=S|(1<<v),e=edge[S*n+v];
  if(e+lo[u]<lo[S]){lo[S]=e+lo[u];lchoice[S]=v;}
  if(e+hi[u]>hi[S]||hchoice[S]<0){hi[S]=e+hi[u];hchoice[S]=v;}
 }
 auto order=[&](vector<int> choice){vector<int> a;int S=0;for(int k=0;k<n;k++){
  int v=choice[S];a.push_back(v+1);S|=1<<v;
 }return a;};
 auto show=[&](vector<int> a){for(int x:a)cout<<x<<' ';cout<<'\n';};
 cout<<"F15 models="<<models<<" exact OBDD min="<<lo[0]<<" max="<<hi[0]<<"\n";
 cout<<"min order: ";show(order(lchoice));
 cout<<"max order: ";show(order(hchoice));
 cout<<"lattice cubes="<<T<<"\nP versus NP OPEN\n";
}
