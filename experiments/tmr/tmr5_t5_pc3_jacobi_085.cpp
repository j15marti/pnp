// Independent raw T5 synchronous path-consistency (Jacobi); no gadget inversion.
// Compile: g++ -std=c++17 -O3 tmr5_t5_pc3_jacobi_085.cpp -o pc3
// Run: ./pc3 < tmr5_t5_pc3_survivor_input_085.txt
#include <iostream>
#include <vector>
#include <cstdint>
using namespace std;
const uint32_t FULL=(1u<<25)-1;
uint32_t trans(uint32_t x){
  uint32_t y=0;
  for(int a=0;a<5;a++)for(int b=0;b<5;b++)
    if((x>>(a*5+b))&1u)y|=1u<<(b*5+a);
  return y;
}
uint32_t compose(uint32_t x,uint32_t y){
  uint32_t result=0;
  for(int a=0;a<5;a++)for(int b=0;b<5;b++){
    for(int c=0;c<5;c++)if(((x>>(a*5+c))&1u)&&((y>>(c*5+b))&1u)){
      result|=1u<<(a*5+b);break;
    }
  }
  return result;
}
int main(){
  int n,m;cin>>n>>m;
  vector<vector<uint32_t>> p(n,vector<uint32_t>(n,FULL));
  for(int i=0;i<n;i++){
    p[i][i]=0;
    for(int a=0;a<5;a++)p[i][i]|=1u<<(6*a);
  }
  uint32_t relation=0;
  for(int a=0;a<5;a++)for(int b=0;b<5;b++)
    if((b-a+5)%5==1||(b-a+5)%5==3)relation|=1u<<(5*a+b);
  for(int t=0;t<m;t++){
    int u,v;cin>>u>>v;
    p[u][v]&=relation;p[v][u]&=trans(relation);
  }
  for(int round=1;round<=1000;round++){
    vector<vector<uint32_t>> next=p;
    int changes=0;
    for(int i=0;i<n;i++)for(int j=i;j<n;j++){
      uint32_t allowed=p[i][j];
      for(int k=0;k<n;k++){
        allowed&=compose(p[i][k],p[k][j]);
        if(allowed==0)break;
      }
      if(allowed!=p[i][j]){
        changes++;next[i][j]=allowed;next[j][i]=trans(allowed);
      }
    }
    p.swap(next);
    for(int i=0;i<n;i++)for(int j=0;j<n;j++)if(!p[i][j]){
      cout<<"REFUTES round="<<round<<" pair="<<i<<","<<j<<"\n";return 0;
    }
    if(!changes){
      cout<<"SURVIVES round="<<round<<" pairs="<<(n*n)<<"\n";return 0;
    }
  }
  cerr<<"No convergence within 1000 synchronous rounds\n";return 1;
}
