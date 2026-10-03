#include <bits/stdc++.h>
using namespace std;

struct Clause { int len; int v[3]; int sign[3]; };
struct Formula { int n; vector<Clause> cs; string fam; double alpha; int seed; };

static inline bool sat_clause(const Clause& c, uint32_t x){
    for(int j=0;j<c.len;j++){
        int b=(x>>c.v[j])&1U;
        if(b==c.sign[j]) return true;
    }
    return false;
}
static inline bool sat_formula(const Formula& F,uint32_t x){
    for(auto &c:F.cs) if(!sat_clause(c,x)) return false;
    return true;
}

Formula rand3(int n,double alpha,uint64_t seed){
    mt19937_64 rng(seed); int m=llround(alpha*n);
    set<array<int,4>> seen; Formula F{n,{},"R3",alpha,(int)(seed&0x7fffffff)};
    uniform_int_distribution<int>D(0,n-1),B(0,1);
    while((int)F.cs.size()<m){
        array<int,3> vv{D(rng),D(rng),D(rng)};
        if(vv[0]==vv[1]||vv[0]==vv[2]||vv[1]==vv[2]) continue;
        sort(vv.begin(),vv.end());
        int p=B(rng)|(B(rng)<<1)|(B(rng)<<2);
        array<int,4> k{vv[0],vv[1],vv[2],p};
        if(!seen.insert(k).second) continue;
        Clause c; c.len=3;
        for(int j=0;j<3;j++){c.v[j]=vv[j];c.sign[j]=(p>>j)&1;}
        F.cs.push_back(c);
    }
    return F;
}
Formula rand2(int n,double alpha,uint64_t seed){
    mt19937_64 rng(seed); int m=llround(alpha*n);
    set<array<int,3>> seen; Formula F{n,{},"R2PLANT",alpha,(int)(seed&0x7fffffff)};
    uniform_int_distribution<int>D(0,n-1),B(0,1);
    uint32_t plant=(uint32_t)rng() & ((1u<<n)-1);
    while((int)F.cs.size()<m){
        int a=D(rng),b=D(rng); if(a==b)continue; if(a>b)swap(a,b);
        int p=B(rng)|(B(rng)<<1);
        bool ok=(((plant>>a)&1)==(p&1)) || (((plant>>b)&1)==((p>>1)&1));
        if(!ok) continue;
        array<int,3>k{a,b,p}; if(!seen.insert(k).second)continue;
        Clause c;c.len=2;c.v[0]=a;c.v[1]=b;c.sign[0]=p&1;c.sign[1]=(p>>1)&1;
        F.cs.push_back(c);
    }
    return F;
}
Formula horn3(int n,double alpha,uint64_t seed){
    mt19937_64 rng(seed); int m=llround(alpha*n);
    set<array<int,4>> seen; Formula F{n,{},"HORN",alpha,(int)(seed&0x7fffffff)};
    uniform_int_distribution<int>D(0,n-1),P(0,3);
    while((int)F.cs.size()<m){
        array<int,3> vv{D(rng),D(rng),D(rng)};
        if(vv[0]==vv[1]||vv[0]==vv[2]||vv[1]==vv[2])continue;
        sort(vv.begin(),vv.end());
        int pos=P(rng),pat=0; if(pos>0) pat|=1<<(pos-1);
        array<int,4>k{vv[0],vv[1],vv[2],pat};
        if(!seen.insert(k).second)continue;
        Clause c;c.len=3;
        for(int j=0;j<3;j++){c.v[j]=vv[j];c.sign[j]=(pat>>j)&1;}
        F.cs.push_back(c);
    }
    return F;
}
Formula chain3(int n,double alpha,uint64_t seed){
    mt19937_64 rng(seed); int m=llround(alpha*n);
    Formula F{n,{},"CHAINPLANT",alpha,(int)(seed&0x7fffffff)};
    uniform_int_distribution<int>B(0,7);
    uint32_t plant=(uint32_t)rng()&((1u<<n)-1);
    for(int q=0;q<m;q++){
        int i=q%(n-2);
        int forbidden=B(rng);
        int pv=((plant>>i)&1)|(((plant>>(i+1))&1)<<1)|(((plant>>(i+2))&1)<<2);
        if(forbidden==pv) forbidden^=1;
        Clause c;c.len=3;
        for(int j=0;j<3;j++){c.v[j]=i+j;c.sign[j]=1-((forbidden>>j)&1);}
        F.cs.push_back(c);
    }
    return F;
}
Formula xor3(int n,double alpha,uint64_t seed){
    mt19937_64 rng(seed); int r=max(1,n-4);
    Formula F{n,{},"XORPLANT",4.0*r/n,(int)(seed&0x7fffffff)};
    uint32_t plant=(uint32_t)rng()&((1u<<n)-1);
    for(int q=0;q<r;q++){
        int i=q%(n-2); array<int,3>vv{i,i+1,i+2};
        int rhs=((plant>>i)&1)^((plant>>(i+1))&1)^((plant>>(i+2))&1);
        for(int a=0;a<8;a++) if((__builtin_popcount((unsigned)a)&1)!=rhs){
            Clause c;c.len=3;
            for(int j=0;j<3;j++){c.v[j]=vv[j];int forbidden=(a>>j)&1;c.sign[j]=1-forbidden;}
            F.cs.push_back(c);
        }
    }
    return F;
}

