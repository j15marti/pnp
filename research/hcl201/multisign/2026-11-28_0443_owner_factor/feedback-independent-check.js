function verify(bundle){
 let report=[];
 const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b),norm=x=>[...new Set(x)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
 for(let x of bundle.cases){
  if(x.missing)continue;
  let F=x.source.trimEnd().split("\n").slice(1).map(l=>norm(l.split(/\s+/).map(Number).slice(0,-1)));
  let c={visits:0,trees:0,learned:0,guards:0,witnesses:0},base=F.map((lits,i)=>({id:i+1,lits}));
  function up(rows,pins){let a=new Map(pins);for(;;){let P=new Map();for(let r of rows){let U=[],ok=false;for(let l of r.lits){c.visits++;let v=Math.abs(l);if(!a.has(v))U.push(l);else if(a.get(v)===Number(l>0)){ok=true;break}}if(ok)continue;if(!U.length)return {bad:true,a};if(U.length===1){let v=Math.abs(U[0]),b=Number(U[0]>0);if(P.has(v)&&P.get(v)!==b)return {bad:true,a};P.set(v,b)}}if(!P.size)return {bad:false,a};for(let [v,b] of P)a.set(v,b)}}
  for(let G of x.guards){
   let u=up(base,G.pins);if(u.bad!==(G.conflict!==null))throw Error("early conflict");
   if(!u.bad){
    let forced=[...u.a].filter(([v])=>!G.pins.some(([w])=>w===v)).sort((a,b)=>a[0]-b[0]);if(!eq(forced,G.forced))throw Error("force map");
    let rows=base.filter(r=>!r.lits.some(l=>u.a.get(Math.abs(l))===Number(l>0))).map(r=>({id:r.id,lits:r.lits.filter(l=>!u.a.has(Math.abs(l)))}));if(!eq(rows,G.rows))throw Error("residual");
   }c.guards++;
  }
  for(let A of x.results)for(let arm of A.arms){
   let G=x.guards.find(g=>g.guard_id===arm.guard_id);if(!G||G.residual_id!==arm.residual_id)throw Error("guard linkage");
   if(G.conflict!==null){if(arm.decision!=="NO")throw Error("early label");continue}
   let rows=G.rows.slice(),idx=new Map(rows.map(r=>[r.id,r]));
   for(let l of arm.learn){let [r,s]=l.parents.map(id=>idx.get(id));if(!r||!s||!r.lits.includes(l.pivot)||!s.lits.includes(-l.pivot))throw Error("pivot");let z=norm([...r.lits.filter(x=>x!==l.pivot),...s.lits.filter(x=>x!==-l.pivot)]);if(!eq(z,l.lits))throw Error("resolvent");idx.set(l.id,l);rows.push(l);c.learned++}
   if(arm.decision==="NO"){
    function tree(t,pins){c.trees++;let u=up(rows,pins);if(t.kind==="leaf")return u.bad;if(u.bad)return true;if(t.kind!=="branch")return false;if(u.a.has(t.v))return tree(u.a.get(t.v)===t.b?t.p:t.q,[...u.a]);return tree(t.p,[...u.a,[t.v,t.b]])&&tree(t.q,[...u.a,[t.v,1-t.b]])}
    if(!tree(arm.proof,[...G.pins,...G.forced]))throw Error("tree");
   }else if(arm.decision==="YES"){
    if(G.pins.some(([v,b])=>arm.witness[v]!==b)||F.some(r=>!r.some(l=>arm.witness[Math.abs(l)]===Number(l>0))))throw Error("witness");c.witnesses++;
   }
  }report.push({alias:x.alias,counts:c});
 }return report;
}
module.exports={verify};
