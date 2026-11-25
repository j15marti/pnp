/* GD24. node checker.js BS17_stalled.json S23_inputs.json */
function experiment(data,sources){
 const bits=(w,n)=>Array.from({length:n},(_,i)=>String((w>>i)&1)).join("");
 const word=(v,p)=>v.map(i=>p[i]).join("");
 const raw=t=>({v:t.v.slice(),a:t.a.map(w=>bits(w,t.v.length))});
 const clone=t=>t.map(z=>({v:z.v.slice(),a:z.a.slice()}));
 const proj=(w,idx)=>idx.map(i=>w[i]).join("");
 const check=(ok,msg)=>{if(!ok)throw Error(msg)};
 const sourceRows=(o)=>({v:o.t,a:Array.from({length:8},(_,i)=>i).filter(i=>!(o.bad||[0,7]).includes(i))});
 const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
 const control=(id,n,t)=>({id,n,guard:[],p:Array(n).fill(-1),remaining:t,eliminations:[]});
 const eq=(u,v,b)=>({v:[u,v],a:b?[1,2]:[0,3]});
 const jobs=[...data.snapshots,control("Fano",7,fano.map(v=>({v,a:[1,2,3,4,5,6]}))),control("Fano-minus",7,fano.slice(1).map(v=>({v,a:[1,2,3,4,5,6]}))),control("parity-cycle-UNSAT",3,[eq(0,1,0),eq(1,2,0),eq(0,2,1)]),control("parity-cycle-SAT",3,[eq(0,1,0),eq(1,2,0),eq(0,2,0)])];
 function run(job,mode){
  let T=job.remaining.map(raw),p=job.p.slice(),lifts=[];
  const C={scans:0,unaryRows:0,semijoinRows:0,semijoinPairs:0,deleted:0,forces:0,mergeTests:0,mergeIndexRows:0,mergeMatches:0,merges:0,nodes:0,peakRows:0};
  const rowCount=T=>T.reduce((s,t)=>s+t.a.length,0);
  const potential=T=>1+new Set(T.flatMap(t=>t.v)).size+T.length+rowCount(T);
  function close(T,p,semi){
   let change=true;
   while(change){
    change=false;C.scans++;C.peakRows=Math.max(C.peakRows,rowCount(T));
    for(const t of T){
     let old=t.a.length;t.a=t.a.filter(w=>{C.unaryRows++;return t.v.every((v,i)=>p[v]<0||String(p[v])===w[i])});C.deleted+=old-t.a.length;if(!t.a.length)return false;if(old!==t.a.length)change=true;
     for(let i=0;i<t.v.length;i++){let v=t.v[i];if(p[v]<0&&t.a.every(w=>w[i]===t.a[0][i])){p[v]=+t.a[0][i];C.forces++;change=true}}
    }
    if(semi)for(let i=0;i<T.length;i++)for(let j=0;j<T.length;j++)if(i!==j){
     let A=T[i],B=T[j],shared=A.v.filter(v=>B.v.includes(v));if(!shared.length)continue;C.semijoinPairs++;
     let ix=shared.map(v=>A.v.indexOf(v)),jx=shared.map(v=>B.v.indexOf(v));
     let S=new Set(B.a.map(w=>{C.semijoinRows++;return proj(w,jx)})),old=A.a.length;
     A.a=A.a.filter(w=>{C.semijoinRows++;return S.has(proj(w,ix))});C.deleted+=old-A.a.length;if(!A.a.length)return false;if(A.a.length!==old)change=true;
    }
   }
   return true
  }
  const initial=potential(T);
  let ok=close(T,p,mode!=="direct");const rootRows=rowCount(T),rootPins=p.map((v,i)=>v>=0?[i,v]:null).filter(Boolean),rootDeleted=C.deleted;
  if(ok&&mode==="combined"){
   let progress=true;
   while(progress&&T.length>1){
    progress=false;
    outer:for(let i=0;i<T.length;i++)for(let j=i+1;j<T.length;j++){
     let A=T[i],B=T[j],shared=A.v.filter(v=>B.v.includes(v));if(!shared.length)continue;
     C.mergeTests++;
     let U=[...new Set([...A.v,...B.v])].sort((a,b)=>a-b),outside=new Set(T.filter((_,k)=>k!==i&&k!==j).flatMap(t=>t.v));
     let W=U.filter(v=>outside.has(v)||p[v]>=0),priv=U.filter(v=>!W.includes(v));
     let ix=shared.map(v=>A.v.indexOf(v)),jx=shared.map(v=>B.v.indexOf(v)),idx=new Map();
     for(let w of B.a){C.mergeIndexRows++;let k=proj(w,jx);if(!idx.has(k))idx.set(k,[]);idx.get(k).push(w)}
     let map=new Map(),cap=A.a.length+B.a.length,decline=false;
     const location=U.map(v=>A.v.includes(v)?[0,A.v.indexOf(v)]:[1,B.v.indexOf(v)]);
     const wi=W.map(v=>U.indexOf(v)),pi=priv.map(v=>U.indexOf(v));
     for(let aw of A.a){C.mergeIndexRows++;for(let bw of idx.get(proj(aw,ix))||[]){
       C.mergeMatches++;let uv=location.map(([k,z])=>(k?bw:aw)[z]).join(""),w=proj(uv,wi);
       if(!map.has(w))map.set(w,proj(uv,pi));
       if(map.size>cap){decline=true;break}
      }if(decline)break}
     if(decline)continue;
     if(map.size===0){ok=false;break outer}
     const old=potential(T);
     T=T.filter((_,k)=>k!==i&&k!==j);T.push({v:W,a:[...map.keys()]});
     check(potential(T)<old,"credit");lifts.push({v:priv,w:W,map});C.merges++;progress=true;
     ok=close(T,p,true);break outer
    }
    if(!ok)break
   }
  }
  const afterRows=rowCount(T),afterPotential=potential(T),beforeSearch={...C};let unknown=false;
  function search(T,p){
   if(++C.nodes>20000){unknown=true;return null}
   if(!close(T,p,mode!=="direct"))return null;
   const active=[...new Set(T.flatMap(t=>t.v))].filter(v=>p[v]<0);
   if(!active.length)return p;
   active.sort((a,b)=>T.filter(t=>t.v.includes(b)).length-T.filter(t=>t.v.includes(a)).length||a-b);
   let v=active[0];for(let b of [0,1]){let q=p.slice();q[v]=b;let hit=search(clone(T),q);if(hit)return hit;if(unknown)return null}return null
  }
  let w=ok?search(clone(T),p.slice()):null, label=w?"SAT":unknown?"UNKNOWN":"UNSAT";
  if(w){
   for(let l of lifts.slice().reverse()){let v=l.map.get(word(l.w,w));check(v!==undefined,"pair lift");l.v.forEach((x,i)=>w[x]=+v[i])}
   for(let t of job.remaining)check(raw(t).a.includes(word(t.v,w)),"snapshot witness");
   for(let e of job.eliminations.slice().reverse()){let z=e.u.reduce((k,v,i)=>k+(w[v]<<i),0),pair=e.lift.find(r=>r[0]===z);check(!!pair,"source lift");w[e.v]=pair[1]}
   w=w.map(x=>x<0?0:x);
   const src=sources.find(s=>s.id===job.id);
   if(src){check(src.ref===job.sourceRef,"source ref");for(let o of src.O){let t=sourceRows(o);check(raw(t).a.includes(word(t.v,w)),"original source witness")}}
   for(let [v,b] of job.guard)check(w[v]===b,"guard");
  }
  return {mode,label,initial,rootRows,rootDeleted,rootPins,afterRows,afterPotential,beforeSearch,C,witness:w};
 }
 return jobs.map(j=>{
   const out=["direct","semijoin","combined"].map(m=>run(j,m));
   check(out.every(x=>x.label===out[0].label),"mode disagreement "+j.id);
   if(j.id==="Fano"||j.id==="parity-cycle-UNSAT")check(out[0].label==="UNSAT","negative");
   if(j.id==="Fano-minus"||j.id==="parity-cycle-SAT")check(out[0].label==="SAT","positive");
   return {id:j.id,guard:j.guard,sourceRef:j.sourceRef||null,out}
 });
}
const fs=require('fs');console.log(JSON.stringify(experiment(JSON.parse(fs.readFileSync(process.argv[2],'utf8')),JSON.parse(fs.readFileSync(process.argv[3],'utf8'))),null,2));
