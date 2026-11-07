"""Independent threshold reachability checker for packet-block interface optima.
Works on actual graph edges, not imported JS implementation. No machine lower bound.
"""
import itertools, json, functools
import networkx as nx

def sources():
    return [('K4',nx.complete_graph(4)),('K3,3',nx.complete_bipartite_graph(3,3)),
            ('cube Q3',nx.hypercube_graph(3)),('Petersen',nx.petersen_graph()),
            ('prism C6 x K2',nx.circular_ladder_graph(6))]

def check_one(g,k,mode="path"):
    n=g.number_of_nodes(); verts=list(g.nodes()); index={v:i for i,v in enumerate(verts)}
    edges=[(index[u],index[v]) for u,v in g.edges()]
    cut=[sum(((mask>>u)&1)!=((mask>>v)&1) for u,v in edges) for mask in range(1<<n)]
    allmask=(1<<n)-1
    def reachable(bound):
        reach={0}
        for mask in range(1<<n):
            if mask not in reach:continue
            available=[i for i in range(n) if not ((mask>>i)&1)]
            for sz in range(1,min(k,len(available))+1):
                for sel in itertools.combinations(available,sz):
                    nextmask=mask | sum(1<<i for i in sel)
                    if cut[nextmask]<=bound: reach.add(nextmask)
        return allmask in reach
    if mode=="path":
        return next(b for b in range(len(edges)+1) if reachable(b))
    def tree_feasible(bound):
        @functools.lru_cache(None)
        def rec(mask):
            if cut[mask] > bound: return False
            if mask.bit_count()<=k: return True
            low=mask&-mask
            for a in range(1,mask):
                if a & ~mask or not (a&low) or a==mask: continue
                if rec(a) and rec(mask^a):return True
            return False
        return rec(allmask)
    return next(b for b in range(len(edges)+1) if tree_feasible(b))

if __name__=='__main__':
    import sys
    js=json.load(open(sys.argv[1] if len(sys.argv)>1 else 'results/raw/arc/2026-11-07_1440_LSPV4_479_PACKET_FRONTIER_RAW.json'))
    checks=0
    for (name,g), row in zip(sources(),js['rows']):
        assert name==row['name']
        assert g.number_of_nodes()==row['vertices'] and g.number_of_edges()==row['edges']
        for item in row['blocks']:
            actual=check_one(g,item['K'])
            assert actual==item['optimum'],(name,item['K'],actual,item['optimum'])
            checks+=1
            treemin=check_one(g,item["K"],"tree")
            assert treemin==item["tree"]["optimum"],(name,item["K"],treemin)
            checks+=1
        print(name,[(b['K'],b['optimum'],b['tree']['optimum']) for b in row['blocks']])
    print('independent threshold optima verified:',checks)
