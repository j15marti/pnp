function syndrome(F,pins,mode,K=4,cap=1500000){
 const C={restrict:0,groupScans:0,joinRows:0,transform:0,elimination:0,verify:0,ownerChecks:0,dp:0};let work=0;function tick(k,n=1){if(work+n>cap)throw Error("cap");C[k]+=n;work+=n}
 const A=new Map(pins),original=new Set(),fs=F.map(f=>{for(let o of f.ids){tick("ownerChecks");if(original.has(o))throw Error("duplicate owner");original.add(o)}let vs=f.vs.filter(v=>!A.has(v)),cost=Array.from({length:2**vs.length},(_,w)=>{tick("restrict");return f.cost[f.vs.reduce((s,v,j)=>s|((A.has(v)?A.get(v):(w>>vs.indexOf(v))&1)<<j),0)]});return {vs,cost,ids:f.ids,parts:[f.i]}}); 
 let groups=fs;
 const uni=(a,b)=>[...new Set([...a,...b])].sort((a,b)=>a-b);
 const idx=(vs,U,w)=>vs.reduce((s,v,j)=>s|(((w>>U.indexOf(v))&1)<<j),0);
 if(mode==="join"){let remain=fs.slice();groups=[];while(remain.length){let f=remain.shift(),best=-1,score=0;for(let j=0;j<remain.length;j++){tick("groupScans");let g=remain[j],u=uni(f.vs,g.vs),overlap=f.vs.length+g.vs.length-u.length;if(u.length<=5&&overlap>score){best=j;score=overlap}}if(best>=0){let g=remain.splice(best,1)[0],vs=uni(f.vs,g.vs);f={vs,cost:Array.from({length:2**vs.length},(_,w)=>{tick("joinRows");return f.cost[idx(f.vs,vs,w)]+g.cost[idx(g.vs,vs,w)]}),ids:[...f.ids,...g.ids],parts:[...f.parts,...g.parts]}}groups.push(f)}}
 const vars=uni([],groups.flatMap(f=>f.vs)),at=new Map(vars.map((v,i)=>[v,i]));
 let features=[],mon=new Map(),basis=new Map(),relations=[];
 const hi=x=>x.toString(2).length-1;
 const toggle=(a,k)=>{if(a.has(k))a.delete(k);else a.add(k)};
 const key=(vs,w)=>vs.filter((_,j)=>(w>>j)&1).join(",");
 for(let i=0;i<groups.length;i++){let f=groups[i],patterns=mode==="indicator"?[-1]:f.cost.map((c,w)=>c>0?w:-1).filter(w=>w>=0);
 for(let row of patterns){let val=f.cost.map((c,w)=>Number(row<0?c>0:w===row)),p=val.slice();for(let j=0;j<f.vs.length;j++)for(let w=0;w<p.length;w++)if(w>>j&1){tick("transform");p[w]^=p[w^(1<<j)]}
 let z=0n;for(let w=1;w<p.length;w++)if(p[w]){let k=key(f.vs,w);if(!mon.has(k))mon.set(k,mon.size);z^=1n<<BigInt(mon.get(k))}
 let b=p[0],proof=1n<<BigInt(features.length),id=features.length;features.push({group:i,row,b});
 while(z){let j=hi(z);if(!basis.has(j)){basis.set(j,{z,b,proof});break}let q=basis.get(j);z^=q.z;b^=q.b;proof^=q.proof;tick("elimination")}
 if(!z){let terms=[];for(let j=0;j<=id;j++){tick("elimination");if(proof>>BigInt(j)&1n)terms.push(j)}relations.push({b,terms})}
 }}
 // Select <= 12 identity rows. Keep every constant-one identity first, then zero ones; prioritize removal of single-owner feasible rows.
 let selected=[],masks=features.map(()=>0),target=0;
 function stateCost(m,t){let good=0;for(let i=0;i<features.length;i++){tick("dp");if(m[i]===t)good++}return good}
 let pending=relations.slice();while(selected.length<12&&pending.length){let best=-1,score=Infinity;
 for(let j=0;j<pending.length;j++){let q=pending[j],S=new Set(q.terms),cnt=0;for(let i=0;i<features.length;i++){tick("dp");if(masks[i]===target&&Number(S.has(i))===q.b)cnt++}let rank=cnt+(selected.length===0&&!q.b?features.length+1:0);if(rank<score){score=rank;best=j}}
 let q=pending.splice(best,1)[0],bit=1<<selected.length;for(let j of q.terms)masks[j]|=bit;if(q.b)target|=bit;selected.push(q);
 if(target&&stateCost(masks,target)===0)break;
 }
 // Independently verify selected identities with direct subset expansion, not fast Mobius.
 for(let q of selected){let out=new Set();for(let id of q.terms){let {group,row}=features[id],f=groups[group];for(let w=0;w<f.cost.length;w++){let p=0;for(let t=w;;t=(t-1)&w){tick("verify");p^=Number(row<0?f.cost[t]>0:t===row);if(t===0)break}if(p)toggle(out,key(f.vs,w))}}if(out.size!==q.b||(q.b&&!out.has("")))throw Error("identity replay")}
 // DP with one choice per owner group, compressed costs at K.
 let D=new Int32Array(1<<selected.length).fill(K);D[0]=0;let opts=groups.map(()=>new Map([[0,0]]));for(let i=0;i<features.length;i++){let {group,row}=features[i],f=groups[group],v=row<0?Math.min(...f.cost.filter(c=>c>0)):f.cost[row],s=masks[i];if(v<(opts[group].get(s)??K))opts[group].set(s,v)}
 // zero-cost option can be relaxed even if all rows positive: lower bound only; exact when feasible zero row.
 for(let o of opts){let T=new Int32Array(D.length).fill(K);for(let j=0;j<D.length;j++)for(let [s,c] of o){tick("dp");T[j^s]=Math.min(T[j^s],D[j]+c,K)}D=T}
 return {mode,pins,work,counters:C,groups:groups.map(g=>({vs:g.vs,ids:g.ids,parts:g.parts,cost:g.cost})),features,selected,allRelations:relations.length,rank:basis.size,target,lower:D[target],states:D.length,peakPayloadBits:D.length*64+features.length*32};
}
function feedback(C,vs,start,mode){let A=new Map(vs.map(v=>[v,start])),reads=0,changed=0,steps=0,trace=[];function score(){let bad=0,zero=0;for(let c of C){let k=0,d=0;for(let l of c){reads++;let x=A.get(Math.abs(l));let s=l>0?x:x-1;k+=s*s;d+=s}let r=k%3,z=(d%3+3)%3;if(k===0)bad++;else if(z===0)zero++}return [bad,zero]}let q=score();trace.push(q);while(steps<vs.length*4){let best=q[0],cands=[];for(let v of vs){A.set(v,1-A.get(v));let z=score();A.set(v,1-A.get(v));if(z[0]<best){best=z[0];cands=[]}if(z[0]===best&&best<q[0])cands.push([v,z])}if(!cands.length)break;let chosen=cands[0];if(mode===2){chosen=cands.slice().sort((a,b)=>a[1][1]-b[1][1]||a[0]-b[0])[0];if(chosen[0]!==cands[0][0])changed++}A.set(chosen[0],1-A.get(chosen[0]));q=chosen[1];trace.push(q);steps++}return {start,mode,steps,changed,reads,final:q,trace}}
function experiment(ins,entry,G,ctx){
 const {chart,V,guards,n,trace}=ctx;
 let initial=ctx.support(chart),affine=ctx.affine(chart,[]),matching=ctx.matching(chart,[]);let lanes=[],cells=[[],...guards];
 for(let ps of cells){let o=ctx.support(chart,ps),a=ctx.affine(chart,ps),m=ctx.matching(chart,ps),b=ctx.bucket(chart,ps,150000),t=ctx.core(chart,ps,100000);let arms=[];for(let mode of ["indicator","rows","join"]){try{let z=syndrome(chart,ps,mode);arms.push(z)}catch(e){arms.push({mode,status:"UNKNOWN",error:String(e),cap:1500000})}}lanes.push({pins:ps,occupancy:o,affine:a,matching:m,bucket:b,tree:t,arms})}
 let intersections=[];for(let mask=1;mask<32;mask++){let P=new Map(),bad=false;for(let i=0;i<5;i++)if(mask>>i&1)for(let [v,x] of guards[i]){if(P.has(v)&&P.get(v)!==x)bad=true;P.set(v,x)}intersections.push(bad?"0":String(1n<<BigInt(V.length-P.size)))}
 let count=intersections.reduce((s,x,i)=>s+(((i+1).toString(2).match(/1/g)||[]).length%2?1n:-1n)*BigInt(x),0n);if(count!==1n<<BigInt(V.length))throw Error("coverage");
 const rawC=ins.dimacs.trimEnd().split("\n").slice(1).map(x=>x.split(/\s+/).map(Number).slice(0,-1));
 const cnfProof=E.proofSearch(rawC,100000),cnfF=rawC.map((ls,i)=>{let vs=[...new Set(ls.map(Math.abs))].sort((a,b)=>a-b);return {vs,cost:Array.from({length:2**vs.length},(_,w)=>2*Number(!ls.some(l=>((w>>vs.indexOf(Math.abs(l)))&1)===Number(l>0)))),ids:[i+1],i}});
 let cnfArms=[];for(let mode of ["indicator","rows","join"]){try{cnfArms.push(syndrome(cnfF,[],mode))}catch(e){cnfArms.push({mode,status:"UNKNOWN",error:String(e),cap:1500000})}}
 let cf=E.asCNF(chart).clauses,fb=[];for(let [C,vs,label] of [[rawC,Array.from({length:ins.nvars},(_,i)=>i+1),"CNF"],[cf,V.map(v=>v+1),"native"]])for(let start of [0,1])for(let mode of [0,1,2])fb.push({label,...feedback(C,vs,start,mode)});
 let w=E.witness(chart,100000,2,137),lift=E.lift(G,n,trace,w);
 return {initial,affine,matching,lanes,intersections,cnfProof,cnfArms,feedback:fb,witness:{...w,defects:lift.defects},normal:ctx.normalCost,chartHash:ctx.chartHash,mapHash:ctx.mapHash,gauge:ctx.gauge,vars:V,trace};
}
module.exports={syndrome,feedback,experiment};
