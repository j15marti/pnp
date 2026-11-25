// Node.js: node this-file RT26_results.json DA21_closure_results.json
// RT26 85e959ac; DA21 6d9917749c8438435d889b31e5c81ed0fc410e9a
function experiment(rt,da){
  const pc=x=>{let z=0;while(x){x&=x-1;z++}return z};
  const pivot=x=>x.toString(2).length-1;
  let assertions=0;
  function check(x){assertions++;if(!x)throw Error("failed check "+assertions)}
  function test(n,registry,peer,expected,tag){
    const D=3,mons=Array.from({length:1<<n},(_,i)=>i).filter(i=>pc(i)<=D+1).sort((a,b)=>pc(a)-pc(b)||a-b), idx=new Map(mons.map((m,i)=>[m,i])),lim=mons.filter(i=>pc(i)<=D).length;
    const bits=mons.map((_,i)=>1n<<BigInt(i));
    const mult=Array.from({length:n},(_,j)=>mons.slice(0,lim).map(m=>bits[idx.get(m|(1<<j))]));
    const add=(B,row)=>{while(row){let p=pivot(row);if(B[p])row^=B[p];else {B[p]=row;return true}}return false};
    const red=(B,row)=>{while(row){let p=pivot(row);if(!B[p])return row;row^=B[p]}return 0n};
    const times=(row,j)=>{let out=0n;while(row){let low=row&-row;out^=mult[j][pivot(low)];row^=low}return out};
    const affine=(mask,b)=>{let p=BigInt(b);for(let i=0;i<n;i++)if(mask>>i&1)p^=bits[idx.get(1<<i)];return p};
    const bad=(row,x)=>row.bad.includes(row.t.reduce((s,j,i)=>s+(((x>>j)&1)<<i),0));
    let fs=registry.map(row=>{let f=0n;for(let k=0;k<8;k++){let coeff=0;for(let s=k;;s=(s-1)&k){coeff^=+row.bad.includes(s);if(!s)break}if(coeff){let m=row.t.reduce((s,j,i)=>s|((k>>i&1)<<j),0);f^=bits[idx.get(m)]}}check(pivot(f)<lim&&mons[pivot(f)]!==undefined);check(mons.filter((_,i)=>((f>>BigInt(i))&1n)!==0n).every(m=>pc(m)<=2));return f});
    const B=[];for(const f of fs){add(B,f);for(let i=0;i<n;i++)add(B,times(f,i))}
    const staticRank=B.filter(Boolean).length;
    const staticRefuted=red(B,1n)===0n;
    const staticCuts=peer.filter(([m,b])=>red(B,affine(parseInt(m,16),b))===0n).length;
    // Explicit singleton closure on empty guard: each owner has full affine hull.
    let singletonScans=0;
    for(const row of registry){singletonScans++;let legal=Array.from({length:8},(_,i)=>i).filter(i=>!row.bad.includes(i));for(let m=1;m<8;m++)check(new Set(legal.map(x=>pc(x&m)%2)).size===2)}
    let products=0,rounds=0,insertions=0;
    // Complete degree-three saturation, allowing cancellation of high-degree terms in each multiplication image.
    while(red(B,1n)!==0n){rounds++;let changes=0;
      for(let j=0;j<n;j++){const H=[];for(const row of B.filter(Boolean)){let v=times(row,j);products++;while(v&&pivot(v)>=lim){let p=pivot(v);if(H[p])v^=H[p];else {H[p]=v;v=0n;break}}if(v&&add(B,v)){changes++;insertions++}}
        if(red(B,1n)===0n)break;
      }
      if(!changes)break;
    }
    let refuted=red(B,1n)===0n, count=0,witness=null,checks=0;
    for(let x=0;x<(1<<n);x++)if(!registry.some(r=>bad(r,x))){count++;witness??=x;for(const [m,b] of peer){check(pc(x&parseInt(m,16))%2===b);checks++}}
    check((count===0)===expected);check(!refuted||count===0);
    const finalCuts=peer.filter(([m,b])=>red(B,affine(parseInt(m,16),b))===0n).length;
    // On a refutation, later affine cuts need not themselves occur; this is a separate membership audit.
    return {tag,n,owners:registry.length,models:count,witness,staticRank,staticRefuted,staticCuts,peerCuts:peer.length,finalCuts,rank:B.filter(Boolean).length,refuted,rounds,products,insertions,singletonScans,peerModelChecks:checks};
  }
  const out=[];
  for(const c of rt.controls){let d=da.rt.find(z=>z.n===c.n);out.push(test(c.n,c.registry,d.alternating.accepted,true,"RT26 root"));
    let neighbor=c.registry.map((r,i)=>i?{...r}:{...r,bad:r.bad.map(v=>v^1)});
    out.push(test(c.n,neighbor,d.neighborAlternating.accepted,false,"RT26 first-owner first-sign neighbor"));
  }
  const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]].map(t=>({t,bad:[0,7]}));
  out.push(test(7,fano,[],true,"Fano root"));
  for(let i=0;i<7;i++)for(let j=0;j<3;j++)out.push(test(7,fano.map((r,k)=>k===i?{t:r.t,bad:r.bad.map(x=>x^(1<<j))}:r),[],false,"Fano sign neighbor "+i+":"+j));
  return {assertions,tests:out};
}
const fs=require('fs'); console.log(JSON.stringify(experiment(JSON.parse(fs.readFileSync(process.argv[2])),JSON.parse(fs.readFileSync(process.argv[3]))),null,2));
