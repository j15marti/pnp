// C04-08 independent finite certificate, no external libraries.
// Bit j is the jth lexicographic unordered pair of five ports.
const E=[];for(let i=0;i<5;i++)for(let j=i+1;j<5;j++)E.push([i,j]);
const U=1023;
function perm(xs){if(!xs.length)return [[]];return xs.flatMap((x,i)=>perm(xs.filter((_,j)=>j!==i)).map(p=>[x,...p]));}
const P=perm([0,1,2,3,4]);
function bit(i,j){return 1<<E.findIndex(([a,b])=>a===Math.min(i,j)&&b===Math.max(i,j));}
function rename(s,p){let t=0;E.forEach(([i,j],k)=>{if(s&(1<<k))t|=bit(p[i],p[j]);});return t;}
function count(s){let t=0;while(s){s&=s-1;t++;}return t;}
const C=new Set();for(let k=3;k<=5;k++)for(const p of P){let m=0;for(let i=0;i<k;i++)m|=bit(p[i],p[(i+1)%k]);C.add(m);}
function core(s){let q=0;for(const c of C)if(!(s&c))q|=c;return q;}
function admissible(s){if(!s)return false;const d=[0,0,0,0,0];E.forEach(([i,j],k)=>{if(s&(1<<k)){d[i]++;d[j]++;}});return !d.includes(1);}
function verify(x,msg){if(!x)throw Error(msg);}
function support({edges,ports,free=[]}){ // enumerate actual indexed edge colors and free-wire values.
 let A=edges.map(e=>e.slice()),ids=Array(5).fill(-1);
 for(let i=0;i<5;i++)if(ports[i]!==null){ids[i]=A.length;A.push([ports[i],-i-1]);}
 for(const [i,j] of free){ids[i]=ids[j]=A.length;A.push([-i-1,-j-1]);}
 let mask=0,used=new Map(),w=[];
 function dfs(k){if(k===A.length){let b=ids.map(i=>w[i]),s=b.map((c,i)=>b.filter(x=>x===c).length===1?i:-1).filter(i=>i>=0);verify(s.length===2,'parity');mask|=bit(...s);return;}
  const [u,v]=A[k];for(let c=1;c<=3;c++){const b=1<<c,x=used.get(u)||0,y=used.get(v)||0;if((x|y)&b)continue;used.set(u,x|b);used.set(v,y|b);w[k]=c;dfs(k+1);used.set(u,x);used.set(v,y);}
 }dfs(0);return mask;
}
const reps={
 127:{edges:[],ports:[null,null,0,0,0],free:[[0,1]]},
 207:{edges:[[0,1],[1,2]],ports:[1,0,2,2,0]},
 220:{edges:[[0,1],[1,2],[2,3],[3,4],[4,0]],ports:[3,2,4,1,0]},
 0:{edges:[[1,2],[1,0],[4,1],[6,3],[5,0],[5,4],[6,0],[3,2]],ports:[2,4,3,6,5]},
 54:{edges:[[0,6],[0,3],[2,5],[3,1],[2,1],[2,6],[4,5],[3,4]],ports:[5,0,4,6,1]},
 19:{edges:[[0,6],[1,4],[4,3],[2,4],[2,1],[5,3],[6,3],[5,0]],ports:[5,0,6,2,1]}
};
const capSupports={},R=new Map(),cyclesRealized=new Set();
for(const [qs,cap] of Object.entries(reps)){let q=Number(qs),s=support(cap);verify(admissible(s)&&core(s)===q,'cap signature');capSupports[q]=s;for(const p of P)R.set(rename(q,p),rename(s,p));if([127,207,220].includes(q))for(const p of P)cyclesRealized.add(rename(s,p));}
verify(C.size===37&&cyclesRealized.size===C.size&&[...C].every(c=>cyclesRealized.has(c)),'cycle caps');
const V=Array.from({length:1023},(_,i)=>i+1).filter(admissible);
let pairs=0;
for(const s of V){let q=core(s),r=R.get(q);verify(r!==undefined&&admissible(r),'catalog coverage');for(const t of V){verify(Boolean(s&t)===Boolean(r&t),'joint compatibility');pairs++;}}
let tariff=0;for(let n=18;n<=300;n+=2)for(let s=9;2*s<=n;s+=2){verify(38n*BigInt(s+5)**32n+BigInt(n-s+7)**32n<BigInt(n)**32n,'tariff');tariff++;}
const result={admissible:V.length,cycleCaps:C.size,signatures:R.size,capSupports,compatibilityPairs:pairs,tariffChecks:tariff};
if(typeof text==='function')text(result);else console.log(JSON.stringify(result,null,2));
