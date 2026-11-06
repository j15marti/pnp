// LSPV-4/452 public independent, executable combinatorial checker.
// Node.js >= 18, no dependencies. Finite controls, not a SAT lower bound.
'use strict';
function assert(x,msg){if(!x)throw new Error(msg||'assertion');}
function comb(a,k){let out=[];function rec(i,v){if(v.length===k){out.push(v.slice());return;}for(let j=i;j<=a.length-(k-v.length);j++){v.push(a[j]);rec(j+1,v);v.pop();}}rec(0,[]);return out;}
function moments(a,k,p){let arr=[];for(let j=1;j<=k;j++){let s=0;for(let x of a){let z=1;for(let t=0;t<j;t++)z=z*x%p;s=(s+z)%p;}arr.push(s);}return arr;}
function same(a,b){return a.length===b.length&&a.every((x,i)=>x===b[i]);}
function errors(a,m){let cnt=Array(m+1).fill(0);for(let x of a)cnt[x]++;let missing=0,excess=0;for(let x=1;x<=m;x++){if(cnt[x]===0)missing++;excess+=Math.max(0,cnt[x]-1);}return [missing,excess];}
function source(H,edges,charge){let inc=Array.from({length:H},()=>[]);edges.forEach(([u,v],i)=>{inc[u].push(i+1);inc[v].push(i+1);});let f=[];for(let v=0;v<H;v++){let [a,b,c]=inc[v].sort((x,y)=>x-y);assert(c!==undefined);for(let p=0;p<2;p++)for(let q=0;q<2;q++){let z=p^q^1^(v===0?charge:0);f.push([p?-a:a,q?-b:b,z?-c:c]);}}return f;}
let edges=[];for(let a=0;a<4;a++)for(let b=a+1;b<4;b++)edges.push([a,b]);
let k4even=source(4,edges,0),k4odd=source(4,edges,1);
assert(k4even.length===16&&k4odd.length===16);
let satCount=[];
for(let f of [k4even,k4odd]){let n=0;for(let a=0;a<64;a++){if(f.every(c=>c.some(lit=>(((a>>(Math.abs(lit)-1))&1)===Number(lit>0)))))n++;}satCount.push(n);}
assert(satCount[0]>0&&satCount[1]===0);
let rows=[],checks=0;
for(let [m,k] of [[16,1],[16,2],[16,3],[16,4],[32,1],[32,2],[32,3]]){
 let h=m/2,A=Array.from({length:h-k},(_,i)=>i+1),P=Array.from({length:h+k},(_,i)=>h-k+i+1);
 let sets=comb(P,k),n=sets.length,lo=Math.ceil(Math.log2(n));assert(n>0);
 let full=Array.from({length:m},(_,i)=>i+1),ref=moments(full,k,65537);
 let ordered=0;
 for(let i=0;i<n;i++){
   if(m===16&&k===4&&i%5!==0)continue;
   if(m===32&&k===3&&i%13!==0)continue;
   let U=sets[i],prefix=[...A,...U],have=new Set(prefix),suffix=full.filter(x=>!have.has(x));
   assert(suffix.length===h&&same(moments([...prefix,...suffix],k,65537),ref));
   checks+=2;
   for(let j=0;j<n;j++){
     if(m===32&&k===3&&j%29!==0)continue;
     let V=sets[j],stream=[...A,...V,...suffix],r=k-V.filter(x=>have.has(x)).length;
     let [missing,excess]=errors(stream,m);
     assert(missing===excess&&missing===r);
     assert(same(moments(stream,k,65537),ref)===(r===0));
     ordered++;checks+=2;
   }
 }
 rows.push({m,k,prefix_states:n,lower_bits:lo,pairs_tested:ordered});
}
for(let k=1;k<=3;k++){
 let n=1<<(k+1),a=[],b=[];for(let i=0;i<n;i++){let t=i,bits=0;while(t){bits^=t&1;t>>=1;}(bits?a:b).push(i+1);}
 let m=32,orig=Array.from({length:m},(_,i)=>i+1),w=orig.filter(x=>!a.includes(x)).concat(b);
 assert(a.length===b.length&&a.length===1<<k);
 assert(same(moments(orig,k,65537),moments(w,k,65537)));
 assert(errors(w,m)[0]===1<<k);
 checks+=3;
}
console.log(JSON.stringify({status:'PASS',checks,k4_sat_assignment_count:satCount,rows},null,2));
