#include <bits/stdc++.h>
using namespace std;
using U128=__uint128_t;

struct Clause { int v[3]; int s[3]; };
struct Stats { uint64_t nodes=0, decisions=0, conflicts=0; };

vector<Clause> gen_formula(int n,int m,mt19937_64&rng){
    unordered_set<uint64_t> seen; seen.reserve(m*2+1);
    vector<Clause> F; F.reserve(m);
    uniform_int_distribution<int> D(0,n-1), S(0,1);
    while((int)F.size()<m){
        int x=D(rng),y=D(rng),z=D(rng);
        if(x==y||x==z||y==z) continue;
        array<int,3> vv{x,y,z}; sort(vv.begin(),vv.end());
        int pat=S(rng)|(S(rng)<<1)|(S(rng)<<2);
        uint64_t key=pat;
        for(int j=0;j<3;j++) key=key*64+vv[j];
        if(!seen.insert(key).second) continue;
        Clause c;
        for(int j=0;j<3;j++){c.v[j]=vv[j];c.s[j]=(pat>>j)&1;}
        F.push_back(c);
    }
    return F;
}

static inline int litval(const Clause& c,int j,const vector<int8_t>& a){
    int x=a[c.v[j]];
    if(x<0) return -1;
    return c.s[j]?x:1-x;
}
bool unit_propagate(const vector<Clause>&F,vector<int8_t>&a,Stats&st){
    bool changed=true;
    while(changed){
        changed=false;
        for(auto &c:F){
            bool sat=false; int un=0,last=-1;
            for(int j=0;j<3;j++){
                int z=litval(c,j,a);
                if(z==1){sat=true;break;}
                if(z<0){un++;last=j;}
            }
            if(sat) continue;
            if(un==0){st.conflicts++;return false;}
            if(un==1){
                int val=c.s[last]?1:0,v=c.v[last];
                if(a[v]>=0&&a[v]!=val){st.conflicts++;return false;}
                if(a[v]<0){a[v]=val;changed=true;}
            }
        }
    }
    return true;
}
bool all_sat(const vector<Clause>&F,const vector<int8_t>&a){
    for(auto &c:F){
        bool sat=false;
        for(int j=0;j<3;j++) if(litval(c,j,a)==1){sat=true;break;}
        if(!sat)return false;
    }
    return true;
}
int choose_var(const vector<Clause>&F,const vector<int8_t>&a){
    int n=a.size(); vector<int> score(n);
    for(auto &c:F){
        bool sat=false;
        for(int j=0;j<3;j++) if(litval(c,j,a)==1){sat=true;break;}
        if(sat) continue;
        for(int j=0;j<3;j++) if(a[c.v[j]]<0) score[c.v[j]]++;
    }
    int best=-1,bs=-1;
    for(int v=0;v<n;v++) if(a[v]<0&&score[v]>bs){bs=score[v];best=v;}
    return best;
}
bool dpll(const vector<Clause>&F,vector<int8_t>a,Stats&st){
    st.nodes++;
    if(!unit_propagate(F,a,st))return false;
    if(all_sat(F,a))return true;
    int v=choose_var(F,a); if(v<0)return false;
    st.decisions++; a[v]=1; if(dpll(F,a,st))return true;
    a[v]=0; return dpll(F,a,st);
}

inline int pop128(U128 x){
    return __builtin_popcountll((uint64_t)x)+__builtin_popcountll((uint64_t)(x>>64));
}
int minfill_width(int n,const vector<Clause>&F){
    vector<U128> adj(n,0);
    for(auto &c:F) for(int i=0;i<3;i++) for(int j=i+1;j<3;j++){
        int a=c.v[i],b=c.v[j]; adj[a]|=U128(1)<<b; adj[b]|=U128(1)<<a;
    }
    U128 alive=(n==128)?~U128(0):((U128(1)<<n)-1);
    int width=0;
    for(int step=0;step<n;step++){
        int best=-1,bfill=INT_MAX,bdeg=INT_MAX;
        U128 scan=alive;
        while(scan){
            int v; uint64_t lo=(uint64_t)scan;
            if(lo)v=__builtin_ctzll(lo); else v=64+__builtin_ctzll((uint64_t)(scan>>64));
            scan&=~(U128(1)<<v);
            U128 N=adj[v]&alive&~(U128(1)<<v);
            int deg=pop128(N),fill=0;
            U128 a=N;
            while(a){
                int u; uint64_t alo=(uint64_t)a;
                if(alo)u=__builtin_ctzll(alo); else u=64+__builtin_ctzll((uint64_t)(a>>64));
                a&=~(U128(1)<<u);
                fill+=pop128(a&~adj[u]);
            }
            if(fill<bfill||(fill==bfill&&deg<bdeg)){bfill=fill;bdeg=deg;best=v;}
        }
        U128 N=adj[best]&alive&~(U128(1)<<best);
        width=max(width,pop128(N));
        U128 a=N;
        while(a){
            int u; uint64_t alo=(uint64_t)a;
            if(alo)u=__builtin_ctzll(alo); else u=64+__builtin_ctzll((uint64_t)(a>>64));
            a&=~(U128(1)<<u);
            adj[u]|=N&~(U128(1)<<u);
        }
        alive&=~(U128(1)<<best);
    }
    return width;
}

int main(){
    uint64_t seed=20261003ULL;
    vector<int> ns={48,64,80,96,112,128};
    vector<double> alphas={3.0,4.0,4.25,4.5,5.0};
    int samples=30;
    cout<<"n,alpha,m,sample,sat,dpll_nodes,dpll_decisions,minfill_width\n";
    for(int n:ns)for(double alpha:alphas){
        int m=llround(alpha*n);
        for(int s=0;s<samples;s++){
            mt19937_64 rng(seed ^ (uint64_t)n*0x9e3779b97f4a7c15ULL ^
                           (uint64_t)m*0xbf58476d1ce4e5b9ULL ^
                           (uint64_t)s*0x94d049bb133111ebULL);
            auto F=gen_formula(n,m,rng);
            Stats st; vector<int8_t>a(n,-1);
            bool sat=dpll(F,a,st);
            int w=minfill_width(n,F);
            cout<<n<<","<<fixed<<setprecision(2)<<alpha<<","<<m<<","<<s<<","
                <<sat<<","<<st.nodes<<","<<st.decisions<<","<<w<<"\n";
        }
    }
}
