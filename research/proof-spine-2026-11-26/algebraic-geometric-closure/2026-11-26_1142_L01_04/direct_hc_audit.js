function direct(){
 const range=n=>Array.from({length:n},(_,i)=>i);
 const perms=a=>a.length?a.flatMap((x,i)=>perms(a.filter((_,j)=>i!==j)).map(p=>[x,...p])):[[]];
 const isHC=p=>{if(new Set(p).size!==p.length||p.some((x,i)=>x===i))return false;let u=0,s=new Set();while(!s.has(u)){s.add(u);u=p[u]}return u===0&&s.size===p.length};
 let checks=0;const check=x=>{checks++;if(!x)throw Error("check "+checks)};
 const facts=[];
 for(let k of [2,3,4,5,6,8]){
  let n=2*k,fs=k<=6?perms(range(k)):Array.from({length:64},(_,z)=>{let a=range(k);for(let i=k-1;i>0;i--){let j=(z*97+i*31+z*i*7)%(i+1);[a[i],a[j]]=[a[j],a[i]]}return a});
  let sigs=new Set(),lifts=0;
  for(const f of fs){let support=Array.from({length:k},()=>Array(k).fill(false));for(let a=0;a<k;a++)for(let c=0;c<k;c++)if(a!==c){let order=[a,c,...range(k).filter(x=>x!==a&&x!==c)],tau=Array(k);for(let i=0;i<k;i++)tau[order[i]]=order[(i+1)%k];let p=[...f.map(b=>k+b),...Array(k)];for(let i=0;i<k;i++)p[k+f[i]]=tau[i];check(isHC(p));check(p[k+f[a]]===c);support[f[a]][c]=true;lifts++}
   for(let a=0;a<k;a++){check(!support[f[a]][a]);let p=Array(n).fill(-1);p[a]=k+f[a];p[k+f[a]]=a;check(p[p[a]]===a)}
   let sig=JSON.stringify(support);sigs.add(sig);
   if(k<=4){let exact=Array.from({length:k},()=>Array(k).fill(false));for(let g of perms(range(k))){let p=[...f.map(b=>k+b),...g];if(isHC(p))g.forEach((a,b)=>exact[b][a]=true)}check(JSON.stringify(exact)===sig)}
  } 
  if(k<=6)check(sigs.size===fs.length);facts.push({vertices:n,prefixesTested:fs.length,distinctSupportSignatures:sigs.size,validLifts:lifts,exhaustivePrefixes:k<=6})
 }
 let blocks=[];for(let n of [4,8,16,32,64,128]){let states=new Set([""]);let total=1n,max=1;for(let i=0;i<n;i+=2){let next=new Set();for(let s of states){next.add(s+"a");next.add(s+"b")}check(next.size===2);max=Math.max(max,next.size);total*=2n;states=new Set([""])}check(total===2n**BigInt(n/2));blocks.push({rows:n,exactCount:total.toString(),width:max,method:"symbolic independent 2x2 complete blocks; two choices, reconverge after pair"})}
 return {checks,facts,blocks,limitations:"k<=4 independent suffix enumeration; k<=6 exhaustive prefix test with constructive lifts; k=8 sampled prefixes may repeat. Block count check uses the proved independent-factor recurrence, not full graph enumeration."}
}
console.log(JSON.stringify(direct(),null,2));
