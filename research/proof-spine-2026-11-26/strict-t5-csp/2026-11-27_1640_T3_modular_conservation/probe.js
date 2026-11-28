function probe(src){
 let f=Function(src.runner.slice(0,src.runner.indexOf("\n let results=[],certs=[];\n for(let id"))+";return {H,P,field,C,B,R};}return run")()(src),{H,P,field,C,B,R}=f;
 const assert=(x,m)=>{if(!x)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b),V=F=>[...new Set(F.flat().map(Math.abs))].sort((a,b)=>a-b),mod=(x,p)=>(x%p+p)%p,cap=1000000;
 // Source independently normalized again; exact chart and guard identities checked before use.
 let results=[],certs=[];
 for(let key of ["joint","random"]){
  let T=JSON.parse(src[key]),id=key==="joint"?"JOINT-24":"RANDOM-3CNF-40",e=R.instances.find(z=>z.alias==="EB-"+id),x=B.instances.find(z=>z.id===id),G=C(x),raw=JSON.stringify(G.network)+"\n";
  assert(H.sha(raw)===e.sha256&&raw.length*8===e.N_bits&&H.sha(x.dimacs)===e.source_cnf.sha256,"source");let S=H.norm(G.network),K=H.compact(S,2e6),D=H.reduce(K.F,2e6);
  assert(T.chart===JSON.stringify({gauge:S.gauge,F:D.F})+"\n","chart");
  function lane(F,g,p,priority=[]){
   let M={up:0,extract:0,field:0,verify:0,probes:0},steps=[],learned=[],db=F.slice(),status="UNKNOWN";
   const count=()=>Object.values(M).reduce((a,b)=>a+b,0);
   for(let round=0;round<32&&count()<cap;round++){
    let u=P.closure(db,g,M);if(u.conflict){status="UNSAT";break}
    let E=H.unique(P.restrict(db,u.p)),vs=V(E),ordered=[...priority.filter(v=>vs.includes(v)),...vs.filter(v=>!priority.includes(v))],next=null;
    outer:for(let v of ordered){for(let b of [1,0]){
     if(count()>=cap)break outer;M.probes++;let z=P.closure(E,[[v,b]],M);let Q=null,bad=z.conflict;
     if(!bad&&p){let F=H.unique(P.restrict(E,z.p));Q=field(F,p);M.extract+=Q.M.extract;M.field+=Q.M.field;M.verify+=Q.M.check;bad=Q.proofs.some(q=>q.type==="conflict")}
     if(bad){next={v,b,conditionalPins:[...z.p].sort((a,b)=>a[0]-b[0]),Q};break outer}
    }}
    if(!next)break;
    let lit=next.b?-next.v:next.v;steps.push(next);learned.push(lit);db.push([lit]);
   }
   let post=P.closure(db,g,M);if(post.conflict)status="UNSAT";return {p,status,steps,learned,metrics:M,remaining:post.conflict?0:V(P.restrict(db,post.p)).length}
  }
  function replay(F,g,L){
   let db=F.slice(),M={up:0},fieldChecks=0;
   for(let t of L.steps){let u=P.closure(db,g,M);assert(!u.conflict,"premature");let E=H.unique(P.restrict(db,u.p)),z=P.closure(E,[[t.v,t.b]],M);assert(eq([...z.p].sort((a,b)=>a[0]-b[0]),t.conditionalPins),"conditional map");
    if(!z.conflict){let A=H.unique(P.restrict(E,z.p)),q=t.Q;assert(q&&q.p===L.p,"proof field");let cert=q.proofs.find(x=>x.type==="conflict");assert(cert,"conflict proof");let lhs=new Map(),rhs=0;
     for(let [i,r] of q.rows.entries()){assert(eq(A[r.proof[0]],r.c),"row");let j=1;for(let a=0;a<r.c.length;a++)for(let b=a+1;b<r.c.length;b++){fieldChecks++;assert(eq(H.canon(A[r.proof[j++]]),H.canon([-r.c[a],-r.c[b]])),"at most one")}let w=cert.coeff[i],d=1;assert(w>=0&&w<q.p&&Number.isInteger(w),"coefficient");for(let l of r.c){fieldChecks++;let v=Math.abs(l);lhs.set(v,mod((lhs.get(v)||0)+w*(l>0?1:-1),q.p));d-=+(l<0)}rhs=mod(rhs+w*d,q.p)}
     let a=[...lhs].filter(x=>x[1]).sort((a,b)=>a[0]-b[0]);assert(eq(a,cert.lhs)&&rhs===cert.rhs&&(!a.length&&rhs!==0||a.length===1&&q.p===3&&mod(rhs*(a[0][1]===2?2:1),3)===2),"checked contradiction")
    }db.push([t.b?-t.v:t.v])
   }
   let u=P.closure(db,g,M);assert((L.status==="UNSAT")===u.conflict,"status replay");return {up:M.up,fieldChecks}
  }
  let lanes=[];for(let g of T.guards.guards){let q=[0,2,3].map(p=>{let L=lane(D.F,g,p);return {...L,replay:replay(D.F,g,L)}});lanes.push(q)}
  let peer=null;if(key==="joint"){assert(H.sha(src.peer)==="1ef91270eee70a05e34460433e20e036068fdda0194d288d75a9652b7ea1c043","peer sha");let candidates=[417,546,578,618,250,562,226,610,34,545],present=candidates.filter(v=>V(D.F).includes(v));let q=lane(D.F,[],3,present);peer={present,notInChart:candidates.filter(v=>!present.includes(v)),status:q.status,rederived:q.learned.filter(l=>candidates.includes(-l)),result:q,replay:replay(D.F,[],q)}}
  let cert={problem_id:T.problem_id,instance:T.instance,instance_id:T.instance_id,original_N_bits:T.original_N_bits,source_pin:T.source_pin,guard_id:"EMPTY",residual_id:"ROOT",original_ids:T.original_ids,parents:["CERT-v1:sha256:"+H.sha(src[key])],guardInfo:T.guardInfo,guards:T.guards,lanes,peer};
  let s=JSON.stringify(cert)+"\n";certs.push({id,content:s,sha:H.sha(s)});
  results.push({id,instance:T.instance_id,N:T.original_N_bits,guardInfo:T.guardInfo,lanes:lanes.map(a=>a.map(({steps,...z})=>z)),peer:peer?{...peer,result:{...peer.result,steps:undefined}}:null,certSha:H.sha(s),bytes:s.length})
 }
 return {results,certs}
}
if(typeof require==='function'){const fs=require('fs');const keys=['compiler','corpus','registry','hybrid','previous','runner','joint','random','peer'];const src=Object.fromEntries(keys.map((k,i)=>[k,fs.readFileSync(process.argv[i+2],'utf8')]));console.log(JSON.stringify(probe(src),null,2));}
