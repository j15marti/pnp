// Node: node early-audit.js DIR; files named compiler,corpus,registry,projection,early,native.
const fs=require('node:fs');const files={"compiler":["research/coordination/shared-eb-2026-11-27/compile.js","21b9d53fb8166c819b24e708656c742cd3c24f10"],"corpus":["research/coordination/shared-unsat-2026-11-27/benchmarks.json","e315349cd6c1fe3fa696504859f28312f6aab69a"],"registry":["research/coordination/shared-eb-2026-11-27/instance-registry-v1.json","0c14cdc57925788cf7a451dcd5aa171dce860f2c"],"projection":["research/proof-spine-2026-11-26/four-partition-nae/2026-11-27_T2_affine_guard_credit/affine-closure.js","d56c096ad434544c918f83cf551d24b930be7b92"],"early":["research/proof-spine-2026-11-26/monotone-exact-22/2026-11-27_1447_T1_intake_feedback/early-signed.js","db3a7ce205eceacb4ea30bd81156597b46c36c96"],"native":["research/agents/ground-up-unsat-bounds/2026-11-27_T3_native_transport_replay/native.js","303d735ba73855b69b47df734d4d3686f760b215"]};const d=Object.fromEntries(Object.keys(files).map(k=>[k,fs.readFileSync(process.argv[2]+'/'+k,'utf8')]));
function run(d){
 const {sha}=new Function(d.native+";return {sha};")(),compile=new Function(d.compiler.slice(d.compiler.indexOf("function compile("),d.compiler.indexOf("function auditLocal"))+"\nreturn compile")(),m={exports:{}},e={exports:{}};
 new Function("module",d.projection)(m);new Function("module",d.early)(e);
 const reg=JSON.parse(d.registry),corpus=JSON.parse(d.corpus),enc=x=>JSON.stringify(x)+"\n",out=[],A=(x,s)=>{if(!x)throw Error(s)};
 for(let alias of ["JOINT-24","RANDOM-3CNF-40"]){
  const t=Date.now(),x=corpus.instances.find(x=>x.id===alias),ent=reg.instances.find(x=>x.alias==="EB-"+alias),g=compile(x),bytes=enc(g.network);
  A(sha(bytes)===ent.sha256&&8*bytes.length===ent.N_bits&&sha(enc(g.source_map))===ent.source_map_sha256&&sha(x.dimacs)===ent.source_cnf.sha256,"auth");
  let n=m.exports.normalize(g.network),f=new Map();for(let a of n.F)for(let v of a.v)f.set(v,(f.get(v)||0)+1);let gauge=[...f].sort((a,b)=>b[1]-a[1]||a[0]-b[0])[0][0];
  let E=e.exports(n.F,gauge);A(!E.conflict,"early contradiction");
  let vars=[...new Set(E.final.flatMap(r=>r.v))].sort((a,b)=>a-b),ix=new Map(vars.map((v,i)=>[v,BigInt(i+1)])),bit=v=>1n<<ix.get(v),B=new Map(),ops={masks:0,parityChecks:0,xors:0},equations=0;
  const parity=w=>{let p=0;while(w){w&=w-1;p^=1}return p};
  for(let a of E.final)for(let mask=1;mask<2**a.v.length;mask++){
   ops.masks++;let b=parity(mask&a.ok[0]);let constant=a.ok.every(w=>{ops.parityChecks++;return parity(mask&w)===b});if(!constant)continue;equations++;let z=BigInt(b);for(let [j,v] of a.v.entries())if(mask>>j&1)z^=bit(v);
   while(z>1n){let k=z.toString(2).length-1;if(!B.has(k)){B.set(k,z);break}z^=B.get(k);ops.xors++}A(z!==1n,"global affine contradiction")
  }
  let keys=[...B.keys()].sort((a,b)=>a-b);for(let v of keys)for(let w of keys)if(w>v&&(B.get(w)>>BigInt(v)&1n)){B.set(w,B.get(w)^B.get(v));ops.xors++}
  let pins=[];for(let [k,z] of B)if(z>>1n===1n<<BigInt(k-1))pins.push([vars[k-1],Number(z&1n)]);
  A(pins.length===0,"new pins need application");
  const guard=[[gauge-1,0]],gid="GUARD-v1:sha256:"+sha(enc(["PNP-GUARD-v1",ent.instance_id,"EB-PORT-PINS-v1",sha(enc(guard))]));
  const reconstruction={root:Array.from(n.root),par:Array.from(n.par),earlyMap:E.map,gauge},rh=sha(enc(E.final)),mh=sha(enc(reconstruction)),rid="RESIDUAL-v1:sha256:"+sha(enc(["PNP-RESIDUAL-v1",ent.instance_id,gid,"EB-TABLE-ROOTPLUS1-v1",rh,mh]));
  out.push({problem_id:"STRICT-EB4-v1",instance:ent.short_id,instance_id:ent.instance_id,original_N_bits:ent.N_bits,source_pin:files,guard_id:gid,residual_id:rid,guard,residualHash:rh,mapHash:mh,original_ids:{vertices:[0,g.network.types.length-1],ports:[0,4*g.network.types.length-1],edges:[0,g.network.edges.length-1]},parents:[],claim:"finite local unary/binary signed table closure and global parity elimination audit before any projection in this separate pass; no additional unary facts beyond gauge",normalization:n.counts,early:E,affine:{rank:B.size,equations,pins,ops},ms:Date.now()-t})
 }
 return out
}
console.log(JSON.stringify(run(d),null,2));
