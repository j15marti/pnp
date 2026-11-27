function affineBridge(G,C,L){
 const S=L.norm(G),H=L.compact(S);let fs=H.fs.slice(),meter={checks:0,affine:0,bothAffected:0,oneInvariant:0,bothInvariant:0,nonAffine:0};
 // Check each forbidden set is an affine translate by XOR closure about its first element.
 function isAffine(B){if(!B.length)return true;let Z=new Set(B.map(x=>x^B[0]));for(const a of Z)for(const b of Z){meter.checks++;if(!Z.has(a^b))return false;}return true}
 for(const t of C.pairTrace){let ff=fs.filter(f=>f.vs.includes(t.v));if(ff.length!==2)throw Error("scope");const V=t.V;
 const bad=ff.map(f=>Array.from({length:2**f.vs.length},(_,i)=>i).filter(w=>!f.ok.includes(w)));
 const af=bad.every(isAffine);if(af)meter.affine++;else meter.nonAffine++;
 const invariant=ff.map((f,i)=>bad[i].every(w=>bad[i].includes(w^(1<<f.vs.indexOf(t.v)))));
 if(invariant.every(x=>x))meter.bothInvariant++;else if(invariant.some(x=>x))meter.oneInvariant++;else meter.bothAffected++;
 for(let w=0;w<2**V.length;w++){
 let a=ff.map((f,i)=>[0,1].map(b=>bad[i].includes(f.vs.reduce((s,v,j)=>s+((v===t.v?b:(w>>V.indexOf(v))&1)<<j),0))));
 let blocked=(a[0][0]&&a[0][1])||(a[1][0]&&a[1][1])||(a[0][0]&&a[1][1])||(a[0][1]&&a[1][0]);meter.checks++;
 if(blocked===t.ok.includes(w))throw Error("orbit disagreement");
 }
 fs=fs.filter(f=>!ff.includes(f));fs.push({id:t.newId,vs:V,ok:t.ok});
 }return meter;
}
// Node CLI: node bridge.js compile.js benchmarks.json registry.json hybrid.js cert1.json cert2.json
const fs=require('node:fs');const [cp,bp,rp,hp,...cs]=process.argv.slice(2);const c=fs.readFileSync(cp,'utf8'),h=fs.readFileSync(hp,'utf8');const compile=Function(c.slice(c.indexOf('function compile('),c.indexOf('function auditLocal('))+';return compile')();const L=Function(h.slice(0,h.lastIndexOf('if(typeof require'))+';return {sha,norm,compact}')();const B=JSON.parse(fs.readFileSync(bp)),R=JSON.parse(fs.readFileSync(rp));for(const path of cs){let s=fs.readFileSync(path,'utf8'),C=JSON.parse(s),e=R.instances.find(z=>z.instance_id===C.instance_id),x=B.instances.find(z=>'EB-'+z.id===e.alias),g=compile(x);if(L.sha(JSON.stringify(g.network)+'\n')!==e.sha256||L.sha(x.dimacs)!==e.source_cnf.sha256||C.guard_id!=='EMPTY'||C.residual_id!=='ROOT')throw Error('id');console.log(JSON.stringify(affineBridge(g.network,C,L)));}
