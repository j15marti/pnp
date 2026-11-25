const results = (function(){
 const L={gauss:0,ranks:0,gram:0,probes:0,joins:0,rejected:0,retained:0,closure:0,pins:0,reference:0,assertions:0,peakTable:0};
 const ok=b=>{L.assertions++;if(!b)throw Error("assert "+L.assertions)};
 const bit=i=>1n<<BigInt(i),z=D=>Array(D).fill(0n);
 function par(x){let p=0;while(x){x&=x-1n;p^=1}return p}
 function ga(e,d){L.gauss++;const a=Array(d).fill(null);for(let [r,b] of e){for(let i=d-1;i>=0;i--)if(r&bit(i)){if(a[i]){r^=a[i][0];b^=a[i][1]}else{a[i]=[r,b];break}}if(!r&&b)return null}return a}
 function count(e,d){const a=ga(e,d);return a?bit(d-a.filter(Boolean).length):0n}
 function solve(e,d){const a=ga(e,d);if(!a)return null;let x=0n;for(let i=0;i<d;i++)if(a[i]&&(a[i][1]^par(a[i][0]&x)))x|=bit(i);return x}
 function bs(rows,d){return ga(rows.map(r=>[r,0]),d).filter(Boolean).map(a=>a[0])}
 function ker(rows,d){const a=ga(rows.map(r=>[r,0]),d),out=[];for(let j=0;j<d;j++)if(!a[j]){let x=bit(j);for(let i=0;i<d;i++)if(a[i]&&par(a[i][0]&x))x|=bit(i);out.push(x)}return out}
 const meet=(a,b,d)=>ker([...ker(a,d),...ker(b,d)],d);
 const ew=(rows,x)=>rows.map(r=>[r,par(r&x)]);
 function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b)[a,b]=[b,a%b];return a}
 function rank(vs,D){L.ranks++;let a=[];for(let u of vs){u=u.slice();for(const [p,r] of a)if(u[p]){let c=u[p],b=r[p];u=u.map((x,i)=>x*b-c*r[i]);let g=u.reduce(gcd,0n);if(g>1n)u=u.map(x=>x/g)}let p=u.findIndex(x=>x!==0n);if(p>=0){a.push([p,u]);a.sort((x,y)=>x[0]-y[0]);if(a.length===D)return D}}return a.length}
 function val(t,x){let v=z(t.D);for(const [j,c,e] of t.terms)if(e.every(([r,b])=>par(r&x)===b))v[j]+=c;return v}
 function gram(t,g,d){L.gram++;let Q=Array.from({length:t.D},()=>z(t.D));for(const [i,c,a] of t.terms)for(const [j,k,b] of t.terms)if(c&&k)Q[i][j]+=c*k*count([...g,...a,...b],d);return Q}
 function basis(t,g,d){let A=[];while(A.length<t.D){const old=A.map(a=>a.v);if(rank([...old,...gram(t,g,d)],t.D)===A.length)break;let p=g.slice(),x=0n;for(let i=0;i<d;i++){L.probes++;let q=[...p,[bit(i),0]];if(rank([...old,...gram(t,q,d)],t.D)>A.length)p=q;else{p.push([bit(i),1]);x|=bit(i)}}const v=val(t,x);ok(g.every(([r,b])=>par(r&x)===b));ok(rank([...old,v],t.D)>A.length);A.push({v,x});L.retained++}return A}
 const leaf=(terms,D=1)=>({terms,D});
 const join=(a,b,D=1,map=[[0,0,0,1n]])=>({a,b,D,map});
 function build(a){if(a.length===1)return a[0];let i=a.length>>1;return join(build(a.slice(0,i)),build(a.slice(i)))}
 function mix(t,a,b){let v=z(t.D);for(const [o,i,j,c] of t.map)v[o]+=c*a[i]*b[j];return v}
 function ev(t,x){return t.terms?val(t,x):mix(t,ev(t.a,x),ev(t.b,x))}
 function tree(t,d){
  function prep(n){n.V=n.terms?bs(n.terms.flatMap(q=>q[2].map(e=>e[0])),d):bs([...prep(n.a),...prep(n.b)],d);return n.V}
  prep(t);let width=0;
  function ann(n,out){n.W=meet(n.V,out,d);width=Math.max(width,n.W.length);if(!n.terms){ann(n.a,bs([...out,...n.b.V],d));ann(n.b,bs([...out,...n.a.V],d))}}
  ann(t,[]);if(width>12)throw Error("width cap");
  const key=(W,x)=>W.map(r=>par(r&x)).join("");
  function go(n){let T=new Map();if(n.terms){for(let k=0;k<2**n.W.length;k++){let g=n.W.map((r,i)=>[r,(k>>i)&1]),a=basis(n,g,d);if(a.length)T.set(g.map(e=>e[1]).join(""),a)}}else{let A=go(n.a),B=go(n.b);for(let aa of A.values())for(let bb of B.values())for(let a of aa)for(let b of bb){L.joins++;let x=solve([...ew(n.a.V,a.x),...ew(n.b.V,b.x)],d);if(x===null){L.rejected++;continue}let v=mix(n,a.v,b.v),k=key(n.W,x),old=T.get(k)||[];ok(ev(n,x).every((q,i)=>q===v[i]));if(rank([...old.map(q=>q.v),v],n.D)>old.length){old.push({v,x});T.set(k,old);L.retained++}}}L.peakTable=Math.max(L.peakTable,[...T.values()].reduce((s,a)=>s+a.length,0));return T}
  return {width,A:go(t).get("")||[]};
 }
 function closure(cs){let p=new Map();while(true){L.closure++;let changed=false;for(const c of cs){if(c.some(l=>p.get(Math.abs(l))===(l>0?1:0)))continue;const u=c.filter(l=>!p.has(Math.abs(l)));if(!u.length)return null;if(u.length===1){p.set(Math.abs(u[0]),u[0]>0?1:0);L.pins++;changed=true;break}}if(!changed)return p}}
 const sat=(cs,x)=>cs.every(c=>c.some(l=>par(x&bit(Math.abs(l)-1))===(l>0?1:0)));
 function cnf(cs,d){const p=closure(cs);if(!p)return {sat:false,width:0};const c=cs.filter(c=>!c.some(l=>p.get(Math.abs(l))===(l>0?1:0))).map(c=>c.filter(l=>!p.has(Math.abs(l))));const t=build(c.length?c.map(cl=>leaf([[0,1n,[]],[0,-1n,cl.map(l=>[bit(Math.abs(l)-1),l>0?0:1])]])):[leaf([[0,1n,[]]])]);let a=tree(t,d);if(a.A.length){let x=a.A[0].x;for(let [i,b] of p)x=b?x|bit(i-1):x&~bit(i-1);ok(sat(cs,x))}return {sat:a.A.length>0,width:a.width}}
 const controls=[];function check(name,c,d){let n=0;for(let x=0n;x<bit(d);x++){L.reference++;if(sat(c,x))n++}let a=cnf(c,d);ok(a.sat===(n>0));controls.push({name,models:n,...a})}
 const f=[[1,2,3],[1,4,5],[1,6,7],[2,4,6],[2,5,7],[3,4,7],[3,5,6]],cn=t=>t.flatMap(c=>[c,c.map(l=>-l)]),fc=cn(f);
 check("Fano",fc,7);for(let i=0;i<14;i++)check("deletion "+i,fc.filter((_,j)=>i!==j),7);
 for(let i=0;i<7;i++)for(let j=0;j<3;j++){let t=f.map(c=>c.slice());t[i][j]*=-1;check("sign "+i+":"+j,cn(t),7)}
 check("opposing units",[[1],[-1]],1);check("unit chain",[[1],[-1,2],[-2,3]],3);
 let seed=83017;const rand=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>8)%n};
 for(let k=0;k<12;k++){let c=[];for(let i=0;i<10+k;i++){let v=new Set();while(v.size<3)v.add(1+rand(5));c.push([...v].map(j=>rand(2)?j:-j))}check("random "+k,c,5)}
 let vectorTests=[];for(let k=0;k<10;k++){let term=()=>Array.from({length:5},()=>[rand(3),BigInt(rand(7)-3),[[BigInt(1+rand(15)),rand(2)]]]);let a=leaf(term(),3),b=leaf(term(),3),c=leaf(term(),3),j=(a,b)=>join(a,b,3,[[0,0,0,1n],[0,1,1,-1n],[1,0,2,2n],[1,2,0,1n],[2,1,2,1n],[2,2,1,-1n]]),t=j(j(a,b),c),s=tree(t,4),ref=[];for(let x=0n;x<16n;x++){L.reference++;ref.push(ev(t,x))}let r=rank(ref,3);ok(rank(s.A.map(a=>a.v),3)===r);vectorTests.push({width:s.width,rank:r})}
 // a,b,a+b: pairwise distinct observation lines; XOR relation makes readout identically zero.
 let a=leaf([[0,1n,[]],[1,1n,[[1n,1]]]],2),b=leaf([[0,1n,[]],[1,1n,[[2n,1]]]],2),c=leaf([[0,1n,[]],[1,1n,[[3n,1]]]],2);
 let j=join(a,b,2,[[0,0,0,1n],[1,1,0,1n],[1,0,1,1n],[1,1,1,-2n]]),t=join(j,c,1,[[0,1,0,1n],[0,0,1,-1n]]),q=tree(t,2);ok(q.A.length===0);
 // High local rank: two independent coordinates of vector output and a codimension-48 packet.
 let high=leaf([[0,1n,[]],[1,1n,Array.from({length:48},(_,i)=>[bit(i),1])]],2),h=tree(high,48);ok(h.A.length===2);
 // Product of nonzero arithmetic outputs, no alphabet recognition.
 let stages=[];for(let i=0;i<4;i++)stages.push(leaf(Array.from({length:4},(_,j)=>[0,bit(j),[[bit(i*4+j),1]]])));let p=build(stages),v=tree(p,16);ok(v.A.length===1);ok(ev(p,v.A[0].x)[0]!==0n);
 return {seed:83017,controls,cnfSAT:controls.filter(c=>c.sat).length,cnfUNSAT:controls.filter(c=>!c.sat).length,vectorTests,dense:{width:q.width,rank:q.A.length},high:{coordinates:48,width:h.width,rank:h.A.length},stages:{count:4,alphabet:16,width:v.width,rank:v.A.length},ledger:L};
})();
console.log(JSON.stringify(results,null,2));
