function replayPeer(F,cert){
 const canon=c=>[...new Set(c)].sort((a,b)=>a-b),key=c=>c.join(",");
 let C=new Map(),counts={rows:0,clauseScans:0,resolventPairs:0,upVisits:0,nodes:0,unitChecks:0};
 const add=c=>{c=canon(c);C.set(key(c),c)};
 for(let a of F)for(let w=0;w<2**a.v.length;w++){counts.rows++;if(!a.ok.includes(w))add(a.v.map((v,i)=>w>>i&1?-v:v))}
 if(cert.gauge_anchor_root!==Math.min(...[...C.values()].flat().map(Math.abs)))throw Error("gauge");
 add([-cert.gauge_anchor_root]);
 for(let v of cert.pivots){let pos=[],neg=[];for(let c of C.values()){counts.clauseScans++;if(c.includes(v))pos.push(c);else if(c.includes(-v))neg.push(c)}
 if(!pos.length&&!neg.length)throw Error("missing pivot");for(let c of [...pos,...neg])C.delete(key(c));for(let a of pos)for(let b of neg){counts.resolventPairs++;let z=canon([...a.filter(l=>l!==v),...b.filter(l=>l!==-v)]);if(!z.some(l=>z.includes(-l)))add(z)}}
 let cf=[...C.values()];
 function walk(t,pins){counts.nodes++;let P=new Set(pins);
  function classify(c){let free=[];for(let l of c){counts.upVisits++;if(P.has(l))return null;if(!P.has(-l))free.push(l)}return free}
  for(let l of t[1]){counts.unitChecks++;if(!cf.some(c=>{let u=classify(c);return u!==null&&u.length===1&&u[0]===l}))throw Error("invalid annotated unit");P.add(l)}
  if(t[0]==="conflict"){if(!cf.some(c=>{let u=classify(c);return u!==null&&!u.length}))throw Error("invalid conflict");return}
  if(t[0]!=="split"||P.has(t[2])||P.has(-t[2]))throw Error("invalid split");walk(t[3],[...P,t[2]]);walk(t[4],[...P,-t[2]])
 }walk(cert.tree,[]);return {verified:true,remaining:cf.length,counts};
}
module.exports=replayPeer;
