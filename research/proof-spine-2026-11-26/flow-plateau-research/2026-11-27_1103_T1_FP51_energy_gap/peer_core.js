
// Translate a peer clause-projection proof into a sufficient source B-owner core.
// Each clause is paired with a set of original B owners whose conjunction entails it.
// Gauge has empty provenance; the caller must independently check complement symmetry.
function peerCore(G,pn,trace,tree,cap=3000000){
 const canon=a=>[...new Set(a)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b),key=a=>a.join(",");
 let M=new Map(),events=0,ownerVisits=0,scans=0,pairs=0,leaves=0;
 function merge(A,B){ownerVisits+=A.size+B.size;if(ownerVisits>cap)throw Error("owner cap");return new Set([...A,...B])}
 function put(M,c,S){let k=key(c),old=M.get(k);if(!old||S.size<old.S.size)M.set(k,{c,S})}
 for(let v=0;v<G.types.length;v++)if(G.types[v]==="B"){let ps=[0,1,2,3].map(i=>4*v+i),vs=canon(ps.map(p=>pn.root[p]));
  for(let w=0;w<2**vs.length;w++){events++;let z=ps.reduce((s,p)=>s+(((w>>vs.indexOf(pn.root[p]))&1)^pn.sign[p]),0);
   if(z!==2)put(M,vs.map((r,i)=>(w>>i)&1?-r:r),new Set([v]))}}
 put(M,[-pn.gauge],new Set());
 if([...M.keys()].sort().join(";")!==pn.C.map(key).sort().join(";"))throw Error("base clauses mismatch");
 for(let v of trace){let pos=[],neg=[];for(let f of M.values()){if(++scans>cap)throw Error("scan cap");if(f.c.includes(v))pos.push(f);if(f.c.includes(-v))neg.push(f)}
  for(let f of [...pos,...neg])M.delete(key(f.c));
  for(let a of pos)for(let b of neg){pairs++;let c=canon([...a.c.filter(l=>l!==v),...b.c.filter(l=>l!==-v)]);if(c.some(l=>c.includes(-l)))continue;put(M,c,merge(a.S,b.S))}
 }
 function conflict(pins){let A=new Map(pins.map(([v,b])=>[v,{b,S:new Set()}]));
  for(;;){let change=false;for(let f of M.values()){if(++scans>cap)throw Error("scan cap");let free=[],sat=false,ante=[];for(let l of f.c){let x=A.get(Math.abs(l));if(!x)free.push(l);else if(x.b===Number(l>0)){sat=true;break}else ante.push(x.S)}if(sat||free.length>1)continue;
   let S=new Set(f.S);for(let a of ante)S=merge(S,a);
   if(!free.length)return S;
   A.set(Math.abs(free[0]),{b:Number(free[0]>0),S});change=true;
  }if(!change)throw Error("unproved leaf")}
 }
 function visit(t,pins){if(t===null){leaves++;return conflict(pins)}return merge(visit(t[1],[...pins,[t[0],0]]),visit(t[2],[...pins,[t[0],1]]))}
 const core=[...visit(tree,[])].sort((a,b)=>a-b);
 return {core,projected:[...M.values()].map(f=>f.c),metrics:{events,ownerVisits,scans,pairs,leaves}}
}

if(typeof module!=="undefined")module.exports={peerCore};
