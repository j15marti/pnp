const fs=require('node:fs');
function experiment(raws){
const [co,corp,reg,helper,...peers]=raws;
const compile=Function(co.slice(co.indexOf("function compile"),co.indexOf("function auditLocal"))+";return compile")();
const H=Function(helper.slice(0,helper.indexOf("function runCase"))+";return {sha,normalize,independentNormalize,eliminate,verifyTrace,gauge}")();
const assert=(x,m)=>{if(!x)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const pop=x=>{let n=0;while(x){x&=x-1n;n++}return n}, high=x=>x.toString(2).length-1, bit=i=>1n<<BigInt(i);
assert(H.sha("abc")==="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad","hash");
const pin=(F,v,b)=>F.map(f=>{let i=f.vs.indexOf(v);return i<0?f:{...f,vs:f.vs.filter(x=>x!==v),ok:f.ok.filter(w=>(w>>i&1)===b).map(w=>(w&((1<<i)-1))|((w>>(i+1))<<i))}});
function closure(F){let pins=[],scans=0;for(;;){if(F.some(f=>!f.ok.length))return {F,pins,scans,conflict:true};let hit=null;outer:for(const f of F){for(let i=0;i<f.vs.length;i++){let b=f.ok[0]>>i&1;let same=f.ok.every(w=>{scans++;return (w>>i&1)===b});if(same){hit=[f.vs[i],b,f.id];break outer}}}if(!hit)return {F,pins,scans,conflict:false};pins.push(hit);F=pin(F,hit[0],hit[1])}}
function fromClause(c,id){let vs=[...new Set(c.map(Math.abs))].sort((a,b)=>a-b),ok=[];assert(vs.length<=10,"clause scope");for(let w=0;w<2**vs.length;w++)if(c.some(l=>(w>>vs.indexOf(Math.abs(l))&1)===+(l>0)))ok.push(w);return{id,vs,ok}}
function span(F,D,cap=2000000){
let V=[...new Set(F.flatMap(f=>f.vs))].sort((a,b)=>a-b), ix=new Map(V.map((v,i)=>[v,i])), mono=[0n], index=new Map([[0n,0]]), basis=new Map(), rows=[],meta=[],xor=0,localChecks=0,multiples=0;
function enc(m){if(!index.has(m)){index.set(m,mono.length);mono.push(m)}return bit(index.get(m))}
function add(row,desc){let id=rows.length;rows.push(row);meta.push(desc);let v=row,p=bit(id);while(v){let i=high(v);if(!basis.has(i)){basis.set(i,[v,p]);return}let [r,q]=basis.get(i);v^=r;p^=q;if(++xor>cap)throw Error("cap")}}
function reduce(v){let p=0n,out=0n;while(v){let i=high(v);if(basis.has(i)){let [r,q]=basis.get(i);v^=r;p^=q}else{out^=bit(i);v^=bit(i)}}return[out,p]}
try{
for(const f of F){let k=f.vs.length;assert(k<=10,"scope");let local=[],LB=new Map(),basisPolys=[];
for(let m=0;m<2**k;m++){if(pop(BigInt(m))>D)continue;let ev=0n;for(let j=0;j<f.ok.length;j++){localChecks++;if((f.ok[j]&m)===m)ev|=bit(j)}
let pol=bit(m);while(ev){let i=high(ev);if(!LB.has(i)){LB.set(i,[ev,pol]);break}let [a,b]=LB.get(i);ev^=a;pol^=b}if(!ev){let terms=[];for(let j=0;j<2**k;j++)if(pol&bit(j))terms.push(j);basisPolys.push(terms)}}
for(let P of basisPolys){let deg=Math.max(...P.map(m=>pop(BigInt(m)))),T=P.map(m=>f.vs.reduce((a,v,j)=>a|((m>>j&1)?bit(ix.get(v)):0n),0n));
let max=D-deg;
function gen(start,m,r){let row=0n;for(let t of T)row^=enc(t|m);multiples++;add(row,{factor:f.id,local:P,mult:V.filter((v,i)=>m&bit(i))});if(r===0)return;for(let i=start;i<V.length;i++)gen(i+1,m|bit(i),r-1)}
gen(0,0n,max);
}}
let [r,p]=reduce(1n);if(!r){let terms=[];let sum=0n;for(let i=0;i<rows.length;i++)if(p&bit(i)){sum^=rows[i];terms.push(meta[i])}assert(sum===1n,"primal replay");return{status:"UNSAT",D,n:V.length,rank:basis.size,monomials:mono.length,rows:rows.length,xor,localChecks,multiples,terms}}
let free=high(r),lam=bit(free);for(let i of [...basis.keys()].sort((a,b)=>a-b)){let v=basis.get(i)[0]^bit(i);if(pop(v&lam)%2)lam|=bit(i)}
assert((lam&1n)===1n,"dual constant");for(let row of rows)assert(pop(row&lam)%2===0,"dual row");
let dual=[];for(let i=0;i<mono.length;i++)if(lam&bit(i))dual.push(V.filter((v,j)=>mono[i]&bit(j)));
return {status:"UNKNOWN",D,n:V.length,rank:basis.size,monomials:mono.length,rows:rows.length,xor,localChecks,multiples,dual,dualChecks:rows.length}
}catch(e){if(String(e).includes("cap"))return{status:"UNKNOWN cap",D,n:V.length,rank:basis.size,rows:rows.length,xor,localChecks,multiples};throw e}}
function rup(F,proof){let M=new Map();for(const f of F)for(let w=0;w<2**f.vs.length;w++)if(!f.ok.includes(w)){let c=f.vs.map((v,i)=>(w>>i&1)?-v:v);M.set(c.join(),c)}let C=[...M.values()],scans=0;
for(let q of proof){assert(q.kind==="UP","rule");let A=new Map(q.clause.map(l=>[Math.abs(l),+(l<0)])),fail=false;for(;;){let u=0;for(let c of C){scans++;if(c.some(l=>A.get(Math.abs(l))===+(l>0)))continue;let a=c.filter(l=>!A.has(Math.abs(l)));if(!a.length){fail=true;break}if(a.length===1){u=a[0];break}}if(fail||!u)break;A.set(Math.abs(u),+(u>0))}assert(fail,"RUP");C.push(q.clause)}assert(proof.at(-1).clause.length===0,"terminal");return scans}
function cluster(F){
 const C=new Map(),key=c=>c.slice().sort((a,b)=>a-b).join(),counters={partial:0,wordChecks:0,pairChecks:0,directWords:0,skipped:0};
 const add=(c,parent)=>{let k=key(c);if(!C.has(k))C.set(k,{c,parent})};
 for(const f of F){let n=f.vs.length;if(n>10)throw Error("cluster scope");if(f.ok.length===2**n-1){let S=new Set(f.ok),bad=0;while(S.has(bad)){bad++;counters.directWords++}add(f.vs.map((v,i)=>(bad>>i&1)?-v:v),f.id);continue}if(n>7){counters.skipped++;continue}
 for(let p=0;p<3**n;p++){let c=[],m=p;for(let i=0;i<n;i++){let t=m%3;m=(m-t)/3;if(t)c.push((t===1?1:-1)*f.vs[i])}if(c.length<2)continue;counters.partial++;if(f.ok.every(w=>{counters.wordChecks++;return c.some(l=>(w>>f.vs.indexOf(Math.abs(l))&1)===+(l>0))}))add(c,f.id)}}
 let added=[],cert=[];
 for(let {c,parent} of C.values()){if(c.length<3)continue;let P=[],hit=true;outer:for(let i=0;i<c.length;i++)for(let j=i+1;j<c.length;j++){counters.pairChecks++;let q=C.get(key([-c[i],-c[j]]));if(!q){hit=false;break outer}P.push(q)}
 if(!hit)continue;let vs=c.map(Math.abs).sort((a,b)=>a-b),ok=[];for(let w=0;w<2**vs.length;w++)if(c.filter(l=>(w>>vs.indexOf(Math.abs(l))&1)===+(l>0)).length===1)ok.push(w);let id="EO"+added.length;added.push({id,vs,ok});cert.push({id,c,parent,pairs:P});
 }
 return {F:[...F,...added],cert,counters};
}
const B=JSON.parse(corp),R=JSON.parse(reg),out=[];
for(let k=0;k<2;k++){let id=["JOINT-24","RANDOM-3CNF-40"][k],x=B.instances.find(z=>z.id===id),e=R.instances.find(z=>z.alias==="EB-"+id),g=compile(x),s=JSON.stringify(g.network)+"\n",map=JSON.stringify(g.source_map)+"\n";assert(H.sha(s)===e.sha256&&s.length*8===e.N_bits&&H.sha(x.dimacs)===e.source_cnf.sha256&&x.dimacs.length*8===e.source_cnf.N_bits&&H.sha(map)===e.source_map_sha256,"source");
let A=H.normalize(g.network),I=H.independentNormalize(g.network);assert(eq(A.fs,I.fs),"normalizers");let initial=closure(A.fs),v=H.gauge(A.fs);assert(A.fs.every(f=>f.ok.every(w=>f.ok.includes(w^(2**f.vs.length-1)))),"gauge");
let E=H.eliminate(pin(A.fs,v,0),false),Q=H.verifyTrace(pin(I.fs,v,0),E.trace);assert(eq(E.fs,Q.fs),"projection");let close=closure(Q.fs);let N=cluster(close.F);let native=[span(N.F,2),span(N.F,3)];let C=x.dimacs.trimEnd().split("\n").slice(1).map((l,i)=>fromClause(l.split(/\s+/).map(Number).slice(0,-1),i+1)),cc=closure(C),CN=cluster(cc.F),cnf=[span(CN.F,2),span(CN.F,3)];
let p=JSON.parse(peers[k]);assert(p.instance_id===e.instance_id&&p.guard_id==="EMPTY"&&p.residual_id==="ROOT"&&p.original_N_bits===e.N_bits&&p.gauge===v&&eq(p.trace,E.trace),"peer source");let peerChecks=rup(Q.fs,p.proof),prefix=p.proof.slice(0,3);assert(prefix.every(q=>q.clause.length>0),"prefix");let hc=closure([...Q.fs,...prefix.map((q,j)=>fromClause(q.clause,-j-1))]),HC=cluster(hc.F),hybrid=[span(HC.F,2),span(HC.F,3)];
out.push({entry:e,gauge:v,initial:{pins:initial.pins,scans:initial.scans},closure:{pins:close.pins,scans:close.scans},projection:{count:E.trace.length,checks:E.checks,scans:E.scans,verifyTests:Q.tests,verifyScans:Q.scans},native,cnf,clusters:{native:{cert:N.cert,counters:N.counters},cnf:{cert:CN.cert,counters:CN.counters},hybrid:{cert:HC.cert,counters:HC.counters}},peer:{sha:H.sha(peers[k]),scans:peerChecks,prefix},hybridClosure:{pins:hc.pins,scans:hc.scans},hybrid})
}
let controls=[];for(let odd of [false,true]){let F=[[1,2],[2,3],...(odd?[[1,3]]:[])].map((vs,id)=>({id,vs,ok:[1,2]})),r=span(F,2);assert((r.status==="UNSAT")===odd,"control");controls.push(r)}
return {out,controls}
}
const raw=process.argv.slice(2).map(p=>fs.readFileSync(p,'utf8'));console.log(JSON.stringify(experiment(raw),null,2));
