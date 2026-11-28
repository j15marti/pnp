function nativeHall(F,V,close){
 const t=Date.now(),key=c=>c.slice().sort((a,b)=>a-b).join(","),D=new Map(F.map((c,i)=>[key(c),i+1])),initial=close(F,V),groups=initial.groups,inc=new Map(V.map(v=>[v,[]])),parts=[],cost={partitionNodes:0,partitionRows:0,pairTests:0,edgeChecks:0,augment:0,check:0},cap={nodes:20000,parts:32,rows:5};
 groups.forEach((q,i)=>q.v.forEach(v=>inc.get(v).push(i)));
 function part(used,rs){if(++cost.partitionNodes>cap.nodes||parts.length>=cap.parts)return;if(used.size===V.length){parts.push(rs);return}if(rs.length>=cap.rows)return;let v=V.find(v=>!used.has(v));for(let i of inc.get(v)){cost.partitionRows++;let g=groups[i];if(g.v.some(v=>used.has(v)))continue;part(new Set([...used,...g.v]),[...rs,i])}}
 part(new Set(),[]);
 let units=[],certs=[];for(let v of V.slice().sort((a,b)=>a-b))for(let b of [0,1]){let Z=new Map();if(!b)Z.set(v,"guard");else for(let u of V){let id=D.get(key([-v,-u]));if(id)Z.set(u,id)}
 let found=null;for(let i=0;i<parts.length&&!found;i++)for(let j=0;j<parts.length&&!found;j++){if(i===j)continue;cost.pairTests++;let L=parts[i],R=parts[j],owner=new Map(R.flatMap(k=>groups[k].v.map(v=>[v,k]))),adj=new Map(L.map(k=>[k,[...new Set(groups[k].v.filter(u=>{cost.edgeChecks++;return !Z.has(u)}).map(u=>owner.get(u)))]])),M=new Map();
 function aug(k,seen){for(let r of adj.get(k)){cost.augment++;if(seen.has(r))continue;seen.add(r);if(!M.has(r)||aug(M.get(r),seen)){M.set(r,k);return true}}return false}
 for(let k of L)aug(k,new Set());if(M.size===L.length)continue;let S=new Set(L.filter(k=>![...M.values()].includes(k))),T=new Set(),q=[...S];for(let a=0;a<q.length;a++)for(let r of adj.get(q[a])){cost.augment++;if(T.has(r))continue;T.add(r);if(M.has(r)&&!S.has(M.get(r))){S.add(M.get(r));q.push(M.get(r))}}
 if(S.size<=T.size)throw Error("Hall extraction");let coef=new Map();for(let [sign,rows] of [[1,[...S]],[-1,[...T]]])for(let k of rows){let g=groups[k];if(!D.has(key(g.v)))throw Error("ALO");for(let a=0;a<g.v.length;a++){let u=g.v[a];coef.set(u,(coef.get(u)||0)+sign);for(let z=a+1;z<g.v.length;z++){cost.check++;if(!D.has(key([-u,-g.v[z]])))throw Error("AMO")}}}
 let reasons=[];for(let [u,c] of coef)if(c>0){cost.check++;let r=Z.get(u);if(r===undefined||r==="guard"&&!(b===0&&v===u)||typeof r==="number"&&!(b===1&&key(F[r-1])===key([-v,-u])))throw Error("Hall sign");reasons.push([u,r])}
 found={guard:[v,b],unit:b?-v:v,left:[...S],right:[...T],rhs:S.size-T.size,positiveZeroReasons:reasons,coeff:[...coef]};}
 if(found){units.push(found.unit);certs.push(found)}}
 let C=units.slice(),full=close([...F,...C.map(l=>[l])],V),trials=[];if(full.earlyConflict)for(let u of units){let c=C.filter(v=>v!==u),z=close([...F,...c.map(l=>[l])],V);trials.push({removed:u,retained:c,conflict:z.earlyConflict,work:z.early.reduce((s,r)=>s+r.up.work+(r.ge?.ops||0)+(r.ge?.checks||0),0)});if(z.earlyConflict)C=c}
 let final=close([...F,...C.map(l=>[l])],V);return {initial,groups,parts,units,certs,full,finalUnits:C,final,trials,cost,cap,ms:Date.now()-t}
}
if(typeof module!=="undefined")module.exports={nativeHall};
