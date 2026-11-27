function auditSourceOnly(){
 const check=(x,m)=>{if(!x)throw Error(m)};
 function top(x){return x.toString(2).length-1}
 function insert(B,x){while(x){const j=top(x);if(B[j])x^=B[j];else{B[j]=x;return true}}return false}
 function parity(x){let p=0;while(x){x&=x-1n;p^=1}return p}
 function nullspace(B,d){const ans=[];for(let j=0;j<d;j++)if(!B[j]){let v=1n<<BigInt(j);for(let k=0;k<d;k++)if(B[k]&&parity(B[k]&v))v|=1n<<BigInt(k);ans.push(v)}return ans}
 const evalCache=new Map();
 function evaluations(w,D){const key=w+":"+D;if(evalCache.has(key))return evalCache.get(key);const mons=[0];for(let i=0;i<w;i++)mons.push(1<<i);if(D===2)for(let i=0;i<w;i++)for(let j=i+1;j<w;j++)mons.push((1<<i)|(1<<j));
 const val=Array.from({length:1<<w},(_,x)=>{let p=0n;for(let k=0;k<mons.length;k++)if((x&mons[k])===mons[k])p|=1n<<BigInt(k);return p});const ans={mons,val};evalCache.set(key,ans);return ans}
 // Generator only. The solver below receives just group scopes and forbidden words.
 function source(n,r){const q=3*n;const mod=i=>(i+q)%q;const a=i=>2*mod(i),b=i=>2*mod(i)+1;
 const groups=[...Array.from({length:n},(_,i)=>[i,i+n,i+2*n]),...Array.from({length:n},(_,i)=>[i,(i-1+n)%n+n,(i-2+n)%n+2*n])];
 return groups.map(E=>{let S=[...new Set(E.flatMap(i=>[a(i),a(i+1),b(i),b(i+1),b(i+2)]))].filter(v=>v%2===0||(v>>1)<r).sort((x,y)=>x-y);
 const forbidden=[];for(let word=0;word<(1<<S.length);word++){const bit=v=>{let j=S.indexOf(v);return j<0?0:(word>>j)&1};const h=i=>bit(a(i))^(bit(b(i))&bit(b(i+1)));if(E.reduce((sum,i)=>sum+(h(i)^h(i+1)),0)!==1)forbidden.push(word)}return {S,forbidden}})}
 function solve(groups,D){
 const monIndex=new Map([["",0]]);const global=[];let acquired=0,truthRows=0,sourceClauses=0,certifiedGroups=0;const widths=[];
 for(const {S,forbidden} of groups){
   const w=S.length;check(w<=15,"width cap");const bad=new Set(forbidden);check(bad.size===forbidden.length,"duplicates");sourceClauses+=bad.size;
   const {mons,val}=evaluations(w,D),local=[];for(let i=0;i<val.length;i++)if(!bad.has(i)){insert(local,val[i]);truthRows++}
   const cons=nullspace(local,mons.length);widths.push({w,rank:local.filter(Boolean).length,consequences:cons.length});
   // Independent certificate check: every acquired consequence vanishes on every allowed word.
   for(const f of cons){for(let i=0;i<val.length;i++)if(!bad.has(i))check(parity(f&val[i])===0,"bad local certificate");let row=0n;
    for(let k=0;k<mons.length;k++)if((f>>BigInt(k))&1n){let ids=[];for(let j=0;j<w;j++)if(mons[k]&(1<<j))ids.push(S[j]);let key=ids.join(",");if(!monIndex.has(key))monIndex.set(key,monIndex.size);row|=1n<<BigInt(monIndex.get(key))}
    acquired++;insert(global,row);
   }certifiedGroups++;
 }
 return {degree:D,sourceClauses,truthRows,acquired,globalRank:global.filter(Boolean).length,globalColumns:monIndex.size,contradiction:global[0]===1n,certifiedGroups,widths};
 }
 const jobs=[];for(const [n,r] of [[5,0],[5,7],[5,15],[7,21]]){const G=source(n,r);const A=solve(G,1),B=solve(G,2);check(B.contradiction,"quadratic failed");if(r>0)check(!A.contradiction,"linear unexpectedly complete");jobs.push({n,r,A,B})}
 return {method:"bounded-width source-only local truth-table kernel; global GF2 coefficient span, no decoder passed to solver",jobs};
}
console.log(JSON.stringify(auditSourceOnly(),null,2));
