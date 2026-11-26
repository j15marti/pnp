import audit as a,json,itertools as I

def neighbor(k,yes):
    T=list(a.V if yes else a.U);m=len(T);base=list(I.product(range(2),repeat=3))
    T += [tuple(3+2*i+v for v in t) for i in range(k) for t in base]
    pairs=[(0,m)]+[(m+8*i+7,m+8*(i+1)) for i in range(k-1)]
    for p,q in pairs:
        u=list(T[p]);v=list(T[q]);u[1],v[1]=v[1],u[1];T[p]=tuple(u);T[q]=tuple(v)
    return T

if __name__=='__main__':
    O={}
    for k in (1,2,4,8,16,32,64):
        for yes in (False,True):
            T=neighbor(k,yes);n=3+2*k;G=a.graph(T,n)
            assert a.nx.check_planarity(G)[0] and a.nx.is_connected(G) and len(set(T))==len(T)
            assert a.close(T,n)==list(range(len(T)))
            q=a.solve(T,n,0,2,saturated=False);assert q['status']==('YES' if yes else 'NO')
            O[f'{k}-{yes}']=q
            open("neighbor_results.json","w").write(json.dumps(O,indent=2))
            print(k,yes,len(T),q['status'],q.get('blocks'),q.get('work'),flush=True)
    open('neighbor_results.json','w').write(json.dumps(O,indent=2))
