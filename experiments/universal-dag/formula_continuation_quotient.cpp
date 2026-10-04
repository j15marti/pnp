#include <bits/stdc++.h>
using namespace std;

struct Constraint {
    uint32_t falsify; // assignments falsifying this constraint
    string label;
    // optional metadata
    int a=0,b=0,c=0,d=0;
};
struct Family {
    string name;
    int n;
    vector<Constraint> cs;
};

static string pack_u32_vec(const vector<uint32_t>& v, char tag='N') {
    string s; s.push_back(tag);
    for (uint32_t x: v) {
        for (int k=0;k<4;k++) s.push_back(char((x>>(8*k))&255));
    }
    return s;
}

static string residual_signature(uint32_t missing, uint32_t suffixMask,
                                 const vector<uint32_t>& incByAssignment) {
    if (missing==0) return string("U",1); // already UNSAT, suffix irrelevant
    vector<uint32_t> inc;
    uint32_t x=missing;
    while(x){
        uint32_t l=x&-x; int a=__builtin_ctz(x); x-=l;
        uint32_t m=incByAssignment[a] & suffixMask;
        if(m==0) return string("S",1); // some uncovered assignment can never be killed
        inc.push_back(m);
    }
    sort(inc.begin(),inc.end(),[](uint32_t x,uint32_t y){
        int px=__builtin_popcount(x),py=__builtin_popcount(y);
        return px!=py?px<py:x<y;
    });
    inc.erase(unique(inc.begin(),inc.end()),inc.end());
    vector<uint32_t> mins;
    for(uint32_t m:inc){
        bool redundant=false;
        for(uint32_t q:mins) if((q&m)==q){redundant=true;break;}
        if(!redundant) mins.push_back(m);
    }
    return pack_u32_vec(mins,'N');
}

static vector<uint32_t> incidence_by_assignment(const Family& F){
    vector<uint32_t> inc(1u<<F.n,0);
    for(int i=0;i<(int)F.cs.size();i++){
        uint32_t fm=F.cs[i].falsify;
        while(fm){uint32_t l=fm&-fm; int a=__builtin_ctz(fm); fm-=l; inc[a]|=(1u<<i);}
    }
    return inc;
}

struct SmallExact {
    Family F;
    int M;
    uint32_t ALLC;
    uint32_t FULLA;
    vector<uint32_t> cover;
    vector<uint32_t> incA;
    vector<int> width;
    vector<int> parent;
    vector<int> order;
    vector<int> profile;

    SmallExact(Family fam):F(std::move(fam)){
        M=F.cs.size();
        if(M>20) throw runtime_error("SmallExact M too large");
        ALLC=(1u<<M)-1; FULLA=(1u<<(1u<<F.n))-1;
        cover.assign(1u<<M,0);
        for(uint32_t s=1;s<=ALLC;s++){
            uint32_t l=s&-s; int i=__builtin_ctz(s);
            cover[s]=cover[s^l] | F.cs[i].falsify;
        }
        incA=incidence_by_assignment(F);
        width.assign(1u<<M,-1);
    }

    int cut_width(uint32_t prefix){
        int &ans=width[prefix]; if(ans>=0) return ans;
        uint32_t suffix=ALLC^prefix;
        unordered_set<string> sigs;
        uint32_t p=prefix;
        while(true){
            uint32_t missing=FULLA ^ cover[p];
            sigs.insert(residual_signature(missing,suffix,incA));
            if(p==0)break; p=(p-1)&prefix;
        }
        return ans=sigs.size();
    }

    void optimize_order(){
        int N=1<<M, INF=1e9;
        vector<int> dp(N,INF); parent.assign(N,-1); dp[0]=cut_width(0);
        for(uint32_t S=1;S<(uint32_t)N;S++){
            uint32_t x=S;
            while(x){uint32_t l=x&-x; int b=__builtin_ctz(x); x-=l; uint32_t P=S^l;
                int v=max(dp[P],cut_width(S));
                if(v<dp[S]){dp[S]=v;parent[S]=b;}
            }
        }
        uint32_t S=ALLC; order.clear();
        while(S){int b=parent[S];order.push_back(b);S^=1u<<b;}
        reverse(order.begin(),order.end());
        profile.clear(); S=0; profile.push_back(cut_width(S));
        for(int b:order){S|=1u<<b;profile.push_back(cut_width(S));}
    }
};

static uint32_t falsify_clause(int n, const vector<pair<int,int>>& lits){
    uint32_t m=0;
    for(int a=0;a<(1<<n);a++){
        bool sat=false;
        for(auto [v,s]:lits) if(((a>>v)&1)==s){sat=true;break;}
        if(!sat)m|=1u<<a;
    }
    return m;
}

