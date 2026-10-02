#include <array>
#include <cstdint>
#include <fstream>
#include <functional>
#include <iostream>
#include <set>
#include <sstream>
#include <stdexcept>
#include <vector>
using namespace std;
struct Node{int q=-1,lo=0,hi=0;};
struct Gate{char op;int a,b;};
int main(int argc,char**argv){try{
 if(argc!=2)throw runtime_error("usage: verify_frontier RESULTS_DIRECTORY");
 string dir=argv[1];array<uint16_t,32> truth{};array<array<int,3>,32> vars{};
 for(int q=0;q<32;q++){
  int t=0;for(int v=0;v<4;v++)if(v!=q/8)vars[q][t++]=v;
  for(int a=0;a<16;a++){bool clause=false;for(int j=0;j<3;j++)clause|=((a>>vars[q][j])&1)!=((q%8>>j)&1);if(clause)truth[q]|=1u<<a;}
 }
 // Materialize the 64-gate AND/OR/NOT circuit; input IDs 0..31.
 vector<Gate> gates;vector<int> covers;
 auto gate=[&](char op,int a,int b){int id=32+gates.size();gates.push_back({op,a,b});return id;};
 for(int a=0;a<16;a++){
  vector<int> incident;for(int q=0;q<32;q++)if(!(truth[q]&(1u<<a)))incident.push_back(q);
  if(incident.size()!=4)throw runtime_error("incidence");
  covers.push_back(gate('O',gate('O',incident[0],incident[1]),gate('O',incident[2],incident[3])));
 }
 while(covers.size()>1){vector<int> next;for(size_t i=0;i<covers.size();i+=2)next.push_back(gate('A',covers[i],covers[i+1]));covers=next;}
 int satout=gate('N',covers[0],covers[0]);
 ofstream circuit(dir+"/coverage.circuit");circuit<<"32 "<<gates.size()<<" "<<satout<<"\n";for(size_t i=0;i<gates.size();i++)circuit<<32+i<<" "<<gates[i].op<<" "<<gates[i].a<<" "<<gates[i].b<<"\n";
 if(gates.size()!=64)throw runtime_error("gate count");
 ofstream results(dir+"/verification.csv");results<<"n,m,inputs,unsat,semantic_functions,dag_nodes,dag_errors,circuit_gates,circuit_errors\n";
 ofstream profiles(dir+"/imbalance_variance.csv");profiles<<"n,m,I,V_times_4,formulas,unsat\n";
 array<uint32_t,4> posbits{},negbits{};for(int q=0;q<32;q++)for(int j=0;j<3;j++)(((q%8>>j)&1)?negbits:posbits)[vars[q][j]]|=1u<<q;
 for(int clauses=8;clauses<=11;clauses++){
  ifstream f(dir+"/D4_"+to_string(clauses)+".dag");int n,m,root,N;if(!(f>>n>>m>>root>>N)||n!=4||m!=clauses||root<0||root>=N)throw runtime_error("DAG header");
  vector<Node> nodes(N);for(int i=2;i<N;i++){int id;if(!(f>>id>>nodes[i].q>>nodes[i].lo>>nodes[i].hi)||id!=i||nodes[i].q<0||nodes[i].q>=32||nodes[i].lo<0||nodes[i].hi<0||nodes[i].lo>=i||nodes[i].hi>=i)throw runtime_error("non-topological DAG");}
  set<int> reachable;function<void(int)> visit=[&](int id){if(id<2||!reachable.insert(id).second)return;visit(nodes[id].lo);visit(nodes[id].hi);};visit(root);
  vector<uint32_t> labels(N);for(int i=2;i<N;i++){auto v=nodes[i];uint32_t below=labels[v.lo]|labels[v.hi];if(below&(1u<<v.q))throw runtime_error("repeat query");labels[i]=below|(1u<<v.q);}
  const int stride=5000;vector<uint64_t> counts(34*stride),unsats(34*stride);
  uint64_t total=0,unsat=0,de=0,ce=0;array<bool,65536> sem{};
  function<void(int,int,uint32_t,uint16_t)> enumerate=[&](int start,int left,uint32_t selected,uint16_t satmask){
   if(left){for(int q=start;q<=32-left;q++)enumerate(q+1,left-1,selected|(1u<<q),satmask&truth[q]);return;}
   bool expected=satmask!=0;total++;unsat+=!expected;sem[satmask]=true;
   {int id=root;while(id>=2){auto v=nodes[id];id=(selected&(1u<<v.q))?v.hi:v.lo;}de+=(id==0)!=expected;}
   int I=0,dsq=0;for(int v=0;v<4;v++){int p=__builtin_popcount(selected&posbits[v]),n=__builtin_popcount(selected&negbits[v]);I+=abs(p-n);dsq+=(p+n)*(p+n);}int V4=4*dsq-9*clauses*clauses;counts[I*stride+V4]++;unsats[I*stride+V4]+=!expected;
   bool values[96];for(int q=0;q<32;q++)values[q]=(selected>>q)&1;
   for(size_t i=0;i<gates.size();i++){auto g=gates[i];values[32+i]=g.op=='O'?(values[g.a]|values[g.b]):g.op=='A'?(values[g.a]&values[g.b]):!values[g.a];}
   ce+=values[satout]!=expected;
  };enumerate(0,clauses,0,65535);int distinct=0;for(bool v:sem)distinct+=v;
  results<<4<<","<<clauses<<","<<total<<","<<unsat<<","<<distinct<<","<<reachable.size()<<","<<de<<",64,"<<ce<<"\n";results.flush();
  for(int I=0;I<34;I++)for(int V4=0;V4<stride;V4++)if(counts[I*stride+V4])profiles<<4<<","<<clauses<<","<<I<<","<<V4<<","<<counts[I*stride+V4]<<","<<unsats[I*stride+V4]<<"\n";profiles.flush();
  cerr<<"verified m="<<clauses<<" inputs="<<total<<" dag_errors="<<de<<" circuit_errors="<<ce<<"\n";if(de||ce)throw runtime_error("classification mismatch");
 }
 ifstream pairs(dir+"/pair_witnesses.csv");string line;getline(pairs,line);set<pair<int,int>> seen;int extended=0;
 ofstream ext(dir+"/extended_pair_witnesses.csv");ext<<"m,edge_a,edge_b,unsat_input,sat_input\n";
 while(getline(pairs,line)){for(char&c:line)if(c==',')c=' ';istringstream s(line);int a,b;uint32_t u,v;s>>a>>b>>u>>v;
  if(a<0||b>=32||a>=b||!seen.insert({a,b}).second)throw runtime_error("pair index");
  for(int count=8;count<=11;count++){
   auto mask=[&](uint32_t x){uint16_t t=65535;for(int q=0;q<32;q++)if(x&(1u<<q))t&=truth[q];return t;};
   if(__builtin_popcount(u)!=count||__builtin_popcount(v)!=count||(u^v)!=((1u<<a)|(1u<<b))||mask(u)!=0||mask(v)==0)throw runtime_error("bad witness");
   ext<<count<<","<<a<<","<<b<<","<<u<<","<<v<<"\n";extended++;
   if(count<11){int q=0;while(q<32&&(((u|v)&(1u<<q))||!(mask(v)&truth[q])))q++;if(q==32)throw runtime_error("extension failed");u|=1u<<q;v|=1u<<q;}
  }
 }
 if(seen.size()!=496)throw runtime_error("incomplete certificate");
 cout<<"verified_pair_certificates="<<extended<<" circuit_gates=64\n";
}catch(const exception&e){cerr<<e.what()<<"\n";return 1;}}
