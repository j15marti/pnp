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
 // verify exact local OR and XOR relations independently
 for(let i=0;i<8;i++){let a=i&1,b=(i>>1)&1,c=(i>>2)&1;ck([0,1].some(u=>NAE([a,b,u])&&NAE([1^u,c,0]))===!!(a|b|c));let clauses=[];for(let x=0;x<2;x++)for(let y=0;y<2;y++)clauses.push([a^x,b^y,c^(1^(x^y))]);ck(clauses.every(row=>row.some(Boolean))===(c===(a^b)))}
 let results=[];for(let k of [2,4,6,8,16,32,64,128]){
  let o=make(k), c=compile(o),yes=0,no=0,words=k<=8?2**(k+2):64;
  for(let i=0;i<words;i++){let input=Array.from({length:k+2},(_,j)=>k<=8?(i>>j)&1:((Math.imul(i+123,j+731)>>>((j%13)+1))&1));let want=input[k]!==input[k+1]||input.slice(0,k).reduce((x,y)=>x^y,0)===1;
   let a=solve(o,input);ck(!!a===want);if(a){yes++;let w=lift(c,a);for(let j=0;j<k+2;j++)for(let t=0;t<3;t++)ck(w[c.boundary[j]+t*c.B]===(input[j]^(t===2?1:0)))}else no++;
  }
  let u=Array(k+2).fill(0),v=u.slice();v[0]=1;let ou=make(k,u),ov=make(k,v),cu=compile(ou),cv=compile(ov);ck(cu.B===cv.B);ck(solve(ou,u)===null);let av=solve(ov,v);ck(av!==null);lift(cv,av);
  // Relative pin gadgets force every pin, even with r=1.
  for(let r=0;r<2;r++)for(let l=0;l<2;l++)ck([0,1].some(z=>NAE([l,r,z])&&NAE([l,r,1^z]))===(l!==r));
  results.push({k,variables:3*c.B,owners:4*c.B,boundary:3*(k+2),testedWords:words,yes,no,neighborVariables:3*cu.B,neighborOwners:4*cu.B});
 }
 return {checks,localModels:good,results,scope:"exhaustive diagonal words k<=8; deterministic sampled words above; forward source witness validation; symbolic reverse via module/OR/XOR/pin truth tables, not exhaustive full source or general solver"};
}
console.log(JSON.stringify(audit(),null,2));
