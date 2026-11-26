// Standalone independent finite audit; node independent_audit.js
function independentAudit(){
  const U="000 002 010 011 021 022 100 101 111 201 202 221".split(" ").map(s=>Array.from(s,Number)),V=[...U,[1,1,0]],O=Array.from({length:8},(_,i)=>[i>>2,(i>>1)&1,i&1]),L=[[0,1],[0,2],[1,2]];
  const check=(x,m)=>{if(!x)throw Error(m)};
  const bits=(x,m)=>Array.from({length:m},(_,i)=>i).filter(i=>(x>>i)&1);
  function projections(T,n,a,b){let out=[];function rec(i,used,w){if(i===n){out.push(w);return;}for(let j=0;j<T.length;j++)if(T[j][a]===i&&!(used&(1<<T[j][b])))rec(i+1,used|(1<<T[j][b]),w|(1<<j));}rec(0,0,0);return out;}
  function truth(T,n){return projections(T,n,0,1).filter(w=>new Set(bits(w,T.length).map(i=>T[i][2])).size===n);}
  function phases(T,n,A,B,l,k,E){
    const a=l.find(c=>k.includes(c)),b=l.find(c=>c!==a),c=k.find(c=>c!==a);
    const left=Array(n),right=Array(n),Y=Array(n),Z=Array(n);
    for(const i of bits(A,T.length)){left[T[i][a]]=i;Y[T[i][b]]=T[i][a];}
    for(const i of bits(B,T.length)){right[T[i][a]]=i;Z[T[i][c]]=T[i][a];}
    const used=[new Set(),new Set(),new Set()];for(const i of bits(E,T.length)){for(let j=0;j<3;j++){if(used[j].has(T[i][j]))return [];used[j].add(T[i][j]);}}
    const active=left.map((_,x)=>+!used[a].has(x));
    const f=right.map(i=>Y[T[i][b]]),g=left.map(i=>Z[T[i][c]]);
    const q=left.map((i,x)=>+!used[b].has(T[i][b])-active[x]),r=right.map((i,x)=>+!used[c].has(T[i][c])-active[x]);
    // Independently implement a functional digraph by indegree elimination and
    // enumerate the surviving cycle phases (test-only small-instance audit).
    function solve(h,d,domains){
      const deg=Array(n).fill(0),v=Array(n).fill(-1);h.forEach(x=>deg[x]++);
      const rhs=d.slice(),Q=[];deg.forEach((x,i)=>{if(x===0)Q.push(i);});
      for(let k=0;k<Q.length;k++){let x=Q[k],z=-rhs[x];if(!domains[x].includes(z))return [];v[x]=z;rhs[h[x]]-=z;if(--deg[h[x]]===0)Q.push(h[x]);}
      let states=[v],seen=new Set();
      for(let x=0;x<n;x++)if(deg[x]>0&&!seen.has(x)){
        const cycle=[x];for(let y=h[x];y!==x;y=h[y])cycle.push(y);cycle.forEach(i=>seen.add(i));
        const words=[];for(const p of domains[x]){const w=[p];for(const i of cycle.slice(1))w.push(w[w.length-1]-rhs[i]);if(w[w.length-1]-p===rhs[x]&&cycle.every((i,j)=>domains[i].includes(w[j])))words.push(w);}
        states=states.flatMap(s=>words.map(w=>{const t=s.slice();cycle.forEach((i,j)=>t[i]=w[j]);return t;}));
      }return states;
    }
    const dom=active.map((v,i)=>v===0||left[i]===right[i]?[0]:[0,1]);
    const ss=solve(f,q,dom),tt=new Set(solve(g,r,dom.map((D,i)=>D.map(x=>active[i]-x))).map(v=>v.map((x,i)=>active[i]-x).join("")));
    return ss.filter(s=>tt.has(s.join(""))).map(s=>active.reduce((w,v,i)=>v?w|(1<<(s[i]?right[i]:left[i])):w,E)).sort((x,y)=>x-y);
  }
  const rows=[];
  for(const [name,T,n] of [["U",U,3],["V",V,3],["O",O,2],["O-minus-one",O.slice(0,-1),2]]){
    const P=L.map(([a,b])=>projections(T,n,a,b)),ref=truth(T,n);let fibers=0,charts=0,nonempty=0,maxFree=0,checks=0;
    for(let u=0;u<3;u++)for(let v=u+1;v<3;v++)for(const A of P[u])for(const B of P[v]){
      const D=((1<<T.length)-1)&~(A|B);let count=0;charts++;
      for(let E=D;;E=(E-1)&D){
        const expected=ref.filter(w=>(w&D)===E).sort((x,y)=>x-y),got=phases(T,n,A,B,L[u],L[v],E);
        check(got.join(",")===expected.join(","),"fiber mismatch");fibers++;count+=got.length;
        if(got.length){nonempty++;const h=Math.log2(got.length);check(Number.isInteger(h),"not cube count");maxFree=Math.max(maxFree,h);
          for(let i=0;i<T.length;i++)for(let b=0;b<2;b++){const x=got.filter(w=>((w>>i)&1)===b),y=expected.filter(w=>((w>>i)&1)===b);check(x.join(",")===y.join(","),"guard mismatch");checks++;}
        }if(E===0)break;
      }check(count===ref.length,"count mismatch");
    }rows.push({source:name,charts,all_outside_subsets:fibers,nonempty,maxFree,literal_comparisons:checks,exact_count:ref.length});
  }
  // Independently count the known generated family by enumerating each XZ
  // block's actual indexed pairs and running a transfer over neighboring Y
  // incidence. This is a fixture audit, not the production decomposition.
  function fixture(k,seed,name){
    const groups=[];let offset=0;for(let j=0;j<k;j++){let T=(j===0&&seed?seed:O).map(t=>t.map(v=>v+offset));groups.push(T);offset+=j===0&&seed?3:2;}
    for(let j=0;j+1<k;j++){let x=name==="stationary"?1:groups[j].length-1,y=name==="stationary"?2:0;let a=groups[j][x][1];groups[j][x][1]=groups[j+1][y][1];groups[j+1][y][1]=a;}
    const owner=new Map();groups.forEach((T,j)=>T.forEach(t=>{if(!owner.has(t[1]))owner.set(t[1],new Set());owner.get(t[1]).add(j);}));
    let prev=new Map([["",1n]]);
    for(let j=0;j<groups.length;j++){
      const T=groups[j],n=j===0&&seed?3:2,xx=Array.from(new Set(T.map(t=>t[0]))).sort((a,b)=>a-b),zz=new Set(),Y=new Set();
      const left=Array.from(owner).filter(([y,S])=>S.has(j)&&S.has(j-1)).map(([y])=>y).sort((a,b)=>a-b);
      const right=Array.from(owner).filter(([y,S])=>S.has(j)&&S.has(j+1)).map(([y])=>y).sort((a,b)=>a-b);
      const priv=Array.from(owner).filter(([y,S])=>S.size===1&&S.has(j)).map(([y])=>y);
      const next=new Map();
      function rec(i){if(i===n){if(!priv.every(y=>Y.has(y)))return;const want=left.filter(y=>!Y.has(y)).join(","),out=right.filter(y=>Y.has(y)).join(",");const q=prev.get(want)||0n;if(q)next.set(out,(next.get(out)||0n)+q);return;}for(const t of T)if(t[0]===xx[i]&&!zz.has(t[2])&&!Y.has(t[1])){zz.add(t[2]);Y.add(t[1]);rec(i+1);zz.delete(t[2]);Y.delete(t[1]);}}rec(0);prev=next;
    }return String(prev.get("")||0n);
  }
  const scale=[];for(const k of [1,2,4,8,16,32,64,128])scale.push({k,stationary:fixture(k,null,"stationary"),U:fixture(k,U,"U"),V:fixture(k,V,"V")});
  return {rows,scale};
}
console.log(JSON.stringify(independentAudit(),null,2));
