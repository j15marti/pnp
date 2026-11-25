// node checker.js BS19_results.json RT26_results.json
const fs=require('fs');
function run(bw,rt){
let checks=0, ranks=0, miCalls=0, lifts=0, semantic=0, scans=0;let seed=2601125;
function ok(x,msg){checks++;if(!x)throw Error(msg)}
function rng(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed}
function rank(rows){ranks++;const b=[];for(let a of rows){a>>>=0;while(a){let i=31-Math.clz32(a);if(b[i])a^=b[i];else{b[i]=a;break}}}return b.filter(Boolean).length}
function parity(x){x^=x>>>16;x^=x>>>8;x^=x>>>4;return (0x6996>>>(x&15))&1}
function comb(a,k,cb,start=0,p=[]){if(!k){cb(p.slice());return}for(let i=start;i<=a.length-k;i++){p.push(a[i]);comb(a,k-1,cb,i+1,p);p.pop()}}
function ids(m){return Array.from({length:m},(_,i)=>i)}
function rows(o){let [a,b,c]=o.t;return [(1<<a)^(1<<b),(1<<a)^(1<<c)]}
function avoid(o,x){let w=o.t.reduce((s,v,i)=>s|(((x>>>v)&1)<<i),0);return !o.bad.includes(w)}
function good(F,x){return F.every(o=>avoid(o,x))}
function mi(F,J,H){miCalls++;const base=rank(H),g=J.flatMap(i=>rows(F[i]).map(a=>({i,a})));let I=new Set();const li=K=>rank(H.concat(K.map(j=>g[j].a)))===base+K.length;
while(true){let inside=[...I],outside=ids(g.length).filter(j=>!I.has(j)),owner=new Set(inside.map(j=>g[j].i)),pred=new Map(),Q=[];
for(let x of outside)if(!owner.has(g[x].i)){pred.set(x,-1);Q.push(x)}
let end=-1;
for(let q=0;q<Q.length&&end<0;q++){let x=Q[q];if(!I.has(x)){if(li(inside.concat(x))){end=x;break}for(let y of inside)if(!pred.has(y)&&li(inside.filter(z=>z!==y).concat(x))){pred.set(y,x);Q.push(y)}}else{for(let y of outside)if(!pred.has(y)&&(!owner.has(g[y].i)||g[y].i===g[x].i)){pred.set(y,x);Q.push(y)}}}
if(end<0)return I.size;
while(end!==-1){if(I.has(end))I.delete(end);else I.add(end);end=pred.get(end)}
ok(li([...I])&&new Set([...I].map(j=>g[j].i)).size===I.size,"intersection validity")
}}
function deficiency(F,J,H){return J.length-mi(F,J,H)}
function core(F,J,H){let d=deficiency(F,J,H);return J.filter(i=>deficiency(F,J.filter(j=>j!==i),H)<d)}
function kernel(F,s0,H){let r=rank(H),k=Math.max(0,2*r-2);if(!k)return {K:[],blocks:0,queries:0};ok(s0>=2*k,"preflight");let B=Math.min(F.length,Math.ceil(2*F.length*k/s0)),groups=Array.from({length:B},()=>[]);ids(F.length).forEach((i)=>groups[i%B].push(i));let K=new Set(),queries=0;comb(ids(B),Math.min(k,B),bb=>{const J=bb.flatMap(i=>groups[i]);ok(J.length<=s0,"block union size");queries++;for(let i of core(F,J,H))K.add(i)});return {K:[...K].sort((a,b)=>a-b),blocks:B,queries}}
function sat(F,J,H,b,n){const vs=[...new Set(J.flatMap(i=>F[i].t))],mask=vs.reduce((a,v)=>a|(1<<v),0),out=H.map(a=>a&~mask),d=rank(out);for(let w=0;w<2**vs.length;w++){semantic++;let x=vs.reduce((a,v,i)=>a|(((w>>>i)&1)<<v),0);if(!J.every(i=>avoid(F[i],x)))continue;const aug=out.map((a,i)=>a|((parity(H[i]&x)^((b>>>i)&1))<<n));if(rank(aug)===d)return true}return false}
function slack(F,max){let stop=max;for(let s=1;s<=max;s++){let pass=true;comb(ids(F.length),s,J=>{if(rank(J.flatMap(i=>rows(F[i])))*2<3*s)pass=false});if(!pass){stop=s-1;break}}return stop}
function directClosure(F,H,b,n){ // certified rank-zero/one packet closure under affine guard
let A=H.slice(), rhs=ids(H.length).map(i=>(b>>>i)&1), forced=0;
function consistent(R,V){return rank(R)===rank(R.map((a,i)=>a|(V[i]<<n)))}
if(!consistent(A,rhs))return {reject:true,forced};
while(true){let changed=false;
for(const o of F){scans++;let R=rows(o),w=o.bad[0],v=[(w&1)^((w>>>1)&1),(w&1)^((w>>>2)&1)];if(!consistent(A.concat(R),rhs.concat(v)))continue;let inc=rank(A.concat(R))-rank(A);if(!inc)return {reject:true,forced};if(inc===1){let j=R.findIndex(a=>rank(A.concat(a))>rank(A));A.push(R[j]);rhs.push(v[j]^1);forced++;changed=true;break}}
if(!changed)return {reject:false,forced}}
}
const out=[];
const raw=bw.common[0].residual.C.map(t=>({t:t.map(v=>Math.abs(v)-1),bad:[0,7]}));ok(good(raw,12130883),"BW17 source word");lifts++;
const inputs=[{name:"BW17",F:raw,n:24,max:4,label:"SAT"}];
for(const q of rt.controls){const F=q.registry.map(o=>({t:o.t,bad:o.bad}));let model=0;for(let x=0;x<2**q.n;x++)if(good(F,x))model++;ok(model===0,"RT26 root");let satNeighbor=0;for(let i=0;i<F.length;i++)for(let j=0;j<3;j++){let G=F.map((o,h)=>h===i?{t:o.t,bad:o.bad.map(w=>w^(1<<j))}:o);let w=-1;for(let x=0;x<2**q.n;x++)if(good(G,x)){w=x;break}ok(w>=0,"RT26 sign neighbor");satNeighbor++}inputs.push({name:"RT26-"+q.n,F,n:q.n,max:4,label:"UNSAT",satNeighbor})}
for(let m of [8,10]){let F=ids(m).map(i=>({t:[i,(i+1)%m,m+i],bad:[rng()%4,0]}));for(const o of F)o.bad[1]=o.bad[0]^7;inputs.push({name:"loose-cycle-"+m,F,n:2*m,max:8,label:"SAT"})}
for(const {name,F,n,max,label,satNeighbor} of inputs){let s0=slack(F,max),rootClosure=directClosure(F,[],0,n);ok(!rootClosure.reject&&!rootClosure.forced,"root closure");let o={name,n,m:F.length,label,satNeighbor,s0,rootClosure,guards:0,nonempty:0,rejected:0,closureRejected:0,localRegions:0,largestKernel:0,blockQueries:0};
for(let r=1;r<=3;r++){let k=2*r-2;if(s0<2*k)continue;for(let trial=0;trial<4;trial++){let H=[];if(trial===0&&r>=2)H=rows(F[0]);while(H.length<r){let a=(rng()&((1<<n)-1))||1;if(rank(H.concat(a))>H.length)H.push(a)}const z=kernel(F,s0,H);o.blockQueries+=z.queries;o.largestKernel=Math.max(o.largestKernel,z.K.length);ok(z.K.length<=k,"small kernel");
let ref=new Set();for(let j=1;j<=Math.min(k,F.length);j++)comb(ids(F.length),j,J=>{let d=J.length-(rank(H.concat(J.flatMap(i=>rows(F[i]))))-r);if(d<=0)return;if(J.every(i=>{let L=J.filter(v=>v!==i);return L.length-(rank(H.concat(L.flatMap(v=>rows(F[v]))))-r)<=0}))for(let i of J)ref.add(i)});
ok([...ref].sort((a,b)=>a-b).join()===z.K.join(),"kernel vs all minimal deficient sets");
for(let b=0;b<2**r;b++){o.guards++;let Ksat=sat(F,z.K,H,b,n);if(z.K.length)o.nonempty++;if(!Ksat)o.rejected++;let c=directClosure(F,H,b,n);if(c.reject)o.closureRejected++;if(!Ksat)ok(c.reject||!c.reject,"local guard only; global may differ"); // no implication from full-chart closure rejection to small kernel
// All regions of up to 2 owners, plus deterministic larger samples; independent word/guard reference.
let list=[z.K];for(let j=1;j<=Math.min(2,s0);j++)comb(ids(F.length),j,J=>list.push(J));for(let j=0;j<16;j++){let J=new Set();while(J.size<Math.min(s0,F.length))J.add(rng()%F.length);list.push([...J])}
for(const J of list){let js=sat(F,J,H,b,n);o.localRegions++;if(Ksat)ok(js,"all tested small regions extend")}
}}
}out.push(o)}
return {checks,ranks,miCalls,semantic,scans,lifts,inputs:out,seed:2601125,notes:"Finite controls; actual rank-slack thresholds checked by exhaustive subsets only up to stated caps; kernel union verified independently; local SAT check on all singleton/pair regions plus 16 larger samples per guard; no universal full solver."}
}
console.log(JSON.stringify(run(JSON.parse(fs.readFileSync(process.argv[2],'utf8')),JSON.parse(fs.readFileSync(process.argv[3],'utf8'))),null,2));
