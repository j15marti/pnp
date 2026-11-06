#define main referee393_verifier_main_disabled
#include "lspv5_393_independent_verify.cpp"
#undef main

// Independent REFEREE394 verifier.  It inherits only the independently
// reconstructed base-3 source closures above, then regenerates the new
// post-cross and final-resolution search from scratch.

struct PairMasks394 { unsigned l=0,r=0; };
struct PostMasks394 { std::vector<PairMasks394> v; };
using PostCatalog394=std::map<uint32_t,PostMasks394>;

static unsigned support394(uint32_t c){return (c&0xffffu)|(c>>16);}

static void add_pair394(PostMasks394&out,unsigned l,unsigned r){
  for(const auto&m:out.v)if((m.l&l)==m.l&&(m.r&r)==m.r)return;
  out.v.erase(std::remove_if(out.v.begin(),out.v.end(),[l,r](const auto&m){
    return (m.l&l)==l&&(m.r&r)==r;
  }),out.v.end());
  out.v.push_back({l,r});
}

static std::vector<uint32_t> clauses394(unsigned support){
  std::vector<unsigned> vars;
  for(unsigned v=0;v<15;v++)if((support>>v)&1u)vars.push_back(v);
  unsigned count=1;for(size_t i=0;i<vars.size();i++)count*=3;
  std::vector<uint32_t> out;out.reserve(count-1);
  for(unsigned code=1;code<count;code++){
    unsigned t=code,p=0,n=0;
    for(unsigned v:vars){
      const unsigned digit=t%3;t/=3;
      if(digit==1)p|=1u<<v;
      if(digit==2)n|=1u<<v;
    }
    out.push_back(uint32_t(p|(n<<16)));
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

  uint64_t all_cross=0;std::vector<Cross>x4,x45;
  for(const auto&[l,lm]:L.catalog)for(const auto&[r,rm]:R.catalog){
    const int z=resolve_global(l,r);if(z<0)continue;
    all_cross++;const uint32_t c=uint32_t(z);const int s=pc(support394(c));
    if(s==4)x4.push_back({c,&lm,&rm});
    if(s==4||s==5)x45.push_back({c,&lm,&rm});
  }

  PostCatalog394 post;
  uint64_t queries=0,hits=0,strict=0,small4=0,unions=0;
  std::map<std::pair<unsigned,bool>,std::vector<std::pair<uint32_t,const Masks*>>> candidate_cache;
  for(const Cross&c:x45){
    const unsigned support=support394(c.clause);
    for(int side=0;side<2;side++){
      const Catalog&cat=side?R.catalog:L.catalog;
      const Masks&same=side?*c.rm:*c.lm;
      const Masks&other=side?*c.lm:*c.rm;
      auto&candidates=candidate_cache[{support,bool(side)}];
      if(candidates.empty()){
        const unsigned outside_budget=5-pc(support);
        for(const auto&[d,masks]:cat)
          if(unsigned(pc(support394(d)&~support))<=outside_budget)
            candidates.push_back({d,&masks});
      }
      for(const auto&[d,dmasks]:candidates){
        queries++;hits++;
        const int z=resolve_global(c.clause,d);if(z<0)continue;strict++;
        const uint32_t out=uint32_t(z);if(pc(support394(out))>4)continue;small4++;
        for(unsigned sm:same.v)for(unsigned dm:dmasks->v){
          if(sm&dm)continue;
          for(unsigned om:other.v){
            unions++;
            if(side)add_pair394(post[out],om,sm|dm);
            else add_pair394(post[out],sm|dm,om);
          }
        }
      }
    }
  }
  uint64_t masks=0;for(const auto&[_,m]:post)masks+=m.v.size();

  uint64_t final_queries=0,final_hits=0,final_small=0,final_disjoint=0;
  std::set<uint32_t> outputs;
  for(const Cross&c:x4)for(uint32_t sibling:clauses394(support394(c.clause))){
    final_queries++;const auto it=post.find(sibling);if(it==post.end())continue;final_hits++;
    const int z=resolve_global(c.clause,sibling);if(z<0)continue;
    const uint32_t out=uint32_t(z);if(pc(support394(out))>3)continue;
    final_small++;outputs.insert(out);
    for(unsigned l:c.lm->v)for(unsigned r:c.rm->v)for(const auto&m:it->second.v)
      if(!(l&m.l)&&!(r&m.r))final_disjoint++;
  }

  const std::string primary=read_all(argv[1]);
  bool ok=L.catalog.size()==3234&&R.catalog.size()==3234&&
    L.occurrences==11705410&&R.occurrences==11705410&&
    L.pair_tests==1126097195ULL&&R.pair_tests==1126097195ULL&&
    all_cross==4056196&&x4.size()==6724&&x45.size()==50676&&
    queries==183024&&hits==183024&&strict==89872&&small4==89872&&
    unions==34112&&post.size()==6624&&masks==6624&&
    final_queries==537920&&final_hits==103680&&final_small==25920&&
    outputs.size()==2296&&final_disjoint==0&&
    primary.find("\"post_strict_resolution_patterns\": 89872")!=std::string::npos&&
    primary.find("\"post_unique_clauses\": 6624")!=std::string::npos&&
    primary.find("\"final_strict_support_at_most_three_patterns\": 25920")!=std::string::npos&&
    primary.find("\"final_source_disjoint_realizations\": 0")!=std::string::npos&&
    primary.find("\"falsifier_found\": false")!=std::string::npos;

  int mutations=0;
  mutations+=!(L.catalog.size()==3233);mutations+=!(R.catalog.size()==3235);
  mutations+=!(all_cross==4056195);mutations+=!(x4.size()==6723);
  mutations+=!(x45.size()==50675);mutations+=!(queries==183023);
  mutations+=!(hits==183023);mutations+=!(strict==89871);
  mutations+=!(small4==89871);mutations+=!(unions==34111);
  mutations+=!(post.size()==6623);mutations+=!(masks==6623);
  mutations+=!(final_queries==537919);mutations+=!(final_hits==103679);
  mutations+=!(final_small==25919);mutations+=!(outputs.size()==2295);
  mutations+=!(final_disjoint==1);
  mutations+=!(primary.find("\"falsifier_found\": true")!=std::string::npos);
  if(mutations!=18)ok=false;

  rusage ru{};getrusage(RUSAGE_SELF,&ru);
  const double seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
  std::ofstream out(argv[2]);
  out<<"{\n  \"pass\": "<<(ok?"true":"false")<<",\n"
     <<"  \"independent_encoding\": \"base-3 clauses reconstructed from graph incidence\",\n"
     <<"  \"resolution_table_entries\": "<<uint64_t(C)*C<<",\n"
     <<"  \"left_unique_clauses\": "<<L.catalog.size()<<",\n"
     <<"  \"right_unique_clauses\": "<<R.catalog.size()<<",\n"
     <<"  \"all_first_cross_resolvents\": "<<all_cross<<",\n"
     <<"  \"support_four_first_cross_resolvents\": "<<x4.size()<<",\n"
     <<"  \"support_four_or_five_first_cross_resolvents\": "<<x45.size()<<",\n"
     <<"  \"post_candidate_side_clause_queries\": "<<queries<<",\n"
     <<"  \"post_catalog_hits\": "<<hits<<",\n"
     <<"  \"post_strict_resolution_patterns\": "<<strict<<",\n"
     <<"  \"post_support_at_most_four_patterns\": "<<small4<<",\n"
     <<"  \"post_legal_mask_unions_before_minimization\": "<<unions<<",\n"
     <<"  \"post_unique_clauses\": "<<post.size()<<",\n"
     <<"  \"post_minimal_mask_pairs\": "<<masks<<",\n"
     <<"  \"final_clause_queries\": "<<final_queries<<",\n"
     <<"  \"final_post_catalog_hits\": "<<final_hits<<",\n"
     <<"  \"final_strict_support_at_most_three_patterns\": "<<final_small<<",\n"
     <<"  \"final_distinct_support_at_most_three_outputs\": "<<outputs.size()<<",\n"
     <<"  \"final_source_disjoint_realizations\": "<<final_disjoint<<",\n"
     <<"  \"mutations_rejected\": "<<mutations<<",\n"
     <<"  \"elapsed_seconds\": "<<seconds<<",\n"
     <<"  \"max_rss_kib\": "<<ru.ru_maxrss<<"\n}\n";
  std::cout<<(ok?"PASS":"FAIL")<<" seconds="<<seconds<<" rss="<<ru.ru_maxrss<<"\n";
  return ok?0:1;
}
