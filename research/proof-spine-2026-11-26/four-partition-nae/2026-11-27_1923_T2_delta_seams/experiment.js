/* Node reproduction: node experiment.js registry.json benchmarks.json */
function sha(s){const K=[],H=[];for(let p=2;K.length<64;p++){let ok=true;for(let d=2;d*d<=p;d++)if(p%d===0){ok=false;break}if(ok){if(H.length<8)H.push((Math.sqrt(p)*4294967296)|0);K.push((Math.cbrt(p)*4294967296)|0)}}const a=Array.from(s,c=>c.charCodeAt(0));if(a.some(x=>x>127))throw Error("nonascii");let bit=a.length*8;a.push(128);while(a.length%64!==56)a.push(0);for(let j=7;j>=0;j--)a.push(Math.floor(bit/2**(j*8))%256);const r=(x,n)=>(x>>>n)|(x<<(32-n));for(let off=0;off<a.length;off+=64){let w=[];for(let i=0;i<16;i++)w.push((a[off+4*i]<<24)|(a[off+4*i+1]<<16)|(a[off+4*i+2]<<8)|a[off+4*i+3]);for(let i=16;i<64;i++){let x=w[i-15],y=w[i-2];w.push((w[i-16]+(r(x,7)^r(x,18)^(x>>>3))+w[i-7]+(r(y,17)^r(y,19)^(y>>>10)))|0)}let [A,B,C,D,E,F,G,J]=H;for(let i=0;i<64;i++){let t=(J+(r(E,6)^r(E,11)^r(E,25))+((E&F)^(~E&G))+K[i]+w[i])|0,u=((r(A,2)^r(A,13)^r(A,22))+((A&B)^(A&C)^(B&C)))|0;[A,B,C,D,E,F,G,J]=[(t+u)|0,A,B,C,(D+t)|0,E,F,G]}[A,B,C,D,E,F,G,J].forEach((x,i)=>H[i]=(H[i]+x)|0)}return H.map(x=>(x>>>0).toString(16).padStart(8,"0")).join("")}
function compile(instance){
 const lines=instance.dimacs.trimEnd().split("\n"),h=lines.shift().split(" ").map((s,i)=>i>=2?Number(s):s);
 if(h[0]!=="p"||h[1]!=="cnf"||h[2]!==instance.nvars||h[3]!==lines.length)throw Error("header");
 const n=instance.nvars,F=[],parents=[];let next=n;
 const add=(a,id)=>{F.push(a);parents.push(id)};
 lines.forEach((line,i)=>{const a=line.split(/\s+/).map(Number);if(a.pop()!==0||a.some(l=>!Number.isInteger(l)||!l||Math.abs(l)>n))throw Error("bad clause");const id=i+1;if(a.length===0){let v=++next;add([v,v,v],id);add([-v,-v,-v],id)}else if(a.length<=3){while(a.length<3)a.push(a[a.length-1]);add(a,id)}else{let prev=++next;add([a[0],a[1],prev],id);for(let j=2;j<a.length-2;j++){let t=++next;add([-prev,a[j],t],id);prev=t}add([-prev,a[a.length-2],a[a.length-1]],id)}});
 const types=[],used=[],edges=[],groups=new Map(),reps={},owners=[];
 const V=(t,owner)=>{types.push(t);used.push(0);owners.push(owner);return types.length-1};
 const P=v=>{if(used[v]>=4)throw Error("port overflow");return 4*v+used[v]++};
 const E=(a,b,s=0)=>edges.push([a,b,s]);
 const wire=(a,b,s)=>{const v=Array.from({length:5},()=>V("E",["wire",a,b]));for(let i=0;i<5;i++)for(let j=i+1;j<5;j++)if(i!==0||j!==1)E(P(v[i]),P(v[j]));E(a,P(v[0]),s);E(b,P(v[1]),0)};
 const occ=(id,s,p)=>{if(!groups.has(id))groups.set(id,[]);groups.get(id).push([p,s])};
 F.forEach(([a,b,c],i)=>{const L=x=>["x"+Math.abs(x),Number(x<0)],z="z"+i,T=[[L(a),L(b),[z,0]],[[z,1],L(c),["f",0]]];for(let j=0;j<2;j++)for(let k=0;k<2;k++){let v=V("B",["clause",parents[i],i,j,k]);for(const [id,s] of T[j])occ(id,s,P(v));occ("w"+i+"_"+j,0,P(v))}});
 for(const [id,O] of groups){if(O.length%2||O.length<2)throw Error("occurrence parity");reps[id]=O[0];if(O.length===2){wire(O[0][0],O[1][0],O[0][1]^O[1][1]);continue}const a=Array.from({length:(O.length-2)/2},()=>V("E",["carrier",id]));for(let i=1;i<a.length;i++)wire(P(a[i-1]),P(a[i]),0);let k=0;for(const v of a)while(used[v]<4){const [p,s]=O[k++];wire(P(v),p,s)}if(k!==O.length)throw Error("fanout")}
 const seen=new Set(),ports=new Set();for(const [a,b,s] of edges){let u=Math.floor(a/4),v=Math.floor(b/4),key=Math.min(u,v)+":"+Math.max(u,v);if(u===v||seen.has(key)||ports.has(a)||ports.has(b)||![0,1].includes(s))throw Error("not simple signed 4-regular");seen.add(key);ports.add(a);ports.add(b)}
 if(used.some(x=>x!==4)||ports.size!==4*types.length)throw Error("degree");
 const network={format:"STRICT-EB4-v1",types,edges};
 return {network,source_map:{original_n:n,ternary_clauses:F,original_clause_ids:parents,representative_ports:reps,vertex_provenance:owners}};
}

