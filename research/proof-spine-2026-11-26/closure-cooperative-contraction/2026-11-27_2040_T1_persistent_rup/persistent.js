// Input: exported chart rows; use experiment(F, mode, seed), then check(F,proof).
function experiment(F0,mode,seed=[]){
 const X=[...new Set(F0.flat().map(Math.abs))].sort((a,b)=>a-b),n=X.length,ix=new Map(X.map((v,i)=>[v,i+1])),dense=c=>c.map(l=>Math.sign(l)*ix.get(Math.abs(l))),orig=c=>c.map(l=>Math.sign(l)*X[Math.abs(l)-1]),F=F0.map(dense),key=c=>c.join(","),norm=c=>c.slice().sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b),seen=new Set(F.map(c=>key(norm(c)))),idx=Array.from({length:2*n+1},()=>[]),proof=[],states=new Map();
 let m={probes:0,candidates:0,epochs:0,literal:0,rowTests:0,assignments:0,newRows:0,cacheHits:0,failed:0,seedAccepted:0,seedRejected:0,peakStates:0,initialForced:0};
 function index(c,i){for(let l of c)idx[l+n].push(i)}F.forEach(index);
 function query(c,cache){
  m.probes++;let k=key(c),s=cache?states.get(k):null;
  if(!s){s={a:new Int8Array(n+1),at:0};if(cache){states.set(k,s);m.peakStates=Math.max(m.peakStates,states.size)}}else m.cacheHits++;
  let queue=[],head=0,conf=false;
  function put(l){let i=Math.abs(l),b=Math.sign(l);if(s.a[i]===-b){conf=true;return}if(!s.a[i]){s.a[i]=b;queue.push(l);m.assignments++}}
  function test(row){m.rowTests++;let u=0,num=0;for(let l of row){m.literal++;let a=s.a[Math.abs(l)]*Math.sign(l);if(a===1)return;if(!a){u=l;num++}}if(!num)conf=true;else if(num===1)put(u)}
  if(s.at===0)for(let l of c)put(-l);
  for(let i=s.at;i<F.length&&!conf;i++){m.newRows++;test(F[i])}
  while(head<queue.length&&!conf){let l=queue[head++];for(let j of idx[n-l]){test(F[j]);if(conf)break}}
  s.at=F.length;
  if(conf){if(cache)states.delete(k);return true}
  if(c.length===0&&proof.length===0)m.initialForced=s.a.reduce((a,b)=>a+Number(b!==0),0);
  m.failed++;return false
 }
 function admit(c){seen.add(key(c));proof.push(orig(c));index(c,F.length);F.push(c)}
 const cache=mode!=="fresh";
 if(query([],cache)){admit([]);return {status:"NO",m,proof,n}}
 for(let q of seed){let c=norm(dense(q));if(c.some(l=>!l)||seen.has(key(c)))continue;if(query(c,cache)){admit(c);m.seedAccepted++}else m.seedRejected++}
 const candidates=[];for(let i=1;i<=n;i++)for(let s of [-1,1])candidates.push([s*i]);for(let i=1;i<=n;i++)for(let j=i+1;j<=n;j++)for(let s of [-1,1])for(let t of [-1,1])candidates.push([s*i,t*j]);
 for(;;){m.epochs++;let change=false;for(let c of candidates){m.candidates++;if(seen.has(key(c)))continue;if(query(c,cache)){admit(c);change=true;if(query([],cache)){admit([]);return {status:"NO",m,proof,n}}}}if(!change)return {status:"STALL",m,proof,n}}
}
function check(F,proof){let rows=F.slice(),vis=0;for(let c of proof){let A=new Set(c.map(l=>-l)),conf=false,change=true;while(change&&!conf){change=false;for(let row of rows){let u=0,k=0,s=false;for(let l of row){vis++;if(A.has(l)){s=true;break}if(!A.has(-l)){k++;u=l}}if(s)continue;if(k===0){conf=true;break}if(k===1&&!A.has(u)){A.add(u);change=true}}}if(!conf)throw Error("invalid RUP "+JSON.stringify(c));rows.push(c)}return {vis,steps:proof.length,empty:proof.at(-1)?.length===0}}
module.exports={experiment,check};
