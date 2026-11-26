function audit(){
const assert=(x,msg)=>{if(!x)throw Error(msg);checks++};let checks=0;
const ag=[[[0,1,2],[3,4,5],[6,7,8]],...Array.from({length:3},(_,a)=>Array.from({length:3},(_,b)=>Array.from({length:3},(_,x)=>3*x+(a*x+b)%3)))];
const aux=[[[1,9,11],[0,2,5],[6,7,8],[3,4,10]],[[0,6,10],[3,7,9],[2,8,11],[1,4,5]],[[3,5,11],[0,4,7],[2,6,9],[1,8,10]],[[5,8,9],[4,6,11],[0,1,3],[2,7,10]]];
const lines=ag.flat(), ports=aux[0][0], nae=(s,t)=>s[t[0]]!==s[t[1]]||s[t[0]]!==s[t[2]],bits=(w,n)=>Array.from({length:n},(_,i)=>(w>>i)&1);
const monoMasks=Array.from({length:512},(_,w)=>lines.map((t,i)=>nae(bits(w,9),t)?-1:i).filter(i=>i>=0));
let pairTests=0;assert(Math.min(...monoMasks.map(x=>x.length))===2,"AG minimum mono");
for(let i=0;i<12;i++)for(let j=i+1;j<12;j++){assert(monoMasks.some(x=>x.length===2&&x[0]===i&&x[1]===j),"pair deletion");pairTests++}
const loc=monoMasks.map((x,w)=>({x,w})).filter(({x})=>x.every(i=>i===0||i===1));
for(const {w} of loc){const s=bits(w,9);assert(s[0]===s[1]&&s[1]===s[2]&&s[3]===s[4]&&s[4]===s[5]&&s[0]!==s[3],"exact signed equality")}
assert(loc.length>0,"nonempty");
const B=bits(71,9),A=bits(285,12);
assert(lines.slice(2).every(t=>nae(B,t))&&B[0]===1&&B[3]===0,"base word");
assert(ports.every(v=>!A[v])&&aux.flat().slice(1).every(t=>nae(A,t)),"aux witness");
function make(k,neighbor=false){
 const C=[],core=[],ring=[];const add=(p,v,type,i)=>{const obj={id:C.length,p,v,type,i};C.push(obj);if(type==="internal"||type==="ring")core.push(obj);if(type==="ring")ring.push(obj)};
 for(let i=0;i<k;i++){for(let p=0;p<4;p++)for(let j=0;j<3;j++)if(p||j===2)add(p,ag[p][j].map(x=>9*i+x),"internal",i);
 const next=(i+1)%k;add(0,[9*i,9*next+1,9*next+2],"ring",i);
 for(let h=0;h<2;h++){const off=9*k+12*(2*i+h);for(let p=0;p<4;p++)for(let j=0;j<4;j++)if(p||j)add(p,aux[p][j].map(x=>off+x),"aux",i);}
 for(let j=0;j<3;j++)add(0,[9*i+3+j,9*k+24*i+ports[j],9*k+24*i+12+ports[j]],"neutral",i);
 }
 if(neighbor){const a=ring[0].v,b=ring[1].v;[a[0],b[1]]=[b[1],a[0]];}
 return {n:33*k,C,core,ring,k,neighbor};
}
function validate(F){
 const {n,C}=F,used=new Set(),cnt=Array.from({length:4},()=>new Uint8Array(n));
 for(const {p,v} of C){assert(v.length===3&&new Set(v).size===3&&v.every(x=>x>=0&&x<n),"triple");for(const x of v)cnt[p][x]++;
 for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){const key=Math.min(v[i],v[j])+","+Math.max(v[i],v[j]);assert(!used.has(key),"linear");used.add(key)}}
 assert(cnt.every(a=>a.every(x=>x===1)),"partition");
}
function rank(n,C){const p=Array.from({length:n},(_,i)=>i);function f(x){while(p[x]!==x){p[x]=p[p[x]];x=p[x]}return x}let r=0;for(const {v} of C)for(const y of v.slice(1)){const a=f(v[0]),b=f(y);if(a!==b){p[a]=b;r++}}return r}
function pathColors(k,start,count,val){const a=Array(k).fill(-1);for(let j=0;j<count;j++)a[(start+j)%k]=val^(j&1);return a}
function lift(F,c,special=-1,local=null){
 const {k,n}=F,s=Array(n).fill(-1);
 for(let i=0;i<k;i++){const word=i===special?local:B.map(x=>x^1^c[i]);s.splice(9*i,9,...word);
 for(let h=0;h<2;h++)s.splice(9*k+24*i+12*h,12,...A.map(x=>x^h));}return s
}
function check(F,s,skip=-1){assert(s.length===F.n&&s.every(x=>x===0||x===1),"word");assert(F.C.every(o=>o.id===skip||nae(s,o.v)),"lift");if(skip>=0)assert(!nae(s,F.C[skip].v),"deleted owner must fail");}
function deletion(F,o){
 const k=F.k,i=o.i;if(o.type==="ring")return lift(F,pathColors(k,(i+1)%k,k,0));
 const j=lines.findIndex(t=>t.every((x,a)=>x===o.v[a]-9*i));assert(j>=2,"internal index");const w=monoMasks.findIndex(x=>x.length===2&&x.includes(1)&&x.includes(j));assert(w>=0,"two deletion local");let a=bits(w,9);if(a[0])a=a.map(x=>x^1);return lift(F,pathColors(k,(i+1)%k,k-1,1),i,a)
}
const sizes=[];
for(const k of [3,5,7,17,65]){
 const U=make(k),V=make(k,true);validate(U);validate(V);
 const r=rank(U.n,U.core),full=rank(U.n,U.C);assert(r===9*k-1&&full===33*k-1,"ranks");
 for(const o of U.core)check(U,deletion(U,o),o.id);
 check(V,lift(V,pathColors(k,1,k,0)));
 // On complete core block constraints exact equality forces odd ring; exhaustive color words at small sizes.
 if(k<=7)for(let w=0;w<(1<<k);w++)assert(!U.ring.every(o=>((w>>o.i)&1)!==((w>>((o.i+1)%k))&1)),"odd ring");
 sizes.push({k,variables:U.n,owners:U.C.length,uniqueMUS:U.core.length,coreRank:r,coreDeficiency:U.core.length-r,fullRank:full,deletionWitnesses:U.core.length,neighbor:"SAT"});
}
for(const k of [4,8,64]){const F=make(k);validate(F);check(F,lift(F,pathColors(k,0,k,0)))}
const kg=[[[0,1],[2,3]],[[0,2],[1,4]],[[0,3],[2,4]],[[0,4],[1,3]],[[1,2],[3,4]]];
const vec=(e)=>e.reduce((a,v)=>a^(v===4?0:1<<v),0);
function br(vs){let b=new Map();for(let v of vs){while(v){const i=31-Math.clz32(v);if(b.has(i))v^=b.get(i);else{b.set(i,v);break}}}return b.size}
const gr=kg.map(g=>g.map(vec)),comp=new Set(gr.flatMap(([a,b])=>[a,b,a^b]));assert(comp.size===15&&Array.from({length:15},(_,i)=>i+1).every(x=>comp.has(x)),"PG(3,2)");
const model=(w,flip)=>kg.every((g,i)=>g.some(([a,b],j)=>(((w>>a)^(w>>b))&1)===(2*i+j===flip?0:1)));
assert(!Array.from({length:32},(_,w)=>w).some(w=>model(w,-1)),"K5 no");
for(let f=0;f<10;f++)assert(Array.from({length:32},(_,w)=>w).some(w=>model(w,f)),"K5 neighbor");
for(let m=1;m<32;m++){const S=gr.filter((_,i)=>m>>i&1).flat();assert(br(S)>=Math.min(m.toString(2).replace(/0/g,"").length,4),"K5 strict")}
const cyc=[vec([2,3]),vec([1,4]),vec([2,4]),vec([1,3])];assert(br(cyc)===3&&br([...cyc,...gr[4]])===3,"balanced nonextendible");
let childChecks=0;
for(const w of gr[0])for(let mask=1;mask<16;mask++){const s=gr.slice(1).filter((_,i)=>mask>>i&1).flat(),n=mask.toString(2).replace(/0/g,"").length;assert(br([w,...s])-1>=Math.min(n,3),"K5 children");childChecks++}
for(let m=3;m<=11;m++){const es=Array.from({length:m},(_,i)=>i<m-1?1<<i:(1<<(m-1))-1);const groups=es.map((e,i)=>[e,es[(i+1)%m]]);
 for(const w of groups[0])for(let mask=1;mask<1<<(m-1);mask++){const s=groups.slice(1).filter((_,i)=>mask>>i&1).flat(),n=mask.toString(2).replace(/0/g,"").length;assert(br([w,...s])-1>=Math.min(n,m-2),"cycle children");childChecks++}}
return {checks,pairDeletionCases:pairTests,localModelCount:loc.length,coreDeletionWitnesses:sizes.reduce((a,b)=>a+b.deletionWitnesses,0),sizes,evenSizes:[4,8,64],K5signNeighbors:10,childChecks,limits:"Full-source NO and unique-MUS conclusions rely on symbolic odd-ring proof and all single-deletion lifts. No general closure solver, matroid intersection, full source search, or general critical classifier executed."};
}
console.log(JSON.stringify(audit(),null,2));
