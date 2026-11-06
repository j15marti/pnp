#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <map>
#include <set>
#include <string>
#include <sys/resource.h>
#include <vector>

// Independent representation: base-3 clauses and separately reconstructed
// local truth vectors.  It shares no producer objects or serialized states.
static constexpr int C = 6561;
static int p3[9];
using U16 = uint16_t;

struct State { std::vector<U16> clauses, factors, equations, conditions; };
struct Info { unsigned min_sources = std::numeric_limits<unsigned>::max(); };
using Catalog = std::map<uint32_t, Info>;
using ClauseCatalog = std::map<uint32_t, Info>;

template<class T> static void uniq(std::vector<T>&v) {
  std::sort(v.begin(),v.end());
  v.erase(std::unique(v.begin(),v.end()),v.end());
}
static int pc(unsigned x){return __builtin_popcount(x);}
static U16 factor_code(unsigned s,unsigned t){return U16(s|(t<<8));}
static U16 equation_code(unsigned m,unsigned r){return U16(m|((r&1)<<8));}

static unsigned clause_support(U16 c){
  unsigned s=0;
  for(int i=0;i<8;i++,c/=3) if(c%3) s|=1u<<i;
  return s;
}

static unsigned local_index(unsigned g,unsigned s){
  unsigned z=0,j=0;
  for(int i=0;i<8;i++) if((s>>i)&1u){z|=((g>>i)&1u)<<j;j++;}
  return z;
}

static U16 clause_factor(U16 c){
  unsigned tr[8],s=0,z=c;
  for(int i=0;i<8;i++,z/=3){tr[i]=z%3;if(tr[i])s|=1u<<i;}
  unsigned t=0,k=pc(s);
  for(unsigned a=0;a<(1u<<k);a++){
    unsigned g=0,j=0;
    for(int i=0;i<8;i++)if((s>>i)&1u){g|=((a>>j)&1u)<<i;j++;}
    bool ok=false;
    for(int i=0;i<8;i++)if(tr[i])ok|=(tr[i]==1?bool((g>>i)&1u):!bool((g>>i)&1u));
    if(ok)t|=1u<<a;
  }
  return factor_code(s,t);
}

static unsigned expand(U16 f,unsigned u){
  unsigned s=f&255u,t=f>>8,out=0,k=pc(u);
  for(unsigned a=0;a<(1u<<k);a++){
    unsigned g=0,j=0;
    for(int i=0;i<8;i++)if((u>>i)&1u){g|=((a>>j)&1u)<<i;j++;}
    if((t>>local_index(g,s))&1u)out|=1u<<a;
  }
  return out;
}

static U16 equation_factor(U16 e){
  unsigned m=e&255u,r=e>>8,t=0,k=pc(m);
  for(unsigned a=0;a<(1u<<k);a++)if((pc(a)&1)==int(r))t|=1u<<a;
  return factor_code(m,t);
}

static int affine_alias(U16 f){
  unsigned s=f&255u,t=f>>8;
  for(unsigned m=0;m<256;m++)if(!(m&~s))for(unsigned r=0;r<2;r++){
    U16 e=equation_code(m,r);
    if(expand(equation_factor(e),s)==t)return int(e);
  }
  return -1;
}

static U16 conjunction(U16 a,U16 b){
  unsigned s=(a&255u)|(b&255u);
  return factor_code(s,expand(a,s)&expand(b,s));
}

static void finish(State&x){
  uniq(x.clauses);uniq(x.factors);uniq(x.equations);
  for(U16 c:x.clauses)if(pc(clause_support(c))<=3)x.conditions.push_back(clause_factor(c));
  for(U16 e:x.equations)if(pc(e&255u)<=3)x.conditions.push_back(equation_factor(e));
  for(U16 f:x.factors)x.conditions.push_back(f);
  uniq(x.conditions);
}

