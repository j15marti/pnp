// Run with node; prints deterministic JSON.
console.log(JSON.stringify((function experiment(){
const rng=(()=>{let s=7012026;return n=>{s=(Math.imul(s,1664525)+1013904223)>>>0;return s%n}})();
const par=x=>{let a=0;while(x){a^=1;x&=x-1n}return a};
const add=(m,a,b)=>{let v=(m.get(a)||0n)+b;if(v)m.set(a,v);else m.delete(a)};
const conv=(a,b)=>{let r=new Map();for(let [i,x] of a)for(let [j,y] of b)add(r,i^j,x*y);return r};
const evalf=(m,z)=>{let v=0n;for(let [a,c] of m)v+=par(a&z)?-c:c;return v};
function cost(B,i){let f=new Map();for(let e of B.edges)if(e.i===i){add(f,0n,e.w);add(f,e.a,e.b?e.w:-e.w)}return f}
function recognize(B,h){
 let mins=[],scales=[],nums=[];
 for(let i=0;i<h;i++){
  let f=cost(B,i),base=evalf(f,0n);add(f,0n,-base);
  if(!f.size){mins.push(base/2n);scales.push(0n);nums.push(new Map());continue}
  let sq=conv(f,f),a=f.get(0n)||0n,b=sq.get(0n)||0n;
  if(!a||b%a!==0n)return null;
  let d=b/a;if(!d||d%2n!==0n)return null;
  for(let [k,v] of f)add(sq,k,-d*v);
  if(sq.size)return null;
  let m=base+(d<0n?d:0n);add(f,0n,base-m);
  mins.push(m/2n);scales.push((d<0n?-d:d)/2n);nums.push(f)
 }
 for(let i=0;i<h;i++)for(let j=0;j<i;j++)if((conv(nums[i],nums[j]).get(0n)||0n)!==0n)return null;
 let D=1n;for(let d of scales)if(d)D*=2n*d;
 let cats=new Map(),dummy=new Map([[0n,D]]);
 for(let i=0;i<h;i++)if(scales[i]){let f=new Map();for(let [a,v] of nums[i]){let x=v*(D/(2n*scales[i]));add(f,a,x);add(dummy,a,-x)}cats.set(i,f)}
 if(dummy.get(0n)>0n)cats.set(h,dummy);
 return {mins,scales,cats,D}
}
function system(rows){let piv=new Map();for(let [a,b] of rows){while(a){let k=a&-a;if(!piv.has(k)){piv.set(k,[a,b]);break}let [c,d]=piv.get(k);a^=c;b^=d}if(!a&&b)return null}return piv}
function mean(f,rows){let p=system(rows);if(!p)return null;let n=0n;for(let [a,c] of f){let b=0;while(a){let k=a&-a;if(!p.has(k))break;let [v,d]=p.get(k);a^=v;b^=d}if(!a)n+=b?-c:c}return n}
function witness(B,f,rows){if(!(mean(f,rows)>0n))return null;let z=0n,rr=rows.slice();for(let j=0;j<B.k;j++){let a=1n<<BigInt(j);if(mean(f,rr.concat([[a,0]]))>0n)rr.push([a,0]);else{rr.push([a,1]);z|=a}}if(evalf(f,z)<=0n)throw Error("lift");return z}
function tag(B,p){let a=0n,b=0;for(let j=0;j<B.edges.length;j++)if((p>>BigInt(j))&1n){a^=B.edges[j].a;b^=B.edges[j].b}return [a,b]}
function graph(h,free,mode=0){
 let edges=[],n=2,addEdge=(u,v,a,b,i,w)=>edges.push({u,v,a,b,i,w});
 let chosen=[];for(let i=0;i<h;i++)if(rng(4)!==0&&chosen.length<4){let t=rng(4);while(chosen.some(x=>x.t===t))t=(t+1)%4;chosen.push({i,t})}
 for(let j=0;j<3;j++){let a=BigInt(j+1),u=0;for(let {i,t} of chosen){let v=n++;addEdge(u,v,a,1^par(a&BigInt(t)),i,BigInt(i+1));u=v}addEdge(u,1,a,0,h,0n)}
 for(let j=0;j<free;j++){let a=1n<<BigInt(j+2),u=n++,v=n++,i=mode&&j<2?j%h:h;addEdge(0,u,a,0,i,i===h?0n:1n);addEdge(u,v,a,0,h,0n);addEdge(v,0,a,0,h,0n)}
 let target=0n;for(let e of edges)if(e.b)target^=(1n<<BigInt(e.u))^(1n<<BigInt(e.v));
 return {edges,k:2+free,n,target}
}
function actual(B,z,h){let c=Array(h).fill(0n),T=0n;for(let e of B.edges)if(e.b^par(e.a&z)){T^=(1n<<BigInt(e.u))^(1n<<BigInt(e.v));if(e.i<h)c[e.i]+=e.w}if(T!==B.target)throw Error("boundary");return c}
function rows(B,h){let a=[];for(let z=0n;z<(1n<<BigInt(B.k));z++)a.push({z,c:actual(B,z,h)});return a}
function refclass(R,h){let mins=[],scales=[];for(let i=0;i<h;i++){let v=[...new Set(R.map(r=>r.c[i]))].sort((a,b)=>a<b?-1:a>b?1:0);if(v.length>2)return null;mins.push(v[0]);scales.push(v.length===2?v[1]-v[0]:0n)}if(R.some(r=>r.c.filter((x,i)=>x>mins[i]).length>1))return null;return {mins,scales}}
function flow(opts,cap,pin=null){let B=opts.length,slots=[];for(let i=0;i<cap.length;i++)for(let j=0;j<Math.min(B,cap[i]);j++)slots.push(i);let match=Array(slots.length).fill(-1);
 function aug(b,seen){for(let s=0;s<slots.length;s++)if(!seen[s]&&opts[b].has(slots[s])&&(!pin||b!==pin[0]||slots[s]===pin[1])){seen[s]=true;if(match[s]<0||aug(match[s],seen)){match[s]=b;return true}}return false}
 for(let b=0;b<B;b++)if(!aug(b,[]))return null;let out=[];match.forEach((b,s)=>{if(b>=0)out[b]=slots[s]});return out
}
function oddCycle(opts,cap,A){let B=A.length,H=cap.length,t=B+H,n=t+1,adj=Array.from({length:n},()=>[]),load=Array(H).fill(0);let arc=(u,v,p)=>adj[u].push({u,v,p});for(let b=0;b<B;b++){load[A[b]]++;for(let [i,L] of opts[b]){let p=L[0];if(i===A[b])arc(B+i,b,p);else arc(b,B+i,p)}}for(let i=0;i<H;i++){if(load[i]<cap[i])arc(B+i,t,0);if(load[i]>0)arc(t,B+i,0)}
 for(let root=0;root<n;root++){let start=root*2,goal=start+1,prev=new Map([[start,null]]),q=[start];for(let j=0;j<q.length&&!prev.has(goal);j++){let x=q[j];for(let e of adj[x>>1]){let y=e.v*2+((x&1)^e.p);if(!prev.has(y)){prev.set(y,[x,e]);q.push(y)}}}
 if(!prev.has(goal))continue;let walk=[];for(let x=goal;x!==start;){let [y,e]=prev.get(x);walk.push(e);x=y}walk.reverse();let st=[],vs=[root];for(let e of walk){let i=vs.indexOf(e.v);if(i<0){st.push(e);vs.push(e.v)}else{let cy=st.slice(i).concat([e]);if(cy.reduce((p,a)=>p^a.p,0)){let C=A.slice();for(let a of cy)if(a.u<B)C[a.u]=a.v-B;return C}st=st.slice(0,i);vs=vs.slice(0,i+1)}}throw Error("odd walk lost")}
 return null
}
function decide(blocks,rec,K,probes,target){let B=blocks.length,h=K.length,cap=[],opts=[],tags=[];for(let i=0;i<h;i++){let m=rec.reduce((a,r)=>a+r.mins[i],0n),d=rec.find(r=>r.scales[i])?.scales[i]||1n;if(K[i]<m)return null;if(rec.some(r=>r.scales[i]&&r.scales[i]!==d))throw Error("scale");cap.push(Number((K[i]-m)/d>BigInt(B)?BigInt(B):(K[i]-m)/d))}cap.push(B);
 for(let b=0;b<B;b++){let q=tag(blocks[b],probes[b]);tags.push(q);let o=new Map();for(let [i,f] of rec[b].cats){let L=[];for(let p=0;p<2;p++)if(mean(f,[[q[0],p^q[1]]])>0n)L.push(p);if(L.length)o.set(i,L)}opts.push(o)}
 let A=flow(opts,cap);if(!A)return null;
 let flex=null;outer:for(let b=0;b<B;b++)for(let [i,L] of opts[b])if(L.length===2){let C=flow(opts,cap,[b,i]);if(C){A=C;flex=b;break outer}}
 let P=A.map((i,b)=>opts[b].get(i)[0]),v=P.reduce((a,b)=>a^b,0);
 if(v!==target){if(flex!==null)P[flex]^=1;else{A=oddCycle(opts,cap,A);if(!A)return null;P=A.map((i,b)=>opts[b].get(i)[0]);if(P.reduce((a,b)=>a^b,0)!==target)throw Error("cycle parity")}}
 let Z=A.map((i,b)=>witness(blocks[b],rec[b].cats.get(i),[[tags[b][0],P[b]^tags[b][1]]]));if(Z.some(x=>x===null))throw Error("missing lift");let C=Array(h).fill(0n),p=0;Z.forEach((z,b)=>{actual(blocks[b],z,h).forEach((x,i)=>C[i]+=x);p^=par(tags[b][0]&z)^tags[b][1]});if(C.some((x,i)=>x>K[i])||p!==target)throw Error("global lift");return Z
}
let counts={local:0,recognized:0,rejected:0,localReferenceRows:0,categoryParityChecks:0,global:0,sat:0,unsat:0,referenceTuples:0,lifts:0,scaling:[],errors:0};
for(let j=0;j<180;j++){let h=3,B=graph(h,rng(3),j%3===0?1:0),R=rows(B,h),a=recognize(B,h),b=refclass(R,h);counts.local++;counts.localReferenceRows+=R.length;if(!!a!==!!b)throw Error("recognition");if(!a){counts.rejected++;continue}counts.recognized++;if(a.mins.some((x,i)=>x!==b.mins[i]||a.scales[i]!==b.scales[i]))throw Error("extrema");let p=BigInt(rng(1<<Math.min(25,B.edges.length))),[mask,off]=tag(B,p);for(let i=0;i<=h;i++)for(let bit=0;bit<2;bit++){let f=a.cats.get(i)||new Map(),want=R.some(r=>{let c=r.c.findIndex((x,j)=>x>a.mins[j]);return (c<0?h:c)===i&&(par(mask&r.z)^off)===bit});let got=witness(B,f,[[mask,bit^off]]);if((got!==null)!==want)throw Error("category parity");counts.categoryParityChecks++}}
for(let j=0;j<100;j++){let h=3,B=Array.from({length:2+rng(3)},()=>graph(h,rng(2))),rec=B.map(b=>recognize(b,h)),R=B.map(b=>rows(b,h)),p=B.map(b=>BigInt(rng(1<<Math.min(25,b.edges.length)))),K=Array.from({length:h},(_,i)=>rec.reduce((a,r)=>a+r.mins[i],0n)+BigInt(rng(B.length+1)*2*(i+1)));if(j%9===0)K[0]-=1n;
 let attainable=[false,false];function visit(b,c,z){if(b===B.length){counts.referenceTuples++;if(c.every((x,i)=>x<=K[i]))attainable[z]=true;return}let [a,o]=tag(B[b],p[b]);for(let r of R[b])visit(b+1,c.map((x,i)=>x+r.c[i]),z^par(a&r.z)^o)}visit(0,Array(h).fill(0n),0);
 for(let t=0;t<2;t++){let Z=decide(B,rec,K,p,t);if(!!Z!==attainable[t])throw Error("global parity");counts.global++;if(Z){counts.sat++;counts.lifts++}else counts.unsat++}}
for(let k of [8,16,32,64,128]){let B=graph(3,k),r=recognize(B,3);if(!r)throw Error("scale reject");let p=1n<<BigInt(B.edges.length-1),[a,o]=tag(B,p);for(let bit=0;bit<2;bit++){let f=[...r.cats.values()][0];if(witness(B,f,[[a,bit^o]])===null)throw Error("scale tag")};counts.scaling.push({freeCycleRank:k,rank:B.k,edges:B.edges.length,categories:r.cats.size})}
return counts
})(), null, 2));
