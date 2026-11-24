const check = function check(){
 const M={assertions:0,leafTuples:0,meetTuples:0,gadgetRims:0,rimDP:0,arcSweeps:0,arcTests:0,dpTransitions:0,referenceRims:0,referenceVisits:0,treeNodes:0,pinChecks:0,sourceClosureSweeps:0,sourcePins:0,sourceNodes:0,sourceReferenceWords:0,sourceWitnesses:0};
 const ok=(x)=>{M.assertions++;if(!x)throw Error("assertion "+M.assertions)};
 let seed=20261124;const rand=n=>{seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return (seed>>>0)%n};
 const bit=(x,j)=>(x>>j)&1, parity=x=>bit(x,0)^bit(x,1), orth=d=>d===1?2:d===2?1:3;
 const meet=(p,q)=>p===q?p:0;
 const leaf=(a,b,c,s)=>{const d=a^b,k=a^c^s;return d&&(k===0||k===d)?d:0};
 function rim(a,b,s,lift=false){
  M.rimDP++;const n=a.length,dom=a.map((x,i)=>[0,1,2,3].filter(y=>y!==x&&y!==b[i]));
  let changed=true;while(changed){changed=false;M.arcSweeps++;for(let i=0;i<n;i++)for(const j of [(i+n-1)%n,(i+1)%n]){
    const shift=j===(i+1)%n?s[i]:s[j];const d=dom[i].filter(x=>{M.arcTests++;return dom[j].some(y=>(x^y)!==shift)});if(d.length!==dom[i].length){dom[i]=d;changed=true}if(!d.length)return null;
  }}
  for(const f of dom[0]){let states=new Map([[f,[f]]]);for(let i=1;i<n;i++){const next=new Map();for(const [x,path] of states)for(const y of dom[i]){M.dpTransitions++;if((x^y)!==s[i-1]&&!next.has(y))next.set(y,lift?[...path,y]:[])}states=next}
   for(const [x,path] of states)if((x^f)!==s[n-1])return lift?path:[];
  }return null
 }
 function verify(a,b,s,w){return w&&w.length===a.length&&w.every((x,i)=>x!==a[i]&&x!==b[i]&&(x^w[(i+1)%w.length])!==s[i])}
 function brute(a,b,s){M.referenceRims++;let count=0;const p=[];function rec(i){M.referenceVisits++;if(i===a.length){if((p[i-1]^p[0])!==s[i-1])count++;return}for(let x=0;x<4;x++)if(x!==a[i]&&x!==b[i]&&(!i||(x^p[i-1])!==s[i-1])){p[i]=x;rec(i+1)}}rec(0);return count}
 function eventWheel(rows){let n=rows.length+1;if(!(n&1))n++;n=Math.max(n,3);let a=Array(n).fill(0),b,s=Array(n).fill(0);for(let i=0;i<rows.length;i++)a[i+1]=rows[i]?0:2;b=a.map(x=>x^1);M.gadgetRims++;const w=rim(a,b,s,true);ok((w===null)===rows.every(Boolean));if(w)ok(verify(a,b,s,w));return w!==null}
 function leafEvents(a,b,c,s,t){const out=[];for(let d=1;d<4;d++){const E=[bit(a^b,0)===bit(d,0),bit(a^b,1)===bit(d,1),parity((a^c^s)&orth(d))===0];for(const e of E)out.push([bit(t,0)===bit(d,0),bit(t,1)===bit(d,1),!e]);for(let j=0;j<2;j++)out.push([...E,bit(t,j)!==bit(d,j)])}return out}
 function meetEvents(p,q,t){const out=[];for(let d=1;d<4;d++){const E=[bit(p,0)===bit(d,0),bit(p,1)===bit(d,1),bit(q,0)===bit(d,0),bit(q,1)===bit(d,1)];for(const e of E)out.push([bit(t,0)===bit(d,0),bit(t,1)===bit(d,1),!e]);for(let j=0;j<2;j++)out.push([...E,bit(t,j)!==bit(d,j)])}return out}
 for(let a=0;a<4;a++)for(let b=0;b<4;b++)for(let c=0;c<4;c++)for(let s=0;s<4;s++)for(let t=0;t<4;t++){M.leafTuples++;const e=leafEvents(a,b,c,s,t).map(eventWheel);ok(e.every(Boolean)===(t===leaf(a,b,c,s)))}
 for(let p=0;p<4;p++)for(let q=0;q<4;q++)for(let t=0;t<4;t++){M.meetTuples++;const e=meetEvents(p,q,t).map(eventWheel);ok(e.every(Boolean)===(t===meet(p,q)))}
 function build(a,b,s,l=0,r=a.length){M.treeNodes++;if(r-l===1)return {l,r,t:leaf(a[l],b[l],a[(l+1)%a.length],s[l])};const m=(l+r)>>1,L=build(a,b,s,l,m),R=build(a,b,s,m,r);return {l,r,t:meet(L.t,R.t),L,R}}
 function nodes(x){return x.L?[x,...nodes(x.L),...nodes(x.R)]:[x]}
 function bad(t,s){return t!==0&&s.reduce((a,b)=>a^b,0)===((s.length&1)?0:t)}
 function pinFormula(a,b,s,x,d){const E=k=>{for(let i=x.l;i<x.r;i++)if((a[i]^b[i])!==k||!([0,k].includes(a[i]^a[(i+1)%a.length]^s[i])))return false;return true};return d?E(d):![1,2,3].some(E)}
 const fixed={SAT:0,UNSAT:0};
 function fixedCase(a,b,s,ref){const x=build(a,b,s),w=rim(a,b,s,true);const v=!bad(x.t,s);ok(v===(w!==null));if(w)ok(verify(a,b,s,w));if(ref)ok(v===(brute(a,b,s)>0));fixed[v?"SAT":"UNSAT"]++;for(const u of nodes(x))for(let d=0;d<4;d++){M.pinChecks++;ok(pinFormula(a,b,s,u,d)===(u.t===d))}}
 for(let x=0;x<4096;x++){const a=[x&3,(x>>2)&3,(x>>4)&3],b=[(x>>6)&3,(x>>8)&3,(x>>10)&3];fixedCase(a,b,[0,0,0],true)}
 for(let i=0;i<500;i++){const n=3+rand(6),a=Array.from({length:n},()=>rand(4)),b=a.map(()=>rand(4)),s=a.map(()=>rand(4));fixedCase(a,b,s,true)}
 const scales=[];for(const n of [5,17,65,129,513,128]){let a=Array(n).fill(0),b=a.map(()=>1),s=a.map(()=>0);if(!(n&1))s[n-1]=1;fixedCase(a,b,s,false);ok(bad(build(a,b,s).t,s));b[0]=0;fixedCase(a,b,s,false);ok(!bad(build(a,b,s).t,s));scales.push(n)}
 function blockRim(clauses,word){let a=[],b=[];for(const C of clauses){const vals=C.map(([i,v])=>bit(word,i)===v?1:0);a.push(0,...vals.map(v=>2*v))}a.push(0);if(!clauses.length)a.push(0,0);b=a.map(x=>x^1);b[b.length-1]=0;const s=a.map(()=>0);let blocks=[];for(let j=0;j<clauses.length;j++)blocks.push(build(a,b,s,4*j,4*j+4));let t=leaf(a[a.length-1],b[b.length-1],a[0],0);for(const u of blocks)t=meet(t,u.t);ok(t===build(a,b,s).t);return {a,b,s,blocks,root:t}}
 function sourceSat(C,w){return C.every(c=>c.some(([i,v])=>bit(w,i)===v))}
 function solve(C,n){const rec=as=>{M.sourceNodes++;let again=true;while(again){M.sourceClosureSweeps++;again=false;for(const c of C){if(c.some(([i,v])=>as[i]===v))continue;const u=c.filter(([i])=>as[i]===-1);if(!u.length)return null;if(u.length===1){as[u[0][0]]=u[0][1];M.sourcePins++;again=true;break}}}
  const i=as.indexOf(-1);if(i<0)return as.reduce((w,b,j)=>w|(b<<j),0);for(let b=0;b<2;b++){const z=as.slice();z[i]=b;const w=rec(z);if(w!==null)return w}return null};return rec(Array(n).fill(-1))}
 const source={SAT:0,UNSAT:0,unpinnedAlwaysSAT:0,neighborCounts:[]};
 function sourceCase(C,n,isFano=false){let count=0;for(let w=0;w<(1<<n);w++){M.sourceReferenceWords++;const z=blockRim(C,w);const accepted=z.blocks.every(x=>x.t===0);ok(accepted===sourceSat(C,w));ok(!bad(z.root,z.s));if(accepted)count++}
  const w=solve(C,n);ok((w!==null)===(count>0));if(w!==null){M.sourceWitnesses++;const z=blockRim(C,w);ok(z.blocks.every(x=>x.t===0));const path=rim(z.a,z.b,z.s,true);ok(verify(z.a,z.b,z.s,path));source.SAT++}else source.UNSAT++;
  source.unpinnedAlwaysSAT++;if(isFano)source.neighborCounts.push(count)
 }
 const cube=Array.from({length:8},(_,i)=>[0,1,2].map(j=>[j,bit(i,j)]));
 for(let mask=0;mask<256;mask++)sourceCase(cube.filter((_,i)=>bit(mask,i)),3);
 const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]].flatMap(c=>[0,1].map(v=>c.map(i=>[i,v])));
 sourceCase(fano,7,true);for(let i=0;i<14;i++)sourceCase(fano.filter((_,j)=>i!==j),7,true);
 return {seed:20261124,fixed,scales,source,ledger:M}
};
console.log(JSON.stringify(check(), null, 2));
