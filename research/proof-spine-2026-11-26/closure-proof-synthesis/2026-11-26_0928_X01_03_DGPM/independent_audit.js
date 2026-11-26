console.log(JSON.stringify((function audit(){
const B2=[[1,1],[1,1]],B3=[[1,1,0],[1,0,1],[1,1,1]],P=[[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]];
let checks=0;const ok=(x)=>{if(!x)throw Error("assertion "+checks);checks++};
const S=A=>P.map(p=>p.slice(0,A.length)).filter(p=>p.every((j,i)=>j<A.length&&A[i][j])).map(p=>p.map((j,i)=>3*i+j)).filter((p,i,a)=>a.findIndex(q=>q.join()==p.join())===i);
const S2=S(B2),S3=S(B3);ok(S2.length===2&&S3.length===3);
const port=[0,3,6];ok(new Set(S3.map(s=>port.map(e=>+s.includes(e)).join())).size===3);
const bit=(M,e)=>+M[e[0]].includes(e[1]), key=e=>e.join(), lit=(l,x)=>x[Math.abs(l)-1]^(l<0),hot=j=>S3.find(s=>s.includes(port[j]));
function compile(F){
 const A=[],G=[],O=Array.from({length:3},()=>[]),V=[],C=[],used=new Set();
 const add=b=>{A.push(b);return A.length-1},link=(a,b)=>{ok(!used.has(key(a))&&!used.has(key(b))&&a[0]!==b[0]);used.add(key(a));used.add(key(b));G.push([a,b])};
 F.forEach((c,i)=>c.forEach((l,j)=>O[Math.abs(l)-1].push([i,j,l])));
 const Q={};
 O.forEach((o,v)=>{const ks=o.map(()=>add(B2));V.push(ks);for(let i=0;i+1<ks.length;i++){const e=i%2?1:0;link([ks[i],e],[ks[i+1],e])}o.forEach(([i,j,l],t)=>{const e=(l>0?[1,3]:[0,4]).find(e=>!used.has(key([ks[t],e])));ok(e!==undefined);Q[i+","+j]=[ks[t],e]})});
 F.forEach((c,i)=>{const s=add(B3),I=c.map(()=>add(B3));C.push([s,I]);I.forEach((k,j)=>{link([s,port[j]],[k,0]);link([k,3],Q[i+","+j])})});
 ok(A.length===7*F.length&&G.length===9*F.length-O.filter(o=>o.length).length);return {A,G,V,C};
}
function solve(D,pins){
 const ds=D.A.map(a=>S(a));D.V.forEach((ks,v)=>ks.forEach(k=>{ds[k]=ds[k].filter(s=>+s.includes(0)===pins[v])}));
 function close(d){while(true){let changed=false;for(const [a,b] of D.G){const p=d[a[0]],q=d[b[0]],p1=p.filter(s=>q.some(t=>s.includes(a[1])===t.includes(b[1]))),q1=q.filter(s=>p1.some(t=>s.includes(b[1])===t.includes(a[1])));if(!p1.length||!q1.length)return false;changed||=p1.length!==p.length||q1.length!==q.length;d[a[0]]=p1;d[b[0]]=q1}if(!changed)return true}}
 function go(d){if(!close(d))return false;const i=d.findIndex(s=>s.length>1);if(i<0)return true;return d[i].some(s=>{const q=d.slice();q[i]=[s];return go(q)})}return go(ds)
}
function lift(F,D,x){const M=[];D.V.forEach((ks,v)=>ks.forEach(k=>M[k]=S2.find(s=>+s.includes(0)===x[v])));F.forEach((c,i)=>{const l=c.map(t=>lit(t,x)),j=l.findIndex(Boolean)<0?0:l.findIndex(Boolean),[s,I]=D.C[i];M[s]=hot(j);I.forEach((k,t)=>M[k]=hot(t===j?0:l[t]===0?1:2))});return M}
function quotient(D,M,F,x){const E=D.A.flatMap((a,k)=>a.flatMap((r,i)=>r.flatMap((b,j)=>b?[[k,3*i+j]]:[]))),used=new Set(D.G.flat().map(key)),pairs=D.G.concat(E.filter(e=>!used.has(key(e))).map(e=>[e])),cb=new Map();D.C.forEach(([s,I],i)=>[s,...I].forEach(k=>cb.set(k,i)));const occ=new Map();
pairs.forEach(p=>{const val=bit(M,p.find(e=>!cb.has(e[0]))||p[0]),vs=[];p.forEach(([k,e])=>vs.push(k+",L,"+Math.floor(e/3),k+",R,"+(e%3)));ok(new Set(vs).size===vs.length);vs.forEach(v=>occ.set(v,[...(occ.get(v)||[]),val]))});
for(const [v,z] of occ){ok(z.length<=3);const i=cb.get(+v.split(",")[0]);if(i===undefined||F[i].some(l=>lit(l,x)))ok(z.reduce((a,b)=>a+b,0)===1)}
}
const all=Array.from({length:8},(_,i)=>[1,2,3].map((v,j)=>i>>j&1?v:-v));let formulas=0,assignmentChecks=0,unsat=0;
for(let mask=1;mask<256;mask++){
 const F=all.filter((_,i)=>mask>>i&1),D=compile(F);let sat=false;formulas++;
 for(let a=0;a<8;a++){const x=[a&1,(a>>1)&1,(a>>2)&1],yes=F.every(c=>c.some(l=>lit(l,x))),M=lift(F,D,x);sat||=yes;ok(D.G.every(([e,f])=>bit(M,e)===bit(M,f))===yes);ok(solve(D,x)===yes);quotient(D,M,F,x);assignmentChecks++}
 if(!sat)unsat++;
}
return {checks,formulas,assignmentChecks,unsat};
})(), null, 2));
