#define main referee393_main_disabled
#include "lspv5_393_double_cross_resolution.cpp"
#undef main
#include <functional>

// REFEREE396: exact source-authenticated test for
// RES(C0, RES(P1,P2)), P_i=RES(C_i,D_i), where every C is a first
// cross-cut resolvent and every D is side-local.  This is the first branched
// post-cross sibling topology after the linear exclusions 394--395.

struct Pair396{unsigned l=0,r=0;};
struct Info396{std::vector<Pair396> masks;};
using Cat396=std::map<uint32_t,Info396>;

static unsigned support396(uint32_t c){return (c&0xffffu)|(c>>16);}
static void add396(Info396&x,unsigned l,unsigned r){
  for(const auto&m:x.masks)if((m.l&l)==m.l&&(m.r&r)==m.r)return;
  x.masks.erase(std::remove_if(x.masks.begin(),x.masks.end(),[l,r](const Pair396&m){
    return (m.l&l)==l&&(m.r&r)==r;
  }),x.masks.end());x.masks.push_back({l,r});
}
static uint64_t nmasks396(const Cat396&c){uint64_t z=0;for(const auto&[_,i]:c)z+=i.masks.size();return z;}

struct Step396{uint64_t states=0,queries=0,strict=0,small=0,unions=0;};
static Cat396 extend396(const Cat396&in,unsigned ceiling,const SideClosure&L,const SideClosure&R,Step396&ct){
  Cat396 out;
  std::map<std::pair<unsigned,bool>,std::vector<std::pair<uint32_t,const MaskInfo*>>> cache;
  for(const auto&[a,ai]:in){const unsigned sup=support396(a),s=pc(sup);
    for(const auto&am:ai.masks){ct.states++;
      for(int side=0;side<2;side++){
        const Catalog&local=side?R.catalog:L.catalog;
        const auto key=std::make_pair(sup,bool(side));auto it=cache.find(key);
        if(it==cache.end()){
          std::vector<std::pair<uint32_t,const MaskInfo*>> v;
          const unsigned budget=ceiling+1-s;
          for(const auto&[d,di]:local)if(unsigned(pc(support396(d)&~sup))<=budget)v.push_back({d,&di});
          it=cache.emplace(key,std::move(v)).first;
        }
        for(const auto&[d,di]:it->second){ct.queries++;
          const int z=strict_resolve_global(a,d);if(z<0)continue;ct.strict++;
          const uint32_t b=uint32_t(z);if(unsigned(pc(support396(b)))>ceiling)continue;ct.small++;
          const unsigned used=side?am.r:am.l;
          for(unsigned dm:di->minimal_masks){if(used&dm)continue;ct.unions++;
            if(side)add396(out[b],am.l,am.r|dm);else add396(out[b],am.l|dm,am.r);
          }
        }
      }
    }
  }
  return out;
}

static std::vector<uint32_t> all_exact_clauses396(unsigned max_support){
  std::vector<uint32_t> out;
  std::function<void(unsigned,unsigned,unsigned)> rec=[&](unsigned next,unsigned need,unsigned mask){
    if(!need){
      std::vector<unsigned> vars;for(unsigned v=0;v<15;v++)if((mask>>v)&1u)vars.push_back(v);
      const unsigned lim=1u<<vars.size();
      for(unsigned signs=0;signs<lim;signs++){
        unsigned p=0,n=0;for(size_t i=0;i<vars.size();i++)((signs>>i)&1u?n:p)|=1u<<vars[i];
        out.push_back(uint32_t(p|(n<<16)));
      }
      return;
    }
    for(unsigned v=next;v+need<=15;v++)rec(v+1,need-1,mask|(1u<<v));
  };
  out.push_back(0);
  for(unsigned k=1;k<=max_support;k++)rec(0,k,0);
  return out;
}

static std::vector<uint32_t> clauses_on_support396(unsigned support){
  std::vector<unsigned> vars;for(unsigned v=0;v<15;v++)if((support>>v)&1u)vars.push_back(v);
  unsigned lim=1;for(size_t i=0;i<vars.size();i++)lim*=3;
  std::vector<uint32_t> out;out.reserve(lim-1);
  for(unsigned code=1;code<lim;code++){
    unsigned t=code,p=0,n=0;for(unsigned v:vars){unsigned d=t%3;t/=3;if(d==1)p|=1u<<v;if(d==2)n|=1u<<v;}
    out.push_back(uint32_t(p|(n<<16)));
  }return out;
}

struct Witness396{bool exists=false;uint32_t c0=0,q=0,out=0;unsigned a=0,b=0,c=0,d=0,total=999;};

