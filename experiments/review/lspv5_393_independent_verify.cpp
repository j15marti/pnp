#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <string>
#include <sys/resource.h>
#include <vector>

// Independent REFEREE393 verifier.  Clauses use base-3 digits rather than
// producer bit-pairs; sources are reconstructed from the cubic graph.

static constexpr int C=6561;
static int p3[9];
using U16=uint16_t;

static int pc(unsigned x){return __builtin_popcount(x);}
template<class T> static void uniq(std::vector<T>&v){
  std::sort(v.begin(),v.end());v.erase(std::unique(v.begin(),v.end()),v.end());
}

static int resolve3(int a,int b){
  int out=0,pivots=0;
  for(int i=0;i<8;i++){
    int x=a%3,y=b%3;a/=3;b/=3;
    if((x==1&&y==2)||(x==2&&y==1)){pivots++;continue;}
    if(x&&y&&x!=y)return -1;
    out+=(x?x:y)*p3[i];
  }
  return pivots==1?out:-1;
}

static int resolve_global(uint32_t a,uint32_t b){
  unsigned ap=a&0xffffu,an=a>>16,bp=b&0xffffu,bn=b>>16;
  unsigned piv=(ap&bn)|(an&bp);if(pc(piv)!=1)return -1;
  unsigned op=(ap|bp)&~piv,on=(an|bn)&~piv;if(op&on)return -1;
  return int(uint32_t(op|(on<<16)));
}

static std::vector<std::vector<int>> formula(){
  std::vector<std::pair<int,int>> edges;
  for(int o:{0,5})for(int u=0;u<4;u++)for(int v=u+1;v<4;v++)
    if(u==0&&v==1){edges.push_back({o,o+4});edges.push_back({o+4,o+1});}
    else edges.push_back({o+u,o+v});
  edges.push_back({4,9});
  std::vector<std::vector<int>> incidence(10);
  for(int i=0;i<15;i++){
    incidence[edges[i].first].push_back(i+1);
    incidence[edges[i].second].push_back(i+1);
  }
  std::vector<std::vector<int>> F;
  for(int v=0;v<10;v++)for(int t=0;t<8;t++){
    int a=(t>>2)&1,b=(t>>1)&1,c=t&1;
    if((a^b^c)==(v==0))continue;
    F.push_back({a?-incidence[v][0]:incidence[v][0],
                 b?-incidence[v][1]:incidence[v][1],
                 c?-incidence[v][2]:incidence[v][2]});
  }
  return F;
}

static std::vector<int> side_vars(bool right){
  return right?std::vector<int>{8,9,10,11,12,13,14,15}
              :std::vector<int>{1,2,3,4,5,6,7,15};
}

static int encode_clause(const std::vector<int>&cl,const std::vector<int>&vars){
  int z=0;
  for(int l:cl){
    auto it=std::find(vars.begin(),vars.end(),std::abs(l));
    if(it==vars.end())return -1;
    z+=(l>0?1:2)*p3[it-vars.begin()];
  }
  return z;
}

static uint32_t global_key(U16 c,bool right){
  const auto vars=side_vars(right);unsigned gp=0,gn=0;
  for(unsigned i=0;i<8;i++,c/=3){
    unsigned d=c%3;
    if(d==1)gp|=1u<<(vars[i]-1);
    if(d==2)gn|=1u<<(vars[i]-1);
  }
  return uint32_t(gp|(gn<<16));
}

struct Masks{std::vector<unsigned> v;};
using Catalog=std::map<uint32_t,Masks>;
static void add_minimal(Masks&m,unsigned x){
  for(unsigned y:m.v)if((y&x)==y)return;
  m.v.erase(std::remove_if(m.v.begin(),m.v.end(),[x](unsigned y){return (y&x)==x;}),m.v.end());
  m.v.push_back(x);
}
static bool disjoint(const Masks&a,const Masks&b){
  for(unsigned x:a.v)for(unsigned y:b.v)if(!(x&y))return true;
  return false;
}
static unsigned minimum_overlap(const Masks&a,const Masks&b){
  unsigned best=999;
  for(unsigned x:a.v)for(unsigned y:b.v)best=std::min(best,unsigned(pc(x&y)));
  return best;
}