struct Geo {
    int sols=0, comps=0, largest=0, backbone=0, frozen_largest=0;
    double avg_deg=0, local_flex=0, disconnected_pair_frac=0;
    double mean_stretch=1,max_stretch=1;
    int hamming_gap=0, diamH=0, diamG=0, min_inter=0;
};

Geo geometry(const Formula&F,uint64_t sample_seed){
    int n=F.n, N=1<<n;
    vector<uint8_t> sat(N,0);
    vector<uint32_t> sols; sols.reserve(N/16);
    vector<int> onecnt(n,0);
    for(int x=0;x<N;x++) if(sat_formula(F,x)){
        sat[x]=1; sols.push_back(x);
        for(int i=0;i<n;i++) if((x>>i)&1) onecnt[i]++;
    }
    Geo g; g.sols=sols.size(); if(sols.empty()) return g;
    for(int i=0;i<n;i++) if(onecnt[i]==0||onecnt[i]==g.sols) g.backbone++;
    long long edge2=0;
    for(uint32_t x:sols) for(int i=0;i<n;i++) if(sat[x^(1u<<i)]) edge2++;
    g.avg_deg=(double)edge2/g.sols; g.local_flex=g.avg_deg/n;

    vector<int> cid(N,-1); vector<vector<uint32_t>> comps;
    for(uint32_t st:sols) if(cid[st]<0){
        int id=comps.size(); vector<uint32_t> cc; deque<uint32_t>q;
        q.push_back(st); cid[st]=id;
        while(!q.empty()){
            auto x=q.front();q.pop_front();cc.push_back(x);
            for(int i=0;i<n;i++){
                auto y=x^(1u<<i);
                if(sat[y]&&cid[y]<0){cid[y]=id;q.push_back(y);}
            }
        }
        comps.push_back(move(cc));
    }
    g.comps=comps.size();
    int li=max_element(comps.begin(),comps.end(),
        [](auto&a,auto&b){return a.size()<b.size();})-comps.begin();
    auto &L=comps[li]; g.largest=L.size();

    if(g.comps>1){
        int mi=n+1;
        for(size_t a=0;a<comps.size();a++) for(size_t b=a+1;b<comps.size();b++)
            for(auto x:comps[a]) for(auto y:comps[b]){
                int d=__builtin_popcount(x^y);
                if(d<mi)mi=d;
                if(mi==2)goto done_inter;
            }
        done_inter:
        g.min_inter=(mi==n+1?0:mi);
    }
    for(int i=0;i<n;i++){
        int b=(L[0]>>i)&1; bool same=true;
        for(auto x:L) if(((x>>i)&1)!=b){same=false;break;}
        if(same)g.frozen_largest++;
    }
    double totalpairs=(double)g.sols*(g.sols-1)/2.0, within=0;
    for(auto &c:comps)within+=(double)c.size()*(c.size()-1)/2.0;
    g.disconnected_pair_frac=totalpairs?1-within/totalpairs:0;

    vector<uint8_t> distseen(n+1,0); mt19937_64 rng(sample_seed);
    auto addpair=[&](uint32_t a,uint32_t b){
        int d=__builtin_popcount(a^b);distseen[d]=1;g.diamH=max(g.diamH,d);
    };
    if(g.sols<=5000){
        for(int i=0;i<g.sols;i++)for(int j=i+1;j<g.sols;j++)addpair(sols[i],sols[j]);
    } else {
        uniform_int_distribution<int>D(0,g.sols-1);
        for(int z=0;z<200000;z++){int i=D(rng),j=D(rng);if(i!=j)addpair(sols[i],sols[j]);}
    }
    int first=-1,last=-1;
    for(int d=1;d<=n;d++)if(distseen[d]){if(first<0)first=d;last=d;}
    int cur=0;
    for(int d=max(1,first);d<=last;d++){
        if(!distseen[d]){cur++;g.hamming_gap=max(g.hamming_gap,cur);}else cur=0;
    }

    int S=min<int>(64,L.size());
    vector<int> sources;
    if((int)L.size()<=S){sources.resize(L.size());iota(sources.begin(),sources.end(),0);}
    else {
        uniform_int_distribution<int>D(0,L.size()-1);set<int>ss;
        while((int)ss.size()<S)ss.insert(D(rng));
        sources.assign(ss.begin(),ss.end());
    }
    vector<int> dist(N,-1); long double sumratio=0; long long rcnt=0;
    for(int si:sources){
        uint32_t src=L[si];deque<uint32_t>q;q.push_back(src);dist[src]=0;
        vector<uint32_t> touched{src};
        while(!q.empty()){
            auto x=q.front();q.pop_front();
            for(int i=0;i<n;i++){
                auto y=x^(1u<<i);
                if(sat[y]&&cid[y]==li&&dist[y]<0){
                    dist[y]=dist[x]+1;q.push_back(y);touched.push_back(y);
                }
            }
        }
        int far=0;
        for(auto y:L){
            int dH=__builtin_popcount(src^y);
            if(dH>0){
                double ratio=(double)dist[y]/dH;
                sumratio+=ratio;rcnt++;g.max_stretch=max(g.max_stretch,ratio);
            }
            far=max(far,dist[y]);
        }
        g.diamG=max(g.diamG,far);
        for(auto y:touched)dist[y]=-1;
    }
    if(rcnt)g.mean_stretch=(double)(sumratio/rcnt);
    return g;
}

