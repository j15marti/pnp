
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

function pairMul(a,b){return 6*M[Math.floor(a/6)][Math.floor(b/6)]+M[a%6][b%6]}
function pairInv(a){return 6*inv(Math.floor(a/6))+inv(a%6)}
function pairComm(a,b){return pairMul(pairInv(pairMul(b,a)),pairMul(a,b))}
function fixture(m,mode="main"){
 let n=m*m,b=n+6,A=range(b),B=range(n).map(i=>i%m*m+Math.floor(i/m)).concat(range(6).map(i=>n+i));
 if(mode==="shift")B=A.slice(Math.floor(n/2),n).concat(A.slice(0,Math.floor(n/2)),A.slice(n));
 let L=range(b).map(i=>i<n?6*gen(i)+3:gen(i-n)),targets=mode==="same"?[0,0]:mode==="shift"?[0,18]:[0,3];
 let v=b,F=[],C=[],paths=[];
 function add(S,R){let rs=new Set(R);F.push({S,R});for(let w=0;w<1<<S.length;w++)if(!rs.has(w))C.push(S.map((x,i)=>bit(w,i)?-x-1:x+1))}
 for(let [side,order] of [A,B].entries())for(let c=0;c<2;c++){
  let p=range(3).map(()=>v++),path=[p];add(p,[0]);
  for(let id of order){let q=range(3).map(()=>v++),R=[],g=c?L[id]%6:Math.floor(L[id]/6);
   for(let s=0;s<6;s++)for(let x=0;x<2;x++)R.push(s+(x<<3)+(M[s][x?g:0]<<4));add(p.concat([id],q),R);p=q;path.push(p)}
  add(p,[c?targets[side]%6:Math.floor(targets[side]/6)]);paths.push(path)}
 return {m,b,A,B,L,targets,v,F,C,paths,mode};
}
function quotient(S,all,cap){
 let ops=0;const mm=(a,b)=>{if(++ops>cap)throw Error("CAP");return pairMul(a,b)};try{
 let pos=new Map(S.B.map((v,i)=>[v,i])),gens=new Set(),inversions=0;
 if(all){for(let a=0;a<36;a++)for(let b=0;b<36;b++)gens.add(mm(pairInv(mm(b,a)),mm(a,b)))}
 else for(let i=0;i<S.b;i++)for(let j=i+1;j<S.b;j++)if(pos.get(S.A[i])>pos.get(S.A[j])){
   inversions++;let a=S.L[S.A[i]],b=S.L[S.A[j]];gens.add(mm(pairInv(mm(b,a)),mm(a,b)))}
 let normalGens=new Set([0]);for(let g of gens)for(let a=0;a<36;a++)normalGens.add(mm(mm(a,g),pairInv(a)));
 let H=new Set([0]);for(let h of H)for(let g of normalGens)H.add(mm(h,g));
 let rep=Array(36);for(let a=0;a<36;a++)rep[a]=Math.min(...[...H].map(h=>mm(a,h)));
 let checks=0;for(let a=0;a<36;a++)for(let b=0;b<36;b++){checks++;if(rep[mm(a,b)]!==rep[mm(rep[a],rep[b])])throw Error("not a congruence")}
 // Verify all inverted pairs commute in quotient independently of closure construction.
 for(let i=0;i<S.b;i++)for(let j=i+1;j<S.b;j++)if(pos.get(S.A[i])>pos.get(S.A[j]))if(rep[mm(S.L[S.A[i]],S.L[S.A[j]])]!==rep[mm(S.L[S.A[j]],S.L[S.A[i]])])throw Error("not aligned");
 let P=new Set([rep[0]]);for(let id of S.A){let Q=new Set();for(let p of P){Q.add(p);Q.add(rep[mm(p,S.L[id])])}P=Q}
 let [a,b]=S.targets.map(x=>rep[x]);return {status:a!==b||!P.has(a)?"NO":"UNKNOWN",H:[...H].sort((a,b)=>a-b),classes:new Set(rep).size,inversions,checks,ops,reachable:[...P].sort((a,b)=>a-b),targetImages:[a,b]};
 }catch(e){if(e.message==="CAP")return {status:"UNKNOWN",ops,reason:"cap"};throw e}}
