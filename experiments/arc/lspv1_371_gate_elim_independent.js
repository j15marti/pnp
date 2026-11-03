// Independent no-import Node verifier for LSPV-1 371 local one-gate substitution.
// Does not import Python producer. Exhausts four names q,a,b,x and every strict pivot.
'use strict';
function normal(xs){let s=new Set(xs);for(let v of s)if(s.has(-v))return null;return [...s].sort((a,b)=>a-b).join(',')}
function arr(s){return s===''?[]:s.split(',').map(Number)}
function resolution(c,d,p){let A=new Set(arr(c)),B=new Set(arr(d));
if(A.has(p)&&B.has(-p)){A.delete(p);B.delete(-p)}
else if(A.has(-p)&&B.has(p)){A.delete(-p);B.delete(p)}
else return undefined;
return normal([...A,...B]);}
function subst(c,a,b){let s=new Set(arr(c));
if(s.has(1)){s.delete(1);return [normal([...s,a]),normal([...s,b])].filter(x=>x!==null)}
if(s.has(-1)){s.delete(-1);return [normal([...s,-a,-b])].filter(x=>x!==null)}
return [c]}
function subsumes(c,d){let D=new Set(arr(d));return arr(c).every(v=>D.has(v))}
const cls=[];for(let v=0;v<81;v++){let k=v,c=[];for(let j=1;j<=4;j++){let s=k%3;k=Math.floor(k/3);if(s)c.push(s===1?j:-j)}cls.push(normal(c))}
let checks=0,fail=[];
for(const a of [2,-2])for(const b of [3,-3])for(const c of cls)for(const d of cls)for(let p=1;p<=4;p++){
 let r=resolution(c,d,p);if(r===undefined||r===null)continue;checks++;
 let known=new Set([...subst(c,a,b),...subst(d,a,b)]);
 for(let layer=0;layer<2;layer++){
  const grown=new Set(),xs=[...known];
  for(const e of xs)for(const f of xs)for(let x=2;x<=4;x++){
   let t=resolution(e,f,x);if(t!==undefined&&t!==null)grown.add(t)
  }
  for(let x of grown)known.add(x)
 }
 for(let t of subst(r,a,b))if(![...known].some(e=>subsumes(e,t)))
   fail.push({a,b,c,d,p,t});
}
let result={status:fail.length?'FAIL':'PASS',checks,failures:fail.slice(0,12),
scope:'Independent explicit two-RES-layer closure, not a general proof-size lower bound'};
console.log(JSON.stringify(result,null,2));
if(fail.length)process.exitCode=1;
