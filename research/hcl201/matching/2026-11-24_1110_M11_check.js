console.log(JSON.stringify((function experiment(){
 const out={seed:11241110,random:{cases:0,queries:0,referenceSAT:0,referenceUNSAT:0,SAT:0,UNSAT:0,UNKNOWN:0,lifts:0,exactCountChecks:0},controls:[],scales:[],work:{counts:0,componentWords:0,convolutionPairs:0,closureScans:0,forcedPins:0,branchChecks:0,maxComponent:0,maxTable:0}};
 let seed=out.seed;const rnd=n=>{seed=(Math.imul(1664525,seed)+1013904223)>>>0;return (seed>>>8)%n};const assert=(v,msg)=>{if(!v)throw Error(msg)};
 const parity=x=>{let p=0;while(x){x&=x-1n;p^=1}return p};
 const row=(mask,c=0)=>({mask:BigInt(mask),c});
 const val=(r,z)=>r.c^parity(r.mask&z);
 const total=n=>(1n<<BigInt(n))-1n;
 function bundle(rows,width,H){let W=width.reduce((a,b)=>a+b,0);assert(rows.length===width.length&&width.every(w=>w>0)&&H>=0&&H<=W,"bad bundle");let a=0n,b=0;for(const r of rows){a^=r.mask;b^=r.c}assert(a===0n&&b===H%2,"missing parity equation");return {rows,width,H,W}}
 function bad(B,z){let a=0,b=0;B.rows.forEach((r,i)=>{let v=val(r,z);a+=v;b+=v^(B.width[i]%2)});return a>B.H||b>B.W-B.H}
 function syndrome(probes,z){let t=0;probes.forEach((r,i)=>{t|=val(r,z)<<i});return t}
 function lift(B,z){let p=B.rows.map(r=>val(r,z)),y=p.slice(),remaining=B.H-p.reduce((a,b)=>a+b,0);assert(remaining>=0&&remaining%2===0&&!bad(B,z),"lift premise");for(let i=0;i<y.length;i++){let t=Math.min(remaining,2*Math.floor((B.width[i]-y[i])/2));y[i]+=t;remaining-=t}assert(remaining===0,"pair fill");const arcs=y.map((x,i)=>Array.from({length:B.width[i]},(_,j)=>+(j<x)));assert(arcs.flat().reduce((a,b)=>a+b,0)===B.H&&arcs.every((v,i)=>v.reduce((a,b)=>a+b,0)%2===p[i]),"arc lift");return arcs}
 function count(n,B,probes,target,fixed=0n,word=0n){
   out.work.counts++;const free=total(n)^fixed,vars=Array.from({length:n},(_,i)=>i).filter(i=>free&(1n<<BigInt(i)));
   const parent=Array.from({length:n},(_,i)=>i),find=i=>{while(parent[i]!==i){parent[i]=parent[parent[i]];i=parent[i]}return i};
   const support=m=>vars.filter(i=>m&(1n<<BigInt(i)));
   const rr=B?B.rows:[],ww=B?B.width:[];const rs=rr.map(r=>support(r.mask));
   for(const s of rs)for(let j=1;j<s.length;j++)parent[find(s[j])]=find(s[0]);
   const groups=new Map();for(const i of vars){const k=find(i);if(!groups.has(k))groups.set(k,{v:[],r:[]});groups.get(k).v.push(i)}
   let a0=0,b0=0;rr.forEach((r,i)=>{if(rs[i].length)groups.get(find(rs[i][0])).r.push(i);else {const v=val(r,word);a0+=v;b0+=v^(ww[i]%2)}});
   const L=rr.length+1,Q=2**probes.length,key=(a,b,s)=>(a*L+b)*Q+s;
   const decode=k=>{let s=k%Q;k=(k-s)/Q;let b=k%L;return [(k-b)/L,b,s]};
   let dp=new Map([[key(a0,b0,syndrome(probes,word)),1n]]);
   for(const g of groups.values()){
     out.work.maxComponent=Math.max(out.work.maxComponent,g.v.length);
     if(g.v.length>12)throw Error("component cap");
     const local=new Map();
     for(let j=0;j<2**g.v.length;j++){
       out.work.componentWords++;let delta=0n;g.v.forEach((v,k)=>{if(j&(1<<k))delta|=1n<<BigInt(v)});
       let a=0,b=0;for(const i of g.r){let v=val(rr[i],word|delta);a+=v;b+=v^(ww[i]%2)}
       let s=0;probes.forEach((p,k)=>{s|=parity(p.mask&delta)<<k});
       let k=key(a,b,s);local.set(k,(local.get(k)||0n)+1n)
     }
     const next=new Map();
     for(const [k,v] of dp)for(const [l,w] of local){out.work.convolutionPairs++;const [a,b,s]=decode(k),[c,d,t]=decode(l),h=key(a+c,b+d,s^t);next.set(h,(next.get(h)||0n)+v*w)}
     dp=next;out.work.maxTable=Math.max(out.work.maxTable,dp.size)
   }
   let M=0n,F=0n;for(const [k,v] of dp){const [a,b,s]=decode(k);if(s===target){M+=v;if(B&&(a>B.H||b>B.W-B.H))F+=v}}
   return {M,F}
 }
 function state(n,bs,pr,t,f,w){let M=count(n,null,pr,t,f,w).M,fs=bs.map(b=>{let v=count(n,b,pr,t,f,w);assert(v.M===M,"count totals");return v.F});let U=fs.reduce((a,b)=>a+b,0n);return {M,fs,U,dead:M===0n||fs.some(v=>v===M)}}
 function close(n,bs,pr,t,f,w){
   while(true){out.work.closureScans++;let s=state(n,bs,pr,t,f,w);if(s.dead||2n*s.U<s.M)return {f,w,s};let changed=false;
    for(let i=0;i<n;i++){let bit=1n<<BigInt(i);if(f&bit)continue;let a=state(n,bs,pr,t,f|bit,w),b=state(n,bs,pr,t,f|bit,w|bit);
     if(a.dead&&b.dead)return {f,w,s:{...s,dead:true}};
     if(a.dead||b.dead){f|=bit;if(a.dead)w|=bit;out.work.forcedPins++;changed=true;break}
    }
    if(!changed)return {f,w,s}
   }
 }
 function solve(n,bs,pr=[],t=0){
   let f=0n,w=0n,st=close(n,bs,pr,t,f,w);({f,w}=st);if(st.s.dead)return {status:"UNSAT"};if(st.s.M<=st.s.U)return {status:"UNKNOWN"};
   while(f!==total(n)){
     let i=0;while(f&(1n<<BigInt(i)))i++;let bit=1n<<BigInt(i);let a=state(n,bs,pr,t,f|bit,w);out.work.branchChecks++;
     if(!(a.M>a.U)){let b=state(n,bs,pr,t,f|bit,w|bit);out.work.branchChecks++;assert(b.M>b.U,"lost additive margin");w|=bit}
     f|=bit;st=close(n,bs,pr,t,f,w);({f,w}=st);assert(!st.s.dead&&st.s.M>st.s.U,"closure destroyed margin")
   }
   assert(syndrome(pr,w)===t&&bs.every(b=>!bad(b,w)),"wrong SAT");bs.forEach(b=>lift(b,w));return {status:"SAT",word:w}
 }
 function reference(n,bs,pr,t){let M=0n,F=bs.map(()=>0n),good=0;for(let z=0n;z<=total(n);z++)if(syndrome(pr,z)===t){M++;let ok=true;bs.forEach((b,i)=>{if(bad(b,z)){F[i]++;ok=false}});if(ok)good++}return {M,F,good}}
 for(let c=0;c<90;c++){
   let n=2+rnd(6),s=1+rnd(4),bs=[];
   for(let j=0;j<s;j++){let k=3+rnd(5),rs=[],ws=[],x=0n,y=0;for(let i=0;i<k-1;i++){let r=row(rnd(2**n),rnd(2));rs.push(r);ws.push(1+rnd(3));x^=r.mask;y^=r.c}ws.push(1+rnd(3));let W=ws.reduce((a,b)=>a+b,0),H=rnd(W+1);rs.push(row(x,y^(H%2)));bs.push(bundle(rs,ws,H))}
   let pr=[row(rnd(2**n),rnd(2)),row(rnd(2**n),rnd(2))];out.random.cases++;
   for(let t=0;t<4;t++){let r=reference(n,bs,pr,t),s=state(n,bs,pr,t,0n,0n);assert(r.M===s.M&&r.F.every((v,i)=>v===s.fs[i]),"reference bad counts");out.random.exactCountChecks+=bs.length+1;let a=solve(n,bs,pr,t);out.random.queries++;out.random[r.good?"referenceSAT":"referenceUNSAT"]++;out.random[a.status]++;assert(a.status==="UNKNOWN"||(a.status==="SAT")===!!r.good,"wrong decision");if(a.status==="SAT")out.random.lifts++}
 }
 let clauses=[];for(let z=0;z<8;z++){let rs=[0,1,2].map(i=>row(1n<<BigInt(i),1^((z>>i)&1)));let x=rs.reduce((a,b)=>a^b.mask,0n),y=rs.reduce((a,b)=>a^b.c,0);rs.push(row(x,y));clauses.push(bundle(rs,[2,2,2,2],2))}
 for(let i=-1;i<8;i++){let bs=clauses.filter((_,j)=>j!==i),r=reference(3,bs,[],0),a=solve(3,bs);assert(r.good===(i<0?0:1),"cube control");assert(i<0?a.status!=="SAT":a.status==="SAT","cube solver");out.controls.push({type:"RT10_cube",deleted:i,reference:r.good,status:a.status})}
 let dead=[bundle([row(0,1),row(0,1),row(0,1),row(0,1)],[2,2,2,2],2)];assert(solve(1,dead).status==="UNSAT","single covering event");out.controls.push({type:"covering_event",status:"UNSAT"});
 assert(solve(1,[],[row(0,0)],1).status==="UNSAT","inconsistent guard");out.controls.push({type:"inconsistent_probe",status:"UNSAT"});
 function choose(n,k){if(k<0||k>n)return 0n;let a=1n;for(let i=1;i<=k;i++)a=a*BigInt(n-i+1)/BigInt(i);return a}
 for(let n of [16,32,64,128]){
   let bs=[];for(let j=0;j<4;j++){let rs=[];for(let i=0;i<n;i++){let c=+(i%4===j),m=1n<<BigInt(i);rs.push(row(m,c),row(m,c),row(m,c),row(m,1^c))}bs.push(bundle(rs,Array(4*n).fill(2),5*n/2))}
   let s=state(n,bs,[],0,0n,0n),expected=0n;for(let i=3*n/4+1;i<=n;i++)expected+=choose(n,i);
   assert(s.fs.every(v=>v===expected)&&s.M===1n<<BigInt(n)&&4n*s.U<s.M,"scale count/probe margin");
   let amb=0n;for(let i=5*n/2+1;i<=4*n;i++)if(i%2===0)amb+=choose(4*n,i);assert(amb>=s.M,"ambient bound should fail");
   let pr=[row(total(n)),row(total(n)^1n)],sts=[];
   for(let t=0;t<4;t++){let a=state(n,bs,pr,t,0n,0n);assert(a.M>a.U,"joint margin");sts.push({target:t,M:String(a.M),U:String(a.U)})}
   let a=solve(n,bs,pr,3);assert(a.status==="SAT","scale witness");
   out.scales.push({n,classesPerBundle:4*n,bundles:4,deficit:3*n/2,localBad:String(expected),M:String(s.M),U:String(s.U),ambientLower:String(amb),jointCounts:sts,verifiedLift:true})
 }
 return out
})(),null,2));
