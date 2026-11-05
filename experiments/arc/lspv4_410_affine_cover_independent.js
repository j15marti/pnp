// Independent no-import RREF verifier for LSPV-4/410 (run from repository root with node).
'use strict';
const fs=require('fs');
const data=JSON.parse(fs.readFileSync(process.argv[2] || 'results/raw/arc/2026-11-05_0302_LSPV4_410_AFFINE_COVER.json','utf8'));
function pop(x){let n=0;while(x){n++;x&=x-1;}return n}
function Q(w,k){let m=(1<<k)-1;return pop((w&m)&((w>>k)&m))&1}
function B(u,v,k){let m=(1<<k)-1;return (pop((u&m)&((v>>k)&m))+pop((v&m)&((u>>k)&m)))&1}
function* choose(n,k,start=0,p=[]){if(!k){yield p;return}for(let i=start;i<=n-k;i++)yield* choose(n,k-1,i+1,[...p,i])}
function rref(n,r){
 let all=[];
 for(const piv of choose(n,r)){
  let opts=[];
  for(let i=0;i<r;i++){
   let cols=[];for(let j=piv[i]+1;j<n;j++)if(!piv.includes(j))cols.push(j);
   let v=[];for(let m=0;m<(1<<cols.length);m++){let w=1<<piv[i];for(let j=0;j<cols.length;j++)if(m&(1<<j))w|=1<<cols[j];v.push(w)}
   opts.push(v);
  }
  function run(i,rows){if(i===r){all.push(rows);return}for(const row of opts[i])run(i+1,[...rows,row])}
  run(0,[]);
 }
 return all;
}
let checks=0;
for(let k=1;k<=3;k++){
 let num={},iso={};
 for(let d=0;d<=2*k;d++){
  let bs=rref(2*k,d);num[d]=bs.length;let count=0;
  for(const basis of bs){
   let good=true;for(let i=0;i<d;i++)for(let j=i+1;j<d;j++)if(B(basis[i],basis[j],k))good=false;
   if(good)count++;
   if(d<=3){
    let space=[0];for(const v of basis){let old=[...space];for(const x of old)space.push(x^v)}
    let direct=true;for(const a of space)for(const b of space)if(Q(a^b,k)!==(Q(a,k)^Q(b,k)))direct=false;
    if(direct!==good)throw Error('isotropy/affinity mismatch');checks++;
   }
  }
  iso[d]=count;checks++;
 }
 let row=data.exhaustive_linear_direction_checks.find(r=>r.k===k);
 if(JSON.stringify(num)!==JSON.stringify(row.all_direction_subspaces_by_dim)||JSON.stringify(iso)!==JSON.stringify(row.isotropic_subspaces_by_dim))throw Error('counts mismatch');
 checks+=2;
}
for(const r of data.sizes){
 let k=r.k,m=(1<<k)-1;
 if(r.paid_def_nodes!==2*k-1||r.lower_bound_pieces!==1<<k)throw Error('wrong source counts');checks++;
 let points=new Set;
 for(let word=0;word<(1<<(2*k));word++){let x=word&m,y=word>>k;let z=Q(word,k);if(z!==(pop(x&y)&1))throw Error('cover error');points.add(2*word+z);checks++}
 if(points.size!==(1<<(2*k)))throw Error('incomplete cover');checks++;
}
for(let k=1;k<=5;k++){let a=0,b=0;for(let w=0;w<(1<<(2*k+1));w++){let t=(w>>(2*k))&1;if(t)a++;if(t&&!t)b++}if(a!==(1<<(2*k))||b!==0)throw Error('source models');checks+=2}
if(Q(3,1)!==1||Q(1,1)!==0||B(1,2,1)!==1)throw Error('hostile check');checks+=3;
if(checks!==7687)throw Error('unexpected count '+checks);
console.log(JSON.stringify({status:'PASS',checks,method:'independent RREF finite linear-subspace enumeration'}));
