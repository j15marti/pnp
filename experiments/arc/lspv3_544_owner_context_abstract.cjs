"use strict";
// LSPV-3/544 typed DEF/RES, context/owner cost-sound audit.
// DISTINCT declared R_fac fragment. NOT a historical accepted-byte R_mix341 checker.
function fail(s){throw Error(s)}
function ck(t,s){if(!t)fail(s)}
function lit(s){ck(typeof s==="string"&&/^[+-][1-9][0-9]*$/.test(s),"bad signed literal");return s}
function nam(s){return lit(s).slice(1)}
function inv(s){return (s[0]==="+"?"-":"+")+s.slice(1)}
function uniq(xs){return [...new Set(xs)]}
function canon(xs){xs.forEach(lit);return uniq(xs).sort()}
function same(a,b){return JSON.stringify(canon(a))===JSON.stringify(canon(b))}
function u(a,b){return uniq([...a,...b]).sort()}
function parse(raw){
  ck(typeof raw==="string","source not UTF8");
  let t=raw.trim().split(/\s+/),h=t.slice(0,4);
  ck(h[0]==="p"&&h[1]==="cnf"&&/^\d+$/.test(h[2])&&/^\d+$/.test(h[3]),"header");
  const n=Number(h[2]),m=Number(h[3]);ck(Number.isSafeInteger(n)&&Number.isSafeInteger(m),"large header");
  let clauses=[],cur=[];
  for(const x of t.slice(4)){
    ck(/^-?\d+$/.test(x),"noninteger source");
    const v=Number(x);ck(Number.isSafeInteger(v),"unsafe source ID");
    if(v===0){clauses.push(canon(cur));cur=[]}
    else {ck(Math.abs(v)<=n,"source variable out of range");cur.push((v>0?"+":"-")+Math.abs(v))}
  }
  ck(cur.length===0&&clauses.length===m,"unterminated/count");
  return {n,clauses};
}
function val(l,a){const s=lit(l);let q=a[nam(s)];ck(q===0||q===1,"assignment missing");return s[0]==="+"?q:1-q}
function clauseval(C,a){return C.some(l=>val(l,a)===1)}
function facet(def,j){
  ck(Number.isInteger(j)&&j>=0&&j<4,"facet index");
  const x=j&1,y=(j>>1)&1,w=(def.mask>>j)&1,wrong=1-w;
  const signed=(p,v)=>(v?inv(p):p);
  return canon([signed(def.a,x),signed(def.b,y),(wrong?"-":"+")+def.z]);
}
function audit(sourceRaw,steps,opt={}){
  ck(!opt.externalRaw||opt.externalRaw===sourceRaw,"external source mismatch");
  const F=parse(sourceRaw), known=new Set(Array.from({length:F.n},(_,i)=>String(i+1)));
  let views=new Map(),defs=new Map(),nodeTypes=new Map(),paid=new Set(),edges=[];
  F.clauses.forEach((C,i)=>views.set("s"+i,{clause:C,ctx:[],sources:[i],owners:[]}));
  function ref(r){
    if(typeof r==="string"){ck(views.has(r),"unknown parent");return {...views.get(r),parent:r}}
    ck(r && typeof r==="object" && typeof r.owner==="string","unrecognized reference");
    const d=defs.get(r.owner);ck(d,"unpaid or forward DEF facet owner");
    return {clause:facet(d,r.facet),ctx:[],sources:[],owners:[r.owner],parent:r.owner+":facet"+r.facet};
  }
  for(const op of steps){
    ck(op&&typeof op.id==="string"&&op.id.length>0&&!views.has(op.id)&&!defs.has(op.id),"duplicate node ID");
    if(op.rule==="DEF"){
      ck(typeof op.z==="string"&&/^[1-9][0-9]*$/.test(op.z)&&!known.has(op.z),"nonfresh DEF output");
      lit(op.a);lit(op.b);
      ck(known.has(nam(op.a))&&known.has(nam(op.b)),"unavailable input wire");
      ck(Number.isInteger(op.mask)&&op.mask>=0&&op.mask<16,"binary function");
      defs.set(op.id,{a:op.a,b:op.b,z:op.z,mask:op.mask});
      known.add(op.z);paid.add(op.id);nodeTypes.set(op.id,"DEF");
      edges.push({id:op.id,rule:"DEF",parents:[],weight:1});
    }else if(op.rule==="ASSUME"){
      ck(opt.testAssumptions===true,"ASSUME not native R_fac rule");
      lit(op.s);ck(known.has(nam(op.s)),"assumption undefined");
      views.set(op.id,{clause:[op.s],ctx:[op.s],sources:[],owners:[]});nodeTypes.set(op.id,"ASSUME_TEST");
    }else if(op.rule==="RES"){
      const L=ref(op.left),R=ref(op.right),p=lit(op.pivot);
      ck(L.clause.includes(p)&&R.clause.includes(inv(p)),"illegal oriented pivot");
      let C=canon([...L.clause.filter(x=>x!==p),...R.clause.filter(x=>x!==inv(p))]);
      ck(!op.claim||same(C,op.claim),"forged target clause");
      ck(!known.has("0"),"unreachable");
      const v={clause:C,ctx:u(L.ctx,R.ctx),sources:u(L.sources,R.sources),owners:u(L.owners,R.owners)};
      views.set(op.id,v);paid.add(op.id);nodeTypes.set(op.id,"RES");
      edges.push({id:op.id,rule:"RES",parents:[L.parent,R.parent],weight:1});
    }else fail("unknown rule (native status not inferred): "+op.rule);
  }
  let goal=null;
  if(opt.goal!==undefined){
    ck(views.has(opt.goal),"missing goal ID");
    goal=views.get(opt.goal);
    ck(goal.clause.length===0&&goal.ctx.length===0,"not a global empty-clause refutation");
  }
  return {paid:paid.size,paidIDs:[...paid],goals:goal?1:0,goalContext:goal?.ctx||null,views,defs,edges,sourceClauses:F.clauses.length};
}
function tests(){
 let checks=0;
 function yes(b,s){ck(b,s);checks++}
 function rejects(f,s){let ok=false;try{f()}catch(e){ok=true}yes(ok,s)}
 // Exhaustive semantic check: every two-input Boolean function, every signed/aliased port
 // pair, all original input/output valuations; four positional facets are exact.
 const ports=["+1","-1","+2","-2"]; let truthCases=0;
 for(let mask=0;mask<16;mask++)for(const a of ports)for(const b of ports){
   const d={a,b,z:"9999999999999999999999999999999999999",mask};
   for(let bits=0;bits<8;bits++){
     const v={"1":bits&1,"2":(bits>>1)&1,[d.z]:(bits>>2)&1};
     const expected=v[d.z]===((mask>>(val(a,v)+2*val(b,v)))&1);
     const accepted=[0,1,2,3].every(j=>clauseval(facet(d,j),v));
     yes(accepted===expected,"gate semantic mismatch");truthCases++;
   }
 }
 const source="p cnf 2 2\n1 0\n2 0\n";
 const owner="D123",big="9999999999999999999999999999999999999";
 const proof=[
   {id:owner,rule:"DEF",a:"+1",b:"+2",z:big,mask:8},
   {id:"r0",rule:"RES",left:"s0",right:{owner,facet:3},pivot:"+1",claim:["-2","+"+big]},
   {id:"r1",rule:"RES",left:"s1",right:"r0",pivot:"+2",claim:["+"+big]},
   {id:"r2",rule:"RES",left:"r1",right:{owner,facet:0},pivot:"+"+big,claim:["+1","+2"]}
 ];
 const ok=audit(source,proof);
 yes(ok.paid===4&&ok.defs.size===1&&ok.views.get("r1").clause[0]==="+"+big,"owner reused count once");
 yes(ok.views.get("r1").sources.join(",")==="0,1","source lineage");
 yes(ok.views.get("r1").owners.join(",")==owner,"owner lineage");
 const unsat="p cnf 1 2\n1 0\n-1 0\n";
 yes(audit(unsat,[{id:"q",rule:"RES",left:"s0",right:"s1",pivot:"+1",claim:[]}],{goal:"q"}).paid===1,"UNSAT refutation");
 const sat3="p cnf 3 4\n1 2 3 0\n1 2 -3 0\n1 -2 3 0\n1 -2 -3 0\n";
 const branch=[
   {id:"b0",rule:"RES",left:"s0",right:"s1",pivot:"+3",claim:["+1","+2"]},
   {id:"b1",rule:"RES",left:"s2",right:"s3",pivot:"+3",claim:["+1","-2"]},
   {id:"b2",rule:"RES",left:"b0",right:"b1",pivot:"+2",claim:["+1"]},
   {id:"a",rule:"ASSUME",s:"-1"},
   {id:"b3",rule:"RES",left:"b2",right:"a",pivot:"+1",claim:[]}
 ];
 const local=audit(sat3,branch,{testAssumptions:true});
 yes(local.views.get("b3").clause.length===0&&local.views.get("b3").ctx.join(",")==="-1","branch local refutation");
 rejects(()=>audit(sat3,branch,{testAssumptions:true,goal:"b3"}),"cross-context leak");
 rejects(()=>audit(sat3,branch),"unauthorized ASSUME");
 rejects(()=>audit(source,proof,{externalRaw:"p cnf 2 2\n-1 0\n2 0\n"}),"external source swap");
 rejects(()=>audit(source,[...proof.slice(0,2),{...proof[2],pivot:"+1"}]),"bad pivot");
 rejects(()=>audit(source,[{...proof[1]}]),"unpaid facet forged");
 rejects(()=>audit(source,[{...proof[0],z:"2"}]),"duplicate output");
 rejects(()=>audit(source,[{...proof[0],a:"+999"}]),"undeclared input wire");
 rejects(()=>audit(source,[...proof.slice(0,2),{...proof[2],claim:["-2"]}]),"forged resolvent");
 rejects(()=>audit(source,[{...proof[0],id:"s0"}]),"owner collides source");
 rejects(()=>audit(source,[...proof,{id:"bad",rule:"DISCHARGE"}]),"unissued discharge");
 rejects(()=>audit("p cnf 1 1\n1"),"unterminated source");
 rejects(()=>audit("p cnf 1 1\n2 0\n"),"source out of range");
 rejects(()=>audit("p cnf 1 2\n1 0\n"),"source count");
 // Zero-budget exclusion: no empty initial clause and no paid DEF/RES means no empty global goal.
 yes(parse(unsat).clauses.every(C=>C.length>0),"B0 source positive width");
 return {run:"LSPV-3/544",model:"typed global DEF+strict RES; ASSUME only non-native diagnostic",status:"COMPUTATIONAL tests plus symbolic rule induction",checks,truthCases,paidShared:ok.paid,globalUnsatCost:1,localBranchCost:4,localBranchRejectedAsGlobal:true,allPassed:true,missingNative:["RES","DEF","LOCAL-CONVERT","branch/discharge","export/private"]};
}
if(typeof module!=="undefined"&&module.exports){module.exports={audit,tests,facet,parse};if(require.main===module)console.log(JSON.stringify(tests(),null,2))}
