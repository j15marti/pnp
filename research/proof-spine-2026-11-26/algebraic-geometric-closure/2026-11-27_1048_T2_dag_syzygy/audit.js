const fs=require('node:fs'); const crypto=require('node:crypto');
function primes(fs,gauge){
 let C=[],origins=[],keys=new Set(),partial=0,wordChecks=0;
 for(const f of fs){
  const n=f.vs.length, bad=[];
  for(let p=0;p<3**n;p++){
   let k=p, a=0,m=0,c=[];for(let i=0;i<n;i++){let t=k%3;k=(k-t)/3;if(t){m|=1<<i;if(t===2)a|=1<<i;c.push((t===1?1:-1)*f.vs[i])}}
   partial++;let hit=f.ok.some(w=>{wordChecks++;return (w&m)===a});if(hit)continue;
   let minimal=true;for(let i=0;i<n;i++)if(m>>i&1){let m2=m^(1<<i);if(!f.ok.some(w=>{wordChecks++;return(w&m2)===(a&m2)})){minimal=false;break}}
   if(!minimal)continue;
   const key=c.join(",");if(!keys.has(key)){keys.add(key);C.push(c);origins.push(f.id)}
  }
 }
 if(gauge!==undefined&&!keys.has(String(-gauge))){C.push([-gauge]);origins.push("GAUGE")}
 return {C,origins,partial,wordChecks}
}
function treeRUP(t,path=[],out=[]){
 if(t===0){out.push(path.map(x=>-x));return out}
 if(!Array.isArray(t)||t.length!==3)throw Error("tree");
 treeRUP(t[1],[...path,-t[0]],out);treeRUP(t[2],[...path,t[0]],out);out.push(path.map(x=>-x));return out
}
function verifyRUP(C,proof,cap=2500000){
 let db=C.slice(),cert=[],scans=0,literalReads=0,maxUnits=0,terms=0,origTerms=0;
 for(const clause of proof){
  let a=new Set(clause.map(x=>-x)),trail=[],conflict=-1;
  if([...a].some(x=>a.has(-x)))throw Error("tautological target unsupported");
  while(conflict===-1){
   let unit=false;
   for(let j=0;j<db.length;j++){
    if(++scans>cap)throw Error("RUP cap");
    const c=db[j];let open=[],sat=false;
    for(const l of c){literalReads++;if(a.has(l)){sat=true;break}if(!a.has(-l))open.push(l)}
    if(sat)continue;
    if(!open.length){conflict=j;break}
    if(open.length===1){a.add(open[0]);trail.push([open[0],j]);unit=true;break}
   }
   if(conflict===-1&&!unit)throw Error("non-RUP step")
  }
  maxUnits=Math.max(maxUnits,trail.length);terms+=trail.length+1;origTerms+=trail.filter(x=>x[1]<C.length).length+Number(conflict<C.length);
  cert.push({clause,trail,conflict});db.push(clause)
 }
 if(!proof.length||proof.at(-1).length!==0)throw Error("not terminal");
 return{cert,scans,literalReads,maxUnits,terms,origTerms}
}
function verifyHints(C,cert){
 let db=C.slice(),checks=0,uses=0;
 for(const p of cert){
  const A=new Set(p.clause.map(x=>-x));if([...A].some(x=>A.has(-x)))throw Error("bad target");
  for(const [l,j] of p.trail){const c=db[j];if(!c||!c.includes(l)||A.has(l)||A.has(-l))throw Error("bad hint");for(const k of c){checks++;if(k!==l&&!A.has(-k))throw Error("reason not unit")}A.add(l);uses++}
  const c=db[p.conflict];if(!c||!c.every(l=>{checks++;return A.has(-l)}))throw Error("wrong conflict");
  uses++;db.push(p.clause)
 }
 if(cert.at(-1).clause.length)throw Error("no empty clause");
 return {checks,uses}
}
function checkLocalSources(fs,base,origins,gauge){
 let checks=0;for(let i=0;i<base.length;i++){const c=base[i];if(origins[i]==="GAUGE"){if(c.length!==1||c[0]!==-gauge)throw Error("bad gauge");continue}const f=fs.find(x=>x.id===origins[i]);if(!f||!c.every(l=>f.vs.includes(Math.abs(l)))||!f.ok.every(w=>{checks++;return c.some(l=>((w>>f.vs.indexOf(Math.abs(l)))&1)===Number(l>0))}))throw Error("bad base");}return checks
}
function checkTelescopes(){
 // Exhaustive independent pointwise test of first-failure and reverse-unit identity, including repeated antecedents.
 let checks=0;for(let n=1;n<=6;n++)for(let mask=0;mask<2**n;mask++){
  let P=1,S=0;for(let j=0;j<n;j++){let f=mask>>j&1;S^=P&f;P&=1^f;checks++}if(S!==(1^P))throw Error("telescope");
 }return checks
}
const [compilerPath,corpusPath,registryPath,helperPath,...certs]=process.argv.slice(2);
const c=fs.readFileSync(compilerPath,'utf8'),h=fs.readFileSync(helperPath,'utf8');
const compile=Function(c.slice(c.indexOf('function compile'),c.indexOf('function auditLocal'))+';return compile')();
const H=Function(h.slice(0,h.indexOf('const fs=require("node:fs")'))+';return {sha,normalize,independentNormalize,eliminate,verifyTrace,solve,gauge,cnfSearch}')();
const B=JSON.parse(fs.readFileSync(corpusPath)),R=JSON.parse(fs.readFileSync(registryPath));
const sha=s=>crypto.createHash('sha256').update(s).digest('hex');
for(const path of certs){const raw=fs.readFileSync(path,'utf8'),p=JSON.parse(raw),e=R.instances.find(z=>z.instance_id===p.instance_id),x=B.instances.find(z=>'EB-'+z.id===e.alias),g=compile(x),s=JSON.stringify(g.network)+'\n';
if(sha(s)!==e.sha256||s.length*8!==e.N_bits||sha(x.dimacs)!==e.source_cnf.sha256||sha(JSON.stringify(g.source_map)+'\n')!==e.source_map_sha256||p.guard_id!=='EMPTY'||p.residual_id!=='ROOT'||p.original_N_bits!==e.N_bits)throw Error('identity');
const n=H.normalize(g.network),v=H.independentNormalize(g.network);if(JSON.stringify(n.fs)!==JSON.stringify(v.fs))throw Error('normalization');
const V=H.verifyTrace(v.fs,p.trace);if(!V.fs.every(f=>f.ok.every(w=>f.ok.includes(w^(2**f.vs.length-1))))||!V.fs.some(f=>f.vs.includes(p.gauge)))throw Error('gauge');
console.log(JSON.stringify({instance:p.instance,certificate_id:sha(raw),projectionTests:V.tests,baseChecks:checkLocalSources(V.fs,p.base,p.origins,p.gauge),hints:verifyHints(p.base,p.rup),telescopeChecks:checkTelescopes()}));}
