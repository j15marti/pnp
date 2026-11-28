// Node: node hybrid.js DIR; files named cert,minimum,corpus,native.
const fs=require('node:fs');const files={"cert":["research/proof-spine-2026-11-26/monotone-exact-22/2026-11-27_1620_T1_residue_selectivity/JOINT-24.syzygy.json","d361104d31d73cbe76e30c64d9ac8481171cf240"],"minimum":["research/proof-spine-2026-11-26/monotone-exact-22/2026-11-27_1620_T1_residue_selectivity/JOINT-24.minimum.json","ff3e3d8222ef6107b854e7f76d420aadfeb667e5"],"corpus":["research/coordination/shared-unsat-2026-11-27/benchmarks.json","e315349cd6c1fe3fa696504859f28312f6aab69a"],"native":["research/agents/ground-up-unsat-bounds/2026-11-27_T3_native_transport_replay/native.js","303d735ba73855b69b47df734d4d3686f760b215"]};const d=Object.fromEntries(Object.keys(files).map(k=>[k,fs.readFileSync(process.argv[2]+'/'+k,'utf8')]));
function run(d){
 const {sha}=new Function(d.native+";return {sha};")(),a=JSON.parse(d.cert),p=JSON.parse(d.minimum),src=JSON.parse(d.corpus).instances.find(x=>x.id==="JOINT-24"),C=src.dimacs.trimEnd().split("\n").slice(1).map(l=>l.trim().split(/\s+/).map(Number).slice(0,-1)),n=src.nvars,A=(x,m)=>{if(!x)throw Error(m)};
 A(sha(src.dimacs)===a.instance_id.split(":").pop()&&src.dimacs.length*8===a.original_N_bits&&sha(d.cert)==="7a9444e78ccb6c1a04212f4ddfaab8a3381e823f9d9f105309f4876bd1f8f33d"&&sha(d.minimum)==="c00a282113d3e85399d02c4a9475cfec1f398d859d7451d2415f76c96762731f","parents");
 const U=a.certs.map(c=>c.unit).sort((a,b)=>Math.abs(a)-Math.abs(b));
 const R=a.rows;
 let trials=0,visits=0,xors=0,chosen=[],bySize=[],winner=null,checks=0;
 function attempt(U){
  const live=new Map(U.map(l=>[Math.abs(l),+(l>0)])),trace=[];
  function up(){
   for(;;){let change=false;for(let [i,c] of C.entries()){let f=[],sat=false;for(let l of c){visits++;let b=live.get(Math.abs(l));if(b===undefined)f.push(l);else if(b===+(l>0)){sat=true;break}}if(sat)continue;if(!f.length)return i+1;if(f.length===1){let l=f[0],v=Math.abs(l),z=+(l>0);live.set(v,z);trace.push({type:"UP",v,z,clause:i+1});change=true}}if(!change)return 0}
  }
  for(let j=0;j<=n;j++){
   let clash=up();if(clash)return {status:"UNSAT",trace,terminal:{type:"UP",clause:clash}};
   const eq=[...R.map((r,i)=>({mask:r.v.reduce((m,v)=>m|(1n<<BigInt(v)),1n),src:{row:i}})),...[...live].map(([v,z])=>({mask:(1n<<BigInt(v))|BigInt(z),src:{v,z}}))];
   let B=new Map();function parents(m){return eq.filter((_,i)=>(m>>BigInt(i))&1n).map(q=>q.src)}
   for(let i=0;i<eq.length;i++){let m=eq[i].mask,s=1n<<BigInt(i);while(m>1n){let k=m.toString(2).length-1;if(!B.has(k)){B.set(k,{m,s});break}const b=B.get(k);m^=b.m;s^=b.s;xors++}if(m===1n)return {status:"UNSAT",trace,terminal:{type:"GF2",parents:parents(s)}}}
   const K=[...B.keys()].sort((a,b)=>a-b);for(let v of K)for(let w of K)if(w>v&&(B.get(w).m>>BigInt(v)&1n)){B.get(w).m^=B.get(v).m;B.get(w).s^=B.get(v).s;xors++}
   let fresh=[];for(let [v,q] of B)if((q.m>>1n)===(1n<<BigInt(v-1))&&!live.has(v)){fresh.push({type:"GF2",v,z:Number(q.m&1n),parents:parents(q.s)})}
   if(!fresh.length)return {status:"UNKNOWN",trace};
   for(let q of fresh){trace.push(q);live.set(q.v,q.z)}
  }throw Error("loop")
 }
 const tried=[];function rec(k,j){if(winner)return;if(!k){trials++;let r=attempt(chosen);tried.push({units:chosen.slice(),status:r.status});if(r.status==="UNSAT")winner={units:chosen.slice(),...r};return}for(let i=j;i<=U.length-k;i++){chosen.push(U[i]);rec(k-1,i+1);chosen.pop();if(winner)return}}
 for(let k=0;k<=3;k++){let t=trials;rec(k,0);bySize.push({k,trials:trials-t,found:!!winner});if(winner)break}
 A(winner,"no <=3 terminal");
 // Independent proof replay using sets rather than bit masks, and source rows.
 const live=new Map(winner.units.map(l=>[Math.abs(l),+(l>0)]));
 function parity(ps){let lhs=new Set(),rhs=0;for(let q of ps){checks++;let v,b;if(q.row!==undefined){const r=R[q.row];const expected=[r.v,...r.v.flatMap((v,i)=>r.v.slice(i+1).map(w=>[-v,-w]))];for(let c of expected){checks+=r.ids.length;A(r.ids.some(id=>C[id-1].length===c.length&&C[id-1].every(l=>c.includes(l))),"row")}v=r.v;b=1}else{A(live.get(q.v)===q.z,"unknown parent unit");v=[q.v];b=q.z}rhs^=b;for(let u of v){checks++;if(lhs.has(u))lhs.delete(u);else lhs.add(u)}}return {lhs,rhs}}
 for(let q of winner.trace){A(!live.has(q.v),"duplicate unit");if(q.type==="UP"){const l=q.z?q.v:-q.v,c=C[q.clause-1];checks+=c.length;A(c.includes(l)&&c.filter(v=>v!==l).every(v=>live.get(Math.abs(v))===+(v<0)),"UP")}else{let r=parity(q.parents);A(r.lhs.size===1&&r.lhs.has(q.v)&&r.rhs===q.z,"GF2")}live.set(q.v,q.z)}
 const t=winner.terminal;if(t.type==="UP"){checks+=C[t.clause-1].length;A(C[t.clause-1].every(l=>live.get(Math.abs(l))===+(l<0)),"terminal")}else{let r=parity(t.parents);A(r.lhs.size===0&&r.rhs===1,"parity contradiction")}
 return {problem_id:a.problem_id,instance:a.instance,instance_id:a.instance_id,original_N_bits:a.original_N_bits,source_pin:a.source_pin,guard_id:"EMPTY",residual_id:"ROOT",original_ids:{clauses:[1,C.length],variables:[1,n]},parents:["CERT-v1:sha256:"+sha(d.cert),"CERT-v1:sha256:"+sha(d.minimum)],claim:"minimum cardinality within ten acquired units for the stated UP/GF2 closure, not globally minimal proof",winner,bySize,tried,trials,visits,xors,checks,selectedCertificates:a.certs.filter(p=>winner.units.includes(p.unit))}
}
console.log(JSON.stringify(run(d),null,2));
