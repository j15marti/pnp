'use strict';
// node 2026-11-25_0026_BA18.js DR18_M24_reclosed.json > results.json
function run(input) {
 const C={scoreTests:0,scoreRows:0,scoreTerms:0,dpTransitions:0,closureScans:0,semijoinRows:0,affineRows:0,xors:0,assertions:0};
 const ok=(b,m)=>{C.assertions++;if(!b)throw Error(m)};
 const key=(i,j)=>`${Math.min(i,j)},${Math.max(i,j)}`;
 const sums=(n)=>Array.from({length:n+1},(_,i)=>((n-2*i)**2-n)/2);
 const valid=(ts,x,g)=>g.every(([i,b])=>x[i]===b)&&ts.every(t=>t.a.includes(t.v.map(i=>x[i]).join("")));
 function bitBasis(rows,n){let B=Array(n).fill(0n);for(let a of rows){for(let i=n-1;i>=0;i--)if((a>>BigInt(i))&1n){if(B[i]){a^=B[i];C.xors++}else{B[i]=a;break}}}return B}
 function add(B,a,n){for(let i=n-1;i>=0;i--)if((a>>BigInt(i))&1n){if(B[i]){a^=B[i];C.xors++}else{B[i]=a;return true}}return a===0n}
 function closure(ts,g,n){let total=0;for(;;){C.closureScans++;let before=ts.reduce((s,t)=>s+t.a.length,0);
  for(let t of ts)t.a=t.a.filter(a=>g.every(([i,b])=>!t.v.includes(i)||+a[t.v.indexOf(i)]===b));
  if(ts.some(t=>!t.a.length))return {unsat:true,total};
  for(let i=0;i<ts.length;i++)for(let j=i+1;j<ts.length;j++){let a=ts[i],b=ts[j],u=a.v.filter(v=>b.v.includes(v));if(!u.length)continue;let ai=u.map(v=>a.v.indexOf(v)),bi=u.map(v=>b.v.indexOf(v));let sig=(w,p)=>p.map(k=>w[k]).join("");let A=new Set(a.a.map(w=>sig(w,ai))),B=new Set(b.a.map(w=>sig(w,bi)));C.semijoinRows+=2*(a.a.length+b.a.length);a.a=a.a.filter(w=>B.has(sig(w,ai)));b.a=b.a.filter(w=>A.has(sig(w,bi)))}
  if(ts.some(t=>!t.a.length))return {unsat:true,total};
  let E=Array(n+1).fill(0n), rhs=1n;
  // Use bit 0 as constant; variable v uses bit v+1.
  for(let [v,b] of g)if(!add(E,(1n<<BigInt(v+1))|BigInt(b),n+1)||E[0])return {unsat:true,total};
  for(let t of ts){let k=t.v.length, enc=w=>Array.from(w).reduce((s,b,i)=>s|(BigInt(b)<<BigInt(i)),0n), r=enc(t.a[0]), B=bitBasis(t.a.map(w=>enc(w)^r),k);for(let f=0;f<k;f++)if(!B[f]){
   let h=1n<<BigInt(f);for(let i=0;i<k;i++)if(B[i]){let z=B[i]&h,p=0n;while(z){z&=z-1n;p^=1n}if(p)h|=1n<<BigInt(i)}
   let eq=0n,z=h&r,p=0n;while(z){z&=z-1n;p^=1n}eq=p;for(let i=0;i<k;i++)if((h>>BigInt(i))&1n)eq|=1n<<BigInt(t.v[i]+1);
   add(E,eq,n+1);if(E[0])return {unsat:true,total};
  }}
  for(let t of ts)t.a=t.a.filter(w=>{C.affineRows++;let B=E.slice();for(let i=0;i<t.v.length;i++){add(B,(1n<<BigInt(t.v[i]+1))|BigInt(w[i]),n+1);if(B[0])return false}return true});
  let after=ts.reduce((s,t)=>s+t.a.length,0);total+=before-after;if(ts.some(t=>!t.a.length))return {unsat:true,total};if(before===after)return {unsat:false,total};
 }}
 function candidates(ts){let active=[...new Set(ts.flatMap(t=>t.v))].sort((a,b)=>a-b), M=new Map();let put=(s)=>{s=[...new Set(s)].sort((a,b)=>a-b);if(s.length>=3)M.set(s.join(","),s)};
  put(active);for(let t of ts)put(t.v);for(let i=0;i<ts.length;i++)for(let j=i+1;j<ts.length;j++)if(ts[i].v.some(v=>ts[j].v.includes(v)))put([...ts[i].v,...ts[j].v]);
  let out=[];for(let s of M.values()){out.push({s,flip:-1});if(s.length<=8||s.length===active.length)for(let v of s)out.push({s,flip:v})}return out;
 }
 function probe(ts,can,exact){
  C.scoreTests++;let {s,flip}=can, sg=v=>v===flip?-1:1, S=new Set(s), owners=new Map();
  // Canonical pair allocation: shortest row list, then earliest owner.
  for(let i=0;i<ts.length;i++){let t=ts[i];for(let a=0;a<t.v.length;a++)if(S.has(t.v[a]))for(let b=a+1;b<t.v.length;b++)if(S.has(t.v[b])){let k=key(t.v[a],t.v[b]);let old=owners.get(k);if(!old||t.a.length<ts[old.i].a.length)owners.set(k,{i,a,b,sign:sg(t.v[a])*sg(t.v[b])})}}
  let terms=ts.map(()=>[]);for(let z of owners.values())terms[z.i].push(z);let q=s.length*(s.length-1)/2-owners.size;
  let groups=[];for(let i=0;i<ts.length;i++)if(terms[i].length){let scores=ts[i].a.map(w=>{C.scoreRows++;let v=0;for(let t of terms[i]){C.scoreTerms++;v+=t.sign*(w[t.a]===w[t.b]?1:-1)}return v});groups.push({i,scores,vals:[...new Set(scores)]})}
  let max=q+groups.reduce((a,z)=>a+Math.max(...z.vals),0), minTarget=-Math.floor(s.length/2);
  if(max<minTarget)return {unsat:true,can,max,minTarget,q};
  if(!exact){let cuts=[];for(let z of groups){let m=Math.max(...z.vals), bad=z.scores.map((v,j)=>max-m+v<minTarget?j:-1).filter(j=>j>=0);if(bad.length)cuts.push({i:z.i,bad})}return {cuts,can,max,minTarget,q}}
  groups.push({i:-1,vals:Array.from({length:q+1},(_,i)=>2*i-q)});
  let F=[new Set([0])];for(let z of groups){let next=new Set();for(let a of F[F.length-1])for(let b of z.vals){C.dpTransitions++;next.add(a+b)}F.push(next)}
  let target=new Set(sums(s.length)), good=new Set([...F.at(-1)].filter(a=>target.has(a)));if(!good.size)return {unsat:true,can,max,minTarget,q};
  let cuts=[];for(let i=groups.length-1;i>=0;i--){let z=groups[i], prev=new Set(), allowed=new Set();for(let a of F[i])for(let b of z.vals){C.dpTransitions++;if(good.has(a+b)){prev.add(a);allowed.add(b)}}good=prev;if(z.i>=0){let bad=z.scores.map((v,j)=>allowed.has(v)?-1:j).filter(j=>j>=0);if(bad.length)cuts.push({i:z.i,bad})}}
  return {cuts,can,max,minTarget,q}
 }
 function solve(job,mode){let ts=JSON.parse(JSON.stringify(job.finalTables)),n=job.witness?.length||job.n,g=job.guard||[], start=ts.reduce((s,t)=>s+t.a.length,0), hist=[], witness=job.witness;
  let first=closure(ts,g,n),unsat=first.unsat, init=first.total, rounds=0;
  while(!unsat){rounds++;let changed=false;for(let can of candidates(ts)){let r=probe(ts,can,mode==="dp");if(r.unsat){hist.push({kind:"contradiction",...r});unsat=true;break}
   if(r.cuts.length){let events=[];for(let cut of r.cuts){let t=ts[cut.i],bad=new Set(cut.bad),removed=t.a.filter((w,i)=>bad.has(i));events.push({id:t.id,v:t.v,removed});t.a=t.a.filter((w,i)=>!bad.has(i))}
    let cl=closure(ts,g,n);hist.push({kind:"deletion",can:r.can,max:r.max,minTarget:r.minTarget,q:r.q,events,closure:cl.total});unsat=cl.unsat;changed=true;break}
  }if(!changed)break;}
  if(witness){ok(!unsat,"false UNSAT "+job.id);ok(valid(ts,witness,g),"lost supplied witness "+job.id)}
  return {id:job.id,guard:g,mode,start,initialClosure:init,final:ts.reduce((s,t)=>s+t.a.length,0),unsat,rounds,hist,finalTables:ts};
 }
 function nae(v,mask,id){let a=[];for(let w=0;w<8;w++)if(w!==mask&&w!==(mask^7))a.push(v.map((_,j)=>String((w>>j)&1)).join(""));return {id,v,a}}
 function brute(ts,n,g=[]){let sol=[];for(let a=0;a<2**n;a++){let x=Array.from({length:n},(_,i)=>(a>>i)&1);if(valid(ts,x,g))sol.push(x.join(""))}return sol}
 let jobs=input.results.filter((z,i)=>i%3===0), out=[];
 for(let j of jobs){for(let m of ["bound","dp"])out.push(solve(j,m))}
 let f=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]], plane=[];for(let a=0;a<3;a++)plane.push([3*a,3*a+1,3*a+2]);for(let b=0;b<3;b++)for(let a=0;a<3;a++)plane.push([a,3+(a+b)%3,6+(a+2*b)%3]);
 // 3 horizontal and 9 nonhorizontal lines over F3.
 let controls=[{id:"Fano",n:7,finalTables:f.map((v,i)=>nae(v,0,i))},{id:"M22",n:9,finalTables:plane.map((v,i)=>nae(v,0,i))}];
 for(let i=0;i<7;i++)for(let b=0;b<3;b++)controls.push({id:`Fano-sign-${i}-${b}`,n:7,finalTables:f.map((v,j)=>nae(v,i===j?1<<b:0,j))});
 for(let i=0;i<7;i++)controls.push({id:`Fano-delete-${i}`,n:7,finalTables:f.map((v,j)=>nae(v,0,j)).filter(t=>t.id!==i)});
 for(let i=0;i<12;i++)controls.push({id:`M22-delete-${i}`,n:9,finalTables:plane.map((v,j)=>nae(v,0,j)).filter(t=>t.id!==i)});
 let ctr=[];for(let j of controls){let ref=brute(j.finalTables,j.n);for(let m of ["bound","dp"]){let r=solve(j,m);ok(!r.unsat||ref.length===0,"false UNSAT control");let after=brute(r.finalTables,j.n);if(!r.unsat)ok(JSON.stringify(after)===JSON.stringify(ref),"support changed "+j.id);ctr.push({id:j.id,mode:m,models:ref.length,unsat:r.unsat,start:r.start,final:r.final,hist:r.hist})}}
 return {source:"9ac7e9d745b7220f0634990bd08d919313471f82",counts:C,shared:out,controls:ctr};
}
console.log(JSON.stringify(run(JSON.parse(require('fs').readFileSync(process.argv[2],'utf8'))),null,2));
