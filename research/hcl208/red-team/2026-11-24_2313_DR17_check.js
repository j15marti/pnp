
function experiment(peer) {
 let seed=20261124, draws=0; function rng(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;draws++;return seed/4294967296}
 const n=36,d=0,x=Array.from({length:n},(_,i)=>+(i>=18)),y=x.map((v,i)=>v^(i===d));
 const sh=a=>{a=a.slice();for(let i=a.length-1;i>0;i--){let j=Math.floor(rng()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a};
 const ok=(w,t)=>t.some(i=>w[i]!==w[t[0]]);
 const minority=(w,t)=>t.find(i=>t.filter(j=>w[j]===w[i]).length===1);
 const pair=(a,b)=>Math.min(a,b)*n+Math.max(a,b);
 let tries=0,registry=null;
 for(;tries<2000&&!registry;tries++){
  let used=new Set(),covered=new Set(),O=[];
  for(let p=0;p<4;p++){
   let w=p<2?x:y, zero=w.map((v,i)=>v===0?i:-1).filter(i=>i>=0),one=w.map((v,i)=>v===1?i:-1).filter(i=>i>=0),a=one.length-n/3,b=n/3-a, found=null;
   for(let k=0;k<200&&!found;k++){
    const select=(arr,c)=>sh(arr.filter(i=>i!==d)).sort((i,j)=>Number(covered.has(i))-Number(covered.has(j))).slice(0,c);
    let zmin=select(zero,a-Number(w[d]===0)),omin=select(one,b-Number(w[d]===1));
    (w[d]===0?zmin:omin).push(d);
    let zm=sh(zero.filter(i=>!zmin.includes(i))),om=sh(one.filter(i=>!omin.includes(i)));
    let T=[...zmin.map(i=>[i,om.pop(),om.pop()]),...omin.map(i=>[i,zm.pop(),zm.pop()])];
    if(T.some(t=>t.some(i=>i===undefined)||[[0,1],[0,2],[1,2]].some(([i,j])=>used.has(pair(t[i],t[j])))))continue;
    found=T;
   }
   if(!found)break;
   for(const t of found){O.push({p,t});covered.add(minority(w,t));for(let i=0;i<3;i++)for(let j=i+1;j<3;j++)used.add(pair(t[i],t[j]))}
  }
  if(O.length===48&&covered.size===n)registry=O;
 }
 if(!registry)throw Error("no construction");
 let O=registry;
 function closure(O,w){let scans=0,forces=0;w=w.slice();while(true){let ch=false;for(const {t} of O){scans++;let a=t.filter(i=>w[i]===0),b=t.filter(i=>w[i]===1),u=t.filter(i=>w[i]===-1);if(a.length===3||b.length===3)return {w:null,scans,forces};if(u.length===1&&(a.length===2||b.length===2)){w[u[0]]=a.length===2?1:0;ch=true;forces++}}if(!ch)return {w,scans,forces}}}
 let nodes=0,scans=0,forces=0;
 function solve(w){if(++nodes>100000)return null;let c=closure(O,w);scans+=c.scans;forces+=c.forces;if(!c.w)return null;w=c.w;let j=w.indexOf(-1);if(j<0)return w;for(let v of [0,1]){let z=w.slice();z[j]=v;let r=solve(z);if(r)return r}return null}
 const root=closure(O,Array(n).fill(-1));let witness=solve(Array(n).fill(-1));if(!witness||!O.every(o=>ok(witness,o.t)))throw Error("no SAT witness");
 function analyze(O,x,y,k,pin){
  let A=O.filter(o=>o.p===0||o.p===k),B=O.filter(o=>o.p!==0&&o.p!==k),d=x.findIndex((v,i)=>v!==y[i]);
  if(!A.every(o=>ok(x,o.t))||!B.every(o=>ok(y,o.t))||x.filter((v,i)=>v!==y[i]).length!==1)throw Error("bad start");
  const flip=(w,J)=>w.map((v,i)=>v^Number(J.includes(i)));
  const check=(a,b)=>A.every(o=>ok(a,o.t))&&B.every(o=>ok(b,o.t))&&(pin<0||(a[0]===pin&&b[0]===pin));
  let one=[],joint=[],two=[],checks=0;
  for(let s=0;s<2;s++)for(let j=-1;j<n;j++){if(j===d)continue;let J=j<0?[d]:[d,j],a=s===0?flip(x,J):x,b=s===1?flip(y,J):y;checks++;if(check(a,b))one.push({s,j});}
  for(let i=0;i<n;i++){if(i===d)continue;checks++;if(check(flip(x,[i]),flip(y,[i])))joint.push(i);
   for(let j=i+1;j<n;j++){if(j===d)continue;checks++;if(check(flip(x,[i,j]),flip(y,[i,j])))two.push([i,j])}}
  return {d,one,joint,two,checks,blockA:A.filter(o=>minority(x,o.t)===d).length,blockB:B.filter(o=>minority(y,o.t)===d).length,cover:[...new Set([...A.map(o=>minority(x,o.t)),...B.map(o=>minority(y,o.t))])].sort((a,b)=>a-b)};
 }
 let hostile=analyze(O,x,y,1,-1);
 if(hostile.one.length||hostile.joint.length||hostile.cover.length!==n)throw Error("not isolated");
 const bits=s=>Array.from({length:n},(_,i)=>Number((BigInt(s)>>BigInt(i))&1n));
 let same=peer.jobs.map(j=>{let a=analyze(peer.owners,bits(j.x),bits(j.y),j.k,j.pin);return {k:j.k,pin:j.pin,unilateral:a.one.length,common1:a.joint.length,common2:a.two.length,checks:a.checks}});
 const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
 const fcount=T=>Array.from({length:128},(_,z)=>Array.from({length:7},(_,i)=>(z>>i)&1)).filter(w=>T.every(t=>ok(w,t))).length;
 let controls={fano:fcount(fano),deleted:fano.map((_,i)=>fcount(fano.filter((_,j)=>i!==j)))};
 return {seed:20261124,tries,draws,registry:O,x,y,witness,rootClosure:root,reference:{nodes,scans,forces},hostile,same,controls};
}

if(require.main===module){const fs=require("fs");console.log(JSON.stringify(experiment(JSON.parse(fs.readFileSync(process.argv[2],"utf8"))),null,2));}
