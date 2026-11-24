"use strict";
function main(){
 const stats={gauss:0,xors:0,closureScans:0,rowTests:0,deletions:0,subspaceEdges:0,latticePairs:0,refWords:0,refRepairTuples:0,witnesses:0,assertions:0};
 const ok=(x)=>{stats.assertions++;if(!x)throw Error("assert "+stats.assertions)};
 const bit=i=>1n<<BigInt(i);
 const parity=x=>{let p=0;while(x){p^=1;x&=x-1n}return p};
 const ev=(f,z)=>parity(f[0]&z)^f[1];
 const eq=(f,b)=>[f[0],f[1]^b];
 const add=(f,g)=>[f[0]^g[0],f[1]^g[1]];
 function count(d,rows){stats.gauss++;let piv=new Map();for(let [m,b] of rows){while(m){let k=m.toString(2).length-1;if(!piv.has(k)){piv.set(k,[m,b]);break}let v=piv.get(k);m^=v[0];b^=v[1];stats.xors++}if(!m&&b)return 0n}return bit(d-piv.size)}
 const dot=(a,b)=>parity(BigInt(a&b));
 function span(vs){let s=new Set([0]);for(let h of vs)for(let x of [...s])s.add(x^h);return s}
 function spaces(r){let all=[new Set([0])],seen=new Set(["0"]);for(let i=0;i<all.length;i++)for(let h=1;h<(1<<r);h++){stats.subspaceEdges++;if(all[i].has(h))continue;let s=span([...all[i],h]),k=[...s].sort((a,b)=>a-b).join(",");if(!seen.has(k)){seen.add(k);all.push(s)}}return all.sort((a,b)=>a.size-b.size)}
 const cache=new Map();function lattice(r){if(!cache.has(r))cache.set(r,spaces(r));return cache.get(r)}
 function aeq(a,l,b=0){let f=[0n,0];for(let j=0;j<a.length;j++)if(l>>j&1)f=add(f,a[j]);return eq(f,b)}
 function close(d,r,s,h,a,guards){
  let masks=s.map(()=>7),n=d+s.length;
  while(true){stats.closureScans++;let rows=guards.slice();
   for(let j=0;j<r;j++){let f=a[j].slice();for(let i=0;i<h.length;i++)if(h[i]>>j&1)f[0]^=bit(d+i);rows.push(eq(f,0))}
   for(let i=0;i<s.length;i++){let e=[bit(d+i),0],m=masks[i];if(m!==7)for(let k=1;k<4;k++){let vals=[];for(let j=0;j<3;j++)if(m>>j&1)vals.push(((k&1)?+(j!==0):0)^((k&2)?+(j===2):0));if(vals.every(v=>v===vals[0]))rows.push(eq(add((k&1)?s[i]:[0n,0],(k&2)?e:[0n,0]),vals[0]))}}
   if(!count(n,rows))return null;
   let change=false;outer:for(let i=0;i<s.length;i++)for(let j=0;j<3;j++)if(masks[i]>>j&1){stats.rowTests++;if(!count(n,[...rows,eq(s[i],+(j!==0)),[bit(d+i),+(j===2)]])){masks[i]^=1<<j;stats.deletions++;if(!masks[i])return null;change=true;break outer}}
   if(!change)break;
  }
  let b=a.map(f=>f.slice()),g=guards.slice(),ss=[],hh=[];
  for(let i=0;i<s.length;i++){let m=masks[i],f=s[i];if(m===1)g.push(eq(f,0));if(m===2||m===4||m===6)g.push(eq(f,1));if(m===4||m===5)for(let j=0;j<r;j++)if(h[i]>>j&1)b[j]=add(b[j],m===4?[0n,1]:f);if(m===7||m===6){ss.push(m===6?[0n,1]:f);hh.push(h[i])}}
  return {s:ss,h:hh,a:b,g,masks};
 }
 function project(d,r,s,h,a,g=[]){
  let c=close(d,r,s,h,a,g);if(!c)return 0n;
  let all=lattice(r),answer=0n;
  for(let W of all){let sub=all.filter(U=>[...U].every(v=>W.has(v))),hist=[];
   let target=[];for(let l=1;l<(1<<r);l++)if([...W].every(v=>!dot(l,v)))target.push(aeq(c.a,l));
   for(let U of sub){stats.latticePairs++;let rows=[...c.g,...target];for(let i=0;i<c.h.length;i++)if(!U.has(c.h[i]))rows.push(eq(c.s[i],0));
    let z=count(d,rows);for(let j=0;j<hist.length;j++)if([...sub[j]].every(v=>U.has(v)))z-=hist[j];ok(z>=0n);hist.push(z)
   }answer+=hist[hist.length-1]
  }return answer
 }
 function ref(d,r,s,h,a,g){let total=0n,full=0n;for(let z=0n;z<bit(d);z++){stats.refWords++;if(g.some(([m,b])=>parity(m&z)!==b))continue;let active=h.filter((_,i)=>ev(s[i],z)),t=a.reduce((v,f,j)=>v|(ev(f,z)<<j),0),ways=0;
  for(let e=0;e<(1<<active.length);e++){stats.refRepairTuples++;let x=0;for(let i=0;i<active.length;i++)if(e>>i&1)x^=active[i];if(x===t)ways++}if(ways)total++;full+=BigInt(ways)
 }return [total,full]}
 let seed=20261124;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>8)%n}
 let sat=0,unsat=0,random=120;for(let k=0;k<random;k++){let d=1+rnd(5),r=1+rnd(4),m=1+rnd(7),form=()=>[BigInt(rnd(1<<d)),rnd(2)],s=Array.from({length:m},form),h=s.map(()=>1+rnd((1<<r)-1)),a=Array.from({length:r},form),g=k%3===0?[eq(form(),rnd(2))]:[];
 let v=project(d,r,s,h,a,g),[w]=ref(d,r,s,h,a,g);ok(v===w);if(v){sat++;let pins=g.slice();for(let i=0;i<d;i++){let p=[bit(i),0];if(!project(d,r,s,h,a,[...pins,p]))p[1]=1;pins.push(p)}let [yes]=ref(d,r,s,h,a,pins);ok(yes===1n);stats.witnesses++}else unsat++}
 let hostile=[];for(let t=0;t<4;t++){let s=[[1n,0],[1n,0],[1n,1],[1n,1]],h=[1,1,2,2],a=[[0n,t&1],[0n,t>>1]],v=project(1,2,s,h,a);ok(v===BigInt(t===0?2:t===3?0:1));hostile.push(Number(v))}
 // Exact hard-count compiler identity. Count via independent row-by-row DP, not claimed polynomial in arbitrary chart size.
 function hard(n,clauses,K){let s=[];for(let c of clauses)for(let mask=1;mask<8;mask++){let f=[0n,0];for(let j=0;j<3;j++)if(mask>>j&1){let lit=c[j];f=add(f,[bit(Math.abs(lit)-1),+(lit<0)])}for(let k=0;k<K;k++)s.push(f)}
 let z1=0n,models=0,proj=0;for(let z=0n;z<bit(n);z++){stats.refWords++;let sat=clauses.every(c=>c.some(l=>ev([bit(Math.abs(l)-1),+(l<0)],z)));models+=+sat;let even=1n,odd=0n;for(let f of s)if(ev(f,z)){let a=even+odd;even=a;odd=a}z1+=odd;if(odd)proj++}
 let decoded=(2n*z1)>>BigInt(4*K*clauses.length);ok(decoded===BigInt(models));return {models,projected:proj,rows:s.length,countBits:z1.toString(2).length}}
 let cube=Array.from({length:8},(_,k)=>[1,2,3].map((v,i)=>k>>i&1?-v:v));
 let cubeControls=[];for(let k=-1;k<8;k++)cubeControls.push(hard(3,cube.filter((_,i)=>i!==k),4));
 ok(cubeControls[0].models===0&&cubeControls.slice(1).every(x=>x.models===1));
 let fano=[[1,2,3],[1,4,5],[1,6,7],[2,4,6],[2,5,7],[3,4,7],[3,5,6]].flatMap(c=>[c,c.map(x=>-x)]);
 let fanoControls=[];for(let k=-1;k<14;k++)fanoControls.push(hard(7,fano.filter((_,i)=>i!==k),8));
 ok(fanoControls[0].models===0&&fanoControls.slice(1).every(x=>x.models===5));
 // Small direct tuple verification of the full-count identity.
 let small=hard(3,[[1,2,3]],4);let [p,z]=ref(3,1,Array.from({length:7},(_,k)=>[BigInt(k+1),0]),Array(7).fill(1),[[0n,1]],[]);ok(p===7n&&z===56n);
 return {seed:20261124,random,sat,unsat,hostile,cubeControls,fanoControls,small,stats,latticeSizes:[0,1,2,3,4].map(r=>lattice(r).length)}
}
console.log(JSON.stringify(main(),null,2));
