
const range=n=>Array.from({length:n},(_,i)=>i);
const G=[[0,1,2],[1,0,2],[0,2,1],[1,2,0],[2,0,1],[2,1,0]];
const mul=(a,b)=>G.findIndex(g=>g.every((x,i)=>x===G[a][G[b][i]]));
const M=range(6).map(a=>range(6).map(b=>mul(a,b)));
const inv=a=>range(6).find(b=>M[a][b]===0);
const gen=id=>id%2===0?1:2;
const elt=(id,x)=>x?gen(id):0;
const bit=(w,i)=>(w>>i)&1;
const bits=(x,n)=>range(n).map(i=>bit(x,i));
function make(b,same=false,other=null){
 let A=range(b),B=other||A.slice(b/2).concat(A.slice(0,b/2)),v=b,F=[],C=[];
 const add=(S,R)=>{const rs=new Set(R);F.push({S,R});for(let w=0;w<(1<<S.length);w++)if(!rs.has(w))C.push(S.map((x,i)=>bit(w,i)?-x-1:x+1));};
 let stages=[];
 for(let [order,target] of [[A,0],[B,same?0:1]]){
  let prev=range(3).map(()=>v++);add(prev,[0]);let path=[prev];
  for(let id of order){let next=range(3).map(()=>v++),R=[];for(let s=0;s<6;s++)for(let x=0;x<2;x++)R.push(s+(x<<3)+(M[s][elt(id,x)]<<4));add(prev.concat([id],next),R);prev=next;path.push(prev);}
  add(prev,target===0?[0]:[1,2,3,4,5]);stages.push(path);
 }
 return {b,A,B,v,F,C,stages,same};
}
function mask(h){let r=0;for(let w=0;w<16;w++){let n=bit(w,0),e=bit(w,1),s=bit(w,2),z=bit(w,3);if(e===z&&s===(n|[0,z,1-z][h]))r|=1<<w;}return r;}
const masks=range(3).map(mask);
function native(S){
 let k=Math.max(2,S.v,S.C.length),columns=[],h=2166136261;
 const hash=x=>h=Math.imul(h^x,16777619)>>>0;
 hash(k);hash(masks[0]);hash(0); // north0, horizontal free by fixed convention
 for(let j=0;j<k;j++){
  const C=S.C[j]||[],entries=C.map(l=>[Math.abs(l)-1,masks[l>0?1:2]]).sort((a,b)=>a[0]-b[0]);
  if(entries.some((a,i)=>a[0]>=k||(i&&entries[i-1][0]===a[0])))throw Error("invalid native row");
  columns.push({south:j<S.C.length?1:0,entries});
  hash(j);hash(j<S.C.length?1:0);hash(entries.length);for(const [i,m] of entries){hash(i);hash(m);}
 }
 let decoded=columns.filter(c=>c.south).map(c=>c.entries.map(([i,m])=>m===masks[1]?i+1:m===masks[2]?-i-1:0));
 const key=c=>c.slice().sort((a,b)=>a-b).join(",");
 if(decoded.length!==S.C.length||decoded.some((c,j)=>key(c)!==key(S.C[j])))throw Error("decode");
 let q=0,verified=0;
 for(const f of S.F){let ct=(1<<f.S.length)-f.R.length,actual=decoded.slice(q,q+ct);q+=ct;
  for(let w=0;w<(1<<f.S.length);w++){let ok=actual.every(c=>c.some(l=>bit(w,f.S.indexOf(Math.abs(l)-1))===Number(l>0)));if(ok!==f.R.includes(w))throw Error("source truth table");verified++;}
 }
 if(q!==decoded.length)throw Error("coverage");
 return {k,N:16*k*k+8*k+Math.floor(Math.log2(k))+1,hash:h.toString(16),active:S.v,clauses:S.C.length,verified};
}
function close(S,empty=false){let D=Array(S.v).fill(3),del=0,scans=0;let F=empty?S.F.concat([{S:[],R:[]}]):S.F;
 for(;;){let old=del;for(let {S,R} of F){scans++;let W=R.filter(w=>S.every((x,i)=>D[x]&(1<<bit(w,i))));if(!W.length)return {status:"NO",del,scans};for(let i=0;i<S.length;i++){let d=W.reduce((z,w)=>z|(1<<bit(w,i)),0);if(d!==D[S[i]]){D[S[i]]=d;del++;}}}if(old===del)return {status:"UNKNOWN",del,scans,primaryFull:D.slice(0,S.b).every(x=>x===3)};}
}
function structure(A,B,i,j){let PA=new Set(A.slice(0,i)),PB=new Set(B.slice(0,j));let out=[];
 for(let [order,start,seen,side] of [[A,i,PB,0],[B,j,PA,1]]){let run=[];for(let k=start;k<order.length;k++){if(seen.has(order[k]))run.push(order[k]);else if(run.length){out.push({side,ids:run});run=[];}}if(run.length)out.push({side,ids:run});}
 return out;
}
function plan(A,B,macro){let b=A.length,W=[],P=[];for(let i=0;i<=b;i++){W[i]=Array(b+1).fill(Infinity);P[i]=Array(b+1).fill(null);}W[0][0]=0;
 for(let i=0;i<=b;i++)for(let j=0;j<=b;j++){if(!Number.isFinite(W[i][j]))continue;let R=structure(A,B,i,j);
  for(let side=0;side<2;side++){let k=side?j:i,order=side?B:A;if(k===b)continue;let run=R.find(r=>r.side===side&&r.ids[0]===order[k]),n=macro&&run?run.ids.length:1,ii=i+(side===0?n:0),jj=j+(side===1?n:0),RR=structure(A,B,ii,jj);
   let width=macro?RR.length:RR.reduce((s,r)=>s+r.ids.length,0),cost=Math.max(W[i][j],width);if(cost<W[ii][jj]){W[ii][jj]=cost;P[ii][jj]={i,j,side,n};}}
 }
 let path=[],i=b,j=b;while(i||j){let p=P[i][j];if(!p)throw Error("plan");path.push({...p,ii:i,jj:j});i=p.i;j=p.j;}return {width:W[b][b],path:path.reverse()};
}
function raw(S,p,cap){let states=new Map([["0,0,0",[0,0,0n]]]),ops=0,peak=1;
 for(let e of p.path){let {i,j,side}=e,id=side?S.B[j]:S.A[i],seen=(side?S.A.slice(0,i):S.B.slice(0,j)).includes(id),m=1n<<BigInt(id),out=new Map();
  for(let [a,b,g] of states.values())for(let x of seen?[Number(Boolean(g&m))]:[0,1]){if(++ops>cap)return {status:"UNKNOWN",ops,peak};let t=[a,b,g];t[side]=M[t[side]][elt(id,x)];t[2]=seen?g&~m:(x?g|m:g);out.set(t.join(","),t);}
  states=out;peak=Math.max(peak,states.size);
 }
 return {status:[...states.values()].some(([a,b])=>a===0&&(S.same?b===0:b!==0))?"NOT_REFUTED":"NO",ops,peak};
}
function runs(S,p,cap){let states=new Map([["0,0",[0,0]]]),ops=0,peak=1,flushes=0;
 for(let e of p.path){let {i,j,ii,jj,side,n}=e,id=side?S.B[j]:S.A[i],R=structure(S.A,S.B,i,j),RR=structure(S.A,S.B,ii,jj),hit=R.findIndex(r=>r.side===side&&r.ids[0]===id),out=new Map(),templates=[];
  // For each new run, concatenate whole old runs and optionally the newly seen id, in FUTURE order.
  for(let r of RR){let parts=[],k=0;while(k<r.ids.length){let idx=R.findIndex(q=>q.side===r.side&&q.ids[0]===r.ids[k]);if(idx>=0){let q=R[idx];if(q.ids.some((v,z)=>v!==r.ids[k+z]))throw Error("split run");parts.push(idx);k+=q.ids.length;}else{if(hit>=0||r.ids[k]!==id||r.side===side)throw Error("bad new run");parts.push(-1);k++;}}templates.push(parts);}
  if(hit>=0){if(n!==R[hit].ids.length)throw Error("partial flush");flushes++;}
  for(let t of states.values())for(let x of hit>=0?[0]:[0,1]){if(++ops>cap)return {status:"UNKNOWN",ops,peak,flushes};let z=[t[0],t[1]],g=elt(id,x);z[side]=M[z[side]][hit>=0?t[2+hit]:g];for(let parts of templates){let u=0;for(let k of parts)u=M[u][k<0?g:t[2+k]];z.push(u);}out.set(z.join(","),z);}
  states=out;peak=Math.max(peak,states.size);
 }
 return {status:[...states.values()].some(([a,b])=>a===0&&(S.same?b===0:b!==0))?"NOT_REFUTED":"NO",ops,peak,flushes,finalPairs:[...states.keys()].sort()};
}
function algebra(S){let b=S.b,k=S.A.indexOf(S.B[0]);if(S.B.join(",")!==S.A.slice(k).concat(S.A.slice(0,k)).join(","))return {status:"UNKNOWN",checks:0};let checks=0;
 for(let u=0;u<6;u++)for(let v=0;v<6;v++){if((M[u][v]===0)!==(M[v][u]===0)||M[inv(u)][M[M[u][v]][u]]!==M[v][u])throw Error("conjugation");checks++;}
 return {status:S.same?"NOT_REFUTED":"NO",checks};
}
function brute(S,cap){let tested=0,P=new Set();for(let w=0;w<2**S.b&&tested<cap;w++){let a=0,b=0;for(let id of S.A)a=M[a][elt(id,Math.floor(w/2**id)%2)];for(let id of S.B)b=M[b][elt(id,Math.floor(w/2**id)%2)];P.add([a,b].join(","));tested++;}return {complete:tested===2**S.b,tested,pairs:[...P].sort()};}
function audit(){let result=[],cap=200000;for(let b of [8,12,16,24,32,64]){
 let S=make(b),N=native(S),initial=close(S),P=plan(S.A,S.B,false),Q=plan(S.A,S.B,true);
 let A=raw(S,P,cap),B=algebra(S),C=runs(S,Q,cap),D=brute(S,Math.min(cap,4096));
 if(C.status!=="NO"||B.status!=="NO"||A.status==="NOT_REFUTED"||initial.status!=="UNKNOWN"||!initial.primaryFull)throw Error("unexpected NO control");
 if(D.complete&&D.pairs.join(";")!==C.finalPairs.join(";"))throw Error("joint pair mismatch");
 let reclosure=close(S,true);if(reclosure.status!=="NO")throw Error("imported global conflict");
 let rev=S.B.slice().reverse(),revWidths=[plan(S.A,rev,false).width,plan(S.A.slice().reverse(),S.B,false).width,plan(S.A.slice().reverse(),rev,false).width];
 result.push({b,...N,initial,rawWidth:P.width,orientationMin:Math.min(P.width,...revWidths),runWidth:Q.width,raw:A,algebra:B,runs:C,brute:{complete:D.complete,tested:D.tested},reclosure});
 }
 let S=make(8,true),N=native(S),control=runs(S,plan(S.A,S.B,true),cap),w=Array(S.v).fill(0),witness=S.C.every(c=>c.some(l=>w[Math.abs(l)-1]===Number(l>0)));if(control.status!=="NOT_REFUTED"||!witness)throw Error("false NO");
 // Noncommuting generators, and product equality alone cannot support partial flush.
 let a=1,b=2;let noncommute=[M[a][b],M[b][a]];if(noncommute[0]===noncommute[1])throw Error("commute");
 let hostile=make(8,false,[0,2,1,3,4,5,6,7]),H=native(hostile),HR=runs(hostile,plan(hostile.A,hostile.B,true),cap),HB=brute(hostile,256);if(HR.status!=="NOT_REFUTED"||!HB.pairs.some(s=>s[0]==="0"&&s[2]!=="0")||HR.finalPairs.join(";")!==HB.pairs.join(";"))throw Error("hostile reorder");
 return {cap,result,control:{N,status:control.status,witness},noncommute,hostile:{N:H,status:HR.status,conjugacy:algebra(hostile),brute:HB.complete},partialFlush:{words:[ [0,0],[1,1] ],sameProduct:M[1][1],differentFirst:true}};
}
console.log(JSON.stringify(audit(),null,2));
