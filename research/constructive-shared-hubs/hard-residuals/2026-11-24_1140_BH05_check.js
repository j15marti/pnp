/* BH05 exact signed NAE projection. Run: node 2026-11-24_1140_BH05_check.js */
function experiment(){
 const assert=(b,m)=>{if(!b)throw Error(m)}, abs=Math.abs;
 const norm=a=>{let s=new Set(a);for(let l of s)if(s.has(-l))return null;let c=[...s].sort((a,b)=>abs(a)-abs(b)||a-b);return c[0]<0?c.map(l=>-l):c};
 const value=(l,x)=>x[abs(l)]^(l<0?1:0);
 const ok=(a,x)=>a.length>1&&a.some(l=>value(l,x)!==value(a[0],x));
 let tally={cases:0,SAT:0,UNSAT:0,UNKNOWN:0,referenceAssignments:0,verifiedWitnesses:0,sourceChecks:0,closurePasses:0,binaryDeductions:0,consensusDeductions:0,normalizations:0,eliminations:0,pairAttempts:0,failedCandidates:0,consensusKeys:0,maxActive:0,maxArchiveLiterals:0};
 function project(n,source,pins={},protect=[],cap=source.length){
   const A=n+1,P=new Set([A,...protect]),archive=[];let ac=0;
   const s={closurePasses:0,binaryDeductions:0,consensusDeductions:0,normalizations:0,eliminations:0,pairAttempts:0,failedCandidates:0,consensusKeys:0,maxActive:0,maxArchiveLiterals:0,peakArity:0,sourceChecks:0};
   const pin=l=>Object.prototype.hasOwnProperty.call(pins,abs(l))?((pins[abs(l)]^(l<0?1:0))?-A:A):l;
   let F=source.map(c=>c.map(pin));
   const save=(v,rows)=>{archive.push([v,rows]);ac+=rows.reduce((a,c)=>a+c.length,0);s.maxArchiveLiterals=Math.max(s.maxArchiveLiterals,ac)};
   function canonical(rows){const M=new Map();for(let row of rows){s.normalizations++;let c=norm(row);if(c===null)continue;if(c.length<2)return [c];M.set(c.join(","),c)}return [...M.values()]}
   function observe(){s.maxActive=Math.max(s.maxActive,F.length);for(let c of F)s.peakArity=Math.max(s.peakArity,c.length)}
   function close(){
     for(;;){
       s.closurePasses++;F=canonical(F);observe();if(F.some(c=>c.length<2))return false;
       let b=F.find(c=>c.length===2&&c.some(l=>!P.has(abs(l))));
       if(b){let v=abs(b.find(l=>!P.has(abs(l))));let t=b.find(l=>abs(l)!==v),vLit=b.find(l=>abs(l)===v);let replacement=-t*(vLit<0?-1:1);
         save(v,[vLit<0?[-t]:[t]]);
         F=F.map(c=>c.map(l=>abs(l)===v?(l>0?replacement:-replacement):l));s.binaryDeductions++;continue}
       let keys=new Map(),hit=null;
       outer:for(let i=0;i<F.length;i++){let c=F[i];for(let j=0;j<c.length;j++){s.consensusKeys++;let rest=c.filter((_,k)=>k!==j),flip=rest[0]<0?-1:1;let a=rest.map(l=>l*flip),l=c[j]*flip;let key=a.join(",")+"|"+abs(l);let old=keys.get(key);if(old&&old.l===-l){hit=[old.i,i,a];break outer}keys.set(key,{i,l})}}
       if(hit){let [i,j,a]=hit;F=F.filter((_,k)=>k!==i&&k!==j);F.push(a);s.consensusDeductions++;continue}
       return true;
     }
   }
   const result=(status)=>({status,residual:F,stats:s,finish:(boundary={})=>{
     if(status==="UNSAT")return null;
     let x=Array(n+2).fill(0);for(let [v,b] of Object.entries(boundary))x[+v]=b;for(let [v,b] of Object.entries(pins))x[+v]=b;x[A]=0;
     if(!F.every(c=>ok(c,x)))return null;
     for(let k=archive.length-1;k>=0;k--){let [v,rows]=archive[k];let forced=null;for(let a of rows){let t=value(a[0],x);if(a.every(l=>value(l,x)===t)){let b=t^1;assert(forced===null||forced===b,"inconsistent lift");forced=b}}x[v]=forced??0}
     for(let c of source){s.sourceChecks++;assert(ok(c,x),"source lift")}
     return x
   }});
   if(!close())return result("UNSAT");
   while(F.length){
     let occ=new Map();F.forEach((c,i)=>c.forEach(l=>{let v=abs(l);if(!P.has(v)){if(!occ.has(v))occ.set(v,[]);occ.get(v).push(i)}}));
     if(!occ.size)return result("PROJECTED");
     let chosen=null;
     for(let [v,ids] of [...occ].sort((a,b)=>a[1].length-b[1].length||a[0]-b[0])){
       let rows=ids.map(i=>{let c=F[i],flip=c.includes(v)?1:-1;return c.filter(l=>abs(l)!==v).map(l=>l*flip)});
       let idset=new Set(ids),keep=F.filter((_,i)=>!idset.has(i)),M=new Map(keep.map(c=>[c.join(","),c])),bad=false;
       outer:for(let i=0;i<rows.length;i++)for(let j=i+1;j<rows.length;j++){
         s.pairAttempts++;let c=norm(rows[i].concat(rows[j].map(l=>-l)));if(c===null)continue;if(c.length<2){chosen={v,rows,next:[c]};break outer}
         M.set(c.join(","),c);if(M.size>cap){bad=true;break outer}
       }
       if(chosen)break;
       if(bad){s.failedCandidates++;continue}
       chosen={v,rows,next:[...M.values()]};break;
     }
     if(!chosen){assert(close(),"closure changed at stagnation");return result("UNKNOWN")}
     save(chosen.v,chosen.rows);s.eliminations++;F=chosen.next;if(!close())return result("UNSAT");
   }
   return result("SAT");
 }
 function record(n,F,pins={},ref=null,cap=F.length){
   let r=project(n,F,pins,[],cap),status=r.status;
   if(status==="PROJECTED")status=r.finish()?"SAT":"UNSAT";
   tally.cases++;tally[status]++;
   if(ref!==null&&status!=="UNKNOWN")assert((status==="SAT")===ref,"decision mismatch");
   if(status==="SAT"){assert(r.finish(),"missing SAT lift");tally.verifiedWitnesses++}
   for(let [k,v] of Object.entries(r.stats)){if(k.startsWith("max"))tally[k]=Math.max(tally[k]||0,v);else if(tally[k]!==undefined)tally[k]+=v}
   return {status,...r.stats,residual:r.residual.length}
 }
 function brute(n,F,pins={}){let count=0;for(let a=0;a<2**n;a++){let x=Array.from({length:n+2},(_,i)=>i>0&&i<=n?(a>>(i-1))&1:0);if(Object.entries(pins).some(([v,b])=>x[+v]!==b))continue;tally.referenceAssignments++;if(F.every(c=>ok(c,x)))count++}return count}
 let seed=0x20261124;const rand=n=>{seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return(seed>>>0)%n};
 let random={SAT:0,UNSAT:0,UNKNOWN:0},refLabels={SAT:0,UNSAT:0};
 for(let k=0;k<180;k++){let n=4+rand(5),F=[];for(let m=0,mmax=3+rand(18);m<mmax;m++){let c=[];for(let j=0,jmax=2+rand(3);j<jmax;j++){let l=1+rand(n);c.push(rand(2)?l:-l)}F.push(c)}let pins=k%3===0?{1:rand(2)}:{};let b=brute(n,F,pins)>0;refLabels[b?"SAT":"UNSAT"]++;let r=record(n,F,pins,b);random[r.status]++}
 let pointwise=0,pointwiseLifts=0;
 for(let k=0;k<80;k++){let n=7,F=[];for(let i=0;i<3;i++){let v=2+rand(6),w=2+rand(6);F.push([rand(2)?1:-1,rand(2)?v:-v,rand(2)?w:-w])}let r=project(n,F,{},[2,3,4,5,6,7]);assert(r.status!=="UNKNOWN","degree-three projection");for(let a=0;a<64;a++){let x=Array(n+2).fill(0),b={};for(let j=2;j<=7;j++)x[j]=b[j]=(a>>(j-2))&1;let expected=[0,1].some(z=>{x[1]=z;return F.every(c=>ok(c,x))});let got=r.status!=="UNSAT"&&r.residual.every(c=>ok(c,x));assert(got===expected,"pointwise projection");if(got){assert(r.finish(b),"projection lift");pointwiseLifts++}pointwise++}}
 const F0=[[1,2,3],[1,4,5],[1,6,7],[2,4,6],[2,5,7],[3,4,7],[3,5,6]];
 const controls=[];
 function neighbors(n,F,label,cap=F.length,all=true,small=false){
   let ref=small?brute(n,F):null;if(small)assert(ref===0,"root reference");
   let r=record(n,F,{},false,cap),out={label,n,m:F.length,cap,root:r,rootReference:ref,neighbors:{SAT:0,UNSAT:0,UNKNOWN:0},neighborModelCounts:{},neighborDetails:[]};
   let idx=all?[...F.keys()]:[0,Math.floor(F.length/2),F.length-1];
   for(let i of idx)for(let b of [0,1]){let G=F.map((c,j)=>i===j?c.concat(b?-(n+1):n+1):c);
     let count=small?brute(n,G):null;if(small){let k=String(count);out.neighborModelCounts[k]=(out.neighborModelCounts[k]||0)+1}
     let q=record(n,G,{},small?count>0:true,cap);out.neighbors[q.status]++;out.neighborDetails.push({i,b,status:q.status,eliminations:q.eliminations,binary:q.binaryDeductions,peak:q.maxActive})}
   controls.push(out)
 }
 neighbors(7,F0,"Fano cap m",7,true,true);
 neighbors(7,F0,"Fano cap 2m",14,true,true);
 let K=[];for(let i=1;i<=5;i++)for(let j=i+1;j<=5;j++)for(let k=j+1;k<=5;k++)K.push([i,j,k]);neighbors(5,K,"K5^3",10,true,true);
 let S=[];for(let a=0;a<3;a++)S.push([1+3*a,2+3*a,3+3*a]);for(let slope=0;slope<3;slope++)for(let b=0;b<3;b++)S.push([0,1,2].map(x=>1+3*x+(slope*x+b)%3));
 neighbors(9,S,"AG(2,3) cap m",12,true,true);
 neighbors(9,S,"AG(2,3) cap 2m",24,true,true);
 // DO02 Boolean incidence only, reconstructed from its source; no manifest passed to project.
 const F=F0.slice(1).map(c=>c.map(v=>v-1));
 function fresh(n){return {n,e:[]}}
 function gad(G,a,b){let ids=[a,b,...Array.from({length:5},()=>++G.n)];for(let c of F)G.e.push(c.map(v=>ids[v]))}
 function path(G,a,k){for(let i=0;i<k;i++){let b=++G.n;gad(G,a,b);a=b}return a}
 let G=fresh(1),b=path(G,1,4),c=path(G,1,4);G.e.push([1,b,c]);
 neighbors(G.n,G.e,"DO02 49",G.e.length,true);
 function stretch(G){let H=fresh(G.n);for(let c of G.e){let e=[];for(let a of c){let b=++H.n;gad(H,a,b);e.push(b)}H.e.push(e)}return H}
 let H=stretch(G);neighbors(H.n,H.e,"DO02 931",H.e.length,false);
 let J=fresh(5);for(let c of K)J.e.push(c.map((v,i)=>path(J,v,[1,4,4][i])));neighbors(J.n,J.e,"DO02-style positive Hall excess K5^3",J.e.length,false);
 let L=stretch({n:5,e:K});neighbors(L.n,L.e,"single-incidence stretched K5^3",L.e.length,true);
 // A loose Berge cycle has arbitrarily large girth and is SAT. Not a critical high-girth UNSAT test.
 for(let k of [16,64,256]){let e=Array.from({length:k},(_,i)=>[1+i,1+(i+1)%k,1+k+i]);controls.push({label:"loose Berge cycle",girth:k,n:2*k,m:k,root:record(2*k,e,{},true,k)})}
 let hostile=[];for(let i=0;i<4;i++)hostile.push([1,2+2*i,3+2*i]);
 let hh=project(9,hostile,{},[2,3,4,5,6,7,8,9]);assert(hh.status==="UNKNOWN","growth guard");
 let h2=project(9,hostile,{},[2,3,4,5,6,7,8,9],6);assert(h2.residual.length===6,"six pair relations");
 for(let a=0;a<256;a++){let x=Array(11).fill(0);for(let j=2;j<=9;j++)x[j]=(a>>(j-2))&1;let expected=[0,1].some(z=>{x[1]=z;return hostile.every(c=>ok(c,x))});assert(expected===h2.residual.every(c=>ok(c,x)),"hostile projection")}
 return {seed:"0x20261124",random,refLabels,pointwise,pointwiseLifts,controls,tally,hostile:{cap4:hh.status,cap6:h2.status,resolvents:h2.residual,pointwise:256},discrepancies:0}
}
console.log(JSON.stringify(experiment(),null,2));
