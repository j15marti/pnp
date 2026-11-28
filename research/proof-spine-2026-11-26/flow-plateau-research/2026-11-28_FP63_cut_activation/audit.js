function audit(ctx,record){
 const {chart:F,V}=ctx,ct={regional:0,parity:0,rank:0,closure:0,proof:0},cap=2200000,tick=(k,n=1)=>{if(Object.values(ct).reduce((a,b)=>a+b,0)+n>cap)throw Error("cap");ct[k]+=n},zero=F.map(f=>f.cost.map((x,w)=>x===0?w:-1).filter(w=>w>=0)),pop=x=>{let p=0;while(x){p^=1;x&=x-1}return p};
 // Independently construct incidence coordinates and use low-pivot elimination.
 let incidence=new Map(V.map(v=>[v,[]]));F.forEach((f,i)=>f.vs.forEach((v,j)=>incidence.get(v).push([i,j])));let next=0,mask=F.map(f=>f.vs.map(()=>0n));
 for(let O of incidence.values())for(let j=1;j<O.length;j++){let b=1n<<BigInt(next++);for(let [i,t] of [O[0],O[j]])mask[i][t]^=b}
 function GE(vecs){let B=new Map();for(let x of vecs){while(x){tick("rank");let p=x&(-x);if(!B.has(p)){B.set(p,x);break}x^=B.get(p)}}return B.size}
 const encode=(i,w)=>mask[i].reduce((z,b,j)=>z^((w&(1<<j))?b:0n),0n);
 function cutRank(S){let D=S.map((a,i)=>a.map(w=>encode(i,w)^encode(i,a[0])));return record.cuts.map(c=>{let P=new Set(c),a=D.flatMap((v,i)=>P.has(i)?v:[]),b=D.flatMap((v,i)=>P.has(i)?[]:v);return GE(a)+GE(b)-GE([...a,...b])})}
 function equations(S){let A=[];for(let i=0;i<F.length;i++){let a=S[i];if(!a.length){A.push({i,vs:[],rhs:1});continue}let f=F[i],B=[];for(let w=1;w<2**f.vs.length;w++){let b=pop(w&a[0]),ok=true;for(let x of a){tick("parity");if(pop(w&x)!==b){ok=false;break}}if(ok)B.push({i,vs:f.vs.filter((_,j)=>w>>j&1),rhs:b})}A.push(...B)}return A}
 function affineClosure(S){let A=new Map(),round=0,eqs=equations(S);while(true){round++;let B=new Map(),at=new Map(V.map((v,i)=>[v,i])),contradiction=false;for(let q of eqs){let rhs=q.rhs,x=0n;for(let v of q.vs){if(A.has(v))rhs^=A.get(v);else x^=1n<<BigInt(at.get(v))}while(x){tick("closure");let p=x&(-x);if(!B.has(p)){B.set(p,[x,rhs]);break}let [y,b]=B.get(p);x^=y;rhs^=b}if(!x&&rhs){contradiction=true;break}}
 if(contradiction)return {status:"UNSAT",round,pins:[...A],eqs};
 // Extract singleton rows by reverse echelon.
 let rows=[...B].sort((a,b)=>a[0]>b[0]?-1:1),done=[];for(let [p,[x,b]] of rows){for(let [z,y,t] of done){tick("closure");if(x&z){x^=y;b^=t}}done.push([p,x,b]);if(x===p){let j=p.toString(2).length-1;A.set(V[j],b)}}
 let change=false;for(let i=0;i<F.length;i++){let f=F[i],a=S[i].filter(w=>{tick("closure");return f.vs.every((v,j)=>!A.has(v)||A.get(v)===((w>>j)&1))});if(!a.length)return {status:"UNSAT",round,pins:[...A],eqs};for(let [j,v] of f.vs.entries())if(!A.has(v)&&a.every(w=>((w>>j)&1)===((a[0]>>j)&1))){A.set(v,(a[0]>>j)&1);change=true}}
 // Check whether newly forced bits are already incorporated: rebuild with pins and continue only on growth.
 if(!change)return {status:"UNKNOWN",round,pins:[...A],eqs};
 }
 }
 let baseRank=cutRank(zero),baseEq=equations(zero),arms=[];
 for(let a of record.arms){let S=zero.map(v=>v.slice()),rem=0;
 for(let c of a.cert){let owners=F.map((f,i)=>f.vs.every(v=>c.U.includes(v))?i:-1).filter(i=>i>=0);if(owners.join()!==c.owners.join())throw Error("scope owners");let allowed=owners.map(()=>new Set()),min=Infinity;
 for(let w=0;w<2**c.U.length;w++){let bits=c.U.map((_,j)=>(w>>j)&1),words=owners.map(i=>F[i].vs.reduce((z,v,j)=>z+bits[c.U.indexOf(v)]*2**j,0));let e=0;words.forEach((q,j)=>{tick("regional");e+=F[owners[j]].cost[q]});min=Math.min(min,e);if(!e)words.forEach((q,j)=>allowed[j].add(q))}
 if(min!==c.min)throw Error("min mismatch");for(let [i,w] of c.removed){if(!S[i].includes(w)||allowed[owners.indexOf(i)].has(w))throw Error("bad row");S[i]=S[i].filter(x=>x!==w);rem++}}
 let rank=cutRank(S);if(a.after&&rank.some((w,j)=>w!==a.after[j].width))throw Error("rank mismatch");let affine=affineClosure(S);let changes=affine.eqs.filter(q=>!baseEq.some(b=>b.i===q.i&&b.rhs===q.rhs&&b.vs.join()===q.vs.join()));
 // Actual new constraints are zero-energy-only, never used as changed positive energy costs.
 let H=F.map((f,i)=>({...f,cost:f.cost.map((x,w)=>x===0&&!S[i].includes(w)?1:x)}));
 let t=ctx.core(H,[],100000);tick("proof",(t.s.scans||0)+(t.ck?.rows||0)+(t.ck2?.rows||0));
 arms.push({name:a.name,rem,rank,affine:{status:affine.status,round:affine.round,pins:affine.pins,eqs:affine.eqs.length,newEquations:changes},proof:t});
 }
 // Parent removal: each source-growth regional certificate ablated separately, with original rows retained where possible.
 let growth=record.arms.find(a=>a.name==="source-growth"),ablation=[];
 for(let drop=0;drop<growth.cert.length;drop++){let S=zero.map(v=>v.slice());for(let [j,c] of growth.cert.entries())if(j!==drop)for(let [i,w] of c.removed)S[i]=S[i].filter(x=>x!==w);let rank=cutRank(S);ablation.push({drop,rank})}
 return {baseRank,baseEq,arms,ablation,ct,cap};
}
if(typeof module!=="undefined")module.exports={audit};
