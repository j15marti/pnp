// Exact independent finite certificate and source-family audit. Node.js: node independent_audit.js
const run = ()=>{
  let checks=0;const ok=(v)=>{checks++;if(!v)throw Error("failed assertion "+checks)};
  const parse=s=>s.split(" ").map(t=>[...t].map(Number));
  const B=parse("000 012 010 110 111 221 333 332 002 100 103 223");
  const rows=(T,n)=>Array.from({length:3*n},(_,i)=>T.flatMap((t,e)=>t[Math.floor(i/n)]===i%n?[e]:[]));
  const iscover=(T,n,W)=>W.length===n&&rows(T,n).every(r=>r.filter(e=>W.includes(e)).length===1);
  function covers(T,n){const out=[];const rec=(i,W)=>{if(i===n){if(iscover(T,n,W))out.push(W);return}for(let e=0;e<T.length;e++)if(T[e][0]===i)rec(i+1,[...W,e]);};rec(0,[]);return out;}
  const baseCovers=covers(B,4).map(a=>a.sort((x,y)=>x-y));
  const expected=[[0,4,7,11],[1,5,6,9],[2,5,7,10],[3,5,6,8]];
  ok(JSON.stringify(baseCovers)===JSON.stringify(expected));
  // Certified rotation of connected base. X=0..3,Y=4..7,Z=8..11,t=12..23.
  const R=[[12,14,13,20],[15,21,22,16],[17,23],[18,19],[12,20,22,21],[13,14,15,16],[23,17],[19,18],[14,12,21,15],[16,17],[20,13,19],[23,22,18],
    [0,4,8],[10,0,5],[5,0,8],[8,1,5],[1,9,5],[9,2,6],[11,3,7],[3,10,7],[4,0,10],[1,8,4],[11,1,4],[2,11,6]];
  for(let u=0;u<R.length;u++){ok(new Set(R[u]).size===R[u].length);for(const v of R[u])ok(R[v].includes(u));}
  for(let e=0;e<B.length;e++)ok([B[e][0],4+B[e][1],8+B[e][2]].every(v=>R[12+e].includes(v)));
  const visited=new Set();let F=0;for(let u=0;u<R.length;u++)for(let v of R[u])if(!visited.has(`${u},${v}`)){F++;let a=u,b=v;while(!visited.has(`${a},${b}`)){visited.add(`${a},${b}`);let c=R[b][(R[b].indexOf(a)+1)%R[b].length];a=b;b=c;}ok(a===u&&b===v);}
  ok(visited.size===72);ok(24-36+F===2);
  let reach=new Set([0]),todo=[0];while(todo.length)for(let v of R[todo.pop()])if(!reach.has(v)){reach.add(v);todo.push(v);}ok(reach.size===24);
  // Pure exact-one propagation in every local single pin of one-phase events.
  const groups=[[0,4,11],[1,9],[2,10],[3,8]];
  for(let c=0;c<4;c++)for(const e of groups[c]){
    const p=Array(12).fill(-1);p[e]=1;let change=true;
    while(change){change=false;for(const r of rows(B,4)){const one=r.filter(j=>p[j]===1),live=r.filter(j=>p[j]!==0);ok(one.length<=1&&live.length>=1);if(one.length===1){for(const j of r)if(j!==one[0]&&p[j]!==0){ok(p[j]===-1);p[j]=0;change=true;}}else if(live.length===1){p[live[0]]=1;change=true;}}}
    ok(p.every((v,j)=>v===Number(expected[c].includes(j))));
  }
  function chain(k){const T=Array.from({length:k},(_,i)=>B.map(t=>t.map(v=>v+4*i))).flat();for(let i=0;i<k-1;i++){let a=12*i+7,b=12*(i+1);[T[a][1],T[b][1]]=[T[b][1],T[a][1]];}return T;}
  const lift=p=>p.flatMap((c,i)=>expected[c].map(e=>e+12*i));
  const families=[];
  for(const k of [1,2,4,8,16,32,64]){
    const T=chain(k);let words=[];
    // All monotone patterns: inactive prefix, one phase 2 transition if not all active, then phase 0.
    words.push(Array(k).fill(0));words.push(Array(k).fill(1));
    for(let i=0;i<k;i++){let p=Array.from({length:k},(_,j)=>j<i?1:j===i?2:0);words.push(p);let d=Array(k).fill(1);d[i]=3;words.push(d);}
    const witnesses=words.map(lift);for(const W of witnesses)ok(iscover(T,4*k,W));
    // Witness signatures prove all indicated equivalence classes distinct.
    const ids=T.map((_,e)=>witnesses.map(W=>Number(W.includes(e))).join(""));
    const by=new Map();ids.forEach((v,e)=>{if(!by.has(v))by.set(v,[]);by.get(v).push(e);});const Q=[...by.values()];const cls=new Map();Q.forEach((g,i)=>g.forEach(e=>cls.set(e,i)));
    const rr=[...new Set(rows(T,4*k).map(r=>r.map(e=>cls.get(e)).sort((a,b)=>a-b).join(",")))].map(r=>r.split(",").map(Number));
    ok(rr.every(r=>new Set(r).size===r.length));
    const H=Q.map((_,i)=>i).filter(i=>rr.filter(r=>r.includes(i)).length>2);
    ok(H.length===k);ok(H.every((c)=>Q[c].some(e=>e%12===0)));
    const patterns=new Set(witnesses.map(W=>Array.from({length:k},(_,i)=>Number(W.includes(12*i))).join("")));
    ok(patterns.size===k+1);for(const p of patterns)ok(!p.includes("10"));
    // Exhaustively check local state transitions for small sizes, not full 3DM enumeration.
    if(k<=4){let count=0;const rec=(a)=>{if(a.length===k){const valid=a.slice(0,-1).every((v,i)=>Number(v===0||v===2)===Number(a[i+1]===0));ok(iscover(T,4*k,lift(a))===valid);if(valid)count++;return;}for(let c=0;c<4;c++)rec([...a,c]);};rec([]);}
    families.push({k,triples:T.length,high:H.length,patterns:patterns.size,witnesses_checked:witnesses.length});
  }
  // Verify exact integer Farkas certificates from the executed Python LP.
  const certs=[
    {name:"MF_U",n:3,T:parse("000 002 010 011 021 022 100 101 111 201 202 221"),dual:[[5,-1],[9,2],[18,1],[24,-1],[25,1],[27,3],[36,3],[40,-1],[45,-2],[49,-1],[56,-1],[59,2],[62,1],[66,1],[73,-1],[75,1],[88,1],[91,-1],[92,-1],[95,1],[101,1],[116,-1]]},
    {name:"CC_U",n:4,T:parse("000 012 010 110 111 121 123 221 232 333 332 302"),dual:[[2,-1],[12,2],[20,1],[24,-2],[29,1],[41,1],[48,-1],[49,2],[50,1],[61,1],[69,1],[73,-2],[78,1],[90,2],[93,-1],[94,1],[97,-1],[115,1],[119,-1]]}
  ];
  for(const {T,n,dual} of certs){
    const m=T.length,ix=new Map();let p=m;for(let i=0;i<m;i++)for(let j=i+1;j<m;j++)ix.set(`${i},${j}`,p++);
    const E=[],A=[],b=[],d=[];const eq=(r,v)=>{E.push(r);b.push(v)},ub=(r,v)=>{A.push(r);d.push(v)};
    for(let i=0;i<m;i++)ub([[i,1]],1);
    const rs=rows(T,n);for(const r of rs)eq(r.map(i=>[i,1]),1);
    for(let i=0;i<m;i++)for(let j=i+1;j<m;j++){const k=ix.get(`${i},${j}`);ub([[k,1],[i,-1]],0);ub([[k,1],[j,-1]],0);ub([[i,1],[j,1],[k,-1]],1);}
    for(let i=0;i<m;i++)for(const r of rs)eq([...r.map(j=>[i===j?i:ix.get(`${Math.min(i,j)},${Math.max(i,j)}`),1]),[i,-1]],0);
    const M=E.concat(A),rhs=b.concat(d),v=Array(p).fill(0);let value=0;
    for(const [i,w] of dual){ok(i<M.length);if(i>=E.length)ok(w>=0);for(const [j,c] of M[i])v[j]+=w*c;value+=rhs[i]*w;}
    ok(v.every(x=>x>=0));ok(value<=-1);ok(covers(T,n).length===0);
  }
  return {checks,baseCovers,rotation:{vertices:24,edges:36,faces:F},families,exactFarkasCertificates:certs.map(c=>({name:c.name,terms:c.dual.length}))};
};
console.log(JSON.stringify(run(),null,2));
