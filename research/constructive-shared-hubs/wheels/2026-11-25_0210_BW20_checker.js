// BW20 checker: node checker.js BS19_results.json BW17_frozen.json
const fs=require('fs');
function run(data,raw){
 let checks=0;const ok=(b,m)=>{checks++;if(!b)throw Error(m)};
 const bit=(x,l)=>x[Math.abs(l)]^(l<0?1:0),nae=(x,C)=>C.some(l=>bit(x,l)!==bit(x,C[0]));
 const k=data.common.find(x=>x.K===16).residual,C=k.C,v=19, bucket=C.filter(c=>c.some(l=>Math.abs(l)===v)).map(c=>{let q=c.find(l=>Math.abs(l)===v);return c.filter(l=>Math.abs(l)!==v).map(l=>q<0?-l:l)}),rest=C.filter(c=>!c.some(l=>Math.abs(l)===v));
 const ext=[...new Set(C.flat().map(Math.abs))].filter(x=>x!==v).sort((a,b)=>a-b);
 ok(ext.length===13&&bucket.length===34,"authenticated dimensions");
 const orig=raw.O.map(o=>o.t.map(i=>i+1));ok(orig.every((c,i)=>c.slice().sort((a,b)=>a-b).join()===data.common[0].residual.C[i].slice().sort((a,b)=>a-b).join()),"source identity");
 let next=25;const triples=[],gates=[],pins=[]; const fresh=()=>next++;
 function gate(a,b,h,op){let z=fresh();gates.push({a,b,h,z,op});if(op==="or"){a=-a;b=-b;z=-z}triples.push([a,b,-z],[-z,a,h],[-z,b,h]);return Math.abs(z)}
 function fold(L,h,op){return L.reduce((a,b)=>gate(a,b,h,op))}
 function pin(z,h,w){pins.push({z,h,w});let t=w?h:-h;triples.push([z,t,t])}
 const h=ext[0], Z=fold(bucket.map(c=>fold(c.map(l=>-l),h,"and")),h,"or"), O=fold(bucket.map(c=>fold(c,h,"and")),h,"or");
 pin(gate(Z,O,h,"and"),h,0);const pivotGates=gates.length,pivotTriples=triples.length;
 for(const c of rest){let h=c[0];pin(fold(c.slice(1),h,"or"),h,1)}
 // Each gate truth table independent of its reference phase.
 for(const op of ["and","or"])for(let w=0;w<16;w++){
  let [a,b,z,h]=[0,1,2,3].map(i=>(w>>i)&1),x=[0,a,b,z,h];
  const L=op==="and"?[[1,2,-3],[-3,1,4],[-3,2,4]]:[[-1,-2,3],[3,-1,4],[3,-2,4]];
  ok(L.every(c=>nae(x,c))===((z^h)===(op==="and"?((a^h)&(b^h)):((a^h)|(b^h)))),"gate truth");
 }
 // Certified rank-one closure: DSU affine equalities from duplicate positions;
 // signed literals already opposite make a tautology; no semantic oracle.
 const par=Array.from({length:next},(_,i)=>i),delta=Array(next).fill(0);
 function find(a){let d=0;while(par[a]!==a){d^=delta[a];a=par[a]}return [a,d]}
 let scans=0,joins=0,changed=true;
 while(changed){changed=false;for(const c of triples){scans++;let t=c.map(l=>{let [a,d]=find(Math.abs(l));return [a,d^(l<0?1:0)]});
  if(t.some((a,i)=>t.some((b,j)=>j>i&&a[0]===b[0]&&a[1]!==b[1])))continue;
  for(let i=0;i<3;i++)for(let j=i+1;j<3;j++)if(t[i][0]===t[j][0]){
    let p=t[i],q=t[3-i-j];ok(p[0]!==q[0],"closure contradiction");par[q[0]]=p[0];delta[q[0]]=1^p[1]^q[1];joins++;changed=true;
    i=3;break;
  }
 }}
 let gateAccepted=0,fullAccepted=0,first=null,peer=null,wordVisits=0;
 for(let w=0;w<(1<<ext.length);w++){
  let x=Array(next).fill(0);ext.forEach((a,i)=>x[a]=(w>>i)&1);
  for(const g of gates){let a=bit(x,g.a)^bit(x,g.h),b=bit(x,g.b)^bit(x,g.h);x[g.z]=(g.op==="and"?a&b:a|b)^bit(x,g.h)}
  let accept=triples.slice(0,pivotTriples).every(c=>{wordVisits++;return nae(x,c)});
  let actual=[0,1].some(b=>{x[v]=b;return bucket.every(c=>nae(x,[v,...c]))});
  ok(accept===actual,"pivot equivalence");
  let full=triples.every(c=>{wordVisits++;return nae(x,c)}),ref=actual&&rest.every(c=>nae(x,c));
  ok(full===ref,"full equivalence");if(accept)gateAccepted++;
  if(full){fullAccepted++;for(let j=1;j<next;j++){let [p,d]=find(j);ok((x[j]^x[p])===d,"closure lift")}
   if(!first)first=x.slice();
   let y=x.slice();y[v]=[0,1].find(b=>{y[v]=b;return bucket.every(c=>nae(y,[v,...c]))});
   for(const q of k.log.slice().reverse()){y[q.v]=[0,1].find(b=>{y[q.v]=b;return q.bucket.every(c=>nae(y,[q.v,...c]))});ok(y[q.v]!==undefined,"reverse")}
   ok(orig.every(c=>nae(y,c)),"source verification");
   let word=orig.flat().length?Array.from({length:24},(_,i)=>y[i+1]*(2**i)).reduce((a,b)=>a+b,0):0;
   if(word===12130883)peer={x:x.slice(),word};
  }
 }
 ok(gateAccepted===2622&&fullAccepted===200&&peer!==null,"peer counts");
 // Strict physical I21 graph. Bits stored at vertices per port, checked on every wire.
 function native(C,x){
  const V=[],W=[],occ=new Map();let priv=x.length;
  const add=(kind,vals)=>{V.push({kind,vals,degree:0});return V.length-1};
  const wire=(u,i,v,j,s)=>{W.push([u,i,v,j,s]);V[u].degree++;V[v].degree++;};
  const use=(l,u,i)=>{let a=Math.abs(l);if(!occ.has(a))occ.set(a,[]);occ.get(a).push([u,i,l<0?1:0]);};
  for(const c of C){ok(nae(x,c),"native source NAE");let d=priv++,db=2-c.reduce((s,l)=>s+bit(x,l),0);x[d]=db;
   for(let copy=0;copy<2;copy++){let L=[...c,d],u=add("B",L.map(l=>bit(x,l)));L.forEach((l,i)=>use(l,u,i))}
  }
  for(const [a,ports] of occ){let t=ports.length/2;ok(Number.isInteger(t),"even occurrences");if(t===1){let [p,q]=ports;wire(p[0],p[1],q[0],q[1],p[2]^q[2]);continue}
   let E=Array.from({length:t-1},()=>add("E",Array(4).fill(x[a]))),free=[];
   for(let i=0;i<E.length;i++){if(i+1<E.length)wire(E[i],1,E[i+1],0,0);for(let j=0;j<4;j++)if(!(j===0&&i>0)&&!(j===1&&i+1<E.length))free.push([E[i],j])}
   ok(free.length===ports.length,"port capacity");ports.forEach((p,i)=>wire(p[0],p[1],free[i][0],free[i][1],p[2]));
  }
  const core={vertices:V.length,wires:W.length,B:V.filter(v=>v.kind==="B").length,E:V.filter(v=>v.kind==="E").length};
  const old=W.splice(0);V.forEach(v=>v.degree=0);
  // Replace every original wire by private K5 minus edge, maintaining signs.
  for(const [u,i,v,j,s] of old){let b=V[v].vals[j],g=Array.from({length:5},()=>add("E",Array(4).fill(b))),p=Array(5).fill(0);
   for(let a=0;a<5;a++)for(let z=a+1;z<5;z++)if(a!==0||z!==1)wire(g[a],p[a]++,g[z],p[z]++,0);
   wire(u,i,g[0],p[0]++,s);wire(g[1],p[1]++,v,j,0);
  }
  const edges=new Set(),ports=new Set();
  for(const [u,i,v,j,s] of W){let key=[Math.min(u,v),Math.max(u,v)].join();ok(u!==v&&!edges.has(key),"simple");edges.add(key);for(const [a,b] of [[u,i],[v,j]]){let p=a+":"+b;ok(b>=0&&b<4&&!ports.has(p),"port once");ports.add(p)}ok((V[u].vals[i]^V[v].vals[j])===s,"signed wire")}
  for(const a of V){ok(a.degree===4,"degree");ok(a.kind==="E"?a.vals.every(b=>b===a.vals[0]):a.vals.reduce((s,b)=>s+b,0)===2,"vertex")}
  return {core,vertices:V.length,wires:W.length,ports:ports.size};
 }
 const nativeMain=native(triples,peer.x.slice());
 // Fano SAT/UNSAT paired control; native lift for one single-sign SAT witness.
 const fano=[[1,2,3],[1,4,5],[1,6,7],[2,4,6],[2,5,7],[3,4,7],[3,5,6]];
 let modelCounts=[],fanoNative=null;
 for(let j=-1;j<21;j++){let F=fano.map(c=>c.slice());if(j>=0)F[j/3|0][j%3]*=-1;let n=0,first=null;
  for(let w=0;w<128;w++){let x=[0,...Array.from({length:7},(_,i)=>(w>>i)&1)];if(F.every(c=>nae(x,c))){n++;first??=x}}
  modelCounts.push(n);ok(n===(j<0?0:10),"Fano label");if(j===0)fanoNative=native(F,first.slice())
 }
 // Exact equality-chain boundary controls, with matching symmetric-difference
 // path tags represented by the actual local pair edges. Chain uses ports 0,1
 // for adjacent wires where present, remaining ports are distinct terminals.
 const chain=[];
 for(let k=1;k<=8;k++){
  let E0=[],E1=[],boundary=[],labels=new Map(),id=4*k;
  const edge=(L,a,b,tag=0)=>{L.push([a,b]);if(tag)labels.set([Math.min(a,b),Math.max(a,b)].join(),tag)};
  for(let i=0;i<k;i++){edge(E0,4*i,4*i+1,1<<i);edge(E0,4*i+2,4*i+3,1<<i);
   if(i+1<k)edge(E1,4*i+1,4*(i+1));
   for(let j=0;j<4;j++)if(!(j===0&&i>0)&&!(j===1&&i+1<k)){boundary.push(id);edge(E1,4*i+j,id++)}}
  const adj=Array.from({length:id},()=>[]);for(const [a,b] of [...E0,...E1]){adj[a].push(b);adj[b].push(a)}
  let seen=new Set(),pathTags=[];
  for(const a of boundary)if(!seen.has(a)){let u=a,p=-1,mask=0;while(true){seen.add(u);let z=adj[u].find(x=>x!==p);if(z===undefined)break;mask^=labels.get([Math.min(u,z),Math.max(u,z)].join())??0;p=u;u=z}ok(boundary.includes(u)&&u!==a,"path ends");pathTags.push(mask)}
  ok(pathTags.length===k+1,"path count");let kernel=0;for(let w=0;w<(1<<pathTags.length);w++){let m=0;pathTags.forEach((x,i)=>{if(w>>i&1)m^=x});if(m===0)kernel++}ok(kernel===2,"tight equality kernel");chain.push({E4:k,terminals:boundary.length,paths:pathTags.length,kernel});
 }
 return {checks,ext,bucket:bucket.length,tailVolume:bucket.flat().length,rest:rest.length,pivotGates,pivotTriples,allGates:gates.length,allTriples:triples.length,closure:{scans,joins},gateAccepted,fullAccepted,wordVisits,nativeMain,sourceWord:peer.word,modelCounts,fanoNative,chain};
}
console.log(JSON.stringify(run(JSON.parse(fs.readFileSync(process.argv[2],'utf8')),JSON.parse(fs.readFileSync(process.argv[3],'utf8'))),null,2));
