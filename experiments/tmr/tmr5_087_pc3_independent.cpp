// TMR-5/087 independent C++ relation-bitset path-consistency verifier.
// Build: c++ -std=c++17 -O3 tmr5_087_pc3_independent.cpp -o pc3_087
// Run: ./pc3_087 tmr5_087_W33_oriented.txt
#include <cassert>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
using namespace std;
using U=uint32_t;
constexpr U FULL=(1u<<25)-1;
U EQ=0, REL=0;

U transpose(U r){
 U out=0;
 for(int i=0;i<5;i++)for(int j=0;j<5;j++)
   if(r&(1u<<(5*i+j)))out|=(1u<<(5*j+i));
 return out;
}
inline U compose(U a,U b){
 U b0=b&31, b1=(b>>5)&31,b2=(b>>10)&31,b3=(b>>15)&31,b4=(b>>20)&31;
 U out=0;
 for(int i=0;i<5;i++){
  U x=(a>>(5*i))&31;
  U y=((x&1)?b0:0)|((x&2)?b1:0)|((x&4)?b2:0)|((x&8)?b3:0)|((x&16)?b4:0);
  out|=(y<<(5*i));
 }
 return out;
}
struct Result {bool accepts; int rounds; int empty_i;int empty_j;int empty_mid;};
Result pc(const vector<pair<int,int>>& arcs,int n,int root){
 vector<vector<U>> p(n,vector<U>(n,FULL));
 for(int i=0;i<n;i++)p[i][i]=EQ;
 U back=transpose(REL);
 for(auto [u,v]:arcs){p[u][v]&=REL;p[v][u]&=back;}
 if(root>=0){
  U col=0;for(int i=0;i<5;i++)col|=(1u<<(5*i));
  for(int j=0;j<n;j++){p[root][j]&=31u;p[j][root]&=col;}
 }
 for(int round=1;round<=30;round++){
  bool changed=false;
  for(int mid=0;mid<n;mid++)
   for(int i=0;i<n;i++)
    for(int j=i;j<n;j++){
     U r=p[i][j]&compose(p[i][mid],p[mid][j]);
     if(r==0)return {false,round,i,j,mid};
     if(r!=p[i][j]){p[i][j]=r;p[j][i]=transpose(r);changed=true;}
    }
  if(!changed)return {true,round,-1,-1,-1};
 }
 assert(false && "More than 30 PC3 rounds");
 return {false,30,-1,-1,-1};
}
int main(int argc,char**argv){
 if(argc!=2){cerr<<"usage: pc3_087 tmr5_087_W33_oriented.txt\n";return 2;}
 ifstream in(argv[1]);if(!in){cerr<<"cannot open input\n";return 2;}
 int n,m;in>>n>>m;
 if(n!=80||m!=160){cerr<<"unexpected graph size\n";return 2;}
 vector<pair<int,int>> arcs;
 for(int i=0;i<m;i++){int u,v;in>>u>>v;if(u<0||v<0||u>=n||v>=n||u==v)return 2;arcs.emplace_back(u,v);}
 for(int a=0;a<5;a++){
  EQ|=(1u<<(6*a));
  for(int b=0;b<5;b++)if((b-a+5)%5==1||(b-a+5)%5==3)REL|=(1u<<(5*a+b));
 }
 assert(__builtin_popcount(REL)==10);
 Result un=pc(arcs,n,-1);
 int pass=0;
 for(int root=0;root<n;root++)if(pc(arcs,n,root).accepts)pass++;
 cout<<"{\"vertices\":"<<n<<",\"arcs\":"<<m<<",\"unanchored_PC3_accepts\":"
     <<(un.accepts?"true":"false")<<",\"unanchored_PC3_scans\":"<<un.rounds
     <<",\"anchored_PC3_surviving_roots\":"<<pass<<",\"anchors_tested\":"<<n<<"}\n";
 if(!un.accepts || pass!=0)return 1;
 return 0;
}
