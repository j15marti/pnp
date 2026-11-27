function audit(){
 const pop=x=>{let c=0;while(x){x&=x-1n;c^=1}return c}, B=i=>1n<<BigInt(i), dot=(x,y)=>pop(x&y);
 const root=[15,32,13,17,14,36,11,53,10,39].map(BigInt);
 let checks=0;const ck=(b,msg)=>{checks++;if(!b)throw Error(msg)};
 function ge(n,eq){
  let a=eq.map(([r,v])=>[r,v]),p=[],i=0;
  for(let j=0;j<n;j++){let k=i;while(k<a.length&&!(a[k][0]&B(j)))k++;if(k===a.length)continue;[a[i],a[k]]=[a[k],a[i]];for(let l=0;l<a.length;l++)if(l!==i&&(a[l][0]&B(j))){a[l][0]^=a[i][0];a[l][1]^=a[i][1]}p.push(j);i++}
  if(a.some(([r,v])=>r===0n&&v))return null;
  let free=Array.from({length:n},(_,j)=>j).filter(j=>!p.includes(j)), f=Array(n).fill(0n),off=Array(n).fill(0);
  free.forEach((j,k)=>f[j]=B(k));p.forEach((j,k)=>{off[j]=a[k][1];free.forEach((l,z)=>{if(a[k][0]&B(l))f[j]^=B(z)})});
  return {f,off,d:free.length};
 }
 function equationSystem(cols,d,t){return Array.from({length:d},(_,j)=>[cols.reduce((s,c,i)=>s|((c&B(j))?B(i):0n),0n),Number((t>>BigInt(j))&1n)])}
 function local(s,i){let a=s.f[i],b=s.f[i+1],c=s.off[i],d=s.off[i+1],r=[...new Set([a,b,a^b].filter(x=>x!==0n))];return {a,b,c,d,r}}
 function span(a){let m=new Map();for(let x of a){while(x){let j=x.toString(2).length-1;if(m.has(j))x^=m.get(j);else{m.set(j,x);break}}}return m}
 function has(m,x){while(x){let j=x.toString(2).length-1;if(!m.has(j))return false;x^=m.get(j)}return true}
 function findCover(forms,k){let nodes=0;function dfs(w){nodes++;let b=span(w),u=forms.find(r=>!r.some(x=>has(b,x)));if(!u)return w;if(w.length===k)return null;for(let x of u){let z=dfs([...w,x]);if(z)return z}return null}return {w:dfs([]),nodes}}
 function solve(cols,d,t,cap,guards=[]){
  const n=cols.length;let s=ge(n,equationSystem(cols,d,t).concat(guards));if(!s)return {count:0,rank:0,nodes:0,branches:0};
  let eq=[],bad=[];
  for(let i=0;i<n;i+=2){let l=local(s,i);if(l.r.length===0){if(!(l.c||l.d))return {count:0,rank:0,nodes:0,branches:0};continue}
   if(l.r.length===1){let v=l.r[0],allowed=[0,1].filter(z=>(l.c^(l.a===v?z:0))||(l.d^(l.b===v?z:0)));if(!allowed.length)return {count:0,rank:0,nodes:0,branches:0};if(allowed.length===1)eq.push([v,allowed[0]]);continue}bad.push(l)}
  // fixed affine closure in parameter space: solve once, then repeat on original equations via original-coordinate unit equalities
  if(eq.length){const g=ge(s.d,eq);if(!g)return {count:0,rank:0,nodes:0,branches:0};const old=s; s={d:g.d,off:old.off.map((c,i)=>{let v=c;g.off.forEach((b,j)=>{if(b&&(old.f[i]&B(j)))v^=1});return v}),f:old.f.map(a=>g.f.reduce((v,b,j)=>v^((a&B(j))?b:0n),0n))};
   // recursive closure inside parameter space handled as per-branch affine constraints below; recompute local forms
   bad=[];eq=[];for(let i=0;i<n;i+=2){let l=local(s,i);if(l.r.length===3)bad.push(l)}
  }
  let w=null,nodes=0,rank=0;for(;rank<=cap;rank++){let c=findCover(bad.map(l=>l.r),rank);nodes+=c.nodes;if(c.w){w=c.w;break}}if(!w)return {count:null,rank:null,nodes,branches:0};
  const wm=span(w);let count=0,branches=0;
  for(let z=0;z<2**w.length;z++){branches++;let br=w.map((v,j)=>[v,(z>>j)&1]);let base=ge(s.d,br);ck(!!base,"independent branch");
   function image(a,c){let f=0n;for(let j=0;j<s.d;j++)if(a&B(j)){f^=base.f[j];c^=base.off[j]}return [f,c]}
   let rows=[],ok=true;
   for(let i=0;i<n;i+=2){let [a,c]=image(s.f[i],s.off[i]),[b,e]=image(s.f[i+1],s.off[i+1]);let rr=[...new Set([a,b,a^b].filter(x=>x!==0n))];ck(rr.length<=1,"rank cover");
    if(!rr.length){if(!(c||e)){ok=false;break}}else{let v=rr[0],allow=[0,1].filter(j=>(c^(a===v?j:0))||(e^(b===v?j:0)));if(!allow.length){ok=false;break}if(allow.length===1)rows.push([v,allow[0]])}
   }if(ok){let fin=ge(base.d,rows);if(fin)count+=2**fin.d}
  }
  return {count,rank,nodes,branches};
 }
 function lift(cols,d){let out=[];for(let i=0;i<cols.length;i+=2){let a=B(d+i),b=B(d+i+1);out.push(a,b^cols[i],b,a^cols[i+1])}return [out,d+cols.length]}
 function hist(cols,d){let h=new Int32Array(2**d);function go(i,t){if(i===cols.length){h[Number(t)]++;return}go(i+2,t^cols[i]);go(i+2,t^cols[i+1]);go(i+2,t^cols[i]^cols[i+1])}go(0,0n);return h}
 const h=hist(root,6),[lc,ld]=lift(root,6),lh=hist(lc,ld);
 let hole=Array.from(h).map((v,i)=>v?null:i).filter(v=>v!==null);ck(hole.length===1&&hole[0]===29,"root hole");
 const base=solve(root,6,29n,4),lifted=solve(lc,ld,29n,4);
 for(let t=0;t<64;t++){let r=solve(root,6,BigInt(t),4),q=solve(lc,ld,BigInt(t),4);ck(r.count===h[t]&&q.count===h[t]&&lh[t]===h[t],"root/lift all targets")}
 let nonzero=0, sum=0;for(let priv=0;priv<1024;priv++){let expected=1;for(let i=0;i<5;i++)expected*=((priv>>(2*i))&3)?2:3;let got=0;for(let t=0;t<64;t++)got+=lh[(priv<<6)+t];ck(got===expected,"private slice");sum+=got;if(priv)nonzero++}
 // independently compare a deterministic cross section of nonzero-private targets
 let privateChecks=0,rankCounts={};for(let priv=1;priv<1024;priv+=7){for(let t of [0,17,29,63]){let v=(priv<<6)+t,q=solve(lc,ld,BigInt(v),4);ck(q.count===lh[v],"private target");privateChecks++;rankCounts[q.rank]=(rankCounts[q.rank]||0)+1}}
 // explicit rank-two row-spaces on unconditioned root fiber, plus minimum-cover refusal
 let s=ge(10,equationSystem(root,6,29n)),spaces=Array.from({length:5},(_,i)=>local(s,2*i).r);
 let min=0;while(!findCover(spaces,min).w)min++;
 let refusal=findCover(spaces,min-1),w=findCover(spaces,min).w;
 ck(base.count===0&&lifted.count===0,"refutation");
 let deep=root,dd=6,depths=[];for(let l=1;l<=5;l++){[deep,dd]=lift(deep,dd);let q=solve(deep,dd,29n,4),g=ge(deep.length,equationSystem(deep,dd,29n));ck(q.count===0&&g.d===4,"deep lift");depths.push({depth:l,owners:deep.length/2,payload:dd*(deep.length+1),nullity:g.d,rank:q.rank,branches:q.branches,nodes:q.nodes})}
 // native guard replay: 128 deterministic guard/target cases, independently enumerate root or lifted explicit choices
 let guarded=0;for(let j=0;j<128;j++){let t=j%64,mask=BigInt((j*73+19)&1023),rhs=(j>>6)&1,ref=0;for(let x=0;x<1024;x++){let ok=true;for(let i=0;i<10;i+=2)if(!((x>>i)&3)){ok=false;break}if(!ok||dot(BigInt(x),mask)!==rhs)continue;let a=0n;for(let i=0;i<10;i++)if(x&(1<<i))a^=root[i];if(a===BigInt(t))ref++}ck(solve(root,6,BigInt(t),4,[[mask,rhs]]).count===ref,"guard");guarded++}
 return {checks,hole,root:base,lifted,min,spaces:spaces.map(r=>r.map(Number)),cover:w.map(Number),refusalNodes:refusal.nodes,rootCount:Array.from(h).reduce((a,b)=>a+b),liftCount:sum,privateSlices:nonzero+1,privateChecks,rankCounts,guarded,depths}
}
console.log(JSON.stringify(audit(),null,2));
