function audit2(){
 const B=i=>1n<<BigInt(i),par=x=>{let v=0;while(x){v^=1;x&=x-1n}return v},dot=(a,b)=>par(a&b);
 const root=[15,32,13,17,14,36,11,53,10,39].map(BigInt);
 let checks=0;const ck=(b,m)=>{checks++;if(!b)throw Error(m)};
 function ge(n,eq){let a=eq.map(([r,v])=>[r,v]),p=[],i=0;for(let j=0;j<n;j++){let k=i;while(k<a.length&&!(a[k][0]&B(j)))k++;if(k===a.length)continue;[a[i],a[k]]=[a[k],a[i]];for(let l=0;l<a.length;l++)if(l!==i&&(a[l][0]&B(j))){a[l][0]^=a[i][0];a[l][1]^=a[i][1]}p.push(j);i++}if(a.some(([r,v])=>r===0n&&v))return null;let fr=Array.from({length:n},(_,j)=>j).filter(j=>!p.includes(j)),f=Array(n).fill(0n),o=Array(n).fill(0);fr.forEach((j,k)=>f[j]=B(k));p.forEach((j,k)=>{o[j]=a[k][1];fr.forEach((l,z)=>{if(a[k][0]&B(l))f[j]^=B(z)})});return {f,o,d:fr.length}}
 function lift(cols,d){let out=[];for(let i=0;i<cols.length;i+=2){let a=B(d+i),b=B(d+i+1);out.push(a,b^cols[i],b,a^cols[i+1])}return [out,d+cols.length]}
 function equations(cols,d,t){return Array.from({length:d},(_,j)=>[cols.reduce((s,c,i)=>s|((c&B(j))?B(i):0n),0n),Number((t>>BigInt(j))&1n)])}
 function closure(s){let merges=0,rounds=0,imports=0;while(s){rounds++;let group=new Map(),bad=false;for(let i=0;i<s.f.length;i+=2){let a=s.f[i],b=s.f[i+1],c=s.o[i],d=s.o[i+1],r=[...new Set([a,b,a^b].filter(x=>x))].sort((a,b)=>a<b?-1:1);if(!r.length){if(!(c||d)){bad=true;break}continue}let key=r.join(","),g=group.get(key);if(g)merges++;else{g={r,mask:r.length===1?3:15};group.set(key,g)}let bas=r.slice(0,r.length===1?1:2),evalForm=(f,z)=>f===0n?0:f===bas[0]?(z&1):f===bas[1]?((z>>1)&1):((z&1)^((z>>1)&1));for(let z=0;z<(r.length===1?2:4);z++)if(!(c^evalForm(a,z))&&!(d^evalForm(b,z)))g.mask&=~(1<<z)}
 if(bad||[...group.values()].some(g=>!g.mask))return {s:null,merges,rounds,imports,k:0};
 let eq=[],live=[];for(let {r,mask} of group.values()){let vals=Array.from({length:r.length===1?2:4},(_,i)=>i).filter(i=>mask&(1<<i));if(r.length===1){if(vals.length===1)eq.push([r[0],vals[0]])}else if(vals.length===3)live.push(r);else if(vals.length===1){eq.push([r[0],vals[0]&1],[r[1],vals[0]>>1])}else if(vals.length===2){let delta=vals[0]^vals[1];let q=delta===1?2:delta===2?1:3;eq.push([(q&1?r[0]:0n)^(q&2?r[1]:0n),par(BigInt(q&vals[0]))])}}
 if(!eq.length)return {s,live,merges,rounds,imports,k:live.length};imports+=eq.length;let g=ge(s.d,eq);if(!g)return {s:null,merges,rounds,imports,k:0};ck(g.d<s.d,"closure rank decrease");let old=s;s={d:g.d,o:old.o.map((c,i)=>g.o.reduce((v,b,j)=>v^((old.f[i]&B(j))?b:0),c)),f:old.f.map(a=>g.f.reduce((v,b,j)=>v^((a&B(j))?b:0n),0n))};
 }return {s:null,merges,rounds,imports,k:0}}
 function count(s){if(!s)return 0;let n=0;for(let z=0;z<2**s.d;z++){let ok=true;for(let i=0;i<s.f.length;i+=2)if(!(s.o[i]^dot(s.f[i],BigInt(z)))&&!(s.o[i+1]^dot(s.f[i+1],BigInt(z)))){ok=false;break}if(ok)n++}return n}
 const [lc,d]=lift(root,6),hist=new Int32Array(65536);function go(i,t){if(i===lc.length){hist[Number(t)]++;return}go(i+2,t^lc[i]);go(i+2,t^lc[i+1]);go(i+2,t^lc[i]^lc[i+1])}go(0,0n);
 const grouped={};let dpMatches=0;
 for(let priv=0;priv<1024;priv++){let h=Array(64).fill(0);h[0]=1;let nz=0;for(let i=0;i<5;i++){let p=(priv>>(2*i))&1,q=(priv>>(2*i+1))&1,allowed=[];if(p||q)nz++;for(let v=0;v<4;v++){let x=v&1,y=v>>1;if((x||(y^p))&&(y||(x^q)))allowed.push((x?Number(root[2*i]):0)^(y?Number(root[2*i+1]):0))}ck(allowed.length===(p||q?2:3),"private-domain formula");let hh=Array(64).fill(0);for(let j=0;j<64;j++)for(let u of allowed)hh[j^u]+=h[j];h=hh}
 for(let t=0;t<64;t++){ck(h[t]===hist[64*priv+t],"all-target formula");dpMatches++}
 // deterministic sample: all 64 targets for priv=0; all private slices at t=29
 let tests=priv===0?Array.from({length:64},(_,i)=>i):[29];
 for(let t of tests){let src=ge(lc.length,equations(lc,d,BigInt(64*priv+t))),r=closure(src);let c=count(r.s);ck(c===h[t],"closed exact count");let key=String(nz),v=grouped[key]??={cases:0,no:0,closureNo:0,affine:0,remainingLiveMax:0,merges:0,imports:0};v.cases++;v.no+=c===0?1:0;v.closureNo+=r.s===null?1:0;v.affine+=r.s&&r.k===0?1:0;v.remainingLiveMax=Math.max(v.remainingLiveMax,r.k);v.merges+=r.merges;v.imports+=r.imports;}}
 // independent arbitrary affine guard tests on root/lift (fixed seed) using affine point enumeration before and after coalescing
 let seed=123456789,rand=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed},guards=0;
 for(let j=0;j<300;j++){let t=BigInt(rand()&65535),eq=equations(lc,d,t);for(let k=0;k<j%4;k++)eq.push([BigInt(rand()&((1<<20)-1)),rand()&1]);let s=ge(20,eq),a=count(s),r=closure(s);ck(count(r.s)===a,"guard closure");guards++}
 return {checks,dpMatches,groups:grouped,guards};
}
console.log(JSON.stringify(audit2(),null,2));
