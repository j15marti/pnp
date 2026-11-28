// Run with node spectral-scan.js compile.js benchmarks.json checker.js
const fs=require('node:fs');const src=fs.readFileSync(process.argv[2],'utf8');const compile=new Function('return '+src.slice(src.indexOf('function compile'),src.indexOf('function auditLocal')))();const checker=fs.readFileSync(process.argv[4],'utf8');const {native,sha,spectral2}=new Function(checker.slice(checker.indexOf('function sha'),checker.indexOf('const data=JSON.parse'))+'\nreturn {native,sha,spectral2}')();
function reclose(G,seeds){
let extra=seeds.slice(),steps=[],tests=0;
for(let pass=0;pass<100;pass++){
let C=native({...G,edges:G.edges.concat(extra)}),newFacts=new Map();
for(let r of C.tables){tests+=r.words.length;if(!r.words.length)return {C,extra,steps,tests,terminal:r.v};
for(let i=0;i<r.ids.length;i++)for(let j=i+1;j<r.ids.length;j++){
let h=((r.words[0]>>i)^(r.words[0]>>j))&1;if(r.words.every(w=>(((w>>i)^(w>>j))&1)===h)){
let p=[C.roots[r.ids[i]],C.roots[r.ids[j]],h];newFacts.set(p.join(","),{p,vertex:r.v,ids:r.ids,words:r.words})}}}
if(!newFacts.size)return {C,extra,steps,tests,terminal:null};let arr=[...newFacts.values()];steps.push(arr);extra.push(...arr.map(x=>x.p));
}throw Error("closure cap")
}
function scan(C,cap=4000000){
let rr=[],seen=new Set();for(let {v,lits} of C.rows){let m=new Map();for(let [i,s] of lits)m.set(i,(m.get(i)||0)+(s?-1:1));let a=[...m].filter(x=>x[1]).sort((a,b)=>a[0]-b[0]);if(!a.length)continue;if(a[0][1]<0)a=a.map(([i,c])=>[i,-c]);let k=JSON.stringify(a);if(!seen.has(k)){seen.add(k);rr.push({v,a})}}
let pairs=0,proj=0,wordTests=0,checks=0,exact=new Set(),l2=new Set(),l1=new Set(),no=0,certs=[],psd=0,capHit=false;
outer:for(let i=0;i<rr.length;i++)for(let j=i+1;j<rr.length;j++){
let a=rr[i],b=rr[j];if(!a.a.some(x=>b.a.some(y=>x[0]===y[0])))continue;pairs++;
let ids=[...new Set(a.a.concat(b.a).map(x=>x[0]))].sort((a,b)=>a-b),u=ids.map(i=>a.a.find(x=>x[0]===i)?.[1]||0),v=ids.map(i=>b.a.find(x=>x[0]===i)?.[1]||0),k=ids.length,W=[];
for(let w=0;w<2**k;w++){wordTests++;if([u,v].every(q=>q.reduce((s,x,i)=>s+x*((w>>i&1)?-1:1),0)===0))W.push(w)}
if(!W.length){no++;continue}for(let x=0;x<k;x++)for(let y=x+1;y<k;y++){
let h=((W[0]>>x)^(W[0]>>y))&1;if(W.every(w=>(((w>>x)^(w>>y))&1)===h))exact.add([ids[x],ids[y],h].join(","))
}
let aa=u.reduce((z,x)=>z+x*x,0),bb=v.reduce((z,x)=>z+x*x,0),ab=u.reduce((z,x,i)=>z+x*v[i],0),D=aa*bb-ab*ab;if(!D)continue;
for(let x=0;x<k;x++){
let cu=u[x],cv=v[x],al=bb*cu-ab*cv,be=aa*cv-ab*cu,r=u.map((t,i)=>D*Number(i===x)-al*t-be*v[i]);if(r.reduce((s,t)=>s+Math.abs(t),0)<D)psd++;
for(let y=x+1;y<k;y++)for(let h=0;h<2;h++){
if(++proj>cap){capHit=true;break outer}let s=h?1:-1,cu=u[x]+s*u[y],cv=v[x]+s*v[y],al=bb*cu-ab*cv,be=aa*cv-ab*cu,r=u.map((t,i)=>D*(Number(i===x)+s*Number(i===y))-al*t-be*v[i]),L=r.reduce((s,t)=>s+Math.abs(t),0),Q=k*r.reduce((s,t)=>s+t*t,0),key=[ids[x],ids[y],h].join(",");
if(Q<4*D*D)l2.add(key);if(L<2*D){l1.add(key);checks+=W.length;if(!W.every(w=>(((w>>x)^(w>>y))&1)===h))throw Error("spectral");if(certs.length<12){let c=Array(k).fill(0);c[x]=1;c[y]=s;let z=spectral2(u,v,c);if(z.l1!==L||z.l2num!==Q)throw Error("checker mismatch");certs.push({vertices:[a.v,b.v],ports:ids.map(i=>C.roots[i]),fact:[C.roots[ids[x]],C.roots[ids[y]],h],u,v,c,z})}}}
}
}
return {rows:rr.length,pairs,proj,wordTests,exact:exact.size,l2:l2.size,l1:l1.size,checks,no,psd,capHit,certs}
}
function test(inst,seed=[]){let G=compile(inst).network,bytes=JSON.stringify(G)+"\n",C=reclose(G,seed),s=C.terminal===null?scan(C.C):null;return {id:inst.id,digest:sha(bytes),N:bytes.length*8,seeds:seed,carriers:C.C.n,closureRounds:C.steps.map(x=>x.length),closureTests:C.tests,closureTerminal:C.terminal,scan:s}}
const data=JSON.parse(fs.readFileSync(process.argv[3],'utf8'));const j=data.instances.find(x=>x.id==='JOINT-24'),r=data.instances.find(x=>x.id==='RANDOM-3CNF-40'),seed=[[0,433,0],[0,561,0],[0,960,1],[0,969,0]];console.log(JSON.stringify([test(j),test(r),test(j,seed),test({"id":"SAT-1","nvars":3,"dimacs":"p cnf 3 2\n1 2 3 0\n-1 2 -3 0\n"}),test({"id":"SAT-2","nvars":2,"dimacs":"p cnf 2 2\n1 0\n-1 2 0\n"})],null,2));