struct DS{uint64_t nodes=0;};
bool dpll_rec(const Formula&F, vector<int8_t>a, DS&st){
    st.nodes++;
    bool changed=true;
    while(changed){
        changed=false;
        for(auto &c:F.cs){
            bool ok=false;int un=0,last=-1;
            for(int j=0;j<c.len;j++){
                int v=a[c.v[j]];
                if(v<0){un++;last=j;}
                else if(v==c.sign[j]){ok=true;break;}
            }
            if(ok)continue;
            if(un==0)return false;
            if(un==1){
                int val=c.sign[last],v=c.v[last];
                if(a[v]>=0&&a[v]!=val)return false;
                if(a[v]<0){a[v]=val;changed=true;}
            }
        }
    }
    bool all=true;
    for(auto &c:F.cs){
        bool ok=false;
        for(int j=0;j<c.len;j++){
            int v=a[c.v[j]];
            if(v>=0&&v==c.sign[j]){ok=true;break;}
        }
        if(!ok){all=false;break;}
    }
    if(all)return true;
    int n=F.n,best=-1,bs=-1;vector<int>score(n,0);
    for(auto &c:F.cs){
        bool ok=false;
        for(int j=0;j<c.len;j++){
            int v=a[c.v[j]];
            if(v>=0&&v==c.sign[j]){ok=true;break;}
        }
        if(ok)continue;
        for(int j=0;j<c.len;j++)if(a[c.v[j]]<0)score[c.v[j]]++;
    }
    for(int i=0;i<n;i++)if(a[i]<0&&score[i]>bs){bs=score[i];best=i;}
    if(best<0)return false;
    auto b=a;b[best]=1;if(dpll_rec(F,b,st))return true;
    b=a;b[best]=0;return dpll_rec(F,b,st);
}
uint64_t dpll_nodes(const Formula&F){
    DS s;vector<int8_t>a(F.n,-1);dpll_rec(F,a,s);return s.nodes;
}

int main(int argc,char**argv){
    int n=18,reps=12;if(argc>1)n=stoi(argv[1]);if(argc>2)reps=stoi(argv[2]);
    vector<double>alphas={2.5,3.0,3.5,4.0,4.25,4.5};
    cout<<"family,n,alpha,rep,clauses,solutions,components,largest,backbone,frozen_largest,avg_deg,local_flex,disconnected_pair_frac,mean_stretch,max_stretch,hamming_gap,diamH,diamG,min_inter,dpll_nodes\n";
    uint64_t base=20261003ULL;
    for(double a:alphas)for(int r=0;r<reps;r++){
        auto F=rand3(n,a,base^(uint64_t)(a*100)*0x9e3779b97f4a7c15ULL^r*0xbf58476d1ce4e5b9ULL);
        auto g=geometry(F,base+r);auto dn=dpll_nodes(F);
        cout<<F.fam<<','<<n<<','<<a<<','<<r<<','<<F.cs.size()<<','<<g.sols<<','<<g.comps<<','<<g.largest<<','<<g.backbone<<','<<g.frozen_largest<<','<<g.avg_deg<<','<<g.local_flex<<','<<g.disconnected_pair_frac<<','<<g.mean_stretch<<','<<g.max_stretch<<','<<g.hamming_gap<<','<<g.diamH<<','<<g.diamG<<','<<g.min_inter<<','<<dn<<"\n";
    }
    vector<pair<string,function<Formula(int,double,uint64_t)>>>fams={
        {"R2PLANT",rand2},{"HORN",horn3},{"CHAINPLANT",chain3},{"XORPLANT",xor3}};
    for(auto &fp:fams)for(int r=0;r<reps;r++){
        double a=4.0;
        auto F=fp.second(n,a,base^0x123456789abcdefULL^r*0x94d049bb133111ebULL^fp.first.size());
        auto g=geometry(F,base+1000+r);auto dn=dpll_nodes(F);
        cout<<F.fam<<','<<n<<','<<F.alpha<<','<<r<<','<<F.cs.size()<<','<<g.sols<<','<<g.comps<<','<<g.largest<<','<<g.backbone<<','<<g.frozen_largest<<','<<g.avg_deg<<','<<g.local_flex<<','<<g.disconnected_pair_frac<<','<<g.mean_stretch<<','<<g.max_stretch<<','<<g.hamming_gap<<','<<g.diamH<<','<<g.diamG<<','<<g.min_inter<<','<<dn<<"\n";
    }
}
