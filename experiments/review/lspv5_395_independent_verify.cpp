#define main referee393_verifier_main_disabled
#include "lspv5_393_independent_verify.cpp"
#undef main

// Independent REFEREE395 verifier.  The source formula, local clauses, and
// Resolution table are rebuilt using the verifier's base-3 representation.

struct PairV395{unsigned l=0,r=0;};
struct InfoV395{std::vector<PairV395> v;};
using CatV395=std::map<uint32_t,InfoV395>;

static unsigned supportV395(uint32_t c){return (c&0xffffu)|(c>>16);}
static void addV395(InfoV395&x,unsigned l,unsigned r){
  for(const auto&m:x.v)if((m.l&l)==m.l&&(m.r&r)==m.r)return;
  x.v.erase(std::remove_if(x.v.begin(),x.v.end(),[l,r](const PairV395&m){
    return (m.l&l)==l&&(m.r&r)==r;
  }),x.v.end());x.v.push_back({l,r});
}
static uint64_t nmaskV395(const CatV395&c){uint64_t z=0;for(const auto&[_,i]:c)z+=i.v.size();return z;}

struct CountsV395{uint64_t states=0,queries=0,strict=0,small=0,unions=0;};
static CatV395 extendV395(const CatV395&in,unsigned ceiling,
                         const SideResult&L,const SideResult&R,CountsV395&ct){
  CatV395 out;
  std::map<std::pair<unsigned,bool>,std::vector<std::pair<uint32_t,const Masks*>>> cache;
  for(const auto&[a,ai]:in){
    const unsigned sup=supportV395(a),s=pc(sup);
    for(const auto&am:ai.v){ct.states++;
      for(int side=0;side<2;side++){
        const Catalog&local=side?R.catalog:L.catalog;
        auto key=std::make_pair(sup,bool(side));auto it=cache.find(key);
        if(it==cache.end()){
          std::vector<std::pair<uint32_t,const Masks*>> v;
          const unsigned budget=ceiling+1-s;
          for(const auto&[d,di]:local)
            if(unsigned(pc(supportV395(d)&~sup))<=budget)v.push_back({d,&di});
          it=cache.emplace(key,std::move(v)).first;
        }
        for(const auto&[d,di]:it->second){ct.queries++;
          const int z=resolve_global(a,d);if(z<0)continue;ct.strict++;
          const uint32_t b=uint32_t(z);if(unsigned(pc(supportV395(b)))>ceiling)continue;ct.small++;
          const unsigned used=side?am.r:am.l;
          for(unsigned dm:di->v){if(used&dm)continue;ct.unions++;
            if(side)addV395(out[b],am.l,am.r|dm);else addV395(out[b],am.l|dm,am.r);
          }
        }
      }
    }
  }
  return out;
}

static std::vector<uint32_t> clausesV395(unsigned support){
  std::vector<unsigned> vars;for(unsigned v=0;v<15;v++)if((support>>v)&1u)vars.push_back(v);
  unsigned n=1;for(size_t i=0;i<vars.size();i++)n*=3;
  std::vector<uint32_t> out;out.reserve(n-1);
  for(unsigned code=1;code<n;code++){
    unsigned t=code,p=0,q=0;
    for(unsigned v:vars){unsigned d=t%3;t/=3;if(d==1)p|=1u<<v;if(d==2)q|=1u<<v;}
    out.push_back(uint32_t(p|(q<<16)));
  }
  return out;
}

