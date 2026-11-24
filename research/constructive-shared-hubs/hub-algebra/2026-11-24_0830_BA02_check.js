function runBA02(){
 const assert=(x,m)=>{if(!x)throw Error(m)};
 const uniq=a=>[...new Set(a)];
 const xor=a=>a.reduce((s,x)=>s^x,0n);
 const order=(a,b)=>a>b?-1:a<b?1:0;
 function red(x,b){for(const y of b)if((x^y)<x)x^=y;return x}
 function basis(a){const b=[];for(let x of a){x=red(x,b);if(x){b.push(x);b.sort(order)}}return b}
 function span(a){return basis(a.map(x=>x^a[0]))}
 function hull(fs){return [xor(fs.map(a=>a[0])),basis(fs.flatMap(a=>a.map(x=>x^a[0])))]}
 function intersect(u,v){let e=[],out=[];for(const orig of v){let x=red(orig,u),w=orig;for(const [y,z] of e)if((x^y)<x){x^=y;w^=z}if(x){e.push([x,w]);e.sort((a,b)=>order(a[0],b[0]))}else out.push(w)}return basis(out)}
 function fibers(a,p){let m=new Map();for(const x of a){let y=red(x,p);if(!m.has(y))m.set(y,[]);m.get(y).push(x)}return m}
 function width(fs){let u=fs.map(span),r=basis(u.flat()).length,w=0;for(let i=0;i<=fs.length;i++)w=Math.max(w,basis(u.slice(0,i).flat()).length+basis(u.slice(i).flat()).length-r);return w}
 function solve(original,t0,use=true){
  let fs=original.map(uniq),t=t0,trace=[],s={closureScans:0,closureRows:0,deleted:0,pairTrials:0,fiberRows:0,quotients:0,removedRank:0,projectRows:0,repairTrials:0,dpEdges:0,peak:0,initialWidth:0,finalWidth:0};
  const done=w=>({w,s});
  if(fs.some(a=>!a.length))return done(null);
  s.initialWidth=width(fs);
  for(;;){
   let changed=true;while(changed){changed=false;for(let i=0;i<fs.length;i++){s.closureScans++;let [a,b]=hull(fs.filter((_,j)=>j!==i));s.closureRows+=fs[i].length;let keep=fs[i].filter(x=>red(t^a^x,b)===0n);s.deleted+=fs[i].length-keep.length;if(!keep.length)return done(null);if(keep.length!==fs[i].length){fs[i]=keep;changed=true;break}}}
   if(!use)break;
   let u=fs.map(span),pick=null;
   outer:for(let i=0;i<fs.length;i++)for(let j=i+1;j<fs.length;j++){
    s.pairTrials++;let p=intersect(u[i],u[j]);if(!p.length)continue;
    let a=fibers(fs[i],p),b=fibers(fs[j],p);s.fiberRows+=fs[i].length+fs[j].length;
    let ma=Math.min(...Array.from(a.values(),x=>x.length)),mb=Math.min(...Array.from(b.values(),x=>x.length));
    if(BigInt(ma+mb)>(1n<<BigInt(p.length))){pick={i,j,p};break outer}
   }
   if(!pick)break;
   let {i,j,p}=pick;trace.push({fs:fs.map(a=>a.slice()),t,i,j,p});
   s.projectRows+=fs.reduce((n,a)=>n+a.length,0);fs=fs.map(a=>uniq(a.map(x=>red(x,p))));t=red(t,p);s.quotients++;s.removedRank+=p.length;
  }
  s.finalWidth=width(fs);
  let dp=new Map([[0n,[]]]);
  for(let i=0;i<fs.length;i++){let [a,b]=hull(fs.slice(i+1)),next=new Map();for(const [v,w] of dp)for(const x of fs[i]){s.dpEdges++;let z=v^x;if(red(t^z^a,b)===0n&&!next.has(z))next.set(z,[...w,x])}dp=next;s.peak=Math.max(s.peak,dp.size);assert(BigInt(dp.size)<=(1n<<BigInt(s.finalWidth)),"cut");if(!dp.size)return done(null)}
  let w=dp.get(t);if(!w)return done(null);
  for(let k=trace.length-1;k>=0;k--){const {fs,t,i,j,p}=trace[k];let old=w.map((x,l)=>fs[l].find(y=>red(y,p)===x));assert(old.every(x=>x!==undefined),"representative");let d=t^xor(old);assert(!red(d,p),"delta");let A=fs[i].filter(x=>red(x,p)===w[i]),B=new Set(fs[j].filter(x=>red(x,p)===w[j]));let goal=old[i]^old[j]^d,found=false;for(const x of A){s.repairTrials++;if(B.has(goal^x)){old[i]=x;old[j]=goal^x;found=true;break}}assert(found,"fiber repair");w=old}
  assert(w.every((x,i)=>original[i].includes(x))&&xor(w)===t0,"lift");return done(w)
 }
 let seed=0xBA020830;function rng(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return Math.floor(seed/4294967296*n)}
 function brute(fs,t){let n=0,yes=false;function rec(i,x){if(i===fs.length){n++;if(x===t)yes=true;return}for(const a of fs[i])rec(i+1,x^a)}rec(0,0n);return {n,yes}}
 let total={cases:0,sat:0,unsat:0,referenceTuples:0,quotients:0,removedRank:0,pairTrials:0,fiberRows:0,closureRows:0,dpEdges:0,repairTrials:0};
 function compare(fs,t){let r=solve(fs,t),b=brute(fs,t);assert((r.w!==null)===b.yes,"decision");total.cases++;total[b.yes?"sat":"unsat"]++;total.referenceTuples+=b.n;for(let k in r.s)if(k in total)total[k]+=r.s[k];return r}
 for(let k=0;k<180;k++){let d=2+rng(6),fs=Array.from({length:2+rng(4)},()=>uniq(Array.from({length:1+rng(5)},()=>BigInt(rng(2**d)))));compare(fs,k%2?xor(fs.map(a=>a[rng(a.length)])):BigInt(rng(2**d)))}
 const dense=(sh,missing)=>[0n,1n,2n,3n].filter(x=>x!==BigInt(missing)).map(x=>x^sh);
 // Pair with a shared plane P, separate quotient directions and diagonal external coupling.
 function block(p,u,v){let a=[],b=[],c=[];for(let q=0;q<3;q++){let U=(BigInt(q)&1n?u:0n)^(BigInt(q)&2n?u<<1n:0n),V=(BigInt(q)&1n?v:0n)^(BigInt(q)&2n?v<<1n:0n);a.push(...dense(0n,q).map(x=>((x&1n)?p:0n)^((x&2n)?p<<1n:0n)^U));b.push(...dense(0n,3-q).map(x=>((x&1n)?p:0n)^((x&2n)?p<<1n:0n)^V));c.push(U^V)}return [a,b,c]}
 for(let k=0;k<64;k++){let fs=block(1n,4n,16n);let t=BigInt(k);compare(fs,t)}
 // Random dense fibers including sparse exceptional fibers and changed pins.
 for(let k=0;k<100;k++){let A=[],B=[];for(let q=0;q<3;q++){for(let z=0;z<4;z++){if(rng(5)>0)A.push(BigInt(z+4*q));if(rng(5)>0)B.push(BigInt(z+16*q))}}if(!A.length||!B.length)continue;let fs=[A,B,[0n,20n,40n]];compare(fs,BigInt(rng(64)))}
 // Exact occurrence tags: every repeated variable gets equality to first occurrence.
 function formula(n,cs){let occ=Array.from({length:n},()=>[]),tags=cs.map(()=>[0n,0n,0n]);cs.forEach((c,i)=>c.v.forEach((v,j)=>occ[v].push([i,j])));let q=0;for(const os of occ)for(let k=1;k<os.length;k++){let [i,j]=os[0],[l,m]=os[k],b=1n<<BigInt(q++);tags[i][j]^=b;tags[l][m]^=b}
  let maps=cs.map((c,i)=>{let m=new Map();for(const z of c.a){let t=xor(tags[i].filter((_,j)=>(z>>j)&1));if(!m.has(t))m.set(t,z)}return m}),fs=maps.map(m=>[...m.keys()]),r=solve(fs,0n),count=0;for(let x=0;x<2**n;x++)if(cs.every(c=>c.a.includes(c.v.reduce((z,v,j)=>z|(((x>>v)&1)<<j),0))))count++;
  assert((r.w!==null)===(count>0),"source decision");
  if(r.w){let x=Array(n).fill(null);for(let i=0;i<cs.length;i++){let z=maps[i].get(r.w[i]);cs[i].v.forEach((v,j)=>{let b=(z>>j)&1;assert(x[v]===null||x[v]===b,"wire");x[v]=b})}assert(cs.every(c=>c.a.includes(c.v.reduce((z,v,j)=>z|(x[v]<<j),0))),"source lift")}
  return {count,...r.s}
 }
 let lines=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]],f=lines.map(v=>({v,a:[1,2,3,4,5,6]}));
 let fano=[formula(7,f)];for(let i=0;i<7;i++)for(let z of [0,7])fano.push(formula(7,f.map((c,j)=>i===j?{v:c.v,a:[...c.a,z]}:c)));
 let scaling=[];for(let k of [2,4,8,16,32]){let A=[],B=[],C=[];for(let i=0;i<k;i++){let [a,b,c]=block(1n<<BigInt(2*i),1n<<BigInt(2*k),1n<<BigInt(2*k+2));A.push(a);B.push(b);if(i===0)C.push(c)}let fs=[...A,...B,...C],t=(1n<<BigInt(2*k))-1n,r=solve(fs,t);assert(r.w!==null&&r.s.removedRank>=2*k,"scale");let base=k<=4?solve(fs,t,false).s:null;scaling.push({k,rows:fs.reduce((s,a)=>s+a.length,0),...r.s,baseline:base})}
 // At equality of fiber sizes, support is not guaranteed: {0,1}+{0,1} excludes 2.
 const boundary=compare([[0n,1n],[0n,1n]],2n);assert(!boundary.w,"strict inequality");
 return {seed:"0xBA020830",total,fano,scaling,discrepancies:0}
}
console.log(JSON.stringify(runBA02(),null,2));
