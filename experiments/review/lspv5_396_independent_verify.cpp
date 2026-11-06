#define main referee393_verifier_main_disabled
#include "lspv5_393_independent_verify.cpp"
#undef main
#include <functional>

struct PairV396{unsigned l=0,r=0;};
struct InfoV396{std::vector<PairV396> v;};
using CatV396=std::map<uint32_t,InfoV396>;
static unsigned supV396(uint32_t c){return (c&0xffffu)|(c>>16);}
static void addV396(InfoV396&x,unsigned l,unsigned r){
  for(const auto&m:x.v)if((m.l&l)==m.l&&(m.r&r)==m.r)return;
  x.v.erase(std::remove_if(x.v.begin(),x.v.end(),[l,r](const PairV396&m){return(m.l&l)==l&&(m.r&r)==r;}),x.v.end());
  x.v.push_back({l,r});
}
static uint64_t nV396(const CatV396&c){uint64_t z=0;for(const auto&[_,x]:c)z+=x.v.size();return z;}
struct StepV396{uint64_t states=0,queries=0,strict=0,unions=0;};
static CatV396 extendV396(const CatV396&in,const SideResult&L,const SideResult&R,StepV396&ct){
  CatV396 out;std::map<std::pair<unsigned,bool>,std::vector<std::pair<uint32_t,const Masks*>>> cache;
  for(const auto&[a,ai]:in){unsigned sup=supV396(a),s=pc(sup);
    for(const auto&am:ai.v){ct.states++;for(int side=0;side<2;side++){
      const Catalog&local=side?R.catalog:L.catalog;auto key=std::make_pair(sup,bool(side));auto it=cache.find(key);
      if(it==cache.end()){
        std::vector<std::pair<uint32_t,const Masks*>> v;unsigned budget=6-s;
        for(const auto&[d,di]:local)if(unsigned(pc(supV396(d)&~sup))<=budget)v.push_back({d,&di});
        it=cache.emplace(key,std::move(v)).first;
      }
      for(const auto&[d,di]:it->second){ct.queries++;int z=resolve_global(a,d);if(z<0)continue;
        uint32_t b=uint32_t(z);if(pc(supV396(b))>5)continue;ct.strict++;
        unsigned used=side?am.r:am.l;for(unsigned dm:di->v)if(!(used&dm)){ct.unions++;
          if(side)addV396(out[b],am.l,am.r|dm);else addV396(out[b],am.l|dm,am.r);
        }
      }
    }}
  }return out;
}
static std::vector<uint32_t> qV396(){
  std::vector<uint32_t> out{0};
  std::function<void(unsigned,unsigned,unsigned)> rec=[&](unsigned next,unsigned need,unsigned mask){
    if(!need){std::vector<unsigned> vars;for(unsigned v=0;v<15;v++)if((mask>>v)&1u)vars.push_back(v);
      for(unsigned signs=0;signs<(1u<<vars.size());signs++){
        unsigned p=0,n=0;for(size_t i=0;i<vars.size();i++)((signs>>i)&1u?n:p)|=1u<<vars[i];
        out.push_back(uint32_t(p|(n<<16)));
      }return;
    }
    for(unsigned v=next;v+need<=15;v++)rec(v+1,need-1,mask|(1u<<v));
  };
  for(unsigned k=1;k<=4;k++)rec(0,k,0);return out;
}