function experiment(reg,corpus,compile,sha,pins){
 const start=Date.now(),canon=x=>JSON.stringify(x)+"\n",sort=a=>[...new Set(a)].sort((a,b)=>a-b),key=a=>sort(a).join(","),out=[];
 function normalize(net){
  let visits=0,checks=0,joins=0;let P=net.types.length*4,p=Array.from({length:P},(_,i)=>i),s=new Int8Array(P);
  function f(x){let y=x,b=0;while(p[y]!==y){visits++;b^=s[y];y=p[y]}return [y,b]}
  function merge(a,b,c){let [x,t]=f(a),[y,u]=f(b);if(x===y){if((t^u)!==c)throw Error("parity");return}if(x>y)[x,y]=[y,x];p[y]=x;s[y]=t^u^c}
  for(let [a,b,c] of net.edges)merge(a,b,c);net.types.forEach((t,i)=>{if(t==="E")for(let j=1;j<4;j++)merge(4*i,4*i+j,0)});
  const map=Array.from({length:P},(_,i)=>f(i));let G=new Map();
  net.types.forEach((t,i)=>{if(t!=="B")return;let v=sort([0,1,2,3].map(j=>map[4*i+j][0]+1)),r=[];for(let m=0;m<2**v.length;m++){checks++;let k=0;for(let j=0;j<4;j++){let [a,b]=map[4*i+j];k+=((m>>v.indexOf(a+1))&1)^b}if(k===2)r.push(m)}let z={v,r,owners:[i]},k=JSON.stringify([v,r]);if(G.has(k))G.get(k).owners.push(i);else G.set(k,z)});
  let factors=[...G.values()];const anchor=map[10][0]+1;if(map[10][1]!==0)throw Error("anchor parity");
  function restrict(F,x,b){return F.map(z=>{let j=z.v.indexOf(x);if(j<0)return z;let v=z.v.filter(y=>y!==x),r=z.r.filter(m=>((m>>j)&1)===b).map(m=>(m&((1<<j)-1))|((m>>(j+1))<<j));return {v,r:sort(r),owners:z.owners}})}
  function cnf(F){return F.flatMap(z=>Array.from({length:2**z.v.length},(_,m)=>m).filter(m=>!z.r.includes(m)).map(m=>z.v.map((x,j)=>(m>>j)&1?-x:x)))}
  factors=restrict(factors,anchor,0);let early=up(cnf(factors),[],false);if(early.bad)throw Error("unexpected root UP");for(let [x,b] of early.a)factors=restrict(factors,x,b);
  let before={factors:factors.length,vars:sort(factors.flatMap(z=>z.v)).length,clauses:cnf(factors).length,early:early.a,earlyReads:early.reads};let steps=[],scan=0;
  // Exact complete-bucket elimination, retain original owner IDs and full witness rows.
  while(true){let buckets=new Map();for(let z of factors)for(let x of z.v){scan++;if(!buckets.has(x))buckets.set(x,[]);buckets.get(x).push(z)}
   let choices=[];for(let [x,B] of buckets){let v=sort(B.flatMap(z=>z.v));scan+=B.reduce((a,z)=>a+z.v.length,0);if(v.length<=4&&x!==594)choices.push({x,B,v})}
   if(!choices.length)break;choices.sort((a,b)=>a.v.length-b.v.length||a.B.length-b.B.length||a.x-b.x);
   let {x,B,v}=choices[0];let w=v.filter(y=>y!==x),r=[],witness=[];
   for(let m=0;m<2**w.length;m++)for(let b=0;b<2;b++){let a=new Map(w.map((y,j)=>[y,(m>>j)&1]));a.set(x,b);joins++;if(B.every(z=>z.r.includes(z.v.reduce((q,y,j)=>q|(a.get(y)<<j),0)))){r.push(m);witness.push([m,b])}}
   let z={v:w,r:sort(r),owners:sort(B.flatMap(q=>q.owners))};steps.push({x,parents:B,out:z,witness});
   factors=factors.filter(z=>!z.v.includes(x));if(z.r.length!==2**w.length)factors.push(z);
  }
  return {C:cnf(factors),map,anchor,steps,factors,before,visits,checks,joins,scan};
 }
 function up(C,g,rev=false){let a=new Map(g),reads=0;while(true){let changed=false;for(let ii=0;ii<C.length;ii++){let c=C[rev?C.length-1-ii:ii],missing=0,last=0,hit=false;for(let l of c){reads++;let b=a.get(Math.abs(l));if(b===+(l>0)){hit=true;break}if(b===undefined){missing++;last=l}}if(hit)continue;if(!missing)return {bad:true,a:[...a],reads};if(missing===1){a.set(Math.abs(last),+(last>0));changed=true}}if(!changed)return {bad:false,a:[...a],reads}}}
 function dpll(C){let reads=0,nodes=0;function go(g){nodes++;let u=up(C,g);reads+=u.reads;if(u.bad)return ["X"];if(reads>2000000)return ["?"];let a=new Map(u.a),w=new Map();for(let c of C)if(!c.some(l=>a.get(Math.abs(l))===+(l>0)))for(let l of c)if(!a.has(Math.abs(l)))w.set(Math.abs(l),(w.get(Math.abs(l))||0)+1);if(!w.size)return ["S",u.a];let x=[...w].sort((a,b)=>b[1]-a[1]||a[0]-b[0])[0][0];return ["B",x,go([...u.a,[x,0]]),go([...u.a,[x,1]])]}let tree=go([]);let verify=0;function replay(g,t){let u=up(C,g,true);verify+=u.reads;if(u.bad)return true;if(t[0]!=="B")return false;let a=new Map(u.a),x=t[1];if(a.has(x))return replay(u.a,t[2+a.get(x)]);return replay([...u.a,[x,0]],t[2])&&replay([...u.a,[x,1]],t[3])}return {tree,nodes,reads,verify,ok:replay([],tree)}}
 function run(C0,peer){
  const early=up(C0,[]);if(early.bad)return {early};let fixed=new Map(early.a),C=C0.filter(c=>!c.some(l=>fixed.get(Math.abs(l))===+(l>0))).map(c=>c.filter(l=>!fixed.has(Math.abs(l))));let V=sort(C.flat().map(Math.abs));let inc=new Map(V.map(x=>[x,[]]));C.forEach((c,i)=>sort(c.map(Math.abs)).forEach(x=>inc.get(x).push(i)));let occ=C.reduce((a,c)=>a+c.length,0),m=C.length;
  const part=new Map(V.map((x,i)=>[x,i%4]));let seam=C.map((c,i)=>[i,new Set(c.map(l=>part.get(Math.abs(l)))).size]).filter(x=>x[1]>1).map(x=>x[0]);
  let fullReads=0,deltaReads=0,correctionReads=0,verifyReads=0;
  function evalRow(c,a,D){let k=0,s=0;for(let l of c){let b=(a.get(Math.abs(l))||0)^(D?.has(Math.abs(l))?1:0);if(b===+(l>0)){k++;s+=l>0?1:-1}}return [k,k%3,(s%3+3)%3]}
  let records=[],guardPool=new Map(),sum={full:0,delta:0,correction:0,verify:0,naiveWrong:0,wrongMax:0,deltaWords:0,fullWords:0,affected:0};let rng=1,draws=0;
  function rand(n){rng^=rng<<13;rng^=rng>>>17;rng^=rng<<5;draws++;return (rng>>>0)%n}
  function energy(t){return +(t[0]===0)}
  for(let seed=1;seed<=16;seed++){rng=seed;let a=new Map(V.map(x=>[x,1]));let T=C.map(c=>evalRow(c,a));fullReads+=occ;let e=T.reduce((q,t)=>q+energy(t),0);
   // deterministic strict improvement to first stall, same start; use occurrence lists and exact counts.
   let flips=[],flipChecks=0,tieChanges=0;
   while(true){let best=null;for(let x of V){let de=0,z=0;for(let i of inc.get(x)){let r=evalRow(C[i],a,new Set([x]));flipChecks+=C[i].length;de+=energy(r)-energy(T[i]);z+=+(r[0]>0&&r[2]===0)-+(T[i][0]>0&&T[i][2]===0)}if(de<0&&(!best||de<best.de||(de===best.de&&x<best.x)))best={x,de,z}}
    if(!best)break;a.set(best.x,1-a.get(best.x));for(let i of inc.get(best.x))T[i]=evalRow(C[i],a);e+=best.de;flips.push(best.x)}
   // four independent near-identical block proposals: sample one seam variable per block, fallback any.
   let ds=Array.from({length:4},(_,p)=>{let q=V.filter(x=>part.get(x)===p);return new Set(q.length?[q[rand(q.length)]]:[])});
   let D=new Set(ds.flatMap(x=>[...x])),affected=new Set([...D].flatMap(x=>inc.get(x))),ind=0;
   for(let d of ds)for(let i of new Set([...d].flatMap(x=>inc.get(x)))){deltaReads+=C[i].length;ind+=energy(evalRow(C[i],a,d))-energy(T[i])}
   let correction=0,corrRows=[];for(let i of affected){let hit=ds.filter(d=>C[i].some(l=>d.has(Math.abs(l))));if(hit.length<2)continue;let joint=evalRow(C[i],a,D);correctionReads+=C[i].length;let z=energy(joint)-energy(T[i]);for(let d of hit){z-=energy(evalRow(C[i],a,d))-energy(T[i]);correctionReads+=C[i].length}correction+=z;corrRows.push([i,z])}
   let full=C.map(c=>evalRow(c,a,D));fullReads+=occ;let ef=full.reduce((q,t)=>q+energy(t),0);let hybrid=T.slice();for(let i of affected){hybrid[i]=evalRow(C[i],a,D);verifyReads+=C[i].length}
   if(JSON.stringify(full)!==JSON.stringify(hybrid)||e+ind+correction!==ef)throw Error("delta mismatch");
   sum.naiveWrong+=+(e+ind!==ef);sum.wrongMax=Math.max(sum.wrongMax,Math.abs(correction));sum.deltaWords+=D.size;sum.fullWords+=V.length*4;sum.affected+=affected.size;
   // candidate guards are opposite to a proposed partial orientation; only checked UP yields a valid clause.
   for(let i of affected){let v=sort(C[i].map(Math.abs));for(let j=0;j<v.length;j++)for(let k=j+1;k<v.length;k++){let g=[[v[j],a.get(v[j])^(D.has(v[j])?1:0)],[v[k],a.get(v[k])^(D.has(v[k])?1:0)]];let h=JSON.stringify(g);guardPool.set(h,{g,w:(guardPool.get(h)?.w||0)+1})}}
   records.push({seed,base:[...a],deltas:ds.map(d=>[...d]),e,ind,correction,ef,affected:[...affected],corrRows,flips,flipChecks,tieChanges});
  }
  // compare exact whole-table rebuild vs sparse updates and seam-correction costs (reads not wall-time).
  let pool=[...guardPool.values()].sort((a,b)=>JSON.stringify(a.g).localeCompare(JSON.stringify(b.g))),trials={};
  function sample(mode){let r=[],reads=0,replay=0;for(let seed=1;seed<=16;seed++){rng=seed*2654435761|0;for(let j=0;j<2;j++){if(!pool.length)break;let q;if(mode==="det")q=pool[(seed-1)*2+j<pool.length?(seed-1)*2+j:((seed-1)*2+j)%pool.length];else if(mode==="uniform"||rand(4)===0)q=pool[rand(pool.length)];else {let total=pool.reduce((s,p)=>s+p.w,0),z=rand(total);q=pool.find(p=>(z-=p.w)<0)}let u=up(C,q.g);reads+=u.reads;let v=u.bad?up(C,q.g,true):null;if(v){replay+=v.reads;if(!v.bad)throw Error("guard replay")}r.push({seed,g:q.g,bad:u.bad,reads:u.reads,replay:v?.reads||0})}}return {trials:r,reads,replay,success:r.filter(x=>x.bad).length}}
  for(let mode of ["det","uniform","adaptive"])trials[mode]=sample(mode);
  let clauses=new Map();for(let x of trials.adaptive.trials)if(x.bad){let c=x.g.map(([v,b])=>b?-v:v);clauses.set(key(c),c)}
  let imported=[];if(peer&&V.includes(peer[0])){let u=up(C,[peer],true);if(u.bad){let c=[peer[1]?-peer[0]:peer[0]];clauses.set(key(c),c);imported.push({guard:peer,reads:u.reads,c})}else imported.push({guard:peer,reads:u.reads,refused:true})}
  let learned=[...clauses.values()],base=dpll(C),hybrid=dpll([...C,...learned]);
  return {vars:V.length,rows:m,occ,seam:seam.length,early,fullReads,deltaReads,correctionReads,verifyReads,sum,records,pool,trials,draws,learned,imported,base,hybrid,encodingNote:"deltaWords counts variable IDs, not bits; base stored once; sparse response verification reads separately"};
 }
 for(let id of ["JOINT-24","RANDOM-3CNF-40"]){
  let inst=corpus.instances.find(x=>x.id===id),r=reg.instances.find(x=>x.alias==="EB-"+id),G=compile(inst),ns=canon(G.network),ms=canon(G.source_map);
  if(sha(ns)!==r.sha256||ns.length*8!==r.N_bits||sha(ms)!==r.source_map_sha256||sha(inst.dimacs)!==r.source_cnf.sha256||inst.dimacs.length*8!==r.source_cnf.N_bits)throw Error("auth");
  let n=normalize(G.network);let native=run(n.C,id==="JOINT-24"?[594,1]:null);let C=inst.dimacs.trimEnd().split("\n").slice(1).map(x=>x.split(/\s+/).map(Number).slice(0,-1));let cnf=run(C,null);
  let common={source_pin:pins,guard_id:"EMPTY",residual_id:"ROOT",parents:[],problem_id:"STRICT-EB4-v1",instance:r.short_id,instance_id:r.instance_id,original_N_bits:r.N_bits,original_ids:{ports:[0,G.network.types.length*4-1],vertices:[0,G.network.types.length-1],edges:[0,G.network.edges.length-1]}};
  out.push({id,native:{meta:common,mapHash:sha(canon(n.map)),gauge:n.anchor,projection:n.steps,chart:n.factors,chartHash:sha(canon(n.C)),before:n.before,visits:n.visits,checks:n.checks,joins:n.joins,scan:n.scan,experiment:native},cnf:{meta:{...common,problem_id:"DIMACS-CNF-v1",instance:r.source_cnf.short_id,instance_id:r.source_cnf.instance_id,original_N_bits:r.source_cnf.N_bits,original_ids:{vars:[1,inst.nvars],clauses:[1,inst.nclauses]}},experiment:cnf}});
 }
 return {elapsed:Date.now()-start,cases:out};
}
const fs=require('node:fs'); const pins={"registry":"0c14cdc57925788cf7a451dcd5aa171dce860f2c","corpus":"e315349cd6c1fe3fa696504859f28312f6aab69a","compiler":"21b9d53fb8166c819b24e708656c742cd3c24f10"};console.log(JSON.stringify(experiment(JSON.parse(fs.readFileSync(process.argv[2],'utf8')),JSON.parse(fs.readFileSync(process.argv[3],'utf8')),compile,sha,pins),null,2));
