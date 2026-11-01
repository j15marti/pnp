// Exhaustive min fan-in-2 circuit size (gates; wires = 2*gates) for all n-var functions up to depth D.
// usage: mincirc n D basis   basis: b2 | mono
#include <bits/stdc++.h>
using namespace std;
int n,D,mono; int NT; unsigned FULL;
vector<int> best; vector<unsigned> nodes; vector<int> ops;
long long visited=0;
void rec(int d){
  visited++;
  if(d==D) return;
  int m=nodes.size();
  for(int i=0;i<m;i++)for(int j=i+1;j<m;j++)for(int op:ops){
    unsigned a=nodes[i],b=nodes[j],r=0;
    // op: 4-bit table on (a,b): bit (2*abit+bbit)
    for(int k=0;k<4;k++) if(op>>k&1){ unsigned ma=(k&2)?a:~a, mb=(k&1)?b:~b; r|=ma&mb; }
    r&=FULL;
    bool dup=false; for(unsigned x:nodes) if(x==r){dup=true;break;}
    if(dup) continue;
    if(best[r]>d+1) best[r]=d+1;
    nodes.push_back(r); rec(d+1); nodes.pop_back();
  }
}
int main(int c,char**v){
  n=atoi(v[1]);D=atoi(v[2]);mono=strcmp(v[3],"mono")==0;
  NT=1<<n; FULL=(NT==32)?0xffffffffu:((1u<<NT)-1);
  best.assign(1u<<NT,99); // only n<=4 -> 65536
  for(int i=0;i<n;i++){unsigned t=0;for(int x=0;x<NT;x++)if(x>>i&1)t|=1u<<x;nodes.push_back(t);best[t]=0;}
  best[0]=best[FULL]=99; // constants not counted
  if(mono) ops={8,14}; else { for(int o=1;o<15;o++) if(o!=3&&o!=5&&o!=10&&o!=12) ops.push_back(o);}
  rec(0);
  map<int,int> cnt; for(unsigned f=0;f<(1u<<NT);f++) cnt[best[f]]++;
  printf("n=%d D=%d basis=%s nodes_visited=%lld\n",n,D,v[3],visited);
  for(auto&p:cnt) printf("size %d : %d functions\n",p.first,p.second);
  if(n==3&&!mono){ // print a few
    unsigned maj=0xE8, par=0x96; printf("MAJ3=%d PAR3=%d\n",best[maj],best[par]); }
}