static Family make_2sat3(){
    Family F{"2SAT3",3,{}};
    for(int i=0;i<3;i++)for(int j=i+1;j<3;j++)for(int si=0;si<2;si++)for(int sj=0;sj<2;sj++){
        Constraint c; c.falsify=falsify_clause(3,{{i,si},{j,sj}}); c.label="("+to_string(i)+"="+to_string(si)+")v("+to_string(j)+"="+to_string(sj)+")";
        c.a=i;c.b=si;c.c=j;c.d=sj;F.cs.push_back(c);
    }
    return F;
}
static Family make_horn3(){
    Family F{"HORN3_GRAPH",3,{}};
    for(int i=0;i<3;i++){
        Constraint c; c.falsify=falsify_clause(3,{{i,1}});c.label="fact"+to_string(i);c.a=0;c.b=i;F.cs.push_back(c);
    }
    for(int i=0;i<3;i++)for(int j=0;j<3;j++)if(i!=j){
        Constraint c; c.falsify=falsify_clause(3,{{i,0},{j,1}});c.label=to_string(i)+"->"+to_string(j);c.a=1;c.b=i;c.c=j;F.cs.push_back(c);
    }
    for(int i=0;i<3;i++){
        Constraint c; c.falsify=falsify_clause(3,{{i,0}});c.label="goal_not"+to_string(i);c.a=2;c.b=i;F.cs.push_back(c);
    }
    return F;
}
static Family make_xor3(){
    Family F{"XOR3_ALL_EQ",3,{}};
    for(int a=1;a<8;a++)for(int b=0;b<2;b++){
        uint32_t fm=0;for(int x=0;x<8;x++) if((__builtin_parity((unsigned)(a&x)))!=b)fm|=1u<<x;
        Constraint c;c.falsify=fm;c.label="xor"+to_string(a)+"="+to_string(b);c.a=a;c.b=b;F.cs.push_back(c);
    }
    return F;
}
static Family make_chain4(){
    Family F{"CHAIN4_TWO_TRIPLES",4,{}};
    vector<array<int,3>> Ts={array<int,3>{0,1,2},array<int,3>{1,2,3}};
    for(auto T:Ts)for(int p=0;p<8;p++){
        vector<pair<int,int>> lits;for(int j=0;j<3;j++)lits.push_back({T[j],(p>>j)&1});
        Constraint c;c.falsify=falsify_clause(4,lits);c.label="T"+to_string(T[0])+to_string(T[1])+to_string(T[2])+"p"+to_string(p);F.cs.push_back(c);
    }
    return F;
}
static Family make_3sat4(){
    Family F{"3SAT4_FULL",4,{}};
    for(int omit=0;omit<4;omit++){
        vector<int>T;for(int v=0;v<4;v++)if(v!=omit)T.push_back(v);
        for(int p=0;p<8;p++){
            vector<pair<int,int>> lits;for(int j=0;j<3;j++)lits.push_back({T[j],(p>>j)&1});
            Constraint c;c.falsify=falsify_clause(4,lits);c.label="omit"+to_string(omit)+"p"+to_string(p);F.cs.push_back(c);
        }
    }
    return F;
}

static string state_2sat(const Family& F,uint32_t sel){
    uint8_t r[6];for(int i=0;i<6;i++)r[i]=1u<<i;
    auto node=[](int v,int sign){return 2*v+sign;};
    for(int k=0;k<(int)F.cs.size();k++)if(sel>>k&1){auto &c=F.cs[k];int u=node(c.a,c.b),v=node(c.c,c.d);r[u^1]|=1u<<v;r[v^1]|=1u<<u;}
    for(int k=0;k<6;k++)for(int i=0;i<6;i++)if(r[i]&(1u<<k))r[i]|=r[k];
    for(int v=0;v<3;v++)if((r[2*v]&(1u<<(2*v+1)))&&(r[2*v+1]&(1u<<(2*v))))return "BAD";
    string s="R";for(int i=0;i<6;i++)s.push_back(char(r[i]));return s;
}
static string state_horn(const Family& F,uint32_t sel){
    uint8_t r[3];for(int i=0;i<3;i++)r[i]=1u<<i;uint8_t facts=0,goals=0;
    for(int k=0;k<(int)F.cs.size();k++)if(sel>>k&1){auto &c=F.cs[k];if(c.a==0)facts|=1u<<c.b;else if(c.a==2)goals|=1u<<c.b;else r[c.b]|=1u<<c.c;}
    for(int k=0;k<3;k++)for(int i=0;i<3;i++)if(r[i]&(1u<<k))r[i]|=r[k];
    uint8_t clo=0;for(int i=0;i<3;i++)if(facts>>i&1)clo|=r[i];
    if(clo&goals)return "BAD";
    string s="H";s.push_back(char(clo));s.push_back(char(goals));for(int i=0;i<3;i++)s.push_back(char(r[i]));return s;
}
static string state_xor(const Family& F,uint32_t sel){
    uint8_t basis[4]={0,0,0,0};
    for(int k=0;k<(int)F.cs.size();k++)if(sel>>k&1){uint8_t x=(uint8_t)(F.cs[k].a | (F.cs[k].b<<3));for(int b=3;b>=0;b--)if(x>>b&1){if(basis[b])x^=basis[b];else{basis[b]=x;break;}}}
    // reduce to canonical basis
    for(int b=0;b<4;b++)if(basis[b])for(int c=b+1;c<4;c++)if(basis[c]&(1u<<b))basis[c]^=basis[b];
    // inconsistency iff row 0001 in augmented coordinate convention bit3 rhs only is in span; basis[3]==8 after reduction
    bool bad=false;
    // More robust: reduce vector 8 by basis
    uint8_t x=8;for(int b=3;b>=0;b--)if(x>>b&1){if(basis[b])x^=basis[b];}
    if(x==0)bad=true;
    if(bad)return "BAD";
    string s="X";for(int i=0;i<4;i++)s.push_back(char(basis[i]));return s;
}

