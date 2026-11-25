function experiment(data){
 const bit=i=>1n<<BigInt(i), has=(x,i)=>(x&bit(i))!==0n, hex=x=>BigInt("0x"+(x||"0"));
 const check=(x,m)=>{if(!x)throw Error(m)};
 function init(x,ds=[]){
  const n=x.rowMap.length,p=x.pairHex.map(hex),live=x.live.slice();
  for(const d of ds){for(const i of d.removedRows||[])live[i]=false;for(const [i,h] of d.delta||[]){check((p[i]&hex(h))===hex(h),"delta not subset");p[i]&=~hex(h)}}
  const groups=x.ownerIDs.map((_,i)=>Array.from({length:n},(_,j)=>j).filter(j=>live[j]&&x.rowMap[j][0]===i));
  const all=groups.flat(); const map=new Map(all.map((r,i)=>[r,i]));
  for(const i of all)for(const j of all)check(has(p[i],j)===has(p[j],i),"asymmetry");
  return {groups:groups.map(g=>g.map(r=>map.get(r))),m:all.map(i=>all.reduce((v,j)=>has(p[i],j)?v|bit(map.get(j)):v,0n)),lifts:all.map(i=>[i])}
 }
 function close(s,c){
  let gs=s.groups.map(g=>g.slice()), changed=true;
  while(changed){changed=false;c.closurePasses++;const masks=gs.map(g=>g.reduce((m,i)=>m|bit(i),0n));for(let k=0;k<gs.length;k++){
   gs[k]=gs[k].filter(i=>{for(let j=0;j<gs.length;j++)if(j!==k){c.arcChecks++;if(!(s.m[i]&masks[j])){changed=true;c.arcRemoved++;return false}}return true});
   if(!gs[k].length){s.groups=gs;return false}
  }}
  s.groups=gs;return true
 }
 const fresh=()=>({closurePasses:0,arcChecks:0,arcRemoved:0,pairTests:0,compatible:0,dominanceTests:0,declinedCap:0,merges:0,graphTests:0});
 function candidate(s,a,b,c,cap){
  const ext=s.groups.filter((_,k)=>k!==a&&k!==b).flat().reduce((m,i)=>m|bit(i),0n);
  const arr=[];
  for(const i of s.groups[a])for(const j of s.groups[b]){c.pairTests++;if(has(s.m[i],j)){
   c.compatible++;arr.push({i,j,n:s.m[i]&s.m[j]&ext});if(arr.length>cap){c.declinedCap++;return null}
  }}
  const keep=[];
  for(let i=0;i<arr.length;i++){
   let dominated=false;
   for(let j=0;j<arr.length;j++)if(i!==j){c.dominanceTests++;if((arr[i].n&arr[j].n)===arr[i].n&&(arr[i].n!==arr[j].n||j<i)){dominated=true;break}}
   if(!dominated)keep.push(arr[i])
  }
  return {a,b,keep,raw:arr.length,delta:keep.length-s.groups[a].length-s.groups[b].length}
 }
 function merge(s,q,c){
  const gs=s.groups.filter((_,i)=>i!==q.a&&i!==q.b), old=gs.flat(), map=new Map(old.map((r,i)=>[r,i])), n=old.length;
  const m=Array(n+q.keep.length).fill(0n),lifts=old.map(r=>s.lifts[r]);
  for(let i=0;i<n;i++)for(let j=i+1;j<n;j++){c.graphTests++;if(has(s.m[old[i]],old[j])){m[i]|=bit(j);m[j]|=bit(i)}}
  for(let t=0;t<q.keep.length;t++){const z=q.keep[t],r=n+t;lifts.push([...s.lifts[z.i],...s.lifts[z.j]]);for(let j=0;j<n;j++){c.graphTests++;if(has(z.n,old[j])){m[r]|=bit(j);m[j]|=bit(r)}}}
  return {groups:[...gs.map(g=>g.map(r=>map.get(r))),q.keep.map((_,i)=>n+i)],m,lifts}
 }
 function run(s,limit=4,cap=256,allowGrowth=false){
  const c=fresh(), history=[],initial=s.groups.flat().length, bound=allowGrowth?initial*2:initial;let ok=close(s,c);
  const status=()=>!ok?"UNSAT":s.groups.length<=1?"SAT":"OPEN";
  for(let t=0;t<limit&&ok&&s.groups.length>1;t++){
   let best=null; const count=s.groups.flat().length;
   for(let a=0;a<s.groups.length;a++)for(let b=a+1;b<s.groups.length;b++){
    const q=candidate(s,a,b,c,cap);if(!q)continue;
    if(!q.keep.length){ok=false;break}
    if((allowGrowth||q.delta<=0)&&count+q.delta<=bound&&(!best||q.delta<best.delta))best=q;
   }
   if(!ok||!best)break;
   const left=s.groups[best.a].map(i=>s.lifts[i]),right=s.groups[best.b].map(i=>s.lifts[i]);
   const selected=best.keep.map(z=>[s.lifts[z.i],s.lifts[z.j]]);
   s=merge(s,best,c);c.merges++;ok=close(s,c);
   history.push({raw:best.raw,kept:best.keep.length,delta:best.delta,rows:s.groups.flat().length,left,right,selected});
  }
  if(ok)ok=close(s,c);
  return {status:status(),initial,final:s.groups.flat().length,owners:s.groups.length,c,history,s}
 }
 function exhaustive(s){let count=0;const rec=(k,chosen)=>{if(k===s.groups.length){count++;return}for(const r of s.groups[k])if(chosen.every(q=>has(s.m[r],q)))rec(k+1,[...chosen,r])};rec(0,[]);return count}
 function small(groups,compat){const n=groups.flat().length,m=Array(n).fill(0n);for(let a=0;a<groups.length;a++)for(let b=a+1;b<groups.length;b++)for(const i of groups[a])for(const j of groups[b])if(compat(a,b,i,j)){m[i]|=bit(j);m[j]|=bit(i)}return {groups,m,lifts:Array.from({length:n},(_,i)=>[i])}}
 let seed=20261125;const rand=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296};
 let controls={SAT:0,UNSAT:0,merges:0,checks:0,strict:0};
 for(let k=0;k<100;k++){const orig=small([[0,1,2],[3,4,5],[6,7,8],[9,10,11]],()=>rand()<0.58);const before=exhaustive(orig);const x=run({groups:orig.groups.map(g=>g.slice()),m:orig.m.slice(),lifts:orig.lifts},8,256,true);const after=x.status==="UNSAT"?0:exhaustive(x.s);check(!!before===!!after,"decision mismatch");controls[before?"SAT":"UNSAT"]++;controls.merges+=x.c.merges;controls.checks++;if(x.c.merges)controls.strict++;if(after){const rec=(k,chosen)=>{if(k===x.s.groups.length)return chosen;for(const r of x.s.groups[k])if(chosen.every(q=>has(x.s.m[r],q))){const z=rec(k+1,[...chosen,r]);if(z)return z}return null};const lift=rec(0,[]).flatMap(r=>x.s.lifts[r]);check(lift.length===orig.groups.length&&orig.groups.every(g=>g.filter(r=>lift.includes(r)).length===1),"lift partition");for(const i of lift)for(const j of lift)if(i!==j)check(has(orig.m[i],j),"lift pair");controls.checks++}}
 const jobs=[];
 for(let i=0;i<5;i++){
  const x=data[i],ms=data[5].jobs[i].combined,bh=data[6].jobs.find(j=>j.ref===data[5].refs[i]&&j.mode===true);
  check(!!bh,"missing BH mode");for(const [mode,ds] of [["BD18",[]],["combined",[ms,bh]]]){
   const s=init(x,ds),q=run(s,4,256,true);const {s:unused,...r}=q;jobs.push({id:x.id,guard:x.guard,mode,...r});
  }
 }
 return {seed:20261125,controls,jobs}
}
// Usage: node checker.js pairs0.json pairs1.json pairs2.json pairs3.json pairs4.json MS24.json BH18.json
if(typeof require!=="undefined"&&require.main===module){const fs=require("fs");console.log(JSON.stringify(experiment(process.argv.slice(2).map(p=>JSON.parse(fs.readFileSync(p,"utf8")))),null,2));}