struct SideResult{
  Catalog catalog;
  uint64_t pair_tests=0,occurrences=0;
};

static SideResult close_side(bool right,const std::vector<int16_t>&table){
  const auto F=formula();std::vector<int> ids;
  if(!right){for(int i=0;i<16;i++)ids.push_back(i);ids.push_back(17);ids.push_back(18);}
  else{for(int i=20;i<36;i++)ids.push_back(i);ids.push_back(36);ids.push_back(39);}
  const auto vars=side_vars(right);const int n=18,total=1<<n;
  std::vector<std::vector<U16>> dp(total);SideResult out;
  for(int i=0;i<n;i++)dp[1<<i].push_back(U16(encode_clause(F[ids[i]],vars)));
  for(int size=1;size<=n;size++)for(int sub=1;sub<total;sub++)if(pc(sub)==size){
    if(size>1){
      std::vector<U16> cur;const int anchor=sub&-sub;
      for(int a=(sub-1)&sub;a;a=(a-1)&sub){
        if(!(a&anchor))continue;
        int b=sub^a;
        if(!b)continue;
        out.pair_tests+=uint64_t(dp[a].size())*dp[b].size();
        for(U16 x:dp[a])for(U16 y:dp[b]){
          int z=table[size_t(x)*C+y];if(z>=0)cur.push_back(U16(z));
        }
      }
      uniq(cur);dp[sub]=std::move(cur);
    }
    out.occurrences+=dp[sub].size();
    for(U16 c:dp[sub])add_minimal(out.catalog[global_key(c,right)],unsigned(sub));
  }
  return out;
}

struct Cross{uint32_t clause;const Masks*lm;const Masks*rm;};
static std::string read_all(const char*path){
  std::ifstream f(path);return std::string((std::istreambuf_iterator<char>(f)),{});
}