static void report_states(SmallExact& E, function<string(uint32_t)> stateFn, ostream& out){
    uint32_t S=0;
    for(int k=0;k<=E.M;k++){
        uint32_t suffix=E.ALLC^S;
        unordered_map<string,string> stateToResidual;
        unordered_set<string> states;
        int violations=0;
        uint32_t p=S;
        while(true){
            string st=stateFn(p); string rs=residual_signature(E.FULLA ^ E.cover[p],suffix,E.incA);
            auto it=stateToResidual.find(st);if(it==stateToResidual.end())stateToResidual.emplace(st,rs);else if(it->second!=rs)violations++;
            states.insert(st);
            if(p==0)break;p=(p-1)&S;
        }
        out<<E.F.name<<","<<k<<","<<E.profile[k]<<","<<states.size()<<","<<violations<<"\n";
        if(k<E.M)S|=1u<<E.order[k];
    }
}

struct ProfileResult{vector<int> width;vector<int> reachable;int peak=0;};
static ProfileResult profile_large(const Family& F,const vector<int>& order){
    int M=F.cs.size(); uint32_t ALLC=(M==32?0xffffffffu:((1u<<M)-1));uint32_t FULLA=(1u<<(1u<<F.n))-1;auto incA=incidence_by_assignment(F);
    unordered_set<uint32_t> covs;covs.insert(0);uint32_t prefix=0;ProfileResult R;
    for(int k=0;k<=M;k++){
        uint32_t suffix=ALLC^prefix;unordered_set<string>sigs;sigs.reserve(covs.size()*2+1);
        for(uint32_t cov:covs)sigs.insert(residual_signature(FULLA^cov,suffix,incA));
        R.width.push_back((int)sigs.size());R.reachable.push_back((int)covs.size());R.peak=max(R.peak,(int)sigs.size());
        if(k<M){int idx=order[k];uint32_t fm=F.cs[idx].falsify;vector<uint32_t> add;add.reserve(covs.size());for(uint32_t c:covs)add.push_back(c|fm);for(uint32_t c:add)covs.insert(c);prefix|=1u<<idx;}
    }
    return R;
}

static pair<int,int> chain_separator_state_counts(const Family& F){
    // Cut after the first 8 clauses (triple 0,1,2). State = feasible assignments to separator (x1,x2).
    unordered_set<int> states; unordered_map<int,string> state2res; int viol=0;
    auto incA=incidence_by_assignment(F); uint32_t FULLA=(1u<<16)-1; uint32_t prefix=(1u<<8)-1, suffix=((1u<<16)-1)^prefix;
    vector<uint32_t> cover(1u<<16,0);for(uint32_t s=1;s<(1u<<16);s++){uint32_t l=s&-s;int i=__builtin_ctz(s);cover[s]=cover[s^l]|F.cs[i].falsify;}
    for(uint32_t p=0;p<(1u<<8);p++){
        int feas=0;
        for(int b12=0;b12<4;b12++){
            bool ok=false;for(int x0=0;x0<2;x0++){
                int a=x0 | ((b12&1)<<1) | (((b12>>1)&1)<<2); // x3 arbitrary; prefix clauses ignore x3
                // choose x3=0 assignment index; falsification independent of x3 for prefix
                if(((cover[p]>>a)&1)==0){ok=true;break;}
            }
            if(ok)feas|=1<<b12;
        }
        string rs=residual_signature(FULLA^cover[p],suffix,incA);
        auto it=state2res.find(feas);if(it==state2res.end())state2res[feas]=rs;else if(it->second!=rs)viol++;
        states.insert(feas);
    }
    return {(int)states.size(),viol};
}