function runExact(S,p,cap){let states=new Map([["0,0",[0,0]]]),ops=0,updates=0,peak=1;const mm=(a,b)=>{if(++ops>cap)throw Error("CAP");return pairMul(a,b)};try{
 for(let e of p.path){let {i,j,ii,jj,side,n}=e,id=side?S.B[j]:S.A[i],R=structure(S.A,S.B,i,j),RR=structure(S.A,S.B,ii,jj),hit=R.findIndex(r=>r.side===side&&r.ids[0]===id),out=new Map(),templates=[];
 for(let r of RR){let parts=[],k=0;while(k<r.ids.length){let idx=R.findIndex(q=>q.side===r.side&&q.ids[0]===r.ids[k]);if(idx>=0){let q=R[idx];if(q.ids.some((v,z)=>v!==r.ids[k+z]))throw Error("split run");parts.push(idx);k+=q.ids.length}else{if(hit>=0||r.ids[k]!==id||r.side===side)throw Error("new run");parts.push(-1);k++}}templates.push(parts)}
 if(hit>=0&&n!==R[hit].ids.length)throw Error("partial flush");
 for(let t of states.values())for(let x of hit>=0?[0]:[0,1]){updates++;let z=[t[0],t[1]],g=x?S.L[id]:0;z[side]=mm(z[side],hit>=0?t[2+hit]:g);for(let parts of templates){let u=0;for(let k of parts)u=mm(u,k<0?g:t[2+k]);z.push(u)}out.set(z.join(","),z)}
 states=out;peak=Math.max(peak,states.size)}
 return {status:states.has(S.targets.join(","))?"NOT_REFUTED":"NO",ops,updates,peak,final:[...states.keys()].sort()};
 }catch(e){if(e.message==="CAP")return {status:"UNKNOWN",ops,updates,peak};throw e}}
function direct(S,cap){let pos=new Map(S.B.map((x,i)=>[x,i])),checks=0;for(let c=0;c<2;c++){let get=x=>c?x%6:Math.floor(x/6),ok=true;for(let i=0;i<S.b;i++)for(let j=i+1;j<S.b;j++)if(pos.get(S.A[i])>pos.get(S.A[j])){if(++checks>cap)return {status:"UNKNOWN",checks};let a=get(S.L[S.A[i]]),b=get(S.L[S.A[j]]);if(M[a][b]!==M[b][a])ok=false}if(ok&&get(S.targets[0])!==get(S.targets[1]))return {status:"NO",coordinate:c,checks}}
 return {status:"UNKNOWN",checks}}
function exhaustive(S,cap){let tested=0,states=new Set();for(let w=0;w<2**S.b&&tested<cap;w++,tested++){let a=0,b=0;for(let id of S.A)a=pairMul(a,Math.floor(w/2**id)%2?S.L[id]:0);for(let id of S.B)b=pairMul(b,Math.floor(w/2**id)%2?S.L[id]:0);states.add([a,b].join(","))}return {tested,complete:tested===2**S.b,hit:states.has(S.targets.join(",")),pairs:[...states].sort()}}
function auditNew(){let cap=200000,result=[];for(let m of [2,4,6,8,10,12]){
 let S=fixture(m),N=native(S),initial=close(S),p=plan(S.A,S.B,true),rev=S.B.slice().reverse(),widths=[p.width,plan(S.A,rev,true).width,plan(S.A.slice().reverse(),S.B,true).width,plan(S.A.slice().reverse(),rev,true).width],A=runExact(S,p,cap),B=quotient(S,true,cap),C=quotient(S,false,cap),D=direct(S,cap),E=exhaustive(S,1024);
 if(C.status!=="NO"||D.status!=="NO"||B.status!=="UNKNOWN"||A.status==="NOT_REFUTED"||E.hit||initial.status!=="UNKNOWN"||Math.min(...widths)<m/2)throw Error("family "+JSON.stringify({m,initial,A,B,C,D,E,widths}));
 if(E.complete&&A.final&&E.pairs.join(";")!==A.final.join(";"))throw Error("pair support");
 let rec=close(S,true);if(rec.status!=="NO")throw Error("reclosure");
 result.push({m,b:S.b,...N,initial,runWidths:widths,run:A.status==="NO"?{...A,final:undefined}:A,abelian:B,selective:C,direct:D,exhaustive:{tested:E.tested,complete:E.complete},reclosure:rec})
 }
 let S=fixture(2,"same"),N=native(S),Q=quotient(S,false,cap),E=exhaustive(S,1024),w=S.C.every(c=>c.some(l=>l<0));if(Q.status==="NO"||!E.hit||!w)throw Error("SAT control");
 let H=fixture(2,"shift"),HN=native(H),HQ=quotient(H,false,cap),HE=exhaustive(H,1024);if(HQ.status!=="UNKNOWN"||!HE.complete||HE.hit)throw Error("incompleteness");
 return {cap,result,soundness:{N,Q,witness:w},incomplete:{N:HN,Q:HQ,complete:HE.complete,words:HE.tested,hit:HE.hit}};
}
console.log(JSON.stringify(auditNew(),null,2));
