function runGD11(){
 const L={calls:0,closurePasses:0,rowDeletes:0,closureChecks:0,joins:0,peak:0,leafRows:0,rankCuts:0,referenceWords:0,witnesses:0,forcedBits:0,probeCalls:0};
 const B=i=>1n<<BigInt(i), par=x=>{let p=0;while(x){p^=1;x&=x-1n}return p}, assert=(x,msg)=>{if(!x)throw Error(msg)};
 const insert=(M,x)=>{while(x){let i=x.toString(2).length-1;if(M.has(i))x^=M.get(i);else{M.set(i,x);return}}};
 const inSpan=(M,x)=>{while(x){let i=x.toString(2).length-1;if(!M.has(i))return false;x^=M.get(i)}return true};
 const rank=a=>{let M=new Map;for(let x of a)insert(M,x);return M.size};
 const edge=(u,v,forms,word)=>({u,v,forms:forms.map(BigInt),word});
 const enabled=(e,x)=>e.forms.reduce((a,f,i)=>a+(par(f&x)<<i),0)===e.word;
 function ref(n,V,E,pins=[]){let c=0n;for(let x=0n;x<B(n);x++){L.referenceWords++;if(!pins.every(([a,b])=>par(a&x)===b))continue;let r=new Set([0]);for(let k=0;k<V;k++)for(let e of E)if(r.has(e.u)&&enabled(e,x))r.add(e.v);if(!r.has(V-1))c++}return c}
 function solve(n,V,E,pins=[],signed=true){
  L.calls++;let F=[],C=new Map(),M=new Map(),nq=n;
  for(let v=1;v<V-1;v++)if(E.some(e=>e.u===v||e.v===v)){C.set(v,B(nq++));if(signed)M.set(v,B(nq++))}
  const anchor=new Map;for(let v of C.keys()){let i=E.findIndex(e=>e.v===v);if(i<0)i=E.findIndex(e=>e.u===v);anchor.set(v,i)}
  function factor(forms,weight){let fs=[...new Set(forms.filter(x=>x!==0n))];let rows=[];for(let word=0;word<2**fs.length;word++){let get=x=>x===0n?0:(word>>fs.indexOf(x))&1;let w=weight(get);if(w)rows.push({word,w:BigInt(w),tag:0n})}F.push({fs,rows});L.leafRows+=rows.length}
  E.forEach((e,i)=>{
   let forms=[...e.forms,C.get(e.u)||0n,C.get(e.v)||0n,M.get(e.v)||0n];let owned=[...anchor].filter(([v,j])=>j===i).map(([v])=>v);
   for(let v of owned)forms.push(M.get(v)||0n,C.get(v));
   factor(forms,get=>{
    let c=v=>v===0?1:v===V-1?0:get(C.get(v)||0n),m=v=>get(M.get(v)||0n);
    let on=e.forms.reduce((a,f,j)=>a+(get(f)<<j),0)===e.word;
    if(on&&c(e.u)&&(!c(e.v)||m(e.v)))return 0;
    let w=1;for(let v of owned)if(m(v)){if(!c(v))return 0;w=-w}return w
   });
  });
  for(let [a,b] of pins)factor([a],get=>get(a)===b?1:0);
  // Row occurrence dependencies: each dependent observation creates one syndrome bit.
  let basis=new Map(),tags=[],dep=0,all=[];
  for(let f of F){f.ids=[];for(let a of f.fs){let j=tags.length;tags.push(0n);f.ids.push(j);all.push(a);let x=a,coeff=B(j);while(x){let k=x.toString(2).length-1;if(!basis.has(k)){basis.set(k,[x,coeff]);break}let [y,z]=basis.get(k);x^=y;coeff^=z}if(!x){let t=B(dep++);for(let l=0;l<tags.length;l++)if(coeff&B(l))tags[l]^=t}}}
  for(let f of F)for(let r of f.rows)for(let i=0;i<f.ids.length;i++)if((r.word>>i)&1)r.tag^=tags[f.ids[i]];
  // Certified affine relaxation pruning over nonzero signed rows. Restart after each changed factor.
  let changed=true;while(changed){L.closurePasses++;changed=false;if(F.some(f=>!f.rows.length))return {count:0n,width:0};
   for(let i=0;i<F.length;i++){let a=0n,sp=new Map;for(let j=0;j<F.length;j++)if(j!==i){let rows=F[j].rows;a^=rows[0].tag;for(let r of rows)insert(sp,r.tag^rows[0].tag)}
    let old=F[i].rows;F[i].rows=old.filter(r=>{L.closureChecks++;return inSpan(sp,r.tag^a)});let d=old.length-F[i].rows.length;if(d){L.rowDeletes+=d;changed=true;break}}
  }
  if(F.some(f=>!f.rows.length))return {count:0n,width:0};
  let suffix=Array(F.length+1);suffix[F.length]=new Map;for(let i=F.length-1;i>=0;i--){suffix[i]=new Map(suffix[i+1]);for(let j of F[i].ids)insert(suffix[i],tags[j])}
  let dp=new Map([[0n,1n]]),width=0,pre=[];
  for(let i=0;i<F.length;i++){
   let f=F[i],next=new Map;pre.push(...f.fs);let out=F.slice(i+1).flatMap(g=>g.fs);width=Math.max(width,rank(pre)+rank(out)-basis.size);L.rankCuts++;
   for(let [a,c] of dp)for(let r of f.rows){L.joins++;let t=a^r.tag;if(inSpan(suffix[i+1],t))next.set(t,(next.get(t)||0n)+c*r.w)}
   dp=new Map([...next].filter(([,v])=>v!==0n));L.peak=Math.max(L.peak,dp.size)
  }
  return {count:(dp.get(0n)||0n)*B(nq-basis.size),width}
 }
 let seed=2011100;const rng=m=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%m};
 let stats={random:0,sat:0,unsat:0,guardedComparisons:0,fano:[],scales:[],cycle:null,overcount:null};
 for(let z=0;z<120;z++){
  let n=3+rng(3),V=3+rng(4),E=[];for(let u=0;u<V;u++)for(let v=u+1;v<V;v++)if(rng(3)!==0){let fs=[BigInt(1+rng((1<<n)-1)),BigInt(1+rng((1<<n)-1))];E.push(edge(u,v,fs,rng(4)))}
  let q=solve(n,V,E).count,r=ref(n,V,E);assert(q===r,"random");stats.random++;stats[q>0n?"sat":"unsat"]++;
  let a=BigInt(1+rng((1<<n)-1));for(let bit=0;bit<2;bit++){assert(solve(n,V,E,[[a,bit]]).count===ref(n,V,E,[[a,bit]]),"probe");L.probeCalls++;stats.guardedComparisons++}
  if(q>0n){let pins=[],w=0n;for(let i=0;i<n;i++){let a=B(i),c=solve(n,V,E,[...pins,[a,0]]).count;L.probeCalls++;let b=c>0n?0:1;pins.push([a,b]);if(b)w|=a;assert(solve(n,V,E,pins).count>0n,"lift")}assert(ref(n,V,E,pins)===1n,"source verify");L.witnesses++;
   for(let i=0;i<n;i++){let a=B(i),b=par(a&w);let v=solve(n,V,E,[[a,b^1]]).count;L.probeCalls++;if(v===0n){L.forcedBits++;assert(solve(n,V,E,[[a,b]]).count===q,"forced closure")}}
  }
 }
 let triples=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
 let fano=triples.flatMap(t=>[0,7].map(w=>edge(0,1,t.map(B),w)));
 for(let j=-1;j<14;j++){let e=fano.filter((_,i)=>i!==j),q=solve(7,2,e).count;assert(q===BigInt(j<0?0:5)&&q===ref(7,2,e),"fano");stats.fano.push(Number(q))}
 for(let k of [4,8,16,32,64]){let E=[];for(let i=0;i<k;i++){E.push(edge(0,i+1,[B(2*i)],1),edge(i+1,k+1,[B(2*i+1)],1))}let a=solve(2*k,k+2,E),b=solve(2*k,k+2,E,[],false);assert(a.count===3n**BigInt(k)&&b.count===4n**BigInt(k),"lanes");stats.scales.push({lanes:k,sourceBits:2*k,width:a.width,ordinaryWidth:b.width,signedCount:String(a.count),ordinaryCutCount:String(b.count)})}
 let cycle=[edge(1,2,[],0),edge(2,1,[],0)];let cyc=solve(0,4,cycle).count;assert(cyc===2n&&ref(0,4,cycle)===1n,"cycle boundary");stats.cycle={signed:String(cyc),correct:"1"};
 return {seed:2011100,stats,ledger:L};
}
console.log(JSON.stringify(runGD11(),null,2));
