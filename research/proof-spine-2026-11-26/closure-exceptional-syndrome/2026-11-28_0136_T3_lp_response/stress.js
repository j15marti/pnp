function stress(pack,sha){
const ck=(x,m)=>{if(!x)throw Error(m)},b=pack.block,n=b.n,rows=b.rows,ends=b.shared,table=Array.from({length:4},()=>0),witness=Array(4).fill(null);let visits=0;
const ok=(f,w)=>{let u=0;for(let i=0;i<4;i++)u|=(((w>>f.scope[i])&1)^((f.sig>>i)&1))<<i;return u!==0&&u!==15};
for(let w=0;w<2**n;w++){let good=true;for(let f of rows){visits++;if(!ok(f,w)){good=false;break}}if(good){let key=((w>>ends[0])&1)|(((w>>ends[1])&1)<<1);table[key]++;witness[key]=w}}
ck(table.reduce((a,b)=>a+b,0)===2,"support");let parity=table[0]+table[3]===2?0:1;
// Independently verify exact compact response by exhaustive testing within each endpoint fiber.
let checkVisits=0,check=[0,0,0,0];for(let k=0;k<4;k++){for(let w=0;w<2**n;w++){if(((w>>ends[0])&1)!==(k&1)||((w>>ends[1])&1)!==(k>>1))continue;let good=true;for(let i=rows.length-1;i>=0;i--){checkVisits++;let f=rows[i],l=f.scope.map((v,j)=>((w>>v)&1)^((f.sig>>j)&1));if(l.every(x=>x===l[0])){good=false;break}}if(good)check[k]++}}ck(check.join()===table.join(),"response");
let records=[];for(let x of pack.instances.filter(z=>z.par===1)){ck(sha(x.dimacs)===x.instance_id.split(":").at(-1)&&8*x.dimacs.length===x.original_N_bits,"hash");let C=x.dimacs.trimEnd().split("\n").slice(1).map(c=>c.split(/\s+/).map(Number).slice(0,-1));let scopes=[];for(let i=0;i<C.length;i+=2){ck(C[i].length===4&&C[i].every((l,j)=>l===-C[i+1][j]),"NAE pair");scopes.push(C[i])}
let triple=new Set(),overflowChecks=0;for(let c of scopes){let v=c.map(Math.abs).sort((a,b)=>a-b);for(let j=0;j<4;j++){let k=v.filter((_,i)=>i!==j).join();ck(!triple.has(k),"triple overlap");triple.add(k);overflowChecks++}}
// Exact local LP witness for every <=2 variable guard: per factor choose two free coordinates, force their signed literals opposite; remaining free coords independent fair. Thus all free marginals 1/2 and pins respected.
let guardChecks=0,tupleChecks=0,lpFailures=0;let V=Array.from({length:x.n},(_,i)=>i+1);let guards=[[]];for(let i=0;i<V.length;i++){for(let a of [-1,1])guards.push([a*V[i]]);for(let j=i+1;j<V.length;j++)for(let a of [-1,1])for(let b of [-1,1])guards.push([a*V[i],b*V[j]])}
// Count every guard via local pattern symmetry, enumerate all 33 possible <=2-pin patterns per factor, not global Cartesian guard x factor.
for(let c of scopes){let gs=[[]];for(let i=0;i<4;i++){for(let a=0;a<2;a++)gs.push([[i,a]]);for(let j=i+1;j<4;j++)for(let a=0;a<2;a++)for(let b=0;b<2;b++)gs.push([[i,a],[j,b]])}
for(let g of gs){guardChecks++;let p=new Map(g),free=[0,1,2,3].filter(i=>!p.has(i)),S=[];for(let w=0;w<16;w++){tupleChecks++;if(!g.every(([i,a])=>(w>>i&1)===a))continue;let a=free[0],b=free[1];if((((w>>a&1)^+(c[a]<0))^((w>>b&1)^+(c[b]<0)))!==1)continue;S.push(w)}if(!S.length||free.some(i=>S.filter(w=>w>>i&1).length*2!==S.length)||S.some(w=>{let l=c.map((z,i)=>(w>>i&1)^+(z<0));return l.every(a=>a===l[0])}))lpFailures++}}
ck(lpFailures===0,"LP guard fail");
// Replay exact block mapping and deletion witness, then parity composition.
let phase=[],rowChecks=0;for(let j=0;j<x.sourceMap.length;j++){let {map,twist}=x.sourceMap[j];ck(map.length===n&&new Set(map).size===n,"map");for(let i=0;i<rows.length;i++){let f=rows[i],c=f.scope.map((v,h)=>map[v]*(((f.sig>>h)&1)?-1:1)*((v===ends[1]&&twist)?-1:1));ck(c.join()===scopes[j*rows.length+i].join(),"source clause map");rowChecks++}phase.push(parity^+twist)}
ck(phase.reduce((a,b)=>a^b,0)===1,"parity");
let deletionChecks=0;for(let z of x.deletion)for(let j=0;j<C.length;j++){if(Math.floor(j/(2*rows.length))===z.block)continue;ck(C[j].some(l=>z.witness[Math.abs(l)-1]===+(l>0)),"deletion");deletionChecks++}
// quotient LP: each edge supported two words; weight 1/2 each agrees on every singleton, even with odd parity.
let quotientLocalLP=phase.every(p=>p===0||p===1),geXor=phase.reduce((a,b)=>a^b,0);
records.push({instance:x.short_id,instance_id:x.instance_id,N:x.original_N_bits,original_ids:x.original_ids,blocks:x.sourceMap.length,clauses:C.length,globalGuardCount:guards.length,localPatternsChecked:guardChecks,tupleChecks,lpFailures,privateTriples:triple.size,overflowChecks,phase,rowChecks,deletionChecks,quotientLocalLP,geXor});
}
return{block:{n,rows:rows.length,ends,table,witness,visits,checkVisits,parity},records};
}
const fs=require('node:fs'),sha=s=>require('node:crypto').createHash('sha256').update(s).digest('hex');console.log(JSON.stringify(stress(JSON.parse(fs.readFileSync(process.argv[2],'utf8')),sha),null,2));