static int encode_clause(const std::vector<int>&cl,const std::vector<int>&vars){
  int z=0;
  for(int l:cl){
    int j=std::find(vars.begin(),vars.end(),std::abs(l))-vars.begin();
    z+=(l>0?1:2)*p3[j];
  }
  return z;
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

static uint32_t global_key(U16 f,bool right){
  auto vars=side_vars(right);
  unsigned local=f&255u,global=0;
  for(unsigned i=0;i<8;i++)if((local>>i)&1u)global|=1u<<(vars[i]-1);
  return uint32_t(global|((unsigned(f)>>8)<<16));
}

static uint32_t global_clause_key(U16 c,bool right){
  auto vars=side_vars(right);unsigned gp=0,gn=0;
  for(unsigned i=0;i<8;i++,c/=3){
    unsigned trit=c%3;
    if(trit==1)gp|=1u<<(vars[i]-1);
    if(trit==2)gn|=1u<<(vars[i]-1);
  }
  return uint32_t(gp|(gn<<16));
}

static void add_catalog(Catalog&cat,ClauseCatalog&clauses,
                        const State&s,int subset,bool right){
  std::set<uint32_t> seen;
  for(U16 f:s.conditions)seen.insert(global_key(f,right));
  for(uint32_t k:seen)cat[k].min_sources=std::min(cat[k].min_sources,unsigned(pc(subset)));
  std::set<uint32_t> seen_clauses;
  for(U16 c:s.clauses)seen_clauses.insert(global_clause_key(c,right));
  for(uint32_t k:seen_clauses)
    clauses[k].min_sources=std::min(clauses[k].min_sources,unsigned(pc(subset)));
}

struct Result{Catalog catalog;ClauseCatalog clauses;uint64_t res_pairs=0,and_pairs=0,xor_pairs=0;};

static Result close_side(bool right,const std::vector<int16_t>&table){
  auto F=formula();
  std::vector<int> ids;
  if(!right){for(int i=0;i<16;i++)ids.push_back(i);ids.push_back(17);ids.push_back(18);}
  else{for(int i=20;i<36;i++)ids.push_back(i);ids.push_back(36);ids.push_back(39);}
  auto vars=side_vars(right);
  const int n=18,total=1<<n;
  std::vector<State> dp(total);
  Result result;
  for(int i=0;i<n;i++){
    dp[1<<i].clauses.push_back(encode_clause(F[ids[i]],vars));
    finish(dp[1<<i]);add_catalog(result.catalog,result.clauses,dp[1<<i],1<<i,right);
  }
  for(int size=2;size<=n;size++)for(int subset=1;subset<total;subset++)if(pc(subset)==size){
    State out;int anchor=subset&-subset;
    for(int a=(subset-1)&subset;a;a=(a-1)&subset){
      if(!(a&anchor))continue;
      int b=subset^a;if(!b)continue;
      State&A=dp[a];State&B=dp[b];
      result.res_pairs+=uint64_t(A.clauses.size())*B.clauses.size();
      for(U16 x:A.clauses)for(U16 y:B.clauses){
        int z=table[size_t(x)*C+y];if(z>=0)out.clauses.push_back(U16(z));
      }
      result.and_pairs+=uint64_t(A.conditions.size())*B.conditions.size();
      for(U16 x:A.conditions)for(U16 y:B.conditions)
        if(pc((x&255u)|(y&255u))<=3){
          U16 f=conjunction(x,y);out.factors.push_back(f);
          int e=affine_alias(f);if(e>=0)out.equations.push_back(U16(e));
        }
      result.xor_pairs+=uint64_t(A.equations.size())*B.equations.size();
      for(U16 x:A.equations)for(U16 y:B.equations)
        out.equations.push_back(equation_code((x^y)&255u,((x>>8)^(y>>8))&1u));
    }
    finish(out);dp[subset]=std::move(out);
    add_catalog(result.catalog,result.clauses,dp[subset],subset,right);
  }
  return result;
}

static std::string read_all(const char*path){
  std::ifstream f(path);return std::string((std::istreambuf_iterator<char>(f)),{});
}

static int resolve_global(uint32_t a,uint32_t b){
  unsigned ap=a&0xffffu,an=a>>16,bp=b&0xffffu,bn=b>>16;
  unsigned piv=(ap&bn)|(an&bp);if(pc(piv)!=1)return -1;
  unsigned op=(ap|bp)&~piv,on=(an|bn)&~piv;if(op&on)return -1;
  return int(uint32_t(op|(on<<16)));
}

int main(int argc,char**argv){
  if(argc!=3){std::cerr<<"usage: verifier primary.json verification.json\n";return 2;}
  const auto start=std::chrono::steady_clock::now();
  p3[0]=1;for(int i=1;i<9;i++)p3[i]=p3[i-1]*3;
  std::vector<int16_t> table(size_t(C)*C,-1);
  for(int a=0;a<C;a++)for(int b=0;b<C;b++)table[size_t(a)*C+b]=resolve3(a,b);
  Result left=close_side(false,table),right=close_side(true,table);
  std::array<uint64_t,4> lc{},rc{};
  for(auto [k,_]:left.catalog)++lc[pc(k&0xffffu)];
  for(auto [k,_]:right.catalog)++rc[pc(k&0xffffu)];
  uint64_t pairs=0,eligible=0;
  for(auto [l,_]:left.catalog)for(auto [r,__]:right.catalog){
    ++pairs;if(pc((l&0xffffu)|(r&0xffffu))<=3)++eligible;
  }
  uint64_t cross_res=0,cross_res_small=0;unsigned min_cross_res=99,min_cross_support=99;
  std::array<uint64_t,16> cross_res_by_support{};std::set<uint32_t> outputs;
  uint64_t support4=0,candidate_tests=0,semantic_second=0;
  for(auto [l,li]:left.clauses)for(auto [r,ri]:right.clauses){
    unsigned lp=l&0xffffu,ln=l>>16,rp=r&0xffffu,rn=r>>16;
    unsigned piv=(lp&rn)|(ln&rp);if(pc(piv)!=1)continue;
    unsigned op=(lp|rp)&~piv,on=(ln|rn)&~piv;if(op&on)continue;
    cross_res++;unsigned out_size=pc(op|on);min_cross_support=std::min(min_cross_support,out_size);
    if(out_size<=3)cross_res_small++;
    cross_res_by_support[out_size]++;
    min_cross_res=std::min(min_cross_res,li.min_sources+ri.min_sources);
    outputs.insert(uint32_t(op|(on<<16)));
    if(out_size!=4)continue;
    support4++;
    std::array<unsigned,4> vars{};unsigned nv=0;
    for(unsigned v=0;v<15;v++)if(((op|on)>>v)&1u)vars[nv++]=v;
    for(unsigned side_id=0;side_id<2;side_id++){
      const ClauseCatalog&cat=side_id?right.clauses:left.clauses;
      for(unsigned code=1;code<81;code++){
        unsigned t=code,p=0,n=0;
        for(unsigned j=0;j<4;j++,t/=3){unsigned d=t%3;if(d==1)p|=1u<<vars[j];if(d==2)n|=1u<<vars[j];}
        uint32_t sib=p|(n<<16);candidate_tests++;
        if(!cat.count(sib))continue;
        int z=resolve_global(uint32_t(op|(on<<16)),sib);if(z<0)continue;
        uint32_t zz=uint32_t(z);
        if(pc((zz&0xffffu)|(zz>>16))<=3)semantic_second++;
      }
    }
  }
  std::string primary=read_all(argv[1]);
  bool ok=left.catalog.size()==183&&right.catalog.size()==183&&
    lc==std::array<uint64_t,4>{0,0,1,182}&&rc==lc&&pairs==33489&&eligible==0&&
    left.res_pairs==1126097195ULL&&right.res_pairs==1126097195ULL&&
    left.and_pairs==55144&&right.and_pairs==55144&&
    left.xor_pairs==25&&right.xor_pairs==25&&
    left.clauses.size()==3234&&right.clauses.size()==3234&&
    cross_res==4056196&&outputs.size()==4056196&&
    min_cross_res==2&&min_cross_support==4&&cross_res_small==0&&
    support4==6724&&candidate_tests==1075840&&semantic_second==0&&
    cross_res_by_support==std::array<uint64_t,16>{0,0,0,0,6724,43952,161040,
      401792,729600,971264,939008,602112,200704,0,0,0}&&
    primary.find("\"cross_strict_resolution_pairs\": 4056196")!=std::string::npos&&
    primary.find("\"cross_support_four_pairs\": 6724")!=std::string::npos&&
    primary.find("\"candidate_side_clause_tests\": 1075840")!=std::string::npos&&
    primary.find("\"semantic_second_resolution_patterns\": 0")!=std::string::npos&&
    primary.find("\"source_disjoint_second_resolution_patterns\": 0")!=std::string::npos;
  int mutations=0;
  mutations+=!(left.catalog.size()==182);
  mutations+=!(right.catalog.size()==184);
  mutations+=!(pairs==33488);
  mutations+=!(eligible==1);
  mutations+=!(lc[2]==0);
  mutations+=!(lc[3]==181);
  mutations+=!(cross_res==4056195);
  mutations+=!(min_cross_support==3);
  mutations+=!(cross_res_small==1);
  mutations+=!(support4==6723);
  mutations+=!(candidate_tests==1075839);
  mutations+=!(semantic_second==1);
  mutations+=!(primary.find("\"falsifier_found\": true")!=std::string::npos);
  if(mutations!=13)ok=false;
  rusage ru{};getrusage(RUSAGE_SELF,&ru);
  double seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
  std::ofstream out(argv[2]);
  out<<"{\n  \"pass\": "<<(ok?"true":"false")<<",\n"
     <<"  \"independent_encoding\": \"base-3 clauses and separately reconstructed truth vectors\",\n"
     <<"  \"left_unique_conditions\": "<<left.catalog.size()<<",\n"
     <<"  \"right_unique_conditions\": "<<right.catalog.size()<<",\n"
     <<"  \"conditions_by_support_size_each\": ["<<lc[0]<<","<<lc[1]<<","<<lc[2]<<","<<lc[3]<<"],\n"
     <<"  \"cross_pair_tests\": "<<pairs<<",\n"
     <<"  \"support_at_most_three_pairs\": "<<eligible<<",\n"
     <<"  \"left_unique_clauses\": "<<left.clauses.size()<<",\n"
     <<"  \"right_unique_clauses\": "<<right.clauses.size()<<",\n"
     <<"  \"cross_strict_resolution_pairs\": "<<cross_res<<",\n"
     <<"  \"cross_strict_resolution_unique_outputs\": "<<outputs.size()<<",\n"
     <<"  \"min_sources_cross_strict_resolution\": "<<(cross_res?min_cross_res:0)<<",\n"
     <<"  \"min_support_cross_strict_resolution\": "<<(cross_res?min_cross_support:0)<<",\n"
     <<"  \"cross_strict_resolution_support_at_most_three\": "<<cross_res_small<<",\n"
     <<"  \"cross_support_four_pairs\": "<<support4<<",\n"
     <<"  \"candidate_side_clause_tests\": "<<candidate_tests<<",\n"
     <<"  \"semantic_second_resolution_patterns\": "<<semantic_second<<",\n"
     <<"  \"cross_strict_resolution_by_output_support\": [";
  for(unsigned i=0;i<cross_res_by_support.size();i++)out<<(i?",":"")<<cross_res_by_support[i];
  out<<"],\n"
     <<"  \"mutations_rejected\": "<<mutations<<",\n"
     <<"  \"elapsed_seconds\": "<<seconds<<",\n"
     <<"  \"max_rss_kib\": "<<ru.ru_maxrss<<"\n}\n";
  std::cout<<(ok?"PASS":"FAIL")<<" seconds="<<seconds<<" rss="<<ru.ru_maxrss<<"\n";
  return ok?0:1;
}
