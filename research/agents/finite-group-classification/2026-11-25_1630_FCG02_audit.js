// FCG02 independent audit, Node.js or V8, no external dependencies.
function audit(){
 const A=(x,m)=>{if(!x)throw Error(m)}, bits=k=>Array.from({length:1<<k},(_,i)=>Array.from({length:k},(_,j)=>(i>>j)&1)), comb=(a,k)=>k===0?[[]]:a.flatMap((v,i)=>i<=a.length-k?comb(a.slice(i+1),k-1).map(t=>[v,...t]):[]), key=a=>a.join(","), setkey=a=>[...new Set(a.map(key))].sort().join(";"), allsame=a=>new Set(a).size===1, eq=(a,b)=>key(a)===key(b);
 function classify(P){
  const k=P.length,B=[0,0,0];P.forEach(([s,c])=>B[c]+=s);
  if(!allsame(B.map(b=>((b%3)+3)%3)))return null;
  const R=bits(k).filter(w=>{let S=[0,0,0];P.forEach(([s,c],i)=>S[c]+=s*w[i]);return allsame(S.map((x,j)=>3*x-B[j]))});
  let t;
  if(k===3){A(allsame(P.map(p=>p[0])),"3-cut sign");t=allsame(P.map(p=>p[1]))?"onehot3":"eq3";A(R.length===(t==="eq3"?2:3),"3-cut size");}
  else {A(P.filter(p=>p[0]===1).length===2,"4-cut sign");t=B.every(b=>b===0)?(allsame(P.map(p=>p[1]))?"matching4":"paired4"):"onehot4";A(R.length===({matching4:6,paired4:4,onehot4:3})[t],"4-cut size");}
  return {R,t};
 }
 const maj=(a,b,c)=>a.map((x,i)=>+(x+b[i]+c[i]>=2));
 function bij(Q,k){const S=new Set(Q.map(key));for(let a of Q)for(let b of Q)for(let c of Q)A(S.has(key(maj(a,b,c))),"majority failure");const Z=bits(k).filter(w=>Q.length&&comb([...w.keys()],2).every(([i,j])=>Q.some(q=>q[i]===w[i]&&q[j]===w[j])));A(setkey(Z)===setkey(Q),"binary projection");}
 function subrelations(R){return bits(R.length).map(b=>R.filter((_,j)=>b[j]));}
 let patternCounts={},maskCounts={},unique=new Set(),patterns=0;
 for(const k of [3,4]){
  for(let i=0;i<6**k;i++){let x=i,P=[];for(let j=0;j<k;j++){let d=x%6;x=Math.floor(x/6);P.push([d<3?1:-1,d%3]);}let z=classify(P);if(!z)continue;patterns++;let {t,R}=z;patternCounts[t]=(patternCounts[t]||0)+1;
   let sig=t+"|"+setkey(R);if(t==="matching4")sig+="|"+P.map(p=>p[0]).join(",");if(unique.has(sig))continue;unique.add(sig);
   if(t==="eq3"||t==="onehot3"||t==="onehot4"){
    if(t==="eq3")A(setkey(R)==="0,0,0;1,1,1","eq3");
    else A(comb([...P.keys()],3).some(J=>R.every(w=>J.reduce((a,j)=>a+w[j],0)===1)&&new Set(R.map(w=>key(J.map(j=>w[j])))).size===3),"onehot support");
    for(let Q of subrelations(R)){maskCounts[t]=(maskCounts[t]||0)+1;if(!Q.length)continue;let pins=[...P.keys()].filter(j=>allsame(Q.map(w=>w[j])));A(setkey(R.filter(w=>pins.every(j=>w[j]===Q[0][j])))===setkey(Q),"pin closure");}
   }else if(t==="paired4"){for(let Q of subrelations(R)){maskCounts[t]=(maskCounts[t]||0)+1;bij(Q,k);}}
   else{let U=[...P.keys()].filter(i=>P[i][0]===1),V=[...P.keys()].filter(i=>P[i][0]===-1);let lanes=[V,V.slice().reverse()].map(v=>R.filter(w=>U.every((u,i)=>w[u]===w[v[i]])));A(setkey(lanes.flat())===setkey(R),"matching union");
    for(let Q of subrelations(R)){maskCounts[t]=(maskCounts[t]||0)+1;let L=lanes.map(l=>Q.filter(w=>l.some(v=>eq(w,v))));A(setkey(L.flat())===setkey(Q),"mask union");L.forEach(q=>bij(q,k));}
   }
  }
 }
 const H=[[0,5,6],[0,1,7],[1,2,8],[2,5,9],[3,4,10],[3,4,11],[0,3,6],[1,7,8],[2,8,9],[7,9,10],[4,10,11],[5,6,11]],P=[0,1,0,2,1,0,2,2,1,0,2,1],V=[0,3,4,5,6,10,11],C=[0,4,5,6,10,11],port=[10,0,5];
 const n=H.length,ref=bits(n).filter(w=>H.every(c=>c.reduce((a,u)=>a+w[u],0)===1));
 const graph=(H,P)=>{let n=H.length,es=H.flatMap((c,i)=>c.map(u=>[u,n+i])),adj=Array.from({length:2*n},()=>[]);es.forEach(([u,v],i)=>{adj[u].push([v,i]);adj[v].push([u,i]);});A(adj.every(a=>a.length===3),"cubic");A(adj.slice(0,n).every(a=>new Set(a.map(([v])=>P[v-n])).size===3),"partition");A(new Set(adj.slice(0,n).map(a=>a.map(x=>x[0]).sort((x,y)=>x-y).join(","))).size===n,"occurrence signatures");return {es,adj};}
 function components(adj,omitE=new Set(),omitV=new Set()){let seen=new Set(),out=[];for(let v=0;v<adj.length;v++){if(seen.has(v)||omitV.has(v))continue;let q=[v];seen.add(v);for(let i=0;i<q.length;i++)for(let [w,e] of adj[q[i]])if(!omitE.has(e)&&!omitV.has(w)&&!seen.has(w)){seen.add(w);q.push(w);}out.push(q);}return out;}
 let {es,adj}=graph(H,P);for(let k of [0,1,2])for(let S of comb([...adj.keys()],k))A(components(adj,new Set(),new Set(S)).length===1,"3connect");
 let counts={},eqs=new Set(),eos=new Set(),checks=0;
 for(let k of [3,4])for(let E of comb([...es.keys()],k)){
  let cc=components(adj,new Set(E));if(cc.length!==2||cc.some(s=>s.length<=1))continue;
  let S=new Set(cc[0]);if(!E.every(e=>S.has(es[e][0])!==S.has(es[e][1])))continue;
  let W=E.map(e=>es[e]),Q=W.map(([u,v])=>[S.has(u)?1:-1,P[v-n]]),z=classify(Q);A(z,"source pattern");let {R,t}=z;counts[t]=(counts[t]||0)+1;
  for(let w of ref){A(R.some(r=>eq(r,W.map(e=>w[e[0]]))),"source model conservation");checks++;}
  for(let [i,j] of comb([...W.keys()],2))if(W[i][0]!==W[j][0]&&R.every(r=>r[i]===r[j]))eqs.add(W.slice(0,0).concat([W[i][0],W[j][0]]).sort((a,b)=>a-b).join(","));
  for(let J of comb([...W.keys()],3))if(R.every(r=>J.reduce((a,j)=>a+r[j],0)===1))eos.add(J.map(j=>W[j][0]).sort((a,b)=>a-b).join(","));
 }
 let Gwords=bits(V.length).filter(b=>C.every(i=>H[i].reduce((a,u)=>a+b[V.indexOf(u)],0)===1));A(Gwords.length===1&&port.every(u=>Gwords[0][V.indexOf(u)]===0),"zero gadget");
 function graft(F,K,v){let n=F.length,M=new Map(V.map((u,j)=>[u,j===0?v:n+j-1]));return [F.map((c,i)=>c.map(u=>u===v?M.get(port[K[i]]):u)).concat(C.map(j=>H[j].map(u=>M.get(u)))),K.concat(C.map(j=>P[j])),M];}
 let stress=[],F=H.map(c=>c.slice()),K=P.slice(),w=ref.find(w=>w[0]===0).slice(),v=0;
 for(let k=0;k<=64;k++){if([0,1,4,16,64].includes(k)){graph(F,K);A(F.every(c=>c.reduce((a,u)=>a+w[u],0)===1),"graft lift");A(w[v]===0,"root pin");stress.push({grafts:k,n:F.length,witnessVerified:true,forcedZeroByGadget:k>0});}if(k===64)break;let [F2,K2,M]=graft(F,K,v);V.forEach((u,j)=>w[M.get(u)]=Gwords[0][j]);F=F2;K=K2;v=M.get(port[1]);}
 return {patterns,patternCounts,uniqueSignatures:unique.size,maskCounts,base:{n,models:ref.map(w=>w.reduce((s,x,i)=>s+(x<<i),0)),counts,derivedEqualities:eqs.size,derivedTriples:eos.size,newTriples:[...eos].filter(s=>!H.some(c=>key(c.slice().sort((a,b)=>a-b))===s)).length,modelProjectionChecks:checks,gadgetWords:Gwords},stress};
}
console.log(JSON.stringify(audit(),null,2));
