#include <bits/stdc++.h>
using namespace std;

struct Edge { int u,v; };

int main(){
    vector<Edge> E; map<pair<int,int>,int> idx;
    for(int v=0;v<16;v++) for(int d=0;d<4;d++){
        int w=v^(1<<d);
        if(v<w){ idx[{v,w}] = (int)E.size(); E.push_back({v,w}); }
    }
    int inc[16][4];
    for(int v=0;v<16;v++) for(int d=0;d<4;d++){
        int w=v^(1<<d); auto p=minmax(v,w); inc[v][d]=idx[p];
    }

    int ord[16][4] = {
        {0,1,3,2},{2,3,1,0},{0,3,1,2},{3,1,2,0},
        {2,3,1,0},{0,1,3,2},{2,1,3,0},{0,2,1,3},
        {3,2,0,1},{1,0,2,3},{1,2,0,3},{0,3,1,2},
        {0,2,3,1},{3,2,0,1},{1,3,0,2},{2,1,3,0}
    };

    vector<int> global_occ(32,0);
    for(int v=0;v<16;v++) for(int j=0;j<4;j++) global_occ[inc[v][ord[v][j]]]++;
    cout << "edges=" << E.size()
         << " query_nodes=" << 64
         << " max_global_occurrences_per_variable="
         << *max_element(global_occ.begin(),global_occ.end()) << "\n";

    auto direct_edge_cover = [&](uint32_t m){
        for(int v=0;v<16;v++){
            bool covered=false;
            for(int d=0;d<4;d++) if((m>>inc[v][d])&1U){covered=true;break;}
            if(!covered) return false;
        }
        return true;
    };

    auto bp_eval = [&](uint32_t m){
        int q=0; array<int,32> reads{};
        for(int v=0;v<16;v++){
            bool covered=false;
            for(int j=0;j<4;j++){
                int e=inc[v][ord[v][j]];
                ++q; ++reads[e];
                if((m>>e)&1U){covered=true;break;}
            }
            if(!covered)
                return tuple<bool,int,int>(false,q,*max_element(reads.begin(),reads.end()));
        }
        return tuple<bool,int,int>(true,q,*max_element(reads.begin(),reads.end()));
    };

    unsigned long long total=0,covers=0,mismatch=0;
    int maxq=0,maxreads=0,accept_maxq=0,reject_maxq=0;
    uint32_t maxmask=0;
    uint64_t x=(1ULL<<8)-1, limit=1ULL<<32;
    while(x<limit){
        uint32_t m=(uint32_t)x;
        bool f=direct_edge_cover(m);
        auto [g,q,r]=bp_eval(m);
        ++total; covers += f; mismatch += (f!=g);
        maxreads=max(maxreads,r);
        if(q>maxq){maxq=q;maxmask=m;}
        if(g) accept_maxq=max(accept_maxq,q); else reject_maxq=max(reject_maxq,q);
        uint64_t c=x&-x, y=x+c; if(y>=limit) break;
        x=(((x^y)>>2)/c)|y;
    }

    vector<vector<pair<int,int>>> adj(16);
    for(int e=0;e<32;e++){
        adj[E[e].u].push_back({E[e].v,e});
        adj[E[e].v].push_back({E[e].u,e});
    }
    set<uint32_t> PM;
    function<void(uint16_t,uint32_t)> rec=[&](uint16_t rem,uint32_t m){
        if(!rem){PM.insert(m);return;}
        int u=__builtin_ctz(rem);
        for(auto [v,e]:adj[u]) if(rem&(1u<<v))
            rec(rem & ~(1u<<u) & ~(1u<<v),m|(1u<<e));
    };
    rec(0xffff,0);
    int pm_min=999,pm_max=0; long long pm_sum=0; bool all_accept=true;
    for(uint32_t m:PM){
        auto [g,q,r]=bp_eval(m); all_accept &= g;
        pm_min=min(pm_min,q); pm_max=max(pm_max,q); pm_sum+=q;
    }

    cout << "weight8_total=" << total
         << " edgecovers=" << covers
         << " mismatches=" << mismatch
         << " max_queries=" << maxq
         << " accept_max_queries=" << accept_maxq
         << " reject_max_queries=" << reject_maxq
         << " max_reads_same_variable=" << maxreads << "\n";
    cout << "perfect_matchings=" << PM.size()
         << " all_accept=" << all_accept
         << " pm_min_queries=" << pm_min
         << " pm_avg_queries=" << fixed << setprecision(6)
         << (double)pm_sum/PM.size()
         << " pm_max_queries=" << pm_max << "\n";
    cout << "worst_weight8_mask=0x" << hex << maxmask << dec << "\n";

    mt19937_64 rng(20261004);
    unsigned random_bad=0; int random_maxq=0;
    for(int t=0;t<1000000;t++){
        uint32_t m=(uint32_t)rng();
        auto [g,q,r]=bp_eval(m);
        random_bad += (g!=direct_edge_cover(m));
        random_maxq=max(random_maxq,q);
    }
    cout << "random_full_inputs=1000000 random_mismatch=" << random_bad
         << " random_max_queries=" << random_maxq << "\n";

    cout << "ARCHITECTURE_LOWER_BOUND perfect-matching average = 16*(1+2+3+4)/4 = 40,"
         << " hence worst accepted path >=40 for every local four-edge ordering.\n";
    cout << "STATUS: 64-node syntactic read-twice BP; exact weight-8 verification;"
         << " 41-query worst case for this tested local ordering; no claim that 64 nodes is globally optimal.\n";
}
