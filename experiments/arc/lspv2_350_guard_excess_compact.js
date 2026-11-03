/* GUARD-EXCESS-CAP350: run node thisfile.js. Dependency-free. */
'use strict';
const seed=[[-1,2],[-2,3],[-3,4],[-4,5],[1,-5],[1,2,3,4,5],[-1,-2,-3,-4,-5]];
const base=[[4,6,4],[5,8,5],[1,7,2],[1,9,1],[5,10,1],[2,11,2],[4,12,5],[3,14,4],[13,15,3]];
function norm(a){let o=[...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);if(o.some(x=>o.includes(-x)))throw Error('tautology');return o;}
function res(a,b,p){if(a.includes(p)&&b.includes(-p))return norm([...a.filter(x=>x!==p),...b.filter(x=>x!==-p)]);if(a.includes(-p)&&b.includes(p))return norm([...a.filter(x=>x!==-p),...b.filter(x=>x!==p)]);throw Error('invalid pivot');}
function models(cs,n){let k=0;for(let mask=0;mask<2**n;mask++)if(cs.every(c=>c.some(l=>Boolean(mask&(1<<(Math.abs(l)-1)))===(l>0))))k++;return k;}
function bytes(cs,n){return ('p cnf '+n+' '+cs.length+'\n'+cs.map(c=>c.join(' ')+' 0\n').join('')).length;}
function make(t){let m=seed.length,k=2**t,n=5+t,src=[];for(let e=0;e<k;e++)for(let c of seed)src.push(norm([...Array.from({length:t},(_,j)=>e&(1<<j)?-(6+j):(6+j)),...c]));
let lines=src.map(c=>c.slice()),proof=[];
function add(u,v,p){let clause=res(lines[u],lines[v],p),id=lines.length;lines.push(clause);proof.push({parents:[u,v],pivot:p,clause});return id;}
let leaves=[];for(let i=0;i<m;i++){let active=new Map(Array.from({length:k},(_,e)=>[e,e*m+i]));for(let j=t-1;j>=0;j--){let next=new Map();for(let [e,id] of active)if(!(e&(1<<j)))next.set(e,add(id,active.get(e|(1<<j)),6+j));active=next;}
let v=active.get(0);if(JSON.stringify(lines[v])!==JSON.stringify(norm(seed[i])))throw Error('guard elimination incorrect');leaves.push(v);}
let map=new Map(leaves.map((v,i)=>[i+1,v]));base.forEach(([a,b,p],i)=>map.set(8+i,add(map.get(a),map.get(b),p)));
if(lines.at(-1).length)throw Error('not false');
let deletions=src.map((_,i)=>models(src.filter((_,j)=>i!==j),n)),flips=[];
for(let i=0;i<src.length;i++)for(let j=0;j<src[i].length;j++){let q=src.map(c=>c.slice());q[i][j]=-q[i][j];flips.push(models(q,n));}
if(models(src,n)!==0||deletions.some(x=>!x)||flips.some(x=>!x))throw Error('label control failed');
return {t,variables:n,source_count:src.length,dimacs_bytes:bytes(src,n),general_lower:src.length-1,constructed_upper:proof.length,excess_upper:proof.length-src.length+1,sources:src,proof,deletion_counts:deletions,sign_flip_counts:flips,zero_models:0};}
function main(){let cases=[0,1,2,3].map(make);return {run_id:'LSPV2-GUARD-EXCESS-CAP350',original_n:5,original_m:7,cases,summary:cases.map(x=>({t:x.t,variables:x.variables,source_count:x.source_count,dimacs_bytes:x.dimacs_bytes,general_lower:x.general_lower,constructed_upper:x.constructed_upper,excess_upper:x.excess_upper})),total_deletion_checks:cases.reduce((a,x)=>a+x.deletion_counts.length,0),total_sign_checks:cases.reduce((a,x)=>a+x.sign_flip_counts.length,0)};}
if(typeof module!=='undefined'&&require.main===module)console.log(JSON.stringify(main(),null,2));
