"""Independent full-relation diagram lift, with exact local five-color fibers."""
from hashlib import sha256
from itertools import product
from pathlib import Path
import json
import sys
import t5_construction_positive_offset1_20261121 as c
import t5_accounting_sil_parity_return_20261121 as f
sys.setrecursionlimit(10000)


def models(n, clauses):
    found = []
    def visit(domains):
        domains=list(domains)
        changed=True
        while changed:
            changed=False
            for triple in clauses:
                supported=c.supports(tuple(domains[x] for x in triple))
                if not all(supported):
                    return
                for x,mask in zip(triple,supported):
                    if mask!=domains[x]:
                        domains[x]=mask
                        changed=True
        choices=[i for i,d in enumerate(domains) if d.bit_count()>1]
        if not choices:
            found.append(tuple(d.bit_length()-1 for d in domains))
            return
        at=min(choices,key=lambda i:domains[i].bit_count())
        for value in range(5):
            if domains[at] & (1<<value):
                branch=domains.copy()
                branch[at]=1<<value
                visit(branch)
    visit([31]*n)
    return found


def bits(values):
    return tuple(int(b) for value in values for b in format(value,'03b'))


class Diagram:
    def __init__(self):
        self.nodes=[('zero',),('one',)]
        self.cache={}
    def node(self,record):
        if record not in self.cache:
            self.cache[record]=len(self.nodes)
            self.nodes.append(record)
        return self.cache[record]
    def trie(self,variables,rows,leaves):
        if not rows:
            return 0
        if not variables:
            assert len(rows)==1
            return leaves[0]
        lo=[i for i,r in enumerate(rows) if r[0]==0]
        hi=[i for i,r in enumerate(rows) if r[0]==1]
        children=[]
        for indices in (lo,hi):
            children.append(self.trie(variables[1:],[rows[i][1:] for i in indices],
                                      [leaves[i] for i in indices]))
        return self.node(('decision',variables[0],*children))
    def count(self,root,width):
        scopes=[0,0]
        counts=[0,1]
        for op,*a in self.nodes[2:]:
            if op=='and':
                left,right=a
                assert not scopes[left]&scopes[right]
                scopes.append(scopes[left]|scopes[right])
                counts.append(counts[left]*counts[right])
            else:
                variable,left,right=a
                both=scopes[left]|scopes[right]
                assert not both&(1<<variable)
                scopes.append(both|(1<<variable))
                counts.append(sum(counts[x] << (both.bit_count()-scopes[x].bit_count())
                                  for x in (left,right)))
        return counts[root] << (width-scopes[root].bit_count())


def main():
    tables={}
    for u,v in product(range(5),repeat=2):
        clauses=c.frame([0,1,2,3,4])+[(4,5,1)]
        rows=[a for a in product(range(5),repeat=4)
              if all(c.C(*([u,*a,v][x] for x in t)) for t in clauses)]
        assert len(rows)==(2 if u==v else 0)
        tables[u,v]=rows
    results=[]
    for k in range(1,4):
        switches=(0,)*k
        for pin in (0,1):
            n,clauses=f.images(switches)[pin]
            solutions=models(n,clauses)
            assert len(solutions)==(20 if pin==0 else 0)
            nn,expanded,links=c.split(n,clauses)
            paths=[[] for _ in range(n)]
            for index,triple in enumerate(clauses):
                for slot,x in enumerate(triple):
                    paths[x].append(3*index+slot)
            pairs=[(u,v) for path in paths for u,v in zip(path,path[1:])]
            diagram=Diagram()
            core_rows=[]
            leaves=[]
            for solution in solutions:
                core=[solution[x] for triple in clauses for x in triple]
                core_rows.append(bits(core))
                root=1
                for j,(u,v) in enumerate(pairs):
                    start=3*len(clauses)+4*j
                    private=diagram.trie(list(range(3*start,3*(start+4))),
                                         [bits(a) for a in tables[core[u],core[v]]],[1,1])
                    root=diagram.node(('and',root,private))
                leaves.append(root)
            root=diagram.trie(list(range(9*len(clauses))),core_rows,leaves)
            count=diagram.count(root,3*nn)
            assert count==len(solutions)*(1<<links)
            upper=2+len(solutions)*(9*len(clauses)+25*links)
            assert len(diagram.nodes)<=max(2,upper)
            results.append(dict(k=k,pin=pin,n=nn,m=len(expanded),
                                N=len(c.encode(nn,expanded)),E=links,
                                unsplit_models=len(solutions),diagram_nodes=len(diagram.nodes),
                                node_upper_bound=upper,count=str(count),
                                model_sha256=sha256(repr(solutions).encode()).hexdigest(),
                                diagram_sha256=sha256(repr(diagram.nodes).encode()).hexdigest()))
    print(json.dumps(dict(local_fibers={str(key):len(value) for key,value in tables.items()},
                         results=results,script_sha256=sha256(Path(__file__).read_bytes()).hexdigest()),indent=2))


if __name__=='__main__':
    main()
