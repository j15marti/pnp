
function trial(compiler,corpus,registry,helper,prior,feedback){
 const mod=feedback.slice(0,feedback.lastIndexOf('if(typeof module')).replace('const C=JSON.parse(corpus),Reg=JSON.parse(registry),result=[];', 'return {compile,H,P,discovery,replay,budget,hash}; const C=JSON.parse(corpus),Reg=JSON.parse(registry),result=[];');
 const {compile,H,P,discovery,replay,budget,hash}=Function(mod+";return run")()(compiler,corpus,registry,helper,prior);
 const C=JSON.parse(corpus),Reg=JSON.parse(registry),name="RANDOM-3CNF-40",x=C.instances.find(i=>i.id===name),e=Reg.instances.find(i=>i.alias==="EB-"+name),G=compile(x);
 const s=JSON.stringify(G.network)+"\n",m=JSON.stringify(G.source_map)+"\n";
 if(H.sha(s)!==e.sha256||s.length*8!==e.N_bits||H.sha(x.dimacs)!==e.source_cnf.sha256||x.dimacs.length*8!==e.source_cnf.N_bits||H.sha(m)!==e.source_map_sha256)throw Error("identity");
 const D=H.normalize(G.network),I=H.independentNormalize(G.network);if(JSON.stringify(D.fs)!==JSON.stringify(I.fs))throw Error("normalize");
 const initB=P.budget(),init=P.gac(D.fs,new Map(),initB),E=H.eliminate(D.fs,true),Z=H.verifyTrace(I.fs,E.trace);if(JSON.stringify(E.fs)!==JSON.stringify(Z.fs))throw Error("projection");
 const F=Z.fs,g=P.makeGuards(F),clB=P.budget(),cl=P.gac(F,new Map(),clB);
 function lifts(F,guard,max,seed){
  const T=P.restrict(F,new Map(guard)),V=P.vars(T),next=Math.max(...V)+1;
  let random=seed>>>0;const rng=()=>{random=(Math.imul(random,1664525)+1013904223)>>>0;return random};
  const cand=[],freq=new Map();for(const f of T)for(const v of f.vs)freq.set(v,(freq.get(v)||0)+1);
  for(const f of T){const d=f.vs.length;if(d!==3&&d!==4)continue;
   const bad=Array.from({length:2**d},(_,w)=>w).filter(w=>!f.ok.includes(w));
   if(d===3&&bad.length===1||d===4&&bad.length===2&&(bad[0]^bad[1])===15)cand.push({f,bad:bad[0],kind:d===3?"clause":"complement-pair",score:f.vs.reduce((s,v)=>s+freq.get(v),0),random:rng()})}
  cand.sort((a,b)=>seed?a.random-b.random:b.score-a.score||String(a.f.id).localeCompare(String(b.f.id)));
  const chosen=cand.slice(0,max),rep=new Map(),maps=[];let tests=0;
  for(const [i,c] of chosen.entries()){const f=c.f,d=f.vs.length,qvar=next+i;
   function bits(w){if(d===3)return [0,1,2].map(j=>(w>>j&1)^(c.bad>>j&1));
     return [1,2,3].map(j=>(w>>j&1)^(w&1)^(c.bad>>j&1)^(c.bad&1))}
   function q(w){let b=bits(w);return b[0]*b[1]^b[0]*b[2]^b[1]*b[2]}
   const ok=f.ok.map(w=>w+(q(w)<<d));const nf={...f,id:"score-aux:"+f.id,vs:[...f.vs,qvar],ok};rep.set(f.id,nf);
   for(let w=0;w<2**d;w++){const b=bits(w),p=b[0]^b[1]^b[2],qv=q(w);if(Boolean(p||qv)!==f.ok.includes(w))throw Error("score OR equivalence");
    for(let z=0;z<2;z++){tests++;if(ok.includes(w+(z<<d))!==(f.ok.includes(w)&&z===qv))throw Error("unique lift")}}
   maps.push({originalFactor:f.id,aux:qvar,originalScope:f.vs,kind:c.kind,forbidden:c.bad,sourceOwners:f.ids||[]})
  }
  return{F:T.map(f=>rep.get(f.id)||f),candidates:cand.length,maps,tests}
 }
 const trials=[];for(const [max,seed] of [[16,0],[32,0],[16,20261127]]){
  const B=budget(1000000),S=budget(3000000),out=[];
  for(const guard of g){const L=lifts(F,guard,max,seed);let r,check;
   try{r=discovery(L.F,[],B,true)}catch(e){out.push({guard,candidates:L.candidates,lifted:L.maps.length,tests:L.tests,maps:L.maps,status:"UNKNOWN "+e,events:B.n});continue}
   try{const z=replay(L.F,[],r,S);check={no:z.no,verified:z.verified,events:S.n}}catch(e){check={error:String(e)}}
   out.push({guard,candidates:L.candidates,lifted:L.maps.length,tests:L.tests,maps:L.maps,rec:r,check,events:B.n})
  }
  trials.push({max,seed,out,events:B.n,checkEvents:S.n})
 }
 return{instance:e.short_id,instance_id:e.instance_id,N:e.N_bits,guard_id:"EMPTY",residual_id:"ROOT",projection:{tableHash:hash(F),count:E.trace.length,scans:E.scans,verifyScans:Z.scans},initial:{events:initB.n,no:init.no},closure:{events:clB.n,no:cl.no},trials}
}
if(typeof module!=="undefined"){module.exports=trial;if(require.main===module){const fs=require("fs");console.log(JSON.stringify(trial(...process.argv.slice(2).map(p=>fs.readFileSync(p,"utf8"))),null,2))}}