int main(){
  const auto start=std::chrono::steady_clock::now();
  SideClosure L=close_side(false),R=close_side(true);
  uint64_t allcross=0,x4patterns=0,x456patterns=0;Cat396 x4,x456;
  for(const auto&[l,li]:L.catalog)for(const auto&[r,ri]:R.catalog){
    const int z=strict_resolve_global(l,r);if(z<0)continue;allcross++;
    const uint32_t c=uint32_t(z);const unsigned s=pc(support396(c));if(s<4||s>6)continue;
    x456patterns++;if(s==4)x4patterns++;
    for(unsigned lm:li.minimal_masks)for(unsigned rm:ri.minimal_masks){add396(x456[c],lm,rm);if(s==4)add396(x4[c],lm,rm);}
  }

  Step396 ext;Cat396 post=extend396(x456,5,L,R,ext);
  Cat396 branch;
  uint64_t q_clauses=0,templates=0,parent_hits=0,semantic_pairs=0,legal_unions=0;
  for(uint32_t q:all_exact_clauses396(4)){
    q_clauses++;const unsigned sup=support396(q);
    std::vector<std::pair<unsigned,bool>> lits;
    for(unsigned v=0;v<15;v++)if((sup>>v)&1u)lits.push_back({v,((q>>v)&1u)!=0});
    unsigned pow3=1;for(size_t i=0;i<lits.size();i++)pow3*=3;
    for(unsigned pivot=0;pivot<15;pivot++)if(!((sup>>pivot)&1u)){
      for(unsigned code=0;code<pow3;code++){
        templates++;unsigned t=code,ap=1u<<pivot,an=0,bp=0,bn=1u<<pivot;
        for(const auto&[v,pos]:lits){const unsigned d=t%3;t/=3;
          if(d!=1)(pos?ap:an)|=1u<<v;
          if(d!=0)(pos?bp:bn)|=1u<<v;
        }
        const uint32_t a=uint32_t(ap|(an<<16)),b=uint32_t(bp|(bn<<16));
        auto ia=post.find(a),ib=post.find(b);if(ia==post.end()||ib==post.end())continue;parent_hits++;
        const int z=strict_resolve_global(a,b);if(z<0||uint32_t(z)!=q)continue;semantic_pairs++;
        for(const auto&am:ia->second.masks)for(const auto&bm:ib->second.masks){
          if((am.l&bm.l)||(am.r&bm.r))continue;legal_unions++;add396(branch[q],am.l|bm.l,am.r|bm.r);
        }
      }
    }
  }

  uint64_t fq=0,fh=0,fs=0,fd=0;std::set<uint32_t>outputs;Witness396 best;
  for(const auto&[c0,ci]:x4)for(uint32_t q:clauses_on_support396(support396(c0))){
    fq++;auto it=branch.find(q);if(it==branch.end())continue;fh++;
    const int z=strict_resolve_global(c0,q);if(z<0)continue;const uint32_t o=uint32_t(z);
    if(pc(support396(o))>3)continue;fs++;outputs.insert(o);
    for(const auto&cm:ci.masks)for(const auto&qm:it->second.masks){
      if((cm.l&qm.l)||(cm.r&qm.r))continue;fd++;
      const unsigned total=pc(cm.l)+pc(cm.r)+pc(qm.l)+pc(qm.r);
      if(!best.exists||total<best.total)best={true,c0,q,o,cm.l,cm.r,qm.l,qm.r,total};
    }
  }

  rusage ru{};getrusage(RUSAGE_SELF,&ru);
  const double seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
  std::cout<<"{\n  \"run\": \"LSPV-5/REFEREE396 branched-post-cross test\",\n"
    <<"  \"status\": \"COMPUTATIONAL_EXACT_FINITE\",\n"
    <<"  \"scope\": \"RES(C0,RES(P1,P2)), Pi=RES(Ci,Di); C first-cross, D side-local\",\n"
    <<"  \"left_unique_clauses\": "<<L.catalog.size()<<",\n  \"right_unique_clauses\": "<<R.catalog.size()<<",\n"
    <<"  \"all_first_cross_resolvents\": "<<allcross<<",\n"
    <<"  \"support_four_first_cross_patterns\": "<<x4patterns<<",\n"
    <<"  \"support_four_to_six_first_cross_patterns\": "<<x456patterns<<",\n"
    <<"  \"support_four_to_six_cross_minimal_mask_pairs\": "<<nmasks396(x456)<<",\n"
    <<"  \"post_input_mask_states\": "<<ext.states<<",\n  \"post_candidate_queries\": "<<ext.queries<<",\n"
    <<"  \"post_strict_patterns\": "<<ext.strict<<",\n  \"post_legal_mask_unions\": "<<ext.unions<<",\n"
    <<"  \"post_unique_clauses\": "<<post.size()<<",\n  \"post_minimal_mask_pairs\": "<<nmasks396(post)<<",\n"
    <<"  \"enumerated_support_at_most_four_outputs\": "<<q_clauses<<",\n"
    <<"  \"branch_resolvent_templates\": "<<templates<<",\n"
    <<"  \"branch_templates_with_both_parents\": "<<parent_hits<<",\n"
    <<"  \"branch_semantic_pairs\": "<<semantic_pairs<<",\n"
    <<"  \"branch_legal_mask_unions\": "<<legal_unions<<",\n"
    <<"  \"branch_unique_clauses\": "<<branch.size()<<",\n"
    <<"  \"branch_minimal_mask_pairs\": "<<nmasks396(branch)<<",\n"
    <<"  \"final_clause_queries\": "<<fq<<",\n  \"final_branch_catalog_hits\": "<<fh<<",\n"
    <<"  \"final_strict_support_at_most_three_patterns\": "<<fs<<",\n"
    <<"  \"final_distinct_support_at_most_three_outputs\": "<<outputs.size()<<",\n"
    <<"  \"final_source_disjoint_realizations\": "<<fd<<",\n"
    <<"  \"falsifier_found\": "<<(best.exists?"true":"false")<<",\n"
    <<"  \"best_total_source_leaves\": "<<(best.exists?best.total:0)<<",\n"
    <<"  \"wall_seconds\": "<<std::fixed<<std::setprecision(6)<<seconds<<",\n"
    <<"  \"max_rss_kib\": "<<ru.ru_maxrss<<"\n}\n";
}
