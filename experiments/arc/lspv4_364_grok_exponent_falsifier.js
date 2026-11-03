// LSPV4_364: compact independent finite falsifier, no dependency packages.
const assert=require('node:assert/strict');
function cnf(n,c){return 'p cnf '+n+' '+c.length+'\n'+c.map(x=>x.join(' ')+' 0\n').join('')}
function parse(s){
  if(!s.endsWith('\n'))throw Error('newline');
  let lines=s.slice(0,-1).split('\n'),h=/^p cnf (\d+) (\d+)$/.exec(lines[0]);
  if(!h||Number(h[2])!==lines.length-1)throw Error('header');
  let c=lines.slice(1).map(l=>{
    let a=l.split(' ');if(a.pop()!=='0')throw Error('zero');
    let lits=a.map(z=>{if(!/^-?[1-9]\d*$/.test(z))throw Error('literal');return Number(z)});
    if(lits.some(z=>!Number.isSafeInteger(z)||Math.abs(z)>Number(h[1])))throw Error('range');
    return lits;
  });return {n:Number(h[1]),c};
}
function models(p){if(p.n>12)throw Error('finite-only');let z=0;for(let a=0;a<2**p.n;a++)if(p.c.every(c=>c.some(l=>!!((a>>(Math.abs(l)-1))&1)===(l>0))))z++;return z}
function family(pad,v,sat){let c=[[1],[sat?1:-1]];for(let j=0;j<pad;j++)c.push((v>>j)&1?[-2,2]:[2,-2]);return cnf(2,c)}
function php(h){let c=[],id=(i,j)=>i*h+j+1;for(let i=0;i<h+1;i++)c.push(Array.from({length:h},(_,j)=>id(i,j)));for(let j=0;j<h;j++)for(let i=0;i<h+1;i++)for(let k=i+1;k<h+1;k++)c.push([-id(i,j),-id(k,j)]);return cnf(h*(h+1),c)}
function tseitin(ch){let e=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],c=[];for(let v=0;v<4;v++){let a=e.map((x,i)=>x.includes(v)?i+1:0).filter(Boolean);for(let mask=0;mask<8;mask++)if((((mask&1)>0)^((mask&2)>0)^((mask&4)>0))!==Boolean(ch[v]))c.push(a.map((x,i)=>(mask>>i)&1?-x:x))}return cnf(6,c)}
let checks=0,tests=[],controls=[];
for(let pad of [12,64,256,1024]){let N=family(pad,0,false).length,q=Math.max(2,Math.floor(N**.25));let seen=new Set();for(let j=0;j<q;j++){let a=family(pad,j,false),b=family(pad,j,true);assert.equal(a.length,N);assert.equal(models(parse(a)),0);assert(models(parse(b))>0);seen.add(a);checks+=3}assert.equal(seen.size,q);checks++;tests.push({N,pad,queries:q,source_char_reads:q*N,invalid_guest_omega_K2:q*N*N})}
for(let h=1;h<=3;h++){let s=php(h),p=parse(s),satdel=0;assert.equal(models(p),0);checks++;for(let j=0;j<p.c.length;j++){satdel+=models({n:p.n,c:p.c.filter((_,i)=>i!==j)})>0;checks++}controls.push({family:'PHP',holes:h,clauses:p.c.length,sat_deletions:satdel})}
for(let [lab,ch] of [['odd',[1,0,0,0]],['even',[0,0,0,0]]]){let count=models(parse(tseitin(ch)));assert.equal(count,lab==='odd'?0:8);checks++;controls.push({family:'Tseitin-K4',parity:lab,models:count})}
let bad=['','p cnf 2 2\n1 0\n','p cnf 2 1\n3 0\n','p cnf 2 1\n1 0','p cnf -2 1\n1 0\n'];for(let s of bad){assert.throws(()=>parse(s));checks++}
console.log(JSON.stringify({status:'PASS',assertions:checks,tests,controls,malformed_rejected:bad.length},null,2));