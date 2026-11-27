function controlReplay(raw,h,c){
const {sha,independentNormalize,verifyTrace}=Function(h.slice(0,h.indexOf("// Node runner"))+";return {sha,independentNormalize,verifyTrace}")();
const compile=Function(c.slice(c.indexOf("function compile"),c.indexOf("function auditLocal"))+";return compile")();
const t=JSON.parse(raw).hostile,g=compile({nvars:4,dimacs:t.dimacs}),s=JSON.stringify(g.network)+"\n";
if(sha(s)!==t.nativeSha||8*s.length!==t.N||sha(t.dimacs)!==t.cnfId.split(":").at(-1)||8*t.dimacs.length!==t.cnfN||sha(JSON.stringify(g.source_map)+"\n")!==t.sourceMapSha)throw Error("identity");
let I=independentNormalize(g.network);if(!I.fs.every(f=>f.ok.every(w=>f.ok.includes(w^(2**f.vs.length-1)))))throw Error("gauge");
function pin(F,v){return F.map(f=>{let i=f.vs.indexOf(v);if(i<0)return f;return{...f,vs:f.vs.filter(x=>x!==v),ok:f.ok.filter(w=>!(w>>i&1)).map(w=>(w&((1<<i)-1))|((w>>(i+1))<<i))}})}
let V=verifyTrace(pin(I.fs,t.gauge),t.trace);if(JSON.stringify(V.fs)!==JSON.stringify(t.rootFactors))throw Error("factor replay");
const F=V.fs,ids=[...new Set(F.flatMap(f=>f.vs))].sort((a,b)=>a-b),r=ids.length;
if(r!==4||F.length!==16||F.some(f=>JSON.stringify(f.vs)!==JSON.stringify(ids)||f.ok.length!==15))throw Error("unexpected residual");
let forbidden=F.map(f=>({factor:f.id,word:Array.from({length:16},(_,i)=>i).find(w=>!f.ok.includes(w))}));if(new Set(forbidden.map(x=>x.word)).size!==16)throw Error("not cover");
let membership=0,keep=[];for(let w=0;w<16;w++){let valid=true;for(let f of F){membership++;if(!f.ok.includes(w)){valid=false;break}}if(valid)keep.push(w)}
if(keep.length)throw Error("nonempty intersection");
 // Independently prove named guard-pool stagnation. Check each <=2-bit context and local surviving coordinate supports.
 let contexts=0,inspections=0;
 for(let mask=0;mask<16;mask++){let k=mask.toString(2).replace(/0/g,"").length;if(k>2)continue;for(let value=0;value<16;value++){if(value&~mask)continue;contexts++;for(let f of F){let R=f.ok.filter(w=>{inspections++;return (w&mask)===value});if(!R.length)throw Error("contradictory guard");for(let j=0;j<4;j++)if(!(mask>>j&1)){if(!R.some(w=>w>>j&1)||!R.some(w=>!(w>>j&1)))throw Error("extra bit")}}}}
 // Verify no row can be removed by a one-bit split: its actual local word appears under its own bit.
 let rowChecks=0;for(let f of F)for(let w of f.ok)for(let j=0;j<4;j++){rowChecks++;if(!f.ok.some(u=>u===w&&(u>>j&1)===(w>>j&1)))throw Error("row")}
 return{instance_id:t.nativeId,N:t.N,ids,forbidden,terminal:"UNSAT",join:{memberships:membership,result:keep},guardRefusal:{contexts,inspections,rowChecks},projection:{tests:V.tests,scans:V.scans},normalization:I.counts,cnf:t.dimacs,sourceMapSha:t.sourceMapSha,original_ids:t.original_ids}
}
if(typeof module!=="undefined"){module.exports={controlReplay};if(require.main===module){const fs=require("node:fs");console.log(JSON.stringify(controlReplay(...process.argv.slice(2).map(p=>fs.readFileSync(p,"utf8")))))}}
