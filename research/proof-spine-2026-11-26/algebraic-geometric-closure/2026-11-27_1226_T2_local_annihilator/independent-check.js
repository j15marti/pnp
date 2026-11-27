const fs=require('node:fs');
function independent(raws){
const [c,corp,reg,h,res]=raws,compile=Function(c.slice(c.indexOf("function compile"),c.indexOf("function auditLocal"))+";return compile")(),H=Function(h.slice(0,h.indexOf("function runCase"))+";return {sha,normalize,independentNormalize,eliminate,verifyTrace,gauge}")(),B=JSON.parse(corp),R=JSON.parse(reg),Z=JSON.parse(res),A=(x,m)=>{if(!x)throw Error(m)},key=v=>[...new Set(v)].sort((a,b)=>a-b).join(),out=[];
for(const [i,id] of ["JOINT-24","RANDOM-3CNF-40"].entries()){
let x=B.instances.find(z=>z.id===id),e=R.instances.find(z=>z.alias==="EB-"+id),g=compile(x),s=JSON.stringify(g.network)+"\n";A(H.sha(s)===e.sha256&&s.length*8===e.N_bits&&H.sha(x.dimacs)===e.source_cnf.sha256,"source");
let orig=H.normalize(g.network),alt=H.independentNormalize(g.network),v=H.gauge(orig.fs);A(orig.fs.every(f=>f.ok.every(w=>f.ok.includes(w^(2**f.vs.length-1)))),"gauge");
function restrict(F){return F.map(f=>{let j=f.vs.indexOf(v);if(j<0)return f;let vs=f.vs.filter(a=>a!==v),ok=[];for(let w=0;w<2**vs.length;w++){let pre=0;for(let k=0;k<vs.length;k++)pre|=(w>>k&1)<<f.vs.indexOf(vs[k]);if(f.ok.includes(pre))ok.push(w)}return {...f,vs,ok}})}
let E=H.eliminate(restrict(orig.fs),false),Q=H.verifyTrace(restrict(alt.fs),E.trace),F=new Map(Q.fs.map(f=>[f.id,f])),r=Z.out[i],checks=0,words=0,termChecks=0,pairChecks=0;
A(!r.closure.pins.length,"unexpected pin");
const claim=i===0?"Source-only bounded projection and signed exact-one augmentation yield a degree-two Boolean-ring identity 1 as a sum of 56 monomial multiples of local annihilators.":"Source-only bounded projection yields a dual functional annihilating every row of the static degree-three local-annihilator span, but taking value 1 on the constant. Refusal of this terminal only.";
const proof=i===0?{groups:r.clusters.native.cert,terms:r.native[0].terms}:{dual:r.native[1].dual};
if(i===0){function entailed(c,id){const f=F.get(id);A(f&&c.every(l=>f.vs.includes(Math.abs(l))),"parent");A(f.ok.every(w=>{checks++;return c.some(l=>(w>>f.vs.indexOf(Math.abs(l))&1)===+(l>0))}),"not entailed")}
for(let z of proof.groups){entailed(z.c,z.parent);let seen=new Set();for(let p of z.pairs){entailed(p.c,p.parent);seen.add(p.c.slice().sort((a,b)=>a-b).join())}for(let j=0;j<z.c.length;j++)for(let k=j+1;k<z.c.length;k++){pairChecks++;A(seen.has([-z.c[j],-z.c[k]].sort((a,b)=>a-b).join()),"pair")};let vs=z.c.map(Math.abs).sort((a,b)=>a-b),ok=[];for(let w=0;w<2**vs.length;w++){words++;if(z.c.filter(l=>(w>>vs.indexOf(Math.abs(l))&1)===+(l>0)).length===1)ok.push(w)}F.set(z.id,{id:z.id,vs,ok})}
let sum=new Set();for(let t of proof.terms){let f=F.get(t.factor);A(f,"factor");for(let w of f.ok){let a=0;for(let m of t.local){termChecks++;a^=+( (m&w)===m )}A(!a,"not annihilator")}
for(let m of t.local){let mon=f.vs.filter((_,j)=>m>>j&1),k=key([...mon,...t.mult]);A(k===""||k.split(",").length<=2,"degree");if(sum.has(k))sum.delete(k);else sum.add(k)}}
A(sum.size===1&&sum.has(""),"not constant");
}else{let D=new Set(proof.dual.map(key));A(D.has(""),"constant");for(const f of F.values()){A(f.vs.length===3&&f.ok.length===7&&new Set(f.ok).size===7,"not width3 clause");let bad=Array.from({length:8},(_,j)=>j).find(j=>!f.ok.includes(j)),sum=0;for(let m=0;m<8;m++){// violation polynomial is prod(bit=1 ? x : (1+x)).
if((m&bad)!==bad)continue;termChecks++;sum^=+D.has(key(f.vs.filter((_,j)=>m>>j&1)))}A(!sum,"dual nonzero")}}
let artifact={problem_id:"STRICT-EB4-v1",instance:e.short_id,instance_id:e.instance_id,original_N_bits:e.N_bits,source_pin:{registry:"0c14cdc57925788cf7a451dcd5aa171dce860f2c",compiler:"21b9d53fb8166c819b24e708656c742cd3c24f10",corpus:"e315349cd6c1fe3fa696504859f28312f6aab69a",normalizer:"a830475f2d7b927fe3897079af04ebb99c82106b"},guard_id:"EMPTY",residual_id:"ROOT",original_ids:{vertices:[0,e.vertices-1],ports:[0,4*e.vertices-1],edges:[0,e.edges-1]},parents:[],claim,gauge:v,proof,checker:"independent-check.js",projectionTrace:E.trace,verification:{projectionTests:Q.tests,projectionScans:Q.scans,checks,words,termChecks,pairChecks},discovery:{projection:r.projection,cluster:r.clusters.native.counters,lane:i===0?{D:2,rows:r.native[0].rows,xor:r.native[0].xor,localChecks:r.native[0].localChecks}:{D:3,rows:r.native[1].rows,xor:r.native[1].xor,localChecks:r.native[1].localChecks}}};
out.push(artifact);
}
return out
}
console.log(JSON.stringify(independent(process.argv.slice(2).map(p=>fs.readFileSync(p,'utf8'))),null,2));