int main(int argc,char**argv){
  if(argc!=3){std::cerr<<"usage: verify primary.json verify.json\n";return 2;}
  auto start=std::chrono::steady_clock::now();p3[0]=1;for(int i=1;i<9;i++)p3[i]=p3[i-1]*3;
  std::vector<int16_t> table(size_t(C)*C,-1);for(int a=0;a<C;a++)for(int b=0;b<C;b++)table[size_t(a)*C+b]=resolve3(a,b);
  SideResult L=close_side(false,table),R=close_side(true,table);
  uint64_t all=0,x4p=0,x456p=0;CatV396 x4,x456;
  for(const auto&[l,lm]:L.catalog)for(const auto&[r,rm]:R.catalog){int z=resolve_global(l,r);if(z<0)continue;all++;
    uint32_t c=uint32_t(z);unsigned s=pc(supV396(c));if(s<4||s>6)continue;x456p++;if(s==4)x4p++;
    for(unsigned a:lm.v)for(unsigned b:rm.v){addV396(x456[c],a,b);if(s==4)addV396(x4[c],a,b);}
  }
  StepV396 st;CatV396 post=extendV396(x456,L,R,st),branch;
  uint64_t qs=0,templ=0,hits=0,semantic=0,unions=0;
  for(uint32_t q:qV396()){qs++;unsigned sup=supV396(q);std::vector<std::pair<unsigned,bool>> lits;
    for(unsigned v=0;v<15;v++)if((sup>>v)&1u)lits.push_back({v,((q>>v)&1u)!=0});
    unsigned pow3=1;for(size_t i=0;i<lits.size();i++)pow3*=3;
    for(unsigned pivot=0;pivot<15;pivot++)if(!((sup>>pivot)&1u))for(unsigned code=0;code<pow3;code++){
      templ++;unsigned t=code,ap=1u<<pivot,an=0,bp=0,bn=1u<<pivot;
      for(const auto&[v,pos]:lits){unsigned d=t%3;t/=3;if(d!=1)(pos?ap:an)|=1u<<v;if(d!=0)(pos?bp:bn)|=1u<<v;}
      uint32_t a=uint32_t(ap|(an<<16)),b=uint32_t(bp|(bn<<16));auto ia=post.find(a),ib=post.find(b);
      if(ia==post.end()||ib==post.end())continue;hits++;int z=resolve_global(a,b);if(z<0||uint32_t(z)!=q)continue;semantic++;
      for(const auto&am:ia->second.v)for(const auto&bm:ib->second.v)if(!(am.l&bm.l)&&!(am.r&bm.r)){
        unions++;addV396(branch[q],am.l|bm.l,am.r|bm.r);
      }
    }
  }
  std::string primary=read_all(argv[1]);
  std::vector<std::pair<std::string,uint64_t>> fields={
    {"all_first_cross_resolvents",all},{"support_four_first_cross_patterns",x4p},
    {"support_four_to_six_first_cross_patterns",x456p},{"support_four_to_six_cross_minimal_mask_pairs",nV396(x456)},
    {"post_input_mask_states",st.states},{"post_candidate_queries",st.queries},{"post_strict_patterns",st.strict},
    {"post_legal_mask_unions",st.unions},{"post_unique_clauses",post.size()},{"post_minimal_mask_pairs",nV396(post)},
    {"enumerated_support_at_most_four_outputs",qs},{"branch_resolvent_templates",templ},
    {"branch_templates_with_both_parents",hits},{"branch_semantic_pairs",semantic},
    {"branch_legal_mask_unions",unions},{"branch_unique_clauses",branch.size()},{"branch_minimal_mask_pairs",nV396(branch)}};
  bool ok=L.catalog.size()==3234&&R.catalog.size()==3234&&L.pair_tests==1126097195ULL&&R.pair_tests==1126097195ULL;
  for(const auto&[n,v]:fields)if(primary.find("\""+n+"\": "+std::to_string(v))==std::string::npos)ok=false;
  ok=ok&&unions==0&&branch.empty()&&primary.find("\"falsifier_found\": false")!=std::string::npos;
  int mutations=0;for(const auto&[n,v]:fields)mutations+=primary.find("\""+n+"\": "+std::to_string(v+1))==std::string::npos;
  mutations+=primary.find("\"falsifier_found\": true")==std::string::npos;if(mutations!=int(fields.size()+1))ok=false;
  rusage ru{};getrusage(RUSAGE_SELF,&ru);double sec=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
  std::ofstream o(argv[2]);o<<"{\n  \"pass\": "<<(ok?"true":"false")<<",\n"
   <<"  \"independent_encoding\": \"graph incidence plus base-3 local clauses\",\n"
   <<"  \"resolution_table_entries\": "<<uint64_t(C)*C<<",\n"
   <<"  \"all_first_cross_resolvents\": "<<all<<",\n  \"support_four_to_six_first_cross_patterns\": "<<x456p<<",\n"
   <<"  \"post_candidate_queries\": "<<st.queries<<",\n  \"post_unique_clauses\": "<<post.size()<<",\n"
   <<"  \"branch_resolvent_templates\": "<<templ<<",\n  \"branch_templates_with_both_parents\": "<<hits<<",\n"
   <<"  \"branch_semantic_pairs\": "<<semantic<<",\n  \"branch_legal_mask_unions\": "<<unions<<",\n"
   <<"  \"branch_unique_clauses\": "<<branch.size()<<",\n  \"mutations_rejected\": "<<mutations<<",\n"
   <<"  \"elapsed_seconds\": "<<sec<<",\n  \"max_rss_kib\": "<<ru.ru_maxrss<<"\n}\n";
  std::cout<<(ok?"PASS":"FAIL")<<" seconds="<<sec<<" rss="<<ru.ru_maxrss<<"\n";return ok?0:1;
}