int main(int argc,char**argv){
  if(argc!=3){std::cerr<<"usage: verifier primary.json verification.json\n";return 2;}
  const auto start=std::chrono::steady_clock::now();
  p3[0]=1;for(int i=1;i<9;i++)p3[i]=p3[i-1]*3;
  std::vector<int16_t> table(size_t(C)*C,-1);
  for(int a=0;a<C;a++)for(int b=0;b<C;b++)table[size_t(a)*C+b]=resolve3(a,b);
  SideResult L=close_side(false,table),R=close_side(true,table);

  uint64_t all=0,x4patterns=0,x456patterns=0;CatV395 x4,x456;
  for(const auto&[l,lm]:L.catalog)for(const auto&[r,rm]:R.catalog){
    const int z=resolve_global(l,r);if(z<0)continue;all++;
    const uint32_t c=uint32_t(z);const unsigned s=pc(supportV395(c));if(s<4||s>6)continue;
    x456patterns++;if(s==4)x4patterns++;
    for(unsigned a:lm.v)for(unsigned b:rm.v){addV395(x456[c],a,b);if(s==4)addV395(x4[c],a,b);}
  }
  CountsV395 a,b;CatV395 p1=extendV395(x456,5,L,R,a),p2=extendV395(p1,4,L,R,b);

  uint64_t fq=0,fh=0,fs=0,fd=0;std::set<uint32_t>outputs;
  for(const auto&[c,ci]:x4)for(uint32_t d:clausesV395(supportV395(c))){
    fq++;auto it=p2.find(d);if(it==p2.end())continue;fh++;
    const int z=resolve_global(c,d);if(z<0)continue;
    const uint32_t o=uint32_t(z);if(pc(supportV395(o))>3)continue;fs++;outputs.insert(o);
    for(const auto&cm:ci.v)for(const auto&dm:it->second.v)
      if(!(cm.l&dm.l)&&!(cm.r&dm.r))fd++;
  }

  const std::string primary=read_all(argv[1]);
  bool ok=L.catalog.size()==3234&&R.catalog.size()==3234&&
    L.occurrences==11705410&&R.occurrences==11705410&&
    L.pair_tests==1126097195ULL&&R.pair_tests==1126097195ULL&&
    primary.find("\"falsifier_found\": false")!=std::string::npos&&
    primary.find("\"final_source_disjoint_realizations\": 0")!=std::string::npos;
  // Cross-check every newly generated count against the producer text.
  const std::vector<std::pair<std::string,uint64_t>> fields={
    {"all_first_cross_resolvents",all},{"support_four_first_cross_patterns",x4patterns},
    {"support_four_to_six_first_cross_patterns",x456patterns},{"support_four_unique_cross_clauses",x4.size()},
    {"support_four_cross_minimal_mask_pairs",nmaskV395(x4)},
    {"support_four_to_six_unique_cross_clauses",x456.size()},
    {"support_four_to_six_cross_minimal_mask_pairs",nmaskV395(x456)},
    {"post1_input_mask_states",a.states},{"post1_candidate_queries",a.queries},
    {"post1_strict_patterns",a.strict},{"post1_support_at_most_five_patterns",a.small},
    {"post1_legal_mask_unions",a.unions},{"post1_unique_clauses",p1.size()},
    {"post1_minimal_mask_pairs",nmaskV395(p1)},{"post2_input_mask_states",b.states},
    {"post2_candidate_queries",b.queries},{"post2_strict_patterns",b.strict},
    {"post2_support_at_most_four_patterns",b.small},{"post2_legal_mask_unions",b.unions},
    {"post2_unique_clauses",p2.size()},{"post2_minimal_mask_pairs",nmaskV395(p2)},
    {"final_clause_queries",fq},{"final_post2_catalog_hits",fh},
    {"final_strict_support_at_most_three_patterns",fs},
    {"final_distinct_support_at_most_three_outputs",outputs.size()},
    {"final_source_disjoint_realizations",fd}};
  for(const auto&[name,value]:fields)
    if(primary.find("\""+name+"\": "+std::to_string(value))==std::string::npos)ok=false;

  int mutations=0;
  for(const auto&[name,value]:fields)
    mutations+=primary.find("\""+name+"\": "+std::to_string(value+1))==std::string::npos;
  mutations+=primary.find("\"falsifier_found\": true")==std::string::npos;
  if(mutations!=int(fields.size()+1))ok=false;

  rusage ru{};getrusage(RUSAGE_SELF,&ru);
  const double seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
  std::ofstream out(argv[2]);
  out<<"{\n  \"pass\": "<<(ok?"true":"false")<<",\n"
     <<"  \"independent_encoding\": \"base-3 clauses and graph-incidence source reconstruction\",\n"
     <<"  \"resolution_table_entries\": "<<uint64_t(C)*C<<",\n"
     <<"  \"all_first_cross_resolvents\": "<<all<<",\n"
     <<"  \"support_four_first_cross_patterns\": "<<x4patterns<<",\n"
     <<"  \"support_four_to_six_first_cross_patterns\": "<<x456patterns<<",\n"
     <<"  \"support_four_to_six_unique_cross_clauses\": "<<x456.size()<<",\n"
     <<"  \"support_four_to_six_cross_minimal_mask_pairs\": "<<nmaskV395(x456)<<",\n"
     <<"  \"post1_candidate_queries\": "<<a.queries<<",\n"
     <<"  \"post1_strict_patterns\": "<<a.strict<<",\n"
     <<"  \"post1_unique_clauses\": "<<p1.size()<<",\n"
     <<"  \"post1_minimal_mask_pairs\": "<<nmaskV395(p1)<<",\n"
     <<"  \"post2_candidate_queries\": "<<b.queries<<",\n"
     <<"  \"post2_strict_patterns\": "<<b.strict<<",\n"
     <<"  \"post2_unique_clauses\": "<<p2.size()<<",\n"
     <<"  \"post2_minimal_mask_pairs\": "<<nmaskV395(p2)<<",\n"
     <<"  \"final_strict_support_at_most_three_patterns\": "<<fs<<",\n"
     <<"  \"final_distinct_support_at_most_three_outputs\": "<<outputs.size()<<",\n"
     <<"  \"final_source_disjoint_realizations\": "<<fd<<",\n"
     <<"  \"mutations_rejected\": "<<mutations<<",\n"
     <<"  \"elapsed_seconds\": "<<seconds<<",\n"
     <<"  \"max_rss_kib\": "<<ru.ru_maxrss<<"\n}\n";
  std::cout<<(ok?"PASS":"FAIL")<<" seconds="<<seconds<<" rss="<<ru.ru_maxrss<<"\n";
  return ok?0:1;
}