int main(){
    ios::sync_with_stdio(false);
    vector<SmallExact> exact;
    exact.emplace_back(make_2sat3());
    exact.emplace_back(make_horn3());
    exact.emplace_back(make_xor3());
    for(auto &E:exact){E.optimize_order();cerr<<E.F.name<<" peak "<<*max_element(E.profile.begin(),E.profile.end())<<"\n";}

    ofstream sum("/mnt/data/formula_continuation_summary.csv");
    sum<<"family,constraints,optimal_or_tested_peak,order_status,canonical_peak_state_count,canonical_sufficient_violations\n";
    ofstream prof("/mnt/data/formula_continuation_profiles.csv");
    prof<<"family,cut,residual_classes,canonical_states,canonical_sufficiency_violations\n";

    for(auto &E:exact){
        stringstream tmp;
        if(E.F.name=="2SAT3")report_states(E,[&](uint32_t s){return state_2sat(E.F,s);},tmp);
        else if(E.F.name=="HORN3_GRAPH")report_states(E,[&](uint32_t s){return state_horn(E.F,s);},tmp);
        else report_states(E,[&](uint32_t s){return state_xor(E.F,s);},tmp);
        string line;int maxStates=0,totalViol=0;stringstream rd(tmp.str());
        while(getline(rd,line)){
            prof<<line<<"\n"; // parse state count and viol
            vector<string> f;stringstream ls(line);string z;while(getline(ls,z,','))f.push_back(z);
            if(f.size()>=5){maxStates=max(maxStates,stoi(f[3]));totalViol+=stoi(f[4]);}
        }
        int pk=*max_element(E.profile.begin(),E.profile.end());
        sum<<E.F.name<<","<<E.M<<","<<pk<<",EXACT_MIN_OVER_ALL_ORDERS,"<<maxStates<<","<<totalViol<<"\n";
        cerr<<E.F.name<<" order:";for(int b:E.order)cerr<<" "<<b;cerr<<" profile:";for(int w:E.profile)cerr<<" "<<w;cerr<<"\n";
    }

    Family chain=make_chain4();vector<int> chainOrder(16);iota(chainOrder.begin(),chainOrder.end(),0);auto ch=profile_large(chain,chainOrder);auto [chstates,chviol]=chain_separator_state_counts(chain);
    sum<<chain.name<<",16,"<<ch.peak<<",NATURAL_LOCAL_ORDER,"<<chstates<<","<<chviol<<"\n";
    for(int k=0;k<(int)ch.width.size();k++)prof<<chain.name<<","<<k<<","<<ch.width[k]<<",,"<<"\n";
    cerr<<chain.name<<" peak "<<ch.peak<<" cut8width "<<ch.width[8]<<" separatorStates "<<chstates<<" viol "<<chviol<<"\n";

    Family s3=make_3sat4();
    vector<vector<int>> orders;
    vector<int> nat(32);iota(nat.begin(),nat.end(),0);orders.push_back(nat);
    // sign-major: same sign pattern across the four triples
    vector<int> signMajor;for(int p=0;p<8;p++)for(int t=0;t<4;t++)signMajor.push_back(8*t+p);orders.push_back(signMajor);
    // reverse natural
    vector<int> rev=nat;reverse(rev.begin(),rev.end());orders.push_back(rev);
    mt19937 rng(20261003);for(int r=0;r<5;r++){auto o=nat;shuffle(o.begin(),o.end(),rng);orders.push_back(o);}
    int bestPeak=INT_MAX,bestIdx=-1;ProfileResult bestProf;
    for(int i=0;i<(int)orders.size();i++){
        auto p=profile_large(s3,orders[i]);cerr<<"3SAT4 order "<<i<<" peak "<<p.peak<<"\n";
        if(p.peak<bestPeak){bestPeak=p.peak;bestIdx=i;bestProf=p;}
    }
    sum<<s3.name<<",32,"<<bestPeak<<",BEST_OF_"<<orders.size()<<"_DECLARED_ORDERS,,\n";
    for(int k=0;k<(int)bestProf.width.size();k++)prof<<s3.name<<","<<k<<","<<bestProf.width[k]<<",,"<<"\n";
    ofstream meta("/mnt/data/formula_continuation_meta.txt");
    meta<<"3SAT4 best order index "<<bestIdx<<" peak "<<bestPeak<<"\norder:";for(int b:orders[bestIdx])meta<<" "<<b;meta<<"\nprofile:";for(int w:bestProf.width)meta<<" "<<w;meta<<"\n";
    for(auto &E:exact){meta<<E.F.name<<" exact optimal order:";for(int b:E.order)meta<<" "<<b;meta<<"\nprofile:";for(int w:E.profile)meta<<" "<<w;meta<<"\n";}
    meta<<"CHAIN4 natural profile:";for(int w:ch.width)meta<<" "<<w;meta<<"\ncut8 separator states "<<chstates<<" violations "<<chviol<<"\n";
    return 0;
}
