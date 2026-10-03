#include <bits/stdc++.h>
using namespace std;
using U128=__uint128_t;

struct ClauseMask{U128 p=0,n=0;};
struct Key{uint64_t pl,ph,nl,nh;bool operator==(Key const&o)const{return pl==o.pl&&ph==o.ph&&nl==o.nl&&nh==o.nh;}};
struct KeyHash{size_t operator()(Key const&k)const{uint64_t h=k.pl*0x9e3779b97f4a7c15ULL;h^=k.ph*0xbf58476d1ce4e5b9ULL;h^=k.nl*0x94d049bb133111ebULL;h^=k.nh*0x517cc1b727220a95ULL;return h;}};
inline int popc(U128 x){return __builtin_popcountll((uint64_t)x)+__builtin_popcountll((uint64_t)(x>>64));}
inline int width(ClauseMask c){return popc(c.p)+popc(c.n);}
inline Key key(ClauseMask c){return {(uint64_t)c.p,(uint64_t)(c.p>>64),(uint64_t)c.n,(uint64_t)(c.n>>64)};}

struct Clause{int v[3],s[3];};

vector<Clause> gen_formula(int n,int m,uint64_t seed){
    mt19937_64 rng(seed);
    uniform_int_distribution<int> D(0,n-1),S(0,1);
    unordered_set<uint64_t> seen;
    vector<Clause> F;
    while((int)F.size()<m){
        int x=D(rng),y=D(rng),z=D(rng);
        if(x==y||x==z||y==z) continue;
        array<int,3> vv{x,y,z};
        sort(vv.begin(),vv.end());
        int pat=S(rng)|(S(rng)<<1)|(S(rng)<<2);
        uint64_t id=pat;
        for(int q:vv) id=id*(uint64_t)n+q;
        if(!seen.insert(id).second) continue;
        Clause c;
        for(int j=0;j<3;j++){c.v[j]=vv[j];c.s[j]=(pat>>j)&1;}
        F.push_back(c);
    }
    return F;
}

// status: 1 = empty clause derived, 0 = complete width-W closure without empty,
// -1 = clause cap reached before completion.
pair<int,size_t> saturate(int n,const vector<Clause>&F,int W,size_t cap){
    vector<ClauseMask> clauses;
    clauses.reserve(min<size_t>(cap,1000000));
    unordered_set<Key,KeyHash> seen;
    seen.reserve(min<size_t>(2*cap,5000000));
    vector<vector<int>> index(2*n);
    vector<deque<int>> q(W+1);

    auto add=[&](ClauseMask c)->int{
        if((c.p&c.n)||width(c)>W) return -1;
        Key k=key(c);
        if(!seen.insert(k).second) return -1;
        int id=clauses.size();
        clauses.push_back(c);
        q[width(c)].push_back(id);
        return id;
    };

    for(auto &d:F){
        ClauseMask c;
        for(int j=0;j<3;j++){
            U128 bit=U128(1)<<d.v[j];
            if(d.s[j]) c.p|=bit; else c.n|=bit;
        }
        add(c);
    }

    while(true){
        int qw=-1;
        for(int w=0;w<=W;w++) if(!q[w].empty()){qw=w;break;}
        if(qw<0) break;
        int id=q[qw].front(); q[qw].pop_front();
        ClauseMask c=clauses[id];
        if(!(c.p|c.n)) return {1,clauses.size()};

        U128 lits=c.p|c.n;
        while(lits){
            uint64_t lo=(uint64_t)lits;
            int v=lo?__builtin_ctzll(lo):64+__builtin_ctzll((uint64_t)(lits>>64));
            lits&=~(U128(1)<<v);
            bool positive=(c.p>>v)&1;
            int opposite=positive?2*v+1:2*v;
            U128 bit=U128(1)<<v;
            for(int jd:index[opposite]){
                ClauseMask d=clauses[jd];
                ClauseMask r{(c.p|d.p)&~bit,(c.n|d.n)&~bit};
                if(r.p&r.n) continue;
                int rid=add(r);
                if(rid>=0 && !(r.p|r.n)) return {1,clauses.size()};
                if(clauses.size()>cap) return {-1,clauses.size()};
            }
        }

        U128 pp=c.p;
        while(pp){
            uint64_t lo=(uint64_t)pp;
            int v=lo?__builtin_ctzll(lo):64+__builtin_ctzll((uint64_t)(pp>>64));
            pp&=~(U128(1)<<v);
            index[2*v].push_back(id);
        }
        U128 nn=c.n;
        while(nn){
            uint64_t lo=(uint64_t)nn;
            int v=lo?__builtin_ctzll(lo):64+__builtin_ctzll((uint64_t)(nn>>64));
            nn&=~(U128(1)<<v);
            index[2*v+1].push_back(id);
        }
    }
    return {0,clauses.size()};
}

int main(int argc,char**argv){
    int n=argc>1?stoi(argv[1]):80;
    double alpha=argc>2?stod(argv[2]):5.25;
    int sample=argc>3?stoi(argv[3]):0;
    int maxW=argc>4?stoi(argv[4]):4;
    size_t cap=argc>5?stoull(argv[5]):5000000ULL;
    if(n>128) return 2;
    int m=llround(alpha*n);
    uint64_t seed=20261003ULL ^ (uint64_t)n*0x9e3779b97f4a7c15ULL ^
                  (uint64_t)m*0xbf58476d1ce4e5b9ULL ^
                  (uint64_t)sample*0x94d049bb133111ebULL;
    auto F=gen_formula(n,m,seed);
    for(int W=3;W<=maxW;W++){
        auto t=chrono::steady_clock::now();
        auto r=saturate(n,F,W,cap);
        auto ms=chrono::duration_cast<chrono::milliseconds>(chrono::steady_clock::now()-t).count();
        cout<<"n "<<n<<" alpha "<<alpha<<" sample "<<sample
            <<" width "<<W<<" status "<<r.first
            <<" clauses "<<r.second<<" millis "<<ms<<"\n";
        if(r.first==1 || r.first==-1) break;
    }
}
