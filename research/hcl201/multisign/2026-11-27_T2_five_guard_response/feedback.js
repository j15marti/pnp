const fs=require('node:fs');
const specs=[
  [
    "21b9d53fb8166c819b24e708656c742cd3c24f10",
    "research/coordination/shared-eb-2026-11-27/compile.js"
  ],
  [
    "e315349cd6c1fe3fa696504859f28312f6aab69a",
    "research/coordination/shared-unsat-2026-11-27/benchmarks.json"
  ],
  [
    "a830475f2d7b927fe3897079af04ebb99c82106b",
    "research/hcl201/matching/2026-11-27_T1_hall_clause_feedback/experiment.js"
  ],
  [
    "d7cb4c38ee4dc1df3378177b716cd0d238d0e4db",
    "research/hcl201/interfaces/2026-11-27_T2_quadratic_response/experiment.js"
  ],
  [
    "4e963c692326d1613afb54c7b9faea0f882e1f6e",
    "research/hcl201/multisign/2026-11-27_T2_five_guard_response/results.json"
  ],
  [
    "f8cc222926fe2d9a323985c61c66fe0400fa3af0",
    "research/hcl201/multisign/2026-11-27_T2_five_guard_response/audit-results.json"
  ]
];
function feedback(inputs){
 const [co,corpus,base,qc,raw,audit]=inputs,A=(b,m)=>{if(!b)throw Error(m)},bytes=x=>JSON.stringify(x)+"\n";
 const compile=Function(co.slice(co.indexOf("function compile("),co.indexOf("function auditLocal"))+";return compile")(),{sha,independentNormalize,verifyTrace}=Function(base.slice(0,base.indexOf("function runCase"))+";return {sha,independentNormalize,verifyTrace}")(),quad=Function(qc.slice(qc.indexOf(" function lane("),qc.indexOf(" let shared=[]"))+";return lane")();
 const R=JSON.parse(raw),data=JSON.parse(corpus),Au=JSON.parse(audit);
 function restrict(F,g){let p=new Map(g.map(l=>[Math.abs(l),+(l>0)]));return F.map(f=>{let vs=f.vs.filter(v=>!p.has(v));return {...f,vs,ok:[...new Set(f.ok.filter(w=>f.vs.every((v,i)=>!p.has(v)||p.get(v)===(w>>i&1))).map(w=>vs.reduce((z,v,i)=>z|((w>>f.vs.indexOf(v)&1)<<i),0)))].sort((a,b)=>a-b)}})}
 function table(vs,p,id){return {id,vs,ok:Array.from({length:2**vs.length},(_,i)=>i).filter(p)}}
 let output=[];for(let k=0;k<2;k++){let r=R.shared[k],a=Au[k],e=r.entry,x=data.instances.find(z=>z.id===e.source_cnf.alias),g=compile(x);A(sha(bytes(g.network))===e.sha256&&bytes(g.network).length*8===e.N_bits&&sha(x.dimacs)===e.source_cnf.sha256,"auth");
 let I=independentNormalize(g.network),Z=verifyTrace(restrict(I.fs,[-r.root.gauge]),r.root.mapArtifact.trace),F=Z.fs,[u,v,w]=r.results[4].guard;A(u>0&&v>0&&w>0&&r.results[0].guard[0]===-u&&r.results[0].guard[1]===-v,"guard pattern");
 let A1=table([u,v],t=>t!==0,-1),A2=table([u,v,w],t=>t!==7,-2),B2=table([u,v,w],t=>!((t>>2&1)&(1^(t&1)^(t>>1&1))),-3);
 for(let i=0;i<8;i++)A((A1.ok.includes(i&3)&&A2.ok.includes(i))===(A1.ok.includes(i&3)&&B2.ok.includes(i)),"nonlinear adapter");
 let rawQ=quad([...F,A1,A2],true,16,true),compressedQ=quad([...F,A1,B2],true,16,true),rootQ=quad(F,true,16,true);
 output.push({entry:e,sourcePin:"registry 0c14cdc57925788cf7a451dcd5aa171dce860f2c",residual:r.root.residual,guards:[r.root.guardArtifacts[0],r.root.guardArtifacts[4]],equations:{variables:[u,v,w],polynomials:[["1",u,v,[u,v]],[w,[u,w],[v,w]]]},adapterTruthChecks:8,rawQ,compressedQ,rootQ})
 }return output
}
console.log(JSON.stringify(feedback(process.argv.slice(2).map(p=>fs.readFileSync(p,'utf8'))),null,2));
