/* DS17 reproducible checker. node checker.js DR17.json M23.json BW17.json */
const fs=require('fs');
function run(data){
let assertions=0;function ck(x){assertions++;if(!x)throw Error("assertion "+assertions)}
const nae=(t,w)=>w[t[0]]!==w[t[1]]||w[t[1]]!==w[t[2]];
const good=(O,w)=>O.every(t=>nae(t,w));
function direct(n,O,pin=-1,combined=false,anchor=null){
 const s={nodes:0,scans:0,forces:0,joins:0,greedyTests:0,cutTests:0,greedyTrials:0};let init=Array(n).fill(-1);if(pin>=0)init[0]=pin;
 function close(w){let again=true;while(again){again=false;for(const t of O){s.scans++;let u=t.filter(i=>w[i]<0),v=t.filter(i=>w[i]>=0).map(i=>w[i]);if(v.includes(0)&&v.includes(1))continue;if(!u.length)return false;if(u.length===1){w[u[0]]=1-v[0];s.forces++;again=true}}}return true}
 function dfs(w){if(++s.nodes>4*n*n)return {status:"UNKNOWN"};if(!close(w))return{status:"UNSAT"};if(good(O,w)&&w.every(v=>v>=0))return{status:"SAT",word:w};let i=w.indexOf(-1);if(i<0)return{status:"UNSAT"};for(let b of [0,1]){let a=w.slice();a[i]=b;let r=dfs(a);if(r.status!=="UNSAT")return r}return{status:"UNSAT"}}
 if(!close(init))return {status:"UNSAT",s,stage:"closure"};
 if(combined){
  let seen=new Set(),linear=true;for(const t of O)for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){s.cutTests++;let key=[t[i],t[j]].sort((a,b)=>a-b).join(",");if(seen.has(key))linear=false;seen.add(key)}
  if(linear&&2*O.length>Math.floor(n*n/4))return{status:"UNSAT",s,stage:"cut"};
  for(let trial=0;trial<16;trial++){s.greedyTrials++;let c=Array.from({length:n},(_,i)=>i),p=Array(n).fill(0);let bad=false;
   function join(a,b,q){s.greedyTests++;if(c[a]===c[b])return (p[a]^p[b])===q;let old=c[b],target=c[a],flip=p[a]^p[b]^q;for(let i=0;i<n;i++)if(c[i]===old){c[i]=target;p[i]^=flip}s.joins++;return true}
   function pc(){let changed=true;while(changed){changed=false;for(let t of O){s.greedyTests++;let sat=false;for(let i=0;i<3;i++)for(let j=i+1;j<3;j++)if(c[t[i]]===c[t[j]]&&p[t[i]]!==p[t[j]])sat=true;if(sat)continue;for(let i=0;i<3;i++){let a=t[i],b=t[(i+1)%3],d=t[(i+2)%3];if(c[a]===c[b]&&p[a]===p[b]){let old=s.joins;if(!join(a,d,1))return false;if(s.joins>old)changed=true}}}}return true}
   for(let j=0;j<O.length;j++){let t=O[(trial%2?O.length-1-j:j)+trial*7>=0?((trial%2?O.length-1-j:j)+trial*7)%O.length:0];let pairs=[[t[0],t[1]],[t[0],t[2]],[t[1],t[2]]];if(pairs.some(([a,b])=>c[a]===c[b]&&p[a]!==p[b]))continue;pairs=pairs.slice(trial%3).concat(pairs.slice(0,trial%3));if(anchor&&trial<8)pairs.sort((u,v)=>(anchor[v[0]]^anchor[v[1]])-(anchor[u[0]]^anchor[u[1]]));let q=pairs.find(([a,b])=>c[a]!==c[b]);if(!q||!join(q[0],q[1],1)||!pc()){bad=true;break}}
   if(!bad){let w=p.slice();if(pin>=0&&w[0]!==pin)w=w.map(v=>v^1);if(good(O,w)&&init.every((v,i)=>v<0||v===w[i]))return{status:"SAT",word:w,s,stage:"parity"}}
  }
 }
 let r=dfs(init.slice());return{...r,s,stage:"DPLL"}
}
function compile(n,O,model){
 // BH15 base: signed occurrence [variable,negation], exceptional first.
 let R=[[[2*n,0],[2*n+1,0],[2*n+2,0]]];for(let i=0;i<n;i++)for(let j=0;j<3;j++)R.push([[2*n+j,1],[2*i,0],[2*i+1,0]]);
 for(let t of O){let [a,b,c]=t;R.push([[2*a+1,1],[2*b,0],[2*c,0]])}
 let C=[],anchor=[],lift=model?[]:null,occ=Array.from({length:2*n+3},()=>[]);
 let bm=model?model.flatMap(b=>[b,b^1]).concat([0,1,0]):null;
 function vertex(a,b){let i=anchor.length;anchor.push(a);if(lift)lift.push(b);return i}
 function owner(p,t){C.push({p,t})}
 for(let t of R){let ids=t.map(([v,s])=>{let i=vertex(s,bm?bm[v]^s:0);occ[v].push({i,s});return i});owner(0,ids)}
 const G=[];for(let p=0;p<3;p++)for(let b=0;b<3;b++){if(p===0&&b<2)continue;G.push({p,t:[0,1,2].map(i=>3*i+(p*i+b)%3)})}for(let i=0;i<3;i++)G.push({p:3,t:[3*i,3*i+1,3*i+2]});
 const gw=[0,1,0,0,1,0,0,1,1];
 function wire(a,b,color){ck(anchor[a]!==anchor[b]);if(lift)ck(lift[a]!==lift[b]);let ids=gw.map(v=>vertex(v^(anchor[a]^1),lift?v^(lift[a]^1):0));for(let o of G)owner((o.p+color)%4,o.t.map(i=>ids[i]));owner(color,[a,ids[0],ids[3]]);owner(color,[b,ids[1],ids[4]])}
 let links=0;for(let list of occ){let color=1;for(let j=1;j<list.length;j++){let a=list[j-1],b=list[j];if(a.s===b.s){let mid=vertex(anchor[a.i]^1,lift?lift[a.i]^1:0);wire(a.i,mid,color);color=3-color;links++;wire(mid,b.i,color);color=3-color;links++}else{wire(a.i,b.i,color);color=3-color;links++}}}
 while(anchor.length%3)vertex(0,0);
 const partialN=anchor.length;let count=Array.from({length:4},()=>new Uint8Array(partialN));for(let {p,t} of C)for(let i of t){ck(i<partialN&&count[p][i]===0);count[p][i]++}
 function template(p){let ids=[];for(let copy=0;copy<2;copy++){let a=[];for(let i=0;i<21;i++){let v=(Math.floor(i/7)===1?1:0)^copy;a.push(vertex(v,v))}for(let q=0;q<4;q++)for(let k=0;k<7;k++)if(q!==p||k!==0)owner(q,[a[k],a[7+(k+q)%7],a[14+(k+2*q)%7]]);ids.push([a[0],a[7+p],a[14+2*p]])}return ids}
 for(let p=0;p<4;p++){let missing=[];for(let i=0;i<partialN;i++)if(!count[p][i])missing.push(i);ck(missing.length%3===0);for(let j=0;j<missing.length;j+=3){let ids=template(p);for(let k=0;k<3;k++)owner(p,[missing[j+k],ids[0][k],ids[1][k]])}}
 let N=anchor.length, pairs=new Set(),parts=Array.from({length:4},()=>new Int32Array(N).fill(-1));for(let j=0;j<C.length;j++){let {p,t}=C[j];for(let i of t){ck(parts[p][i]===-1);parts[p][i]=j}for(let a=0;a<3;a++)for(let b=a+1;b<3;b++){let key=[t[a],t[b]].sort((a,b)=>a-b).join(",");ck(!pairs.has(key));pairs.add(key)}}for(let p of parts)ck(p.every(i=>i>=0));
 let d=0,x=anchor.slice(),y=anchor.slice();x[d]^=1;ck(C.filter(o=>!nae(o.t,y)).length===1);ck(!nae(C[0].t,y));ck(x.filter((v,i)=>v!==y[i]).length===1);
 function side(w,colors){let ins=0,outs=0,blocks=0;for(let q of colors)for(let {p,t} of C)if(q===p){let s=t.reduce((z,i)=>z+w[i],0);ck(s===1||s===2);if(q===colors[0])ins+=s;else outs+=s;if(t.includes(d)&&t.filter(i=>i!==d).every(i=>w[i]!==w[d]))blocks++}ck(ins===outs);return blocks}
 ck(side(x,[0,3])===1);ck(side(y,[1,2])===1);
 if(lift){ck(C.every(o=>nae(o.t,lift)));let dec=occ.map(l=>lift[l[0].i]^l[0].s);ck(dec.slice(0,2*n).every((v,i)=>v===bm[i]));ck(good(O,dec.filter((_,i)=>i<2*n&&i%2===0)));side(lift,[0,3]);side(lift,[1,2]);}
 return {n,N,partialN,owners:C.length,links,sourceSAT:!!model,defect:d,blockers:[1,1],liftVerified:!!lift,closure:"complement supports both marginal bits; each unpinned NAE has no unary force"};
}
let [dr,m,bw]=data;const bits=(v,n)=>Array.from({length:n},(_,i)=>Number((BigInt(v)>>BigInt(i))&1n));
let jobs=[{name:"DR17 root",n:36,O:dr.registry.map(o=>o.t),pin:-1,anchor:dr.x},{name:"BW17 root",n:bw.n,O:bw.O.map(o=>o.t),pin:-1,anchor:bits(bw.x,bw.n)}];
for(let j of m.jobs)jobs.push({name:`M23 k${j.k} pin${j.pin}`,n:m.n,O:m.owners.map(o=>o.t),pin:j.pin,anchor:bits(j.x,m.n)});
const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]],plane=[];for(let a=0;a<3;a++)for(let b=0;b<3;b++)plane.push([0,1,2].map(i=>3*i+(a*i+b)%3));for(let i=0;i<3;i++)plane.push([3*i,3*i+1,3*i+2]);
jobs.push({name:"Fano",n:7,O:fano,pin:-1},{name:"M22 plane",n:9,O:plane,pin:-1});
for(let i=0;i<7;i++)jobs.push({name:"Fano deletion "+i,n:7,O:fano.filter((_,j)=>j!==i),pin:-1});
const comparison=[];for(let j of jobs){let a=direct(j.n,j.O,j.pin,false),b=direct(j.n,j.O,j.pin,true,j.anchor);ck(a.status===b.status);for(let v of [a,b])if(v.status==="SAT"){ck(good(j.O,v.word));ck(j.pin<0||v.word[0]===j.pin)}comparison.push({name:j.name,standalone:a,combined:b})}
const compiled=[];for(let i of [0,1,2,11,12,13]){let j=jobs[i],a=comparison[i].combined;ck(a.status!=="UNKNOWN");compiled.push({name:j.name,...compile(j.n,j.O,a.word||null)})}
let seed=12345678;function rnd(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed}
for(let k=0;k<12;k++){let n=5,O=[];for(let j=0;j<8;j++){let t=[];while(t.length<3){let i=rnd()%n;if(!t.includes(i))t.push(i)}O.push(t)}let ref=null;for(let v=0;v<1<<n;v++){let w=bits(v,n);if(good(O,w)){ref=w;break}}compiled.push({name:"random "+k,...compile(n,O,ref)})}
return{assertions,comparison,compiled,limits:"4n^2 DPLL nodes; 16 greedy parity trials; not a universal solver. Negative compiled labels by theorem and source reference, no exhaustive expanded search."}
}
console.log(JSON.stringify(run(process.argv.slice(2).map(p=>JSON.parse(fs.readFileSync(p,'utf8')))),null,2));
