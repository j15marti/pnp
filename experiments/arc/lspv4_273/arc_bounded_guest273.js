"use strict";
const FILL="ABCDEF";
function gcd(a,b){while(b){let z=a%b;a=b;b=z}return a}
function source(q,b){
  let nv=0, clauses=[];const v=()=>++nv;
  let t=v(),p=v(),at=v(),dt=v(),ap=v(),dp=v(),f=[v(),v(),v()];
  function G(L,a,d){for(const x of [1,-1])for(const y of [1,-1])clauses.push([L,x*a,y*d])}
  G(t,at,dt);G(-p,ap,dp);
  let z=Array.from({length:q},v);for(let j=0;j<q;j++)clauses.push([b[j]?t:-t,-z[j],p]);
  if(q===3)clauses.push(z.slice());else{
    let y=Array.from({length:q-3},v);
    clauses.push([z[0],z[1],y[0]]);
    for(let i=0;i<q-4;i++)clauses.push([-y[i],z[i+2],y[i+1]]);
    clauses.push([-y[q-4],z[q-2],z[q-1]]);
  }
  let r=Math.ceil(q**(5/3));for(let i=0;i<r;i++)clauses.push(f.slice());
  return {n:nv,clauses,r,t,p,forced:[t,-p],q,b};
}
function child(S,j){
  let cls=[],nv=S.n;
  function G(L,a,d){for(let x of [1,-1])for(let y of [1,-1])cls.push([L,x*a,y*d])}
  // Distinct private auxiliary variables on each call.
  let a=()=>++nv,s=a(),at=a(),dt=a(),ap=a(),dp=a(),as=a(),ds=a();
  G(S.t,at,dt);G(-S.p,ap,dp);G(s,as,ds);
  cls.push([S.b[j]?S.t:-S.t,-s,S.p]);
  let h=Math.ceil(Math.sqrt(S.r/Math.log2(S.q+2)));
  for(let i=0;i<h;i++)cls.push([a(),a(),a()]);
  return {n:nv,clauses:cls,source_idx:j,h};
}
function serial(F){
  let W=1+String(F.n).length;let header="p cnf "+F.n+" "+F.clauses.length+"\n";
  let rows=F.clauses.map(c=>c.map(l=>String(l).padStart(W," ")).join(" ")+" 0\n");
  if(!rows.every(x=>x.length===3*W+5))throw Error("stride");
  return {bytes:header+rows.join(""),H:header.length,D:3*W+5,W};
}
function counts(F,a){return F.clauses.map(c=>c.reduce((s,l)=>s+((a[Math.abs(l)]=== (l>0?1:0))?1:0),0))}
function satDpll(F){
  let nodes=0, tests=0, unsatLeaves=0;
  function dfs(init){
    nodes++;let a=init.slice();let changed=true;
    while(changed){changed=false;
      for(const c of F.clauses){
        let open=[],ok=false;
        for(const l of c){tests++;let x=Math.abs(l),z=a[x];if(z===-1)open.push(l);else if(z===(l>0?1:0)){ok=true;break}}
        if(ok)continue;
        if(!open.length){unsatLeaves++;return null}
        if(open.length===1){let l=open[0],x=Math.abs(l),z=l>0?1:0;
          if(a[x]!==-1&&a[x]!==z){unsatLeaves++;return null}
          if(a[x]===-1){a[x]=z;changed=true}
        }
      }
    }
    let isDone=true;for(const c of F.clauses){let ok=false;for(const l of c){tests++;if(a[Math.abs(l)]===(l>0?1:0)){ok=true;break}}if(!ok){isDone=false;break}}
    if(isDone){for(let i=1;i<=F.n;i++)if(a[i]===-1)a[i]=0;return a}
    let v=0;for(const c of F.clauses){for(const l of c){if(a[Math.abs(l)]===-1){v=Math.abs(l);break}}if(v)break}
    if(!v)throw Error("DPLL no branch");
    for(const x of [0,1]){let b=a.slice();b[v]=x;let out=dfs(b);if(out)return out}
    return null;
  }
  let witness=dfs(Array(F.n+1).fill(-1));return {sat:!!witness,nodes,tests,unsatLeaves,witness:witness?counts(F,witness).every(x=>x>0):false};
}
function stats(F){
  let zeros=Array(F.n+1).fill(0),ones=Array(F.n+1).fill(1);
  let tr0=counts(F,zeros),tr1=counts(F,ones),trail=[],a=ones.slice();
  const hist=tr=>Array.from({length:4},(_,r)=>tr.filter(x=>x===r).length);
  for(let i=1;i<=Math.min(4,F.n);i++){a[i]^=1;trail.push({flip:i,hist:hist(counts(F,a))})}
  let pairModes=[0,0,0,0],invalid=0;
  for(let i=0;i<F.clauses.length;i++)for(let j=i+1;j<F.clauses.length;j++){
    let A=F.clauses[i],B=F.clauses[j],same=A.some(x=>B.includes(x)),opp=A.some(x=>B.includes(-x));
    let mask=[!opp,!same,!same,!opp];
    mask.forEach((v,k)=>{if(v)pairModes[k]++});if(same&&opp)invalid++;
  }
  for(let r=0;r<tr0.length;r++)if(tr0[r]+tr1[r]!==3)throw Error("complement theorem");
  return {clauses:F.clauses.length,endpoint0:hist(tr0),endpoint1:hist(tr1),flipTrail:trail,extremeModes:[...pairModes],noExtremePairs:invalid,fullExtremeTables: F.clauses.length<=50,
  targets_sample:F.clauses.slice(0,Math.min(3,F.clauses.length)).map((c,j)=>({clause:j+1,S:c.map(l=>[Math.abs(l),l>0?1:0]),U:c.map(l=>[Math.abs(l),l>0?0:1]),S_inverted_U:c.map(l=>[Math.abs(l),l>0?0:1]),U_inverted_S:c.map(l=>[Math.abs(l),l>0?1:0])}))};
}
function probeGuest(str,h,extra=2){
  let A={idx:new Map(),ih:0,head:0,w:[new Map(),new Map()],wi:[new Map(),new Map()],wh:[0,0],whead:[0,0]};
  let B={idx:new Map(),ih:0,head:0,w:[new Map(),new Map()],wi:[new Map(),new Map()],wh:[0,0],whead:[0,0]};
  let ctr={guestSteps:0,hostIndexedJumps:0,hostInputBufferReads:0,hostIndexCellClears:0,hostAddressWrites:0,guestWorkWrites:0,
           guestIndexedJumps:0,guestBlankReads:0,sourceReads:0,outputBytes:0,peakBufferCells:str.length,peakInputIndexCells:h,workTapeCount:3};
  function same(){
    if(A.ih!==B.ih||A.head!==B.head||A.idx.size!==B.idx.size)throw Error("index-head mismatch");
    for(const [k,v]of A.idx)if(B.idx.get(k)!==v)throw Error("index-tape mismatch");
    for(let w=0;w<2;w++){if(A.wh[w]!==B.wh[w]||A.whead[w]!==B.whead[w])throw Error("work-head mismatch")}
  }
  function event(type,arg){
    ctr.guestSteps++;
    for(const X of [A,B]){
      if(type==="moveIdx")X.ih=arg;
      else if(type==="setIdx"){if(arg)X.idx.set(X.ih,1);else X.idx.delete(X.ih)}
      else if(type==="jump"){let pos=0;for(let k=0;k<h;k++)if(X.idx.get(k))pos+=2**k;X.head=pos;X.idx.clear()}
      else if(type==="inputMove")X.head+=arg;
      else if(type==="workWrite"){let [i,pos,value]=arg;X.w[i].set(pos,value);X.whead[i]=pos}
      else if(type==="workJump"){let [i,pos]=arg;X.wh[i]=pos;X.wi[i].clear()}
      else if(type==="read"){}
      else throw Error(type);
    }
    if(type==="jump"){ctr.guestIndexedJumps++;ctr.hostIndexCellClears+=h;ctr.hostAddressWrites+=h;ctr.hostIndexedJumps++}
    if(type==="read"){ctr.hostInputBufferReads++;if(A.head>=str.length)ctr.guestBlankReads++}
    if(type==="workWrite")ctr.guestWorkWrites++;
    same();
    if(type==="read"){let u=A.head<str.length?str[A.head]:"",v=B.head<str.length?str[B.head]:"";if(u!==v)throw Error("read mismatch");return u}
  }
  function go(addr){
    for(let k=0;k<h;k++){event("moveIdx",k);event("setIdx",(addr>>k)&1)}
    event("jump");
  }
  let acc=Array(str.length).fill(null),stride=str.length-1;while(gcd(stride,str.length)!==1)stride--;
  for(let k=0;k<str.length;k++){
    let pos=(k*stride)%str.length;go(pos);acc[pos]=event("read");
    if(k<3){event("inputMove",1);event("read");event("inputMove",-1);if(event("read")!==str[pos])throw Error("restore")}
    if(k%11===0){event("workWrite",[0,k%23,pos%2]);event("workJump",[1,k%19]);event("workWrite",[1,k%17,1])}
  }
  go(str.length+extra);if(event("read")!=="")throw Error("blank");
  go(0);if(event("read")!==str[0])throw Error("jump clears tape");
  // With erased index tape, the next jump targets address zero, preserving the index-head coordinate.
  event("jump");if(A.head!==0||A.ih!==h-1)throw Error("erase semantics");
  if(acc.join("")!==str)throw Error("guest byte reconstruction");
  return {events:ctr,reconstructedLength:acc.length,indexHeadAfterErase:A.ih,workTape0Cells:A.w[0].size,workTape1Cells:A.w[1].size};
}
function run(){
  const cases=[],qq=[3,4,8,16];
  for(const q of qq)for(const variant of ["allzero","lastone","alternating"]){
    let b=Array.from({length:q},(_,j)=>variant==="allzero"?0:variant==="lastone"?(j===q-1?1:0):j%2);
    let F=source(q,b),orig=satDpll(F),ss=serial(F);if(orig.sat!==b.some(Boolean))throw Error("source SAT");
    let d=stats(F),children=[],sumGuest=0,sumOut=0;
    for(let j=0;j<q;j++){
      let C=child(F,j),ser=serial(C),label=satDpll(C);if(label.sat!==!!b[j])throw Error("child SAT");
      let h=Math.ceil(Math.log2(2*ser.bytes.length+4)),g=probeGuest(ser.bytes,h);
      sumGuest+=g.events.guestSteps;sumOut+=ser.bytes.length;
      children.push({j,sourcePin:b[j],childChars:ser.bytes.length,childBits:ser.bytes.length*8,
        guestSAT:label.sat,guestDPLLNodes:label.nodes,guestLiteralTests:label.tests,trace:g.events});
    }
    let recovered=children.some(c=>c.guestSAT);if(recovered!==orig.sat)throw Error("OR semantics");
    let allNo=children.every(c=>!c.guestSAT);if(allNo===orig.sat)throw Error("UNSAT semantics");
    cases.push({q,variant,sourceChars:ss.bytes.length,sourceBits:8*ss.bytes.length,
      sourceSAT:orig.sat,baselineDPLLNodes:orig.nodes,baselineLiteralTests:orig.tests,
      sourceDiagnostics:d,childCount:q,children,chargedController:{sourceCharactersInspected:ss.bytes.length,
        policySelections:q,failedPolicies:0,sourcePinProbes:q,childCharactersOutput:sumOut,
        guestInstructionEvents:sumGuest,peakLiveChildBuffer:Math.max(...children.map(c=>c.childChars)),
        peakTotalProxyCells:Math.max(...children.map(c=>c.childChars+Math.ceil(Math.log2(2*c.childChars+4))+3+2*23)),
        sourceRetainedBits:Math.ceil(Math.log2(q+1))+1}});
  }
  return {schema:"ARC-BOUNDED-GUEST-INPUT273",date:"2026-10-31 PDT",status:"COMPUTATIONAL trace of restricted bounded-head guest and exact both-label decomposition; universal ARC OPEN",
    machineScope:"abstract FLMV operations simulated for read-only guest input and two guest work tapes; NOT native transition benchmarking",
    seed:"deterministic coprime stride",cases,
    checks:{cases:cases.length,childLabels:cases.reduce((s,x)=>s+x.childCount,0),
       byteReads:cases.reduce((s,x)=>s+x.children.reduce((t,c)=>t+c.trace.hostInputBufferReads,0),0)}};
}
if(typeof require!=="undefined"&&require.main===module){process.stdout.write(JSON.stringify(run(),null,2)+"\n")}
