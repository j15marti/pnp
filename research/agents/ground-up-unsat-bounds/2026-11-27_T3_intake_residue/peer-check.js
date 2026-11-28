const fs=require('node:fs');const d=Object.fromEntries(['corpus','native','peer'].map(k=>[k,fs.readFileSync(process.argv[2]+'/'+k,'utf8')]));const run=function run(d){
 const {sha,solve,check,up}=new Function(d.native+";return {sha,solve,check,up};")(); const A=(t,m)=>{if(!t)throw Error(m)};
 A(sha(d.peer)==="3f669411797c44b34514243c32334e7d3acd0a486ec285124e6b81d8ba23f3ca","peer hash");
 const s=JSON.parse(d.corpus).instances.find(x=>x.id==="JOINT-24"),C=s.dimacs.trimEnd().split("\n").slice(1).map(l=>l.trim().split(/\s+/).map(Number).slice(0,-1)),p=JSON.parse(d.peer);
 A(sha(s.dimacs)==="68d21d234f32956200617b3a714d9f81f992cf2fa373f1285d639d6a703fa22b"&&s.dimacs.length*8===13416,"source");
 let checks=0,word=0,units=[],support=[];
 for(let q of p.certs){
  let coef=new Map(),rhs=0,used=new Set(),guard=q.guard[0][0];A(q.guard.length===1&&q.guard[0][1]===1&&q.unit===-guard,"guard");
  for(let [rows,sign] of [[q.rowsPlus,1],[q.rowsMinus,-1]])for(let row of rows){
   let vs=row.v,cl=row.ids.map(i=>{used.add(i);return C[i-1]});A(cl.every(c=>c&&c.every(l=>vs.includes(Math.abs(l)))),"row scope");
   // Exhaustive row equivalence to exact one, not just supplied row types.
   for(let w=0;w<2**vs.length;w++){word++;let count=0;for(let i=0;i<vs.length;i++)count+=w>>i&1;let ok=cl.every(c=>{checks++;return c.some(l=>+(l>0)===(w>>vs.indexOf(Math.abs(l))&1))});A(ok===(count===1),"exact-one")}
   for(let v of vs)coef.set(v,(coef.get(v)||0)+sign);rhs+=sign;
  }
  A(rhs>0&&rhs===q.rhs&&JSON.stringify([...coef].filter(x=>x[1]).sort((a,b)=>a[0]-b[0]))===JSON.stringify(q.coeff),"syzygy");
  let zero=new Set();for(let [v,i] of q.zeroReasons){used.add(i);A(C[i-1].length===2&&C[i-1].includes(-v)&&C[i-1].includes(-guard),"guard zero");zero.add(v)}
  A([...coef].every(([v,c])=>c<=0||zero.has(v)),"sign");units.push(q.unit);support.push({unit:q.unit,clauses:[...used].sort((a,b)=>a-b)});
 }
 let baseline=solve(C),D=[...C,...units.map(l=>[l])],hybrid=solve(D),m={scans:0,lits:0,cap:10000000},u=up(D,[],m);
 return {units,support,checks,word,baseline:{...baseline,check:check(C,baseline.tree)},hybrid:{...hybrid,check:check(D,hybrid.tree)},early:{m,pins:[...u.A],conflict:!!u.conflict},peerBytes:d.peer.length}
};console.log(JSON.stringify(run(d)));