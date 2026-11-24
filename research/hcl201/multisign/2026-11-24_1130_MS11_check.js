function run(){
 let seed=20261124, stats={systems:0,fibers:0,sat:0,unsat:0,certifiedSystems:0,certifiedFibers:0,strictSystems:0,lifts:0,gauss:0,terms:0,assertions:0,scale:[]};
 const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>8)%n};
 const parity=x=>{let p=0;while(x){x&=x-1n;p^=1}return p};
 const check=(v,msg)=>{stats.assertions++;if(!v)throw Error(msg)};
 // Low private bits first; subsequent pivots impose exact external equations.
 function elim(rows){stats.gauss++;let piv=new Map();for(let [a,b] of rows){while(a){let p=a&-a;if(!piv.has(p)){piv.set(p,[a,b]);break}let [c,d]=piv.get(p);a^=c;b^=d}if(!a&&b)return null}return piv}
 function info(rows,k){let p=elim(rows);if(!p)return null;let r=0, ext=[];for(let [b,[a,c]] of p){if(b<(1n<<BigInt(k)))r++;else ext.push([a>>BigInt(k),c])}return {r,ext}}
 function mst(E,k){let s=new Set([0]),tree=[],sum=0n;const weight=(i,j)=>{let t=info([...E[i],...E[j]],k);return t&&!t.ext.length?1n<<BigInt(k-t.r):0n};while(s.size<E.length){let best=null;for(let i of s)for(let j=0;j<E.length;j++)if(!s.has(j)){let w=weight(i,j);if(!best||w>best.w)best={i,j,w}}s.add(best.j);tree.push([best.i,best.j]);sum+=best.w}return {tree,sum}}
 function cert(E,k,q,tree){let scale=1n<<BigInt(k+q),f=new Map();let terms=E.map(e=>[1n,e]).concat(tree.map(([i,j])=>[-1n,[...E[i],...E[j]]]));for(let [sign,rows] of terms){let t=info(rows,k);if(!t)continue;let a=sign*(1n<<BigInt(k+q-t.r-t.ext.length));let list=[[0n,a]];for(let [v,b] of t.ext)list=list.concat(list.map(([w,c])=>[w^v,b?-c:c]));for(let [w,c] of list){stats.terms++;f.set(w,(f.get(w)||0n)+c)}}for(let [w,c] of f)if(!c)f.delete(w);let upper=f.get(0n)||0n;for(let [w,c] of f)if(w)upper+=c<0n?-c:c;return {f,upper,scale}}
 const evalF=(f,z)=>[...f].reduce((a,[w,c])=>a+(parity(w&z)?-c:c),0n);
 const hit=(e,x)=>e.every(([a,b])=>parity(a&x)===b);
 function credit(E,k,z,tree,guard){const shift=BigInt(k),mask=(1n<<shift)-1n;const rows=e=>e.map(([a,b])=>[a&mask,b^parity((a>>shift)&z)]);const count=e=>{let p=elim([...guard,...rows(e)]);return p?1n<<BigInt(k-p.size):0n};return count([])-E.reduce((s,e)=>s+count(e),0n)+tree.reduce((s,[i,j])=>s+count([...E[i],...E[j]]),0n)}
 // Rank-one event closure on a fixed guard: preserve all legal points and positive credit.
 function close(E,k,z,guard){let mask=(1n<<BigInt(k))-1n;for(;;){let base=elim(guard);if(!base)return null;let changed=false;for(let e of E){let rows=e.map(([a,b])=>[a&mask,b^parity((a>>BigInt(k))&z)]);let p=elim([...guard,...rows]);if(!p)continue;if(p.size===base.size)return null;if(p.size===base.size+1){let row=rows.find(([a,b])=>{let t=elim([...guard,[a,b^1]]);return t&&t.size>base.size});if(!row)throw Error("rank one");guard=[...guard,[row[0],row[1]^1]];changed=true;break}}if(!changed)return guard}}
 function lift(E,k,z,tree){let g=close(E,k,z,[]);check(g!==null&&credit(E,k,z,tree,g)>0n,"initial closed credit");let x=0n;for(let i=0;i<k;i++){let a=1n<<BigInt(i);let zero=[...g,[a,0]];g=credit(E,k,z,tree,zero)>0n?zero:[...g,[a,1]];if(g[g.length-1][1])x|=a;g=close(E,k,z,g);check(g!==null&&credit(E,k,z,tree,g)>0n,"closed child credit")}check(E.every(e=>!hit(e,x|(z<<BigInt(k)))),"lift");stats.lifts++;return x}
 function verify(E,k,q,tree,all=true,zs=[]){let c=cert(E,k,q,tree);let old=E.reduce((s,e)=>{let t=info(e,k);return s+(t?1n<<BigInt(k-t.r):0n)},0n)-mst(E,k).sum;let yes=c.upper<c.scale;stats.systems++;if(yes)stats.certifiedSystems++;if(yes&&old>=(1n<<BigInt(k)))stats.strictSystems++;if(all)zs=Array.from({length:1<<q},(_,i)=>BigInt(i));let vals=[];for(let z of zs){let good=0,tot=0;for(let x=0n;x<(1n<<BigInt(k));x++){let a=E.map(e=>hit(e,x|(z<<BigInt(k))));if(!a.some(Boolean))good++;tot+=a.filter(Boolean).length-tree.filter(([i,j])=>a[i]&&a[j]).length}stats.fibers++;if(good)stats.sat++;else stats.unsat++;let exact=BigInt(tot)*(1n<<BigInt(q));check(evalF(c.f,z)===exact,"Fourier identity");check(exact<=c.upper,"upper");if(yes){check(good>0,"uniform certificate");stats.certifiedFibers++;lift(E,k,z,tree)}vals.push({good,treeNumerator:tot})}return {oldNumerator:old.toString(),oldDenominator:(1n<<BigInt(k)).toString(),upper:c.upper.toString(),scale:c.scale.toString(),nonzeroCoefficients:c.f.size,values:vals}}
 const path=m=>Array.from({length:m-1},(_,i)=>[i,i+1]);
 // Full rank-two local equations on private bits: no initial rank-one forced closure.
 for(let j=0;j<240;j++){let k=2+rnd(4),q=1+rnd(4),m=2+rnd(8),E=[];for(let i=0;i<m;i++){let a=1+rnd((1<<k)-1),b;do{b=1+rnd((1<<k)-1)}while(a===b);E.push([[BigInt(a)|(BigInt(rnd(1<<q))<<BigInt(k)),rnd(2)],[BigInt(b)|(BigInt(rnd(1<<q))<<BigInt(k)),rnd(2)]])}verify(E,k,q,path(m))}
 // Explicit strict counterexample to termwise uniform tree bound; dense external parity.
 const raw=[[4,5,0,1,0,0],[5,7,1,1,0,1],[6,7,0,0,0,0],[6,7,0,0,1,0],[6,7,1,1,0,1]];
 for(let q of [1,8,32,128]){let mask=(1n<<BigInt(q))-1n;let E=raw.map(([a,b,c,d,s,t])=>[[BigInt(a)|(s?mask<<3n:0n),c],[BigInt(b)|(t?mask<<3n:0n),d]]);let out=verify(E,3,q,path(5),q===1,[0n,1n,mask,mask^1n]);check(out.oldNumerator==="8"&&BigInt(out.upper)*8n===BigInt(out.scale)*7n,"strict family");stats.scale.push({q,...out})}
 // All four forbidden words cover the repair plane (UNSAT); deleting one is SAT.
 let all=Array.from({length:4},(_,i)=>[[1n,i&1],[2n,i>>1]]);stats.cover=verify(all,2,2,path(4));stats.neighbor=verify(all.slice(0,3),2,2,path(3));check(stats.cover.values.every(v=>v.good===0)&&stats.neighbor.values.every(v=>v.good===1),"controls");
 return stats;
}
console.log(JSON.stringify(run(), null, 2));
