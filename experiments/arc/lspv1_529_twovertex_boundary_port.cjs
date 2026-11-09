'use strict';
/* LSPV-1/529: original-source two-vertex q=3 Tseitin boundary elimination.
 * All output clauses derived by exact signed binary Resolution. */
const DATA = (()=>{
  const Q=3, chargeA=0, chargeB=1, groups='UVEWT';
  const variable=(g,k)=>3*groups.indexOf(g)+k+1;
  const normalize=a=>[...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);
  const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
  const records=[],lookup=new Map(),output=[];
  const key=c=>JSON.stringify(normalize(c));
  function source(c,tag){
    c=normalize(c);if(c.some(x=>c.includes(-x)))throw Error('taut source');
    if(lookup.has(key(c)))throw Error('duplicate source');
    const id=records.length;records.push({id,rule:'SOURCE',clause:c,tag});
    lookup.set(key(c),id);return id;
  }
  function row(g,i,j,e){return [-variable(g,i),-variable(g==='U'?'V':'T',j),-variable('E',e)];}
  for(const g of groups)source([...Array(Q)].map((_,k)=>variable(g,k)),'ALO-'+g);
  for(let a=0;a<Q;a++)for(let b=0;b<Q;b++)for(let e=0;e<Q;e++)
    if((a+b+e)%Q!==chargeA)source([-variable('U',a),-variable('V',b),-variable('E',e)],'A');
  for(let w=0;w<Q;w++)for(let t=0;t<Q;t++)for(let e=0;e<Q;e++)
    if((w+t-e+Q)%Q!==chargeB)source([-variable('W',w),-variable('T',t),-variable('E',e)],'B');
  const sourceCount=records.length;
  if(sourceCount!==41)throw Error('wrong source count');
  const allowed=new Set([...lookup.keys()]);
  function resolveExact(a,b,pivot){
    if(!a.includes(pivot)||!b.includes(-pivot))throw Error('invalid signed pivot');
    const c=normalize([...a.filter(x=>x!==pivot),...b.filter(x=>x!==-pivot)]);
    if(c.some(x=>c.includes(-x)))throw Error('tautological resolvent');
    return c;
  }
  function step(left,right,pivot){
    const clause=resolveExact(records[left].clause,records[right].clause,pivot);
    const id=records.length;records.push({id,rule:'RES',parents:[left,right],pivot,clause});return id;
  }
  const alo=lookup.get(key([variable('E',0),variable('E',1),variable('E',2)]));
  const forced=new Map();
  for(let a=0;a<Q;a++)for(let b=0;b<Q;b++){
    const target=(chargeA-a-b+2*Q)%Q;
    let p=alo;
    for(let j=0;j<Q;j++)if(j!==target)
      p=step(p,lookup.get(key([-variable('U',a),-variable('V',b),-variable('E',j)])),variable('E',j));
    if(!same(records[p].clause,normalize([-variable('U',a),-variable('V',b),variable('E',target)])))throw Error('forced E mismatch');
    forced.set(a*Q+b,p);
  }
  for(let a=0;a<Q;a++)for(let b=0;b<Q;b++)
    for(let w=0;w<Q;w++)for(let t=0;t<Q;t++){
      const e=(chargeA-a-b+2*Q)%Q;
      if((w+t-e+Q)%Q===chargeB)continue;
      const id=step(forced.get(a*Q+b),
         lookup.get(key([-variable('W',w),-variable('T',t),-variable('E',e)])),variable('E',e));
      const expected=normalize([-variable('U',a),-variable('V',b),-variable('W',w),-variable('T',t)]);
      if(!same(records[id].clause,expected))throw Error('bad boundary output');
      output.push(id);
    }
  if(records.length!==113||output.length!==54)throw Error('unexpected cardinality');
  // Separate strict replay: validate every record, parent topology, and exact source membership.
  for(let i=0;i<records.length;i++){
    const r=records[i];
    if(r.id!==i)throw Error('id mismatch');
    if(r.rule==='SOURCE'){if(!allowed.has(key(r.clause)))throw Error('foreign source');}
    else{
      const [l,rid]=r.parents;
      if(l>=i||rid>=i||l<0||rid<0)throw Error('forward reference');
      const newClause=resolveExact(records[l].clause,records[rid].clause,r.pivot);
      if(!same(newClause,r.clause))throw Error('corrupt clause');
    }
  }
  const sat=(c,mask)=>c.some(x=>Boolean((mask>>(Math.abs(x)-1))&1)===(x>0));
  let numModels=0;
  for(let mask=0;mask<(1<<15);mask++){
    if(records.slice(0,sourceCount).every(r=>sat(r.clause,mask))){
      numModels++;
      if(output.some(id=>!sat(records[id].clause,mask)))throw Error('unsound output');
    }
  }
  if(numModels!==27)throw Error('wrong model count');
  let bad=0;
  for(const trial of [
    ()=>resolveExact(records[41].clause,records[42].clause,999),
    ()=>resolveExact([1],[2],1),
    ()=>resolveExact([1],[-2],1)]){
    try{trial()}catch(e){bad++;}
  }
  if(bad!==3)throw Error('corrupt controls escaped');
  const depth=[];
  for(const r of records)depth.push(r.rule==='SOURCE'?0:1+Math.max(...r.parents.map(p=>depth[p])));
  const span=Math.max(...output.map(i=>depth[i]));
  if(span!==3)throw Error('wrong span');
  const summary={q:Q,chargeA,chargeB,inputBooleanVariables:15,originalSourceClauses:sourceCount,
    sourceALO:5,sourceForbidden:36,paidResolutionNodes:records.length-sourceCount,
    totalRecords:records.length,sourceInferencePremiseReferences:2*(records.length-sourceCount),
    portInferences:18,outputInferences:54,fullBoundaryForbiddenClauses:output.length,
    satisfyingOneHotBoundaryAssignments:27,unsatisfyingOneHotBoundaryAssignments:54,
    fullBooleanAssignmentsChecked:1<<15,fullBooleanSourceModels:numModels,
    weightedCriticalPathSpan:span,corruptControlsRejected:bad,
    status:'COMPUTATIONAL Resolution-fragment, not historical R_mix341 bytes'};
  return {summary,records,outputIDs:output};
})();
if(typeof process!=='undefined'&&process.stdout)console.log(JSON.stringify(DATA.summary,null,2));
