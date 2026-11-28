const fs=require('node:fs');
const crypto=require('node:crypto');
const verify=function(C,a){
 const ck=(b,m)=>{if(!b)throw Error(m)},V=[...new Set(C.flat().map(Math.abs))].sort((a,b)=>a-b),B=a.boundary,D=a.demand.flatMap(x=>x.c),S=new Set(D);let checks=0;
 ck(S.size===D.length,"disjoint demand");ck(JSON.stringify(V.filter(v=>!S.has(v)))===JSON.stringify(B),"boundary");ck(a.demand.every(p=>JSON.stringify(C[p.i])===JSON.stringify(p.c)&&p.c.every(v=>v>0)),"positive demands");
 let flat=a.bins.flat();ck(flat.length===D.length&&new Set(flat).size===D.length&&flat.every(v=>S.has(v)),"bin partition");
 function exclusion(u,v){checks++;ck(C.some(c=>c.length===2&&c.includes(-u)&&c.includes(-v)),"missing exclusion "+u+" "+v)}
 let weights=Object.fromEntries(B.map(v=>[v,0]));for(let [j,bin] of a.bins.entries()){for(let i=0;i<bin.length;i++)for(let k=i+1;k<bin.length;k++)exclusion(bin[i],bin[k]);let t=a.blockers[j];if(t!==null){ck(B.includes(t),"selector");weights[t]++;for(let v of bin)exclusion(t,v)}}
 ck(JSON.stringify(weights)===JSON.stringify(a.weights),"weights");ck(a.capacity===a.bins.length-a.demand.length,"capacity");
 let deg=Object.fromEntries(B.map(v=>[v,0]));let consumer=new Set(a.consumer.map(p=>p.i));for(let p of a.consumer){ck(JSON.stringify(C[p.i])===JSON.stringify(p.c)&&p.c.every(v=>B.includes(v)),"consumer");for(let v of p.c)deg[v]++}
 const M=Math.max(1,...Object.values(deg)),lower=Math.max(0,Math.ceil((consumer.size-B.reduce((s,v)=>s+M-deg[v],0))/M));ck(lower===a.lower&&M===a.M,"rounded bound");
 let left=[],right=[],joint=[];for(let w=0;w<2**B.length;w++){let t=a.table.find(x=>x.w===w);ck(t,"coverage");let bit=v=>w>>B.indexOf(v)&1;let lhs=B.reduce((s,v)=>s+weights[v]*bit(v),0),r=[...consumer].every(i=>C[i].some(v=>bit(v)));ck(r===t.right&&lhs===t.weighted,"mask");if(r)right.push(w);if(t.witness){let A=new Map(V.map((v,i)=>[v,t.witness[i]]));ck(t.witness.length===V.length&&t.witness.every(x=>x===0||x===1)&&B.every(v=>A.get(v)===bit(v)),"witness boundary");for(let [i,c] of C.entries())if(!consumer.has(i)){checks++;ck(c.some(l=>A.get(Math.abs(l))===+(l>0)),"left witness")}ck(lhs<=a.capacity,"capacity witness");left.push(w);if(r){for(let c of C){checks++;ck(c.some(l=>A.get(Math.abs(l))===+(l>0)),"joint witness")}joint.push(w)}}else ck(lhs>a.capacity,"unproved exclusion")}
 for(let d of a.removals){let A=new Map(V.map((v,i)=>[v,d.word[i]]));for(let [i,c] of C.entries())if(i!==d.row){checks++;ck(c.some(l=>A.get(Math.abs(l))===+(l>0)),"deletion witness")}}
 ck(JSON.stringify(left)===JSON.stringify(a.leftSupport)&&JSON.stringify(right)===JSON.stringify(a.rightSupport)&&JSON.stringify(joint)===JSON.stringify(a.intersection),"joint support");
 const uniform=B.every(v=>weights[v]===1);ck(uniform&&left.every(w=>w.toString(2).replace(/0/g,"").length<=a.capacity),"count");
 for(let w=0;w<2**B.length;w++){let n=w.toString(2).replace(/0/g,"").length;ck(left.includes(w)===(n<=a.capacity)&&right.includes(w)===(n>=lower),"exact shell")}
 return {checks,left,right,joint,capacity:a.capacity,lower,verified:true,removalWitnesses:a.removals.length}
};
const a=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));if(a.instance_id!=='DIMACS-CNF-v1:sha256:'+crypto.createHash('sha256').update(a.dimacs).digest('hex')||a.original_N_bits!==Buffer.byteLength(a.dimacs)*8)throw Error('authentication');
const C=a.dimacs.trimEnd().split('\n').slice(1).map(l=>l.trim().split(/\s+/).map(Number).slice(0,-1));console.log(JSON.stringify(verify(C,a.proof)));
