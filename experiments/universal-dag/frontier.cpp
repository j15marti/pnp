#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <functional>
#include <iostream>
#include <map>
#include <numeric>
#include <random>
#include <set>
#include <sstream>
#include <stdexcept>
#include <tuple>
#include <unordered_map>
#include <vector>
using namespace std;
using U=uint32_t;
struct Node {int q,lo,hi;};
vector<U> edges;
vector<U> matchings;
uint64_t choose(int n,int k){if(k<0||k>n)return 0;uint64_t v=1;for(int j=1;j<=k;j++)v=v*(n-j+1)/j;return v;}
void init(){
 for(int omit=0;omit<4;omit++)for(int s=0;s<8;s++){
  int a=0,t=0;for(int v=0;v<4;v++)if(v!=omit)a|=((s>>t++)&1)<<v;
  edges.push_back((1u<<a)|(1u<<(a|(1<<omit))));
 }
 function<void(U,U)> visit=[&](U covered,U selected){
  if(covered==65535){matchings.push_back(selected);return;}
  int a=0;while(covered&(1u<<a))a++;
  for(int e=0;e<32;e++)if((edges[e]&(1u<<a))&&!(edges[e]&covered))visit(covered|edges[e],selected|(1u<<e));
 };visit(0,0);sort(matchings.begin(),matchings.end());
 if(matchings.size()!=272)throw runtime_error("matching count");
}
struct Builder {
 vector<int> order;vector<Node> nodes={{-1,0,0},{-1,1,1}};
 map<tuple<int,int,int>,int> unique;
 unordered_map<string,int> memo;
 int mode;mt19937 rng;
 Builder(vector<int> o,int mode=0,int seed=1):order(o),mode(mode),rng(seed){}
 int mk(int q,int l,int h){if(l==h)return l;auto key=make_tuple(q,l,h);auto it=unique.find(key);if(it!=unique.end())return it->second;int id=nodes.size();nodes.push_back({q,l,h});unique[key]=id;return id;}
 int build(U avail,int r,const vector<U>& pos){
  if(pos.empty())return 0;
  int a=__builtin_popcount(avail);
  if(pos.size()==choose(a,r))return 1;
  string key;auto add=[&](U v){for(int j=0;j<4;j++)key.push_back(char(v>>(8*j)));};add(avail);add(r);for(U p:pos)add(p);
  auto it=memo.find(key);if(it!=memo.end())return it->second;
  int q=-1;double best=-1e300;
  for(int e:order)if(avail&(1u<<e)){
   if(!mode){q=e;break;}
   int h=0;for(U p:pos)h+=bool(p&(1u<<e));int l=pos.size()-h;
   double score=0;
   if(mode==1)score=-double(h)*h-double(l)*l;
   if(mode==2)score=double(h)*h+double(l)*l;
   if(mode==3)score=(h==0||l==0?1e6:0)-abs(h-l);
   if(mode==4)score=double(rng());
   if(score>best){best=score;q=e;}
  }
  U bit=1u<<q;vector<U> lo,hi;
  for(U p:pos)if(p&bit)hi.push_back(p^bit);else lo.push_back(p);
  sort(hi.begin(),hi.end());
  int l=build(avail^bit,r,lo),h=build(avail^bit,r-1,hi);
  return memo[key]=mk(q,l,h);
 }
 int count(int root)const{set<int> seen;function<void(int)> visit=[&](int id){if(id<2||!seen.insert(id).second)return;visit(nodes[id].lo);visit(nodes[id].hi);};visit(root);return seen.size();}
 void save(string path,int root,int m=8)const{ofstream f(path);f<<"4 "<<m<<" "<<root<<" "<<nodes.size()<<"\n";for(int i=2;i<int(nodes.size());i++)f<<i<<" "<<nodes[i].q<<" "<<nodes[i].lo<<" "<<nodes[i].hi<<"\n";}
};
int main(int argc,char**argv){try{
 string out=argc>1?argv[1]:".";int passes=argc>2?stoi(argv[2]):3;init();
 ofstream log(out+"/search.csv");log<<"method,trial,nodes,memo_states\n";
 vector<int> order;for(int s=0;s<8;s++)for(int omit=0;omit<4;omit++)order.push_back(omit*8+s);
 int best=1000000,trial=0;vector<int> bestorder=order;
 auto run=[&](vector<int> o,int mode,string label,int seed){Builder b(o,mode,seed);int root=b.build(0xffffffff,8,matchings),n=b.count(root);log<<label<<","<<trial++<<","<<n<<","<<b.memo.size()<<"\n";log.flush();if(n<best){best=n;bestorder=o;b.save(out+"/best.dag",root);cerr<<"best "<<best<<" "<<label<<"\n";}return n;};
 run(order,0,"sign_round_robin",1);
 vector<int> grouped(32);iota(grouped.begin(),grouped.end(),0);run(grouped,0,"grouped",1);
 order=bestorder;
 for(int pass=0;pass<passes;pass++){bool changed=false;for(int i=0;i<31;i++){auto cand=order;swap(cand[i],cand[i+1]);int old=best;run(cand,0,"adjacent",1);if(best<old){order=bestorder;changed=true;}}if(!changed)break;}
 // Deterministic insertion sifting: move each query to every position.
 for(int sweep=0;sweep<3;sweep++){bool changed=false;for(int q=0;q<32;q++){
  auto base=order;base.erase(find(base.begin(),base.end(),q));int before=best;
  for(int at=0;at<32;at++){auto cand=base;cand.insert(cand.begin()+at,q);run(cand,0,"insertion",1);}
  if(best<before){order=bestorder;changed=true;}
 }if(!changed)break;}
 for(int mode=1;mode<=4;mode++)for(int seed=1;seed<=(mode==4?20:1);seed++)run(order,mode,"adaptive_"+to_string(mode),seed);
 ofstream of(out+"/best_order.txt");for(int q:bestorder)of<<q<<" ";of<<"\n";
 ofstream panel(out+"/ordered_panel.csv");panel<<"n,m,order,nodes,memo_states\n";
 for(int m=8;m<=11;m++){
  int incumbent=100000000;
  for(int variant=0;variant<2;variant++){
   vector<int> o=variant?bestorder:vector<int>();if(!variant)for(int s=0;s<8;s++)for(int v=0;v<4;v++)o.push_back(v*8+s);
   Builder b(o);unordered_map<U,int> memo;array<U,33> suffix{};for(int i=31;i>=0;i--)suffix[i]=suffix[i+1]|edges[o[i]];
   function<int(int,int,U)> rec=[&](int i,int r,U cov){
    if(cov==65535)return 1;
    if(r==0||__builtin_popcount(cov)+2*r<16||(cov|suffix[i])!=65535)return 0;
    if(r==32-i)return 1;
    U key=cov|(U(r)<<16)|(U(i)<<22);auto it=memo.find(key);if(it!=memo.end())return it->second;
    int l=rec(i+1,r,cov),h=rec(i+1,r-1,cov|edges[o[i]]);return memo[key]=b.mk(o[i],l,h);
   };
   int root=rec(0,m,0),sz=b.count(root);panel<<4<<","<<m<<","<<(variant?"optimized_m8_order":"sign_round_robin")<<","<<sz<<","<<memo.size()<<"\n";panel.flush();
   if(sz<incumbent){incumbent=sz;b.save(out+"/D4_"+to_string(m)+".dag",root,m);}
  }
 }
 ofstream cert(out+"/pair_witnesses.csv");cert<<"edge_a,edge_b,unsat_input,sat_input\n";
 for(int a=0;a<32;a++)for(int b=a+1;b<32;b++){
  bool found=false;for(U p:matchings)if((p&(1u<<a))&&!(p&(1u<<b))){U s=p^(1u<<a)^(1u<<b),cov=0;for(int e=0;e<32;e++)if(s&(1u<<e))cov|=edges[e];if(cov!=65535){cert<<a<<","<<b<<","<<p<<","<<s<<"\n";found=true;break;}}
  if(!found)throw runtime_error("pair witness missing");
 }
 cout<<"best_nodes="<<best<<" matching_count="<<matchings.size()<<" pair_witnesses=496\n";
}catch(const exception&e){cerr<<e.what()<<"\n";return 1;}}
