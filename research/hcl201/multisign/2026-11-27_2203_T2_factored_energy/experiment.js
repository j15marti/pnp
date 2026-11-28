// Reproduce with Node: node experiment.js compiler.js corpus.json registry.json chart.js hash.js joint.cert.json random.cert.json
// Run node experiment.js compiler.js benchmarks.json registry.json native-chart.js owner-cert.js
function research(I) {
const sha=new Function(I.hash.slice(0,I.hash.indexOf("function quotient"))+";return sha")();
const compile=new Function(I.compiler.slice(I.compiler.indexOf("function compile"),I.compiler.indexOf("function auditLocal"))+";return compile")();
const {project,verifyProjection}=new Function(I.chart.slice(I.chart.indexOf("const key="),I.chart.indexOf("function up("))+";return {project,verifyProjection}")();
const enc=x=>JSON.stringify(x)+"\n", check=(b,s)=>{if(!b)throw Error(s)}, abs=Math.abs;
check(sha("abc")==="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad","sha");
function up(F,g=[]){let A=new Set(g),work=0,trace=[];if(g.some(l=>A.has(-l)))return{A,work,no:true,trace};for(;;){let change=false;for(let j=0;j<F.length;j++){let c=F[j],u=0,n=0,hit=false;for(let l of c){work++;if(A.has(l)){hit=true;break}if(!A.has(-l)){u=l;n++}}if(hit)continue;if(!n)return{A,work,no:true,trace:[...trace,j]};if(n===1&&!A.has(u)){A.add(u);trace.push(j);change=true}}if(!change)return{A,work,no:false,trace}}}
function simplify(F,A){return F.filter(c=>!c.some(l=>A.has(l))).map(c=>c.filter(l=>!A.has(-l)))}
function spectral(F,cap=8){
 const vs=[...new Set(F.flat().map(abs))].sort((a,b)=>a-b),id=new Map(vs.map((v,i)=>[v,1n<<BigInt(i)])),w=Math.max(0,...F.map(c=>c.length));check(w<=16,"width cap");const scale=2**w, M=new Map();let raw=0;
 for(let c of F){for(let m=0;m<2**c.length;m++){let z=0n,a=scale/2**c.length;for(let j=0;j<c.length;j++)if(m>>j&1){z^=id.get(abs(c[j]));if(c[j]<0)a=-a}M.set(z,(M.get(z)||0)+a);raw++}}
 const terms=[...M].filter(([k,a])=>k&&a).sort((a,b)=>abs(b[1])-abs(a[1])||(a[0]<b[0]?-1:1)),zero=[...M].filter(([k,a])=>k&&a===0).length;
 let basis=new Map(),rank=0,ops=0,peak=0,levels=[];
 function reduce(x){let c=0;while(x){ops++;let b=x.toString(2).length-1,q=basis.get(b);if(!q)return[x,c];x^=q[0];c^=q[1]}return[0n,c]}
 function bound(){let keep=[],tail=0;for(let [m,a] of terms){let [z,c]=reduce(m);if(z)tail+=abs(a);else keep.push([c,a])}let min=Infinity;for(let word=0;word<2**rank;word++){let e=M.get(0n)||0;for(let [k,a] of keep){let x=k&word,sg=1;while(x){x&=x-1;sg=-sg}e+=sg*a;ops++}min=Math.min(e,min)}peak=Math.max(peak,keep.length);return{rank,keep:keep.length,tail,min,lb:min-tail}}
 levels.push(bound());for(let [m,a] of terms){if(rank===cap)break;let [z,c]=reduce(m);if(!z)continue;basis.set(z.toString(2).length-1,[z,c^(1<<rank)]);rank++;levels.push(bound())}
 for(let i=1;i<levels.length;i++)check(levels[i].lb>=levels[i-1].lb,"nonmonotone");
 let checks=0;for(let t=0;t<32;t++){let word=0n;for(let j=0;j<vs.length;j++)if(((Math.imul(t+17,j+31)>>>((j+t)%16))&1))word|=1n<<BigInt(j);let direct=0;for(let c of F)if(c.every(l=>Boolean(word&id.get(abs(l)))!==(l>0)))direct+=scale;let y=M.get(0n)||0;for(let [m,a] of terms){let x=m&word,sg=1;while(x){x&=x-1n;sg=-sg}y+=sg*a}check(direct===y&&y>=levels.at(-1).lb,"Fourier replay");checks++}
 return{variables:vs.length,rows:F.length,scale,raw,distinct:terms.length+1,zero,levels,ops,peak,checks}
}
function queueEngine(F){const rows=F.map(c=>c.slice()),idx=new Map(),units=[];let visits=0;function add(c){let j=rows.length;rows.push(c);index(c,j)}function index(c,j){for(let l of c){if(!idx.has(l))idx.set(l,[]);idx.get(l).push(j)}if(c.length<=1)units.push(j)}rows.forEach(index);function probe(g){let A=new Set(),q=[];function set(l){if(A.has(-l))return false;if(!A.has(l)){A.add(l);q.push(l)}return true}for(let l of g)if(!set(l))return true;for(let j of units){visits++;if(!rows[j].length||!set(rows[j][0]))return true}for(let k=0;k<q.length;k++)for(let j of idx.get(-q[k])||[]){let hit=false,n=0,u=0;for(let l of rows[j]){visits++;if(A.has(l)){hit=true;break}if(!A.has(-l)){u=l;n++}}if(!hit&&(!n||n===1&&!set(u)))return true}return false}
return{rows,add,probe,get visits(){return visits}}}
function discover(F,limit=10000000){let E=queueEngine(F),vs=[...new Set(F.flat().map(abs))].sort((a,b)=>a-b),K=c=>c.join(","),C=[[]];for(let v of vs)C.push([v],[-v]);for(let i=0;i<vs.length;i++)for(let j=i+1;j<vs.length;j++)for(let a of [1,-1])for(let b of [1,-1])C.push([a*vs[i],b*vs[j]]);let seen=new Set(F.map(c=>K([...c].sort((a,b)=>abs(a)-abs(b))))),proof=[],attempts=0,epochs=0,status="UNKNOWN";outer:for(;;){epochs++;let change=false;for(let c of C){if(E.visits>=limit)break outer;if(seen.has(K(c)))continue;attempts++;if(E.probe(c.map(l=>-l))){proof.push(c);E.add(c);seen.add(K(c));change=true;if(!c.length){status="UNSAT";break outer}}}if(!change)break}return{status,proof,attempts,epochs,visits:E.visits,candidates:C.length}}
function replay(F,proof){let rows=F.slice(),visits=0;for(let c of proof){let t=up(rows,c.map(l=>-l));visits+=t.work;check(t.no,"RUP replay");rows.push(c)}return visits}
function affine(F){let vs=[...new Set(F.flat().map(abs))],ids=new Map(vs.map((v,i)=>[v,i])),G=new Map(),basis=new Map(),work=0,contradiction=false;for(let c of F){let s=c.map(abs).sort((a,b)=>a-b),k=s.join(",");if(!G.has(k))G.set(k,{s,cs:[]});G.get(k).cs.push(c)}
for(let {s,cs} of G.values()){if(s.length>8)continue;let support=[];for(let x=0;x<2**s.length;x++){work++;if(cs.every(c=>c.some(l=>Boolean(x>>s.indexOf(abs(l))&1)===(l>0))))support.push(x)}if(!support.length){contradiction=true;break}for(let m=1;m<2**s.length;m++){let ps=new Set(support.map(x=>{let y=x&m,p=0;while(y){y&=y-1;p^=1}return p}));work+=support.length;if(ps.size!==1)continue;let row=0n;for(let j=0;j<s.length;j++)if(m>>j&1)row|=1n<<BigInt(ids.get(s[j]));let b=[...ps][0];while(row){let k=row.toString(2).length-1;if(!basis.has(k)){basis.set(k,[row,b]);break}let q=basis.get(k);row^=q[0];b^=q[1];work++}if(!row&&b)contradiction=true}}
return{rank:basis.size,contradiction,work}}
function binary(F){let V=[...new Set(F.flat().map(abs))],D=new Map();for(let c of F.filter(c=>c.length===2)){for(let [a,b] of [[-c[0],c[1]],[-c[1],c[0]]]){if(!D.has(a))D.set(a,[]);D.get(a).push(b)}}let work=0,forced=[];function reach(a){let s=new Set([a]),q=[a];for(let k=0;k<q.length;k++)for(let b of D.get(q[k])||[]){work++;if(!s.has(b)){s.add(b);q.push(b)}}return s.has(-a)}
for(let v of V){let a=reach(v),b=reach(-v);if(a&&b)return{contradiction:true,work,forced};if(a)forced.push(-v);if(b)forced.push(v)}return{contradiction:false,work,forced}}
function separator(F){let rows=F.slice(),work=0,retired=0;for(;;){let vs=[...new Set(rows.flat().map(abs))].sort((a,b)=>a-b),v=vs.find(v=>{let fs=rows.filter(c=>c.some(l=>abs(l)===v));work+=rows.length;return new Set(fs.flat().map(abs)).size<=4});if(v===undefined)break;let a=rows.filter(c=>c.includes(v)),b=rows.filter(c=>c.includes(-v));let R=[];for(let x of a)for(let y of b){work++;let c=[...new Set([...x.filter(l=>l!==v),...y.filter(l=>l!==-v)])];if(!c.some(l=>c.includes(-l)))R.push(c)}rows=rows.filter(c=>!c.some(l=>abs(l)===v)).concat(R);retired++;if(rows.some(c=>!c.length))return{contradiction:true,retired,work};if(rows.length>2000)break}return{contradiction:false,retired,work,remaining:rows.length}}
function feedback(F,mode,seed=91357,cap=200000){let vs=[...new Set(F.flat().map(abs))].sort((a,b)=>a-b),A=new Set(),rand=seed;for(let v of vs){rand=(Math.imul(rand,1664525)+1013904223)>>>0; if(rand>>>31)A.add(v)}
let work=0,ties=0,flips=0;function score(B){let bad=[],z=0;for(let i=0;i<F.length;i++){let k=0,h=0;for(let l of F[i]){work++;if(B.has(abs(l))===(l>0)){k++;h+=Math.sign(l)}}if(!k)bad.push(i);else if((h%3+3)%3===0)z++;let mod=k%3;check(mod>=0,"mod")}return{bad,z}}
let q=score(A);if(mode!=="none")while(q.bad.length&&work<cap){let opts=[];for(let v of vs){if(work>=cap)break;let B=new Set(A);if(B.has(v))B.delete(v);else B.add(v);let t=score(B);if(t.bad.length<q.bad.length)opts.push({v,B,t})}if(!opts.length||work>=cap)break;opts.sort((a,b)=>a.t.bad.length-b.t.bad.length||a.v-b.v);let first=opts[0];if(mode==="residue")opts.sort((a,b)=>a.t.bad.length-b.t.bad.length||a.t.z-b.t.z||a.v-b.v);if(opts[0].v!==first.v)ties++;A=opts[0].B;q=opts[0].t;flips++}
return{mode,work,ties,flips,stalled:q.bad.length,word:vs.map(v=>A.has(v)?v:-v),bad:q.bad}}

function mb(F,cap,budget=350000){
 let rows=F.map(c=>{let s=[...new Set(c.map(abs))].sort((a,b)=>a-b);return {s,t:Array.from({length:2**s.length},(_,w)=>Number(c.every(l=>Boolean(w>>s.indexOf(abs(l))&1)!==(l>0))))}});
 let work=0,split=0,peak=0,trace=[],start=Date.now(),exact=true;
 function union(a,b){return [...new Set([...a,...b])].sort((x,y)=>x-y)}
 while(rows.some(r=>r.s.length)){
  let vs=[...new Set(rows.flatMap(r=>r.s))],best=null;
  for(let v of vs){let s=[];for(let f of rows){work++;if(f.s.includes(v))s=union(s,f.s)}if(!best||s.length<best.s.length||s.length===best.s.length&&v<best.v)best={v,s}}
  if(work>budget)return {status:"CAP",lb:0,work,split,peak,ms:Date.now()-start,exact:false};
  let v=best.v,b=rows.filter(r=>r.s.includes(v)),rest=rows.filter(r=>!r.s.includes(v)),groups=[];
  b.sort((a,b)=>b.s.length-a.s.length);
  for(let f of b){let j=groups.findIndex(g=>union(g.s,f.s).length<=cap);if(j<0){if(f.s.length>cap)return {status:"WIDTH",lb:0,work,split,peak,exact:false};groups.push({s:f.s.slice(),fs:[f]})}else{groups[j].s=union(groups[j].s,f.s);groups[j].fs.push(f)}}
  if(groups.length>1){split+=groups.length-1;exact=false}
  for(let g of groups){let s=g.s.filter(x=>x!==v),t=[],maps=g.fs.map(f=>f.s.map(x=>g.s.indexOf(x))),pos=g.s.indexOf(v);for(let w=0;w<2**s.length;w++){let a=(w&((1<<pos)-1))|((w>>pos)<<(pos+1)),z=[0,0];for(let j=0;j<g.fs.length;j++){for(let bit=0;bit<2;bit++){let full=a|(bit<<pos),u=0;for(let k=0;k<maps[j].length;k++){work++;u|=((full>>maps[j][k])&1)<<k}z[bit]+=g.fs[j].t[u]}}t.push(Math.min(...z));if(work>budget)return {status:"CAP",lb:0,work,split,peak,ms:Date.now()-start,exact:false}}
  rest.push({s,t});trace.push({v,scope:g.s,inputs:g.fs.length,output:t.length})}
  rows=rest;peak=Math.max(peak,rows.reduce((a,f)=>a+f.t.length,0))
 }
 let lb=rows.reduce((a,f)=>a+f.t[0],0);
 return{status:lb>0?"POSITIVE":"INCONCLUSIVE",lb,work,split,peak,ms:Date.now()-start,exact,trace}
}
function signedFactored(k,bad){
 // F = AND_i (u_i OR v_i); t=f, t=f XOR h, h=bad. Each penalty is a Boolean violation.
 // Independent two-state enumeration of (f,t,h); both f values constructible for k>=1.
 let m=4n**BigInt(k),min=3,witness=null,checks=0;
 for(let f=0;f<2;f++)for(let t=0;t<2;t++)for(let h=0;h<2;h++){let e=Number(t!==f)+Number(t!==(f^h))+Number(h!==bad);checks++;if(e<min){min=e;witness={f,t,h}}}
 let brute=null;if(k<=6){brute=3;for(let w=0;w<2**(2*k);w++){let f=1;for(let i=0;i<k;i++)f&=Number(Boolean((w>>(2*i))&3));for(let t=0;t<2;t++)for(let h=0;h<2;h++){let e=Number(t!==f)+Number(t!==(f^h))+Number(h!==bad);brute=Math.min(brute,e);checks++}}check(brute===min,"factored replay")}
 return{k,bad,min,witness,checks,expandedTerms:m.toString(),denominatorBits:2*k+1,featureDegree:2*k}
}

let results=[];
for(let name of ["JOINT-24","RANDOM-3CNF-40"]){
 let x=JSON.parse(I.corp).instances.find(z=>z.id===name),r=JSON.parse(I.reg).instances.find(z=>z.alias==="EB-"+name),G=compile(x),native=enc(G.network),cnf=x.dimacs,map=enc(G.source_map);
 check(sha(native)===r.sha256&&native.length*8===r.N_bits&&sha(cnf)===r.source_cnf.sha256&&cnf.length*8===r.source_cnf.N_bits&&sha(map)===r.source_map_sha256,"auth");
 let p=project(G.network),projectOps=verifyProjection(G.network,p),F=p.clauses,guard=[[p.anchor,0]],gid="GUARD-v1:sha256:"+sha(enc(["PNP-GUARD-v1",r.instance_id,"EB-PORT-PINS-v1",sha(enc(guard))])),rid="RESIDUAL-v1:sha256:"+sha(enc(["PNP-RESIDUAL-v1",r.instance_id,gid,"EB-CHART-SYZYGY-v1",sha(enc({anchor:p.anchor,clauses:p.clauses,raw:p.raw,cond:p.cond,steps:p.steps,final:p.final})),sha(enc({root:p.root,phase:p.phase}))]));
 let early=up(F),S=simplify(F,early.A),vs=[...new Set(S.flat().map(abs))].sort((a,b)=>a-b),guards=Array.from({length:5},(_,i)=>[...vs.slice(0,i),...(i<4?[-vs[i]]:[])]),lanes=[];
 let rootSpectrum=spectral(S,8),base=[4,6,8].map(w=>({w,...mb(S,w)}));
 // Native baseline before peer import; separate independent lane runs.
 for(let g of guards){let u=up(S,g),T=simplify(S,u.A);lanes.push({g,up:{no:u.no,work:u.work,pins:u.A.size,core:u.trace},affine:u.no?null:affine(T),binary:u.no?null:binary(T),separator:u.no?null:separator(T),spectral:u.no?null:spectral(T,8).levels.at(-1),mb:u.no?null:mb(T,6,100000)})}
 let blind=discover(S,1000000),verification=replay(S,blind.proof);
 let pc=JSON.parse(name==="JOINT-24"?I.joint:I.random),expected=name==="JOINT-24"?"85283f86e8cc864a7fd2b3b1c28c60c10d0acda2e51ebd70fe027910c3a5c2a5":"3492643ef33b6d8a128f470fe16ae898093819b598408bf1b7941a058393bc33";
 check(sha(name==="JOINT-24"?I.joint:I.random)===expected&&pc.guard_id===gid&&pc.residual_id===rid&&pc.instance_id===r.instance_id,"parent IDs");
 let parentReplay=replay(F,pc.proof),subsetReplay=replay(pc.base_rows.map(j=>F[j]),pc.proof);
 let pref=pc.proof.slice(0,3),hybrid=[];
 for(let mask=0;mask<8;mask++){let pp=pref.filter((c,i)=>mask>>i&1),valid=true,rv=0,rows=F.slice();for(let c of pp){let u=up(rows,c.map(l=>-l));rv+=u.work;if(!u.no){valid=false;break}rows.push(c)}if(!valid){hybrid.push({mask,valid,rv});continue}let u=up(rows);hybrid.push({mask,valid,rv,pins:u.A.size,closure:u.work,no:u.no,penalty:mb(rows,6),restricted:u.no?null:mb(simplify(F,u.A),6)})}
 let g=guards.find(g=>!up(S,g).no),fb=g?["none","table","residue"].map(m=>feedback(simplify(S,up(S,g).A),m)):null;
 let C=cnf.trimEnd().split("\n").slice(1).map(c=>c.trim().split(/\s+/).map(Number).slice(0,-1)),cu=up(C),cr=discover(simplify(C,cu.A),1000000),cv=replay(simplify(C,cu.A),cr.proof),cm=mb(simplify(C,cu.A),6);
 results.push({name,registry:r,guard,gid,rid,projection:{carriers:p.carriers,retired:p.steps.length,projectOps,cost:p.cost},early:{pins:[...early.A],work:early.work,no:early.no},rootSpectrum,base,lanes,blind:{...blind,verification},peer:{expected,parentReplay,subsetReplay,pref,hybrid},feedback:fb,feedbackGuard:g,cnf:{...cr,verification:cv,earlyPins:[...cu.A],earlyWork:cu.work,mb:cm}})
}
let controls=[];for(let k of [2,4,6,8,12,20])for(let bad of [0,1])controls.push(signedFactored(k,bad));
return {results,controls}
}

if(typeof require!=='undefined'&&require.main===module){const fs=require('fs');const keys=['compiler','corp','reg','chart','hash','joint','random'];console.log(JSON.stringify(research(Object.fromEntries(keys.map((k,i)=>[k,fs.readFileSync(process.argv[i+2],'utf8')]))),null,2))}
