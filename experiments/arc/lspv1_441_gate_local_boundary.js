// LSPV-1/441: typed GATE-LOCAL compiler for REFEREE381, not historical R_mix341.
"use strict";
function nrm(a){return [...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||y-x);}
function eq(a,b){return JSON.stringify(nrm(a))===JSON.stringify(nrm(b));}
function facets(d){return [[-d.out,d.a],[-d.out,d.b],[d.out,-d.a,-d.b]].map(nrm);}
function compile(x){
 const defs=x.trace.nodes.filter(n=>n.kind==="DEF"),extra=[];
 for(const d of defs)for(let j=0;j<3;j++)extra.push({id:"P"+d.id+"F"+j,kind:"LOCAL",parent:d.id,gate_facet:j,clause:facets(d)[j]});
 const ref=v=>typeof v==="string"&&/^N\d+#f[0-2]$/.test(v)?"P"+v.split("#")[0]+"F"+v.slice(-1):v;
 const nodes=[...defs,...extra,...x.trace.nodes.filter(n=>n.kind!=="DEF").map(n=>{let y={...n};for(const f of ["left","right","parent"])if(y[f])y[f]=ref(y[f]);return y;})];
 return {...x,trace:{sources:x.trace.sources,nodes},paid_nodes:nodes.length,gate_local_added:extra.length};
}
function verify(x){
 let checks=0;const ok=(p,s)=>{checks++;if(!p)throw Error(s);};
 const obj=new Map(),deps=new Map(),depth=new Map(),kinds={};
 const get=v=>{ok(obj.has(v),"absent parent "+v);return obj.get(v);};
 const lit=(l,a)=>l>0?!!a[Math.abs(l)]:!a[Math.abs(l)];
 const sat=(c,a)=>c.some(l=>lit(l,a));
 const support=z=>z.kind==="AND3"?z.support:[...new Set(z.clause.map(Math.abs))];
 const val=(z,a)=>z.kind==="AND3"?z.good.has(z.support.reduce((v,q,i)=>v|((a[q]||0)<<i),0)):sat(z.clause,a);
 const lines=x.dimacs.trim().split("\n");ok(lines[0]==="p cnf "+x.source_variables+" "+x.source_clauses,"wrong DIMACS header");
 const originals=lines.slice(1).map(s=>{const a=s.trim().split(/\s+/).map(Number);ok(a.at(-1)===0,"missing terminator");return a.slice(0,-1);});
 const bag=a=>{const m=new Map();for(const c of a){const k=JSON.stringify(nrm(c));m.set(k,(m.get(k)||0)+1);}return JSON.stringify([...m].sort());};
 ok(originals.length===x.trace.sources.length&&bag(originals)===bag(x.trace.sources.map(s=>s.clause)),"original-source mismatch");
 for(const s of x.trace.sources){ok(!obj.has(s.id),"duplicate source");obj.set(s.id,{...s,kind:"SRC"});deps.set(s.id,[]);depth.set(s.id,0);}
 const fresh=new Set();
 for(const v of x.trace.nodes){
  const z={...v};ok(!obj.has(z.id),"duplicate node");kinds[z.kind]=(kinds[z.kind]||0)+1;let p=[];
  if(z.kind==="DEF"){ok(z.out>x.source_variables&&!fresh.has(z.out),"nonfresh DEF");fresh.add(z.out);}
  else if(z.kind==="LOCAL"&&z.gate_facet!==undefined){
   const o=get(z.parent);ok(o.kind==="DEF"&&z.gate_facet>=0&&z.gate_facet<3&&eq(z.clause,facets(o)[z.gate_facet]),"illegal paid facet");
   for(let q=0;q<8;q++){const S=[Math.abs(o.a),Math.abs(o.b),o.out],a={};S.forEach((w,j)=>a[w]=(q>>j)&1);if(a[o.out]===Number(lit(o.a,a)&&lit(o.b,a)))ok(sat(z.clause,a),"unsound paid facet");}
   p=[z.parent];
  }else if(z.kind==="RES"){
   const a=get(z.left),b=get(z.right),t=z.pivot;ok(Array.isArray(a.clause)&&Array.isArray(b.clause)&&Number.isInteger(t)&&t>0,"bad RES operands");
   const ab=a.clause.includes(t)&&b.clause.includes(-t),ba=a.clause.includes(-t)&&b.clause.includes(t);
   ok((ab||ba)&&!(ab&&ba),"bad RES pivot");
   ok(eq(z.clause,nrm([...a.clause,...b.clause].filter(w=>Math.abs(w)!==t))),"bad resolvent");p=[z.left,z.right];
  }else if(z.kind==="AND3"){
   const a=get(z.left),b=get(z.right),S=z.support;
   ok(S.length<=3&&S.length>0&&new Set(S).size===S.length&&[...support(a),...support(b)].every(w=>S.includes(w)),"bad AND3 support");
   z.good=new Set();for(let q=0;q<(1<<S.length);q++){const x={};S.forEach((w,j)=>x[w]=(q>>j)&1);const g=val(a,x)&&val(b,x);if(g)z.good.add(q);
    if(z.affine)ok(g===(z.affine.vars.reduce((u,w)=>u^(x[w]||0),0)===z.affine.rhs),"bad AND3 affine annotation");}
   p=[z.left,z.right];
  }else if(z.kind==="XOR"){
   const a=get(z.left),b=get(z.right);ok(!!a.affine&&!!b.affine,"XOR parent not affine");
   const s=new Set(a.affine.vars);for(const w of b.affine.vars){if(s.has(w))s.delete(w);else s.add(w);}
   ok(JSON.stringify([...s].sort((a,b)=>a-b))===JSON.stringify([...z.affine.vars].sort((a,b)=>a-b))&&(a.affine.rhs^b.affine.rhs)===z.affine.rhs,"bad XOR conclusion");p=[z.left,z.right];
  }else if(z.kind==="LOCAL"){
   const a=get(z.parent);ok(!!a.affine,"LOCAL row parent");
   const S=[...new Set([...a.affine.vars,...z.clause.map(Math.abs)])];ok(S.length<=3,"LOCAL support >3");
   for(let q=0;q<(1<<S.length);q++){const x={};S.forEach((w,j)=>x[w]=(q>>j)&1);
    if(a.affine.vars.reduce((u,w)=>u^(x[w]||0),0)===a.affine.rhs)ok(sat(z.clause,x),"bad LOCAL implication");}
   p=[z.parent];
  }else throw Error("unknown rule "+z.kind);
  obj.set(z.id,z);deps.set(z.id,p);depth.set(z.id,1+Math.max(0,...p.map(w=>depth.get(w))));
 }
 const last=obj.get(x.final_empty);ok(last&&last.clause&&last.clause.length===0,"root not empty");
 const used=new Set(),stack=[x.final_empty];while(stack.length){const v=stack.pop();if(used.has(v))continue;used.add(v);stack.push(...deps.get(v));}
 ok(x.trace.nodes.every(v=>used.has(v.id))&&x.trace.sources.every(v=>used.has(v.id)),"dead sources/paid nodes");
 return {graph:x.graph,h:x.vertices,original_paid:x.paid_nodes-x.gate_local_added,compiled_paid:x.paid_nodes,added_local:x.gate_local_added,source_clauses:x.source_clauses,span:depth.get(x.final_empty),live:used.size,checks,kinds};
}
function run(raw){
 const results=[];let rejected=0;
 for(const original of raw.instances){
  const x=compile(original);results.push(verify(x));
  const invalid=fn=>{const y=JSON.parse(JSON.stringify(x));fn(y);let fail=false;try{verify(y)}catch(e){fail=true;}if(!fail)throw Error("bad mutation accepted");rejected++;};
  invalid(y=>{y.trace.sources[0].clause[0]*=-1;});
  invalid(y=>{y.trace.nodes.find(z=>z.gate_facet===2).clause=[1];});
  invalid(y=>{y.trace.nodes.find(z=>z.kind==="RES").pivot=999999;});
  invalid(y=>{y.trace.nodes.find(z=>z.kind==="XOR").affine.rhs^=1;});
  invalid(y=>{y.trace.nodes=y.trace.nodes.filter(z=>z.id!=="PN1F2");});
  invalid(y=>{y.trace.nodes.find(z=>z.gate_facet===1).parent="FAKE";});
 }
 return {schema:"LSPV1_441_GATELOCAL_BOUNDARY/v1",status:"CONDITIONAL GATE-LOCAL, not authenticated R_mix341",source:"LSPV5_REFEREE381",cases:results,hostile_rejections:rejected,all_passed:true};
}
// Usage: node lspv1_441_gate_local_boundary.js upstream381.json [expanded_certificate.json]
if(typeof process!=="undefined"&&process.argv[1]&&process.argv[1].includes("lspv1_441_gate_local_boundary")){
 const fs=require("node:fs"),upstream=JSON.parse(fs.readFileSync(process.argv[2],"utf8"));
 const summary=run(upstream);
 if(process.argv[3])fs.writeFileSync(process.argv[3],JSON.stringify({schema:summary.schema,cases:upstream.instances.map(compile)}));
 process.stdout.write(JSON.stringify(summary,null,2)+"\n");
}