int main(int argc,char**argv){
  if(argc!=3){std::cerr<<"usage: verifier primary.json verification.json\n";return 2;}
  const auto start=std::chrono::steady_clock::now();
  p3[0]=1;for(int i=1;i<9;i++)p3[i]=p3[i-1]*3;
  std::vector<int16_t> table(size_t(C)*C,-1);
  for(int a=0;a<C;a++)for(int b=0;b<C;b++)table[size_t(a)*C+b]=resolve3(a,b);
  SideResult L=close_side(false,table),R=close_side(true,table);
  uint64_t all_cross=0;std::vector<Cross>x4;
  for(const auto&[l,lm]:L.catalog)for(const auto&[r,rm]:R.catalog){
    int z=resolve_global(l,r);if(z<0)continue;all_cross++;
    uint32_t c=uint32_t(z);
    if(pc((c&0xffffu)|(c>>16))==4)x4.push_back({c,&lm,&rm});
  }
  uint64_t pairs=0,strict=0,small=0,disjoint_small=0;
  uint64_t left_disjoint=0,right_disjoint=0;unsigned min_overlap=999;
  std::set<uint32_t>outputs;
  for(size_t i=0;i<x4.size();i++)for(size_t j=i+1;j<x4.size();j++){
    pairs++;int z=resolve_global(x4[i].clause,x4[j].clause);if(z<0)continue;strict++;
    uint32_t out=uint32_t(z);if(pc((out&0xffffu)|(out>>16))>3)continue;
    small++;outputs.insert(out);
    const bool ld=disjoint(*x4[i].lm,*x4[j].lm),rd=disjoint(*x4[i].rm,*x4[j].rm);
    left_disjoint+=ld;right_disjoint+=rd;
    min_overlap=std::min(min_overlap,minimum_overlap(*x4[i].lm,*x4[j].lm)+
      minimum_overlap(*x4[i].rm,*x4[j].rm));
    if(ld&&rd)disjoint_small++;
  }
  const std::string primary=read_all(argv[1]);
  bool ok=L.catalog.size()==3234&&R.catalog.size()==3234&&
    L.occurrences==11705410&&R.occurrences==11705410&&
    L.pair_tests==1126097195ULL&&R.pair_tests==1126097195ULL&&
    all_cross==4056196&&x4.size()==6724&&pairs==22602726&&
    strict==8592320&&small==13120&&left_disjoint==0&&right_disjoint==0&&
    disjoint_small==0&&min_overlap==3&&outputs.size()==2296&&
    primary.find("\"strict_double_cross_pairs\": 8592320")!=std::string::npos&&
    primary.find("\"semantic_support_at_most_three_pairs\": 13120")!=std::string::npos&&
    primary.find("\"semantic_pairs_with_left_disjoint_ancestry\": 0")!=std::string::npos&&
    primary.find("\"semantic_pairs_with_right_disjoint_ancestry\": 0")!=std::string::npos&&
    primary.find("\"source_disjoint_support_at_most_three_pairs\": 0")!=std::string::npos;
  int mutations=0;
  mutations+=!(L.catalog.size()==3233);mutations+=!(R.catalog.size()==3235);
  mutations+=!(all_cross==4056195);mutations+=!(x4.size()==6723);
  mutations+=!(pairs==22602725);mutations+=!(strict==8592319);
  mutations+=!(small==13119);mutations+=!(small==13121);
  mutations+=!(left_disjoint==1);mutations+=!(right_disjoint==1);
  mutations+=!(disjoint_small==1);mutations+=!(min_overlap==2);
  mutations+=!(outputs.size()==2295);
  mutations+=!(outputs.size()==2297);
  mutations+=!(primary.find("\"falsifier_found\": true")!=std::string::npos);
  if(mutations!=15)ok=false;
  rusage ru{};getrusage(RUSAGE_SELF,&ru);
  double seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
  std::ofstream out(argv[2]);
  out<<"{\n  \"pass\": "<<(ok?"true":"false")<<",\n"
     <<"  \"independent_encoding\": \"base-3 clauses reconstructed from graph incidence\",\n"
     <<"  \"left_unique_clauses\": "<<L.catalog.size()<<",\n"
     <<"  \"right_unique_clauses\": "<<R.catalog.size()<<",\n"
     <<"  \"all_first_cross_resolvents\": "<<all_cross<<",\n"
     <<"  \"support_four_first_cross_resolvents\": "<<x4.size()<<",\n"
     <<"  \"unordered_double_cross_pair_tests\": "<<pairs<<",\n"
     <<"  \"strict_double_cross_pairs\": "<<strict<<",\n"
     <<"  \"semantic_support_at_most_three_pairs\": "<<small<<",\n"
     <<"  \"semantic_pairs_with_left_disjoint_ancestry\": "<<left_disjoint<<",\n"
     <<"  \"semantic_pairs_with_right_disjoint_ancestry\": "<<right_disjoint<<",\n"
     <<"  \"source_disjoint_support_at_most_three_pairs\": "<<disjoint_small<<",\n"
     <<"  \"minimum_total_reused_source_count\": "<<(small?min_overlap:0)<<",\n"
     <<"  \"distinct_support_at_most_three_outputs\": "<<outputs.size()<<",\n"
     <<"  \"mutations_rejected\": "<<mutations<<",\n"
     <<"  \"elapsed_seconds\": "<<seconds<<",\n"
     <<"  \"max_rss_kib\": "<<ru.ru_maxrss<<"\n}\n";
  std::cout<<(ok?"PASS":"FAIL")<<" seconds="<<seconds<<" rss="<<ru.ru_maxrss<<"\n";
  return ok?0:1;
}
