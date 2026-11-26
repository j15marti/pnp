// N4ES09 generator/reference from pinned peer audit research/proof-spine-portfolio-2026-11-25/nae4/closure-exceptional-syndrome/2026-11-25_2335_N4ES09/audit.js; new source-only solver below.
function audit(){
 let checks=0; const ck=(b)=>{if(!b)throw Error("assert "+checks);checks++};
 const NAE=a=>a.some(x=>x!==a[0]);
 const local=[[[6,7,8]],[[0,3,6],[1,4,7],[2,5,8]],[[0,4,8],[1,5,6],[2,3,7]],[[0,5,7],[1,3,8],[2,4,6]]];
 let good=0;for(let i=0;i<512;i++){let a=Array.from({length:9},(_,j)=>(i>>j)&1);let ok=local.flat().every(c=>NAE(c.map(v=>a[v])));ck(ok===(a.slice(0,3).every(x=>x===a[0])&&a.slice(3,6).every(x=>x===1-a[0])&&NAE(a.slice(6))));good+=ok}
 const lit=(v,s=0)=>[v,s],ev=(l,a)=>a[l[0]]^l[1];
 // exact CNF3 XOR gates, and relative NAE3 translation
 function make(k,pins=null){
  let n=k+2, g=k,h=k+1,cnf=[],gates=[],last=0;
  for(let i=1;i<k;i++){let p=n++;gates.push([last,i,p]);for(let a=0;a<2;a++)for(let b=0;b<2;b++)cnf.push([lit(last,a),lit(i,b),lit(p,1^(a^b))]);last=p}
  cnf.push([lit(g),lit(h),lit(last)],[lit(g,1),lit(h,1),lit(last)]);
  let r=n++,f=[];for(const [a,b,c] of cnf){let u=n++;f.push([a,b,lit(u)],[lit(u,1),c,lit(r)])}
  if(pins)for(let v=0;v<k+2;v++){let u=n++,l=lit(v,1^pins[v]);f.push([l,lit(r),lit(u)],[l,lit(r),lit(u,1)])}
  return {n,f,cnf,gates,r,g,h,last,k,pins};
 }
 function compile(obj){
  const {n,f,k}=obj;let occ=Array.from({length:n},()=>[]);f.forEach((c,i)=>c.forEach((l,j)=>occ[l[0]].push([i,j,l[1]])));
  let p=[[],[],[],[]],phase=[],assigned=f.map(()=>[]),boundary=[],used=new Set();
  function add(c){for(let x of c){ck(!used.has(x));used.add(x)}p[0].push(c)}
  for(let v=0;v<n;v++){let d=occ[v].length+(v<k+2?1:0), ids=[];for(let i=0;i<Math.max(1,d);i++){let b=9*phase.length;ids.push(b);phase.push(v);local.forEach((part,j)=>part.forEach(c=>{let row=c.map(x=>x+b);if(j===0)add(row);else p[j].push(row)}))}
   for(let i=0;i+1<ids.length;i++)add([ids[i],ids[i]+1,ids[i+1]+3]);
   occ[v].forEach(([i,j,s],z)=>assigned[i][j]=ids[z]+(s?4:2));if(v<k+2)boundary.push(ids[occ[v].length]+2);
  }
  assigned.forEach(add);const B=9*phase.length, q=p.map(part=>[0,1,2].flatMap(t=>part.map(c=>c.map(x=>x+t*B))));let omit=new Set(boundary),region=q.map(a=>a.slice());for(let i=0;i<B;i++)if(!used.has(i)){let c=[i,i+B,i+2*B];q[0].push(c);if(!omit.has(i))region[0].push(c)}
  let pairs=new Set();for(const part of q){let seen=new Set();for(const c of part){ck(c.length===3&&new Set(c).size===3);for(let x of c){ck(x>=0&&x<3*B&&!seen.has(x));seen.add(x)}for(let a=0;a<3;a++)for(let b=a+1;b<3;b++){let key=[c[a],c[b]].sort((a,b)=>a-b).join(":");ck(!pairs.has(key));pairs.add(key)}}ck(seen.size===3*B)}
  let outside=new Set(q[0].slice(q[0].length-(B-used.size)).flat());let actual=new Set(q[0].filter(c=>c[0]<B&&omit.has(c[0])&&c[1]===c[0]+B&&c[2]===c[0]+2*B).flat());let expected=[0,1,2].flatMap(t=>boundary.map(x=>x+t*B));ck(actual.size===expected.length&&expected.every(x=>actual.has(x)));
  return {q,region,B,phase,boundary};
 }
 function solve(obj,input){
  let a=Array(obj.n).fill(0);input.forEach((v,i)=>a[i]=v);for(let [u,v,p] of obj.gates)a[p]=a[u]^a[v];let ok=obj.cnf.every(c=>c.some(l=>ev(l,a)));if(obj.pins)ok=ok&&obj.pins.every((v,i)=>v===a[i]);
  if(!ok)return null;
  let start=obj.r+1;for(let i=0;i<obj.cnf.length;i++){let [u,v,w]=obj.cnf[i].map(l=>ev(l,a));let choices=[0,1].filter(t=>NAE([u,v,t])&&NAE([1^t,w,0]));ck(choices.length>0);a[start+i]=choices[0]}
  ck(obj.f.every(c=>NAE(c.map(l=>ev(l,a)))));return a;
 }
 function lift(c,a){let w=[];for(let t=0;t<3;t++)for(let v of c.phase){let z=a[v]^(t===2?1:0);w.push(z,z,z,1^z,1^z,1^z,0,0,1)}ck(w.length===3*c.B);for(let row of c.q.flat())ck(NAE(row.map(x=>w[x])));return w}

// Source-only solver: no compiler labels, apart from explicit input boundary guard.
function raw(F,n,guard=[],maxRefs=3,full=false){
 const C=F.flat(),inc=Array.from({length:n},()=>[]);C.forEach((c,i)=>c.forEach(v=>inc[v].push(i)));
 let ps=new Set;for(let p of F){let seen=new Set;for(let c of p){ck(c.length===3&&new Set(c).size===3);for(let v of c){ck(v>=0&&v<n&&!seen.has(v));seen.add(v)}for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){let s=[c[i],c[j]].sort((a,b)=>a-b).join(",");ck(!ps.has(s));ps.add(s)}}ck(seen.size===n)}
 let par=Array.from({length:n+1},(_,i)=>i),ds=Array(n+1).fill(0),sz=Array(n+1).fill(1);
 function find(v){if(par[v]===v)return [v,0];let [r,s]=find(par[v]);ds[v]^=s;par[v]=r;return [r,ds[v]]}
 function join(a,b,d){let [u,s]=find(a),[v,t]=find(b);if(u===v)return (s^t)===d?0:-1;if(sz[u]<sz[v])[u,v]=[v,u];par[v]=u;ds[v]=s^t^d;sz[u]+=sz[v];return 1}
 for(let [v,d] of guard)if(join(v,n,d)<0)return {answer:false,stage:"guard"};
 let motifs=0,seen=new Set,paired=0,merges=0,scans=0,branches=0;
 for(let v=0;v<n;v++){
  let S=[...new Set(inc[v].flatMap(i=>C[i]))].sort((a,b)=>a-b),key=S.join(",");if(seen.has(key)||S.length!==9)continue;seen.add(key);
  let set=new Set(S),rows=[...new Set(S.flatMap(w=>inc[w]))].filter(i=>C[i].every(w=>set.has(w)));
  if(rows.length>=11)return {answer:false,stage:"dense9"};if(rows.length!==10)continue;
  let edges=new Set;for(let i of rows)for(let a=0;a<3;a++)for(let b=a+1;b<3;b++){let [u,w]=[C[i][a],C[i][b]].sort((a,b)=>a-b);edges.add(u+","+w)}
  let miss=S.map((u,i)=>S.filter((w,j)=>i!==j&&!edges.has([u,w].sort((a,b)=>a-b).join(","))));
  let a=miss.findIndex(x=>x.length===2);if(a<0)continue;let A=[S[a],...miss[a]],B=S.filter((v,i)=>miss[i].length===2&&!A.includes(v));
  let tri=L=>L.length===3&&L.every(v=>miss[S.indexOf(v)].length===2&&L.every(w=>w===v||miss[S.indexOf(v)].includes(w)));
  if(!tri(A)||!tri(B)||miss.some((q,i)=>q.length&&!A.includes(S[i])&&!B.includes(S[i])))continue;
  motifs++;for(let w of A)if(join(A[0],w,0)<0)return {answer:false,stage:"module"};for(let w of B)if(join(A[0],w,1)<0)return {answer:false,stage:"module"};
 }
 let norm=q=>{q=q.slice().sort((a,b)=>a-b);return q[0]&1?q.map(l=>l^1).sort((a,b)=>a-b):q};
 function fixed(){
  for(;;){scans++;let map=new Map,progress=0;
   for(let c of C){let q=c.map(v=>{let [r,d]=find(v);return 2*r+d}).sort((a,b)=>a-b);if(q.some((l,i)=>i&&l===(q[i-1]^1)))continue;
    q=[...new Set(q)];if(q.length===1)return null;
    if(q.length===2){let z=join(q[0]>>1,q[1]>>1,1^(q[0]&1)^(q[1]&1));if(z<0)return null;merges+=z;progress+=z;continue}
    q=norm(q);map.set(q.join(","),q)
   }
   if(progress)continue;
   for(let q of map.values())for(let i=0;i<3;i++){let a=q.slice();a[i]^=1;if(map.has(norm(a).join(","))){let b=q.filter((_,j)=>j!==i),z=join(b[0]>>1,b[1]>>1,1^(b[0]&1)^(b[1]&1));if(z<0)return null;paired+=z;progress+=z}}
   if(!progress)return [...map.values()]
  }
 }
 function finish(R){
  if(!R)return {answer:false,stage:"phase"};
  let [anchor,aval]=find(n),adj=new Map,by=new Map;
  for(let c of R){let V=c.map(l=>l>>1).filter(v=>v!==anchor);if(!V.length)return {answer:false,stage:"fixed"};for(let v of V){if(!adj.has(v)){adj.set(v,new Set);by.set(v,[])}by.get(v).push(c);for(let w of V)adj.get(v).add(w)}}
  let vis=new Set,vals=new Map([[anchor,aval]]),maxComponent=0;
  for(let v of adj.keys())if(!vis.has(v)){let q=[v];vis.add(v);for(let i=0;i<q.length;i++)for(let w of adj.get(q[i]))if(!vis.has(w)){vis.add(w);q.push(w)}
   maxComponent=Math.max(maxComponent,q.length);if(q.length>3)return {answer:null,stage:"large-component",maxComponent};
   let rr=[...new Set(q.flatMap(w=>by.get(w)))],success=false;
   for(let mask=0;mask<(1<<q.length);mask++){q.forEach((w,i)=>vals.set(w,(mask>>i)&1));if(rr.every(c=>NAE(c.map(l=>vals.get(l>>1)^(l&1))))){success=true;break}}
   if(!success)return {answer:false,stage:"component",maxComponent};
  }
  let w=Array.from({length:n},(_,v)=>{let [r,d]=find(v);return (vals.get(r)||0)^d});ck(C.every(c=>NAE(c.map(v=>w[v]))));ck(guard.every(([v,d])=>w[v]===d));return {answer:true,stage:"verified",maxComponent}
 }
 let R=fixed(),ans=finish(R);if(ans.answer!==null)return {...ans,motifs,paired,merges,scans,branches};
 let [anchor]=find(n),degree=new Map;for(let c of R)for(let l of c){let v=l>>1;if(v!==anchor)degree.set(v,(degree.get(v)||0)+1)}
 let roots=[...degree.keys()].sort((a,b)=>degree.get(b)-degree.get(a)||a-b),limit=Math.min(maxRefs,roots.length);
 let base=[par.slice(),ds.slice(),sz.slice()];
 function tryTuple(T){let unknown=false;for(let mask=0;mask<(1<<T.length);mask++){[par,ds,sz]=base.map(a=>a.slice());branches++;let good=true;for(let i=0;i<T.length;i++)if(join(T[i],n,(mask>>i)&1)<0){good=false;break}
   let r=good?finish(fixed()):{answer:false,stage:"guard"};if(r.answer===true)return r;if(r.answer===null)unknown=true}
  return {answer:unknown?null:false,stage:unknown?"reference-stall":"all-reference-branches-NO"}}
 if(limit){ans=tryTuple(roots.slice(0,limit));if(ans.answer!==null)return {...ans,motifs,paired,merges,scans,branches};
 if(full){let stop=false;function comb(start,a){if(a.length===limit){let b=tryTuple(a);if(b.answer!==null){ans=b;stop=true}return}for(let i=start;i<=roots.length-(limit-a.length)&&!stop;i++)comb(i+1,[...a,roots[i]])}comb(0,[])}}
 return {...ans,motifs,paired,merges,scans,branches};
}
let seed=20261126;
function perm(n){let a=Array.from({length:n},(_,i)=>i);for(let i=n-1;i>0;i--){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;let j=(seed>>>0)%(i+1);[a[i],a[j]]=[a[j],a[i]]}return a}
function shuffle(F,n,guard=[]){let a=perm(n);return {F:perm(4).map(j=>perm(F[j].length).map(i=>F[j][i].map(v=>a[v]))),guard:guard.map(([v,d])=>[a[v],d])}}
let results=[];
for(let k of [2,4,8,16,32]){
 for(let v of [0,1]){let pins=Array(k+2).fill(0);pins[0]=v;let o=make(k,pins),c=compile(o),n=3*c.B;let w=solve(o,pins);ck(!!w===!!v);if(w)lift(c,w);let s=shuffle(c.q,n);let res=raw(s.F,n,[],0);ck(res.answer===!!v);results.push({kind:"full-neighbor",k,expected:!!v,n,...res})}
 let o=make(k),c=compile(o),n=3*c.B;
 for(let type of [0,1,2,3]){let input=Array(k+2).fill(0);if(type===1)input[0]=1;if(type===2)input[k]=1;if(type===3)input[k]=input[k+1]=1;
  let want=input[k]!==input[k+1]||input.slice(0,k).reduce((a,b)=>a^b,0)===1;let w=solve(o,input);ck(!!w===want);if(w)lift(c,w);
  let guard=[0,1,2].flatMap(t=>c.boundary.map((v,i)=>[v+t*c.B,input[i]^(t===2?1:0)]));let s=shuffle(c.q,n,guard),res=raw(s.F,n,s.guard,3,false);ck(res.answer===null||res.answer===want);results.push({kind:"diagonal-guard",type,k,expected:want,n,...res});
 }
}
return {checks,seed:20261126,results};
}
console.log(JSON.stringify(audit(),null,2));