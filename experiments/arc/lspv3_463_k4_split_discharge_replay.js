/* LSPV-3/463: executable original-source RES-only split-discharge producer.
   No native SPLIT/WEAKEN/DISCHARGE assumed; output only SOURCE and RES.
   Independent Python producer and Node validator in local reproducibility archive.
   Not the historical R_mix341 authoritative accepted-byte checker. */
function replay(){
  const edges=[];for(let u=0;u<4;u++)for(let v=u+1;v<4;v++)edges.push([u,v]);
  const norm=a=>[...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);
  const key=a=>norm(a).join(",");
  const taut=a=>a.some(z=>a.includes(-z));
  const resolve=(a,b,p)=>{if(!a.includes(p)||!b.includes(-p))throw Error("pivot");return norm([...a.filter(z=>z!==p),...b.filter(z=>z!==-p)])};
  const src=[];
  for(let v=0;v<4;v++){const ids=edges.map((e,i)=>e.includes(v)?i+1:null).filter(Boolean);
   for(let q=0;q<8;q++){let bs=[q>>2&1,q>>1&1,q&1];if((bs[0]+bs[1]+bs[2])%2===(v===0?1:0))continue;
    src.push(norm(ids.map((i,j)=>bs[j]?-i:i)));}}
  const nodes=src.map((clause,i)=>({id:i+1,rule:"SOURCE",source_id:i+1,clause}));const cache=new Map(nodes.map(x=>[key(x.clause),x.id]));
  function intern(a,b,p){const clause=resolve(nodes[a-1].clause,nodes[b-1].clause,p);if(taut(clause))throw Error("taut derived");const k=key(clause);if(cache.has(k))return cache.get(k);const id=nodes.length+1;nodes.push({id,rule:"RES",parents:[a,b],pivot:p,clause});cache.set(k,id);return id}
  function branch(truth){let lit=truth?1:-1,active=new Map();for(let i=0;i<src.length;i++){const c=src[i];if(c.includes(lit))continue;const d=c.filter(x=>x!==-lit);active.set(key(d),{restricted:d,ref:i+1})}
   for(let p=2;p<=6;p++){
    const arr=[...active.values()],positive=arr.filter(z=>z.restricted.includes(p)),negative=arr.filter(z=>z.restricted.includes(-p));
    let out=new Map(arr.filter(z=>!z.restricted.includes(p)&&!z.restricted.includes(-p)).map(z=>[key(z.restricted),z]));
    for(const a of positive)for(const b of negative){const r=resolve(a.restricted,b.restricted,p),k=key(r);if(taut(r)||out.has(k))continue;
      const rid=intern(a.ref,b.ref,p);out.set(k,{restricted:r,ref:rid});}
    active=out;if(active.has(""))break;
   }
   if(!active.has(""))throw Error("no branch refutation");return active.get("").ref;
  }
  const pos=branch(true),neg=branch(false);const P=nodes[pos-1].clause,N=nodes[neg-1].clause;
  let root;if(P.length===0||N.length===0)root=P.length===0?pos:neg;
  else if(P.length===1&&P[0]===-1&&N.length===1&&N[0]===1)root=intern(neg,pos,1);
  else throw Error("bad branch endpoints: "+JSON.stringify([P,N]));
  let used=new Set();function mark(i){if(used.has(i))return;used.add(i);for(const j of nodes[i-1].parents||[])mark(j)}mark(root);
  const proof=nodes.filter(z=>used.has(z.id));const depth=new Map();for(const n of proof)depth.set(n.id,n.rule==="SOURCE"?0:1+Math.max(...n.parents.map(p=>depth.get(p))));
  let paid=proof.filter(z=>z.rule==="RES").length;
  return {source:src,proof,root,paid,span:depth.get(root),nodes:proof.length,endpoint:[P,N]};
}
const result=replay();
if(result.paid!==31||result.nodes!==47||result.span!==6)throw Error('failed finite control');
console.log(JSON.stringify(result,null,2));
