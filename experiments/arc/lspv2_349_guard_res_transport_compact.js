// LSPV-2 GUARD-RES-BIDIRECTIONAL349, standalone no dependencies.
'use strict';
const F=[[-1,2],[-2,3],[-3,4],[-4,5],[1,-5],[1,2,3,4,5],[-1,-2,-3,-4,-5]];
const P=[[4,6,4],[5,8,5],[1,7,2],[1,9,1],[5,10,1],[2,11,2],[4,12,5],[3,14,4],[13,15,3]];
function ok(b,why){if(!b)throw Error(why||'assertion');}
function guard(f,z){return [...f.map(c=>[z,...c]),...f.map(c=>[-z,...c])];}
function count(f,n){let total=0;for(let a=0;a<2**n;a++)if(f.every(c=>c.some(v=>Boolean(a&(1<<(Math.abs(v)-1)))===(v>0))))total++;return total;}
function replay(src,proof){let ls=src.map(c=>new Set(c));for(const [l,r,p] of proof){ok(l>=1&&r>=1&&l<=ls.length&&r<=ls.length&&l!==r,'bad parent');const A=ls[l-1],B=ls[r-1];ok((A.has(p)&&B.has(-p))||(A.has(-p)&&B.has(p)),'bad pivot');const C=new Set([...A,...B].filter(x=>Math.abs(x)!==p));ok(![...C].some(x=>C.has(-x)),'tautology');ls.push(C);}ok(ls[ls.length-1].size===0,'not a refutation');return ls;}
function lift(src,proof,z){const m=src.length,q=proof.length;function loc(x,s){return x<=m?x+(s===-1?m:0):2*m+(s===-1?q:0)+(x-m);}const out=[];for(const s of [1,-1])for(const [a,b,p] of proof)out.push([loc(a,s),loc(b,s),p]);out.push([loc(m+q,1),loc(m+q,-1),z]);return out;}
function dimacs(f,n){return 'p cnf '+n+' '+f.length+'\n'+f.map(c=>[...c,0].join(' ')+'\n').join('');}
function parse(s){if(typeof s!=='string')throw Error('malformed');const a=s.trimEnd().split('\n'),h=/^p cnf (\d+) (\d+)$/.exec(a.shift());if(!h)throw Error('header');const n=Number(h[1]),m=Number(h[2]);if(!Number.isSafeInteger(n)||!Number.isSafeInteger(m)||a.length!==m)throw Error('counts');const f=[];for(const line of a){if(!/^(?:-?[1-9]\d* )*0$/.test(line))throw Error('clause');const c=line.split(' ').slice(0,-1).map(Number);if(c.some(v=>Math.abs(v)>n))throw Error('literal index');f.push(c);}return {n,clauses:f};}
function run(){const G=guard(F,6), L=lift(F,P,6);replay(F,P);replay(G,L);ok(count(F,5)===0&&count(G,6)===0);let flipF=0,flipG=0;
const delF=F.map((_,i)=>count(F.filter((_,j)=>i!==j),5));
const delG=G.map((_,i)=>count(G.filter((_,j)=>i!==j),6));
ok(JSON.stringify(delF)==='[4,4,4,4,4,1,1]');
ok(JSON.stringify(delG)==='[4,4,4,4,4,1,1,4,4,4,4,4,1,1]');
for(const [f,n] of [[F,5],[G,6]])for(let i=0;i<f.length;i++)for(let j=0;j<f[i].length;j++){const h=f.map(c=>c.slice());h[i][j]*=-1;ok(count(h,n)>0,'sign flip');if(n===5)flipF++;else flipG++;}
ok(flipF===20&&flipG===54);let bad=0;
for(const p of [[...L.slice(0,1),[999,1,1],...L.slice(2)],L.slice(0,-1),[[4,6,3],...L.slice(1)]]){try{replay(G,p);}catch(e){bad++;}}
ok(bad===3);const a=dimacs(F,5),b=dimacs(G,6);ok(a.length===74&&b.length===174);ok(JSON.stringify(parse(a).clauses)===JSON.stringify(F));const badInput=['p cnf 5 2\n1 0\n','p cnf 5 1\n6 0\n','p cnf 5 1\n1\n','p cnf x 1\n1 0\n','p cnf 5 1\n1 0\n2 0\n','p cnf 5 1\n1 0 0\n'];let malformed=0;for(const x of badInput)try{parse(x)}catch(e){malformed++}ok(malformed===6);
return {status:'COMPUTATIONAL',theorem:'For all UNSAT F, W_Res(F) <= W_Res(G(F)) <= 2 W_Res(F)+1',family:'Peitl Szeider rsmu_5_7_1.cnf',source:F,source_proof:P,guarded_source:G,guarded_proof:L,source_bytes:a.length,guarded_bytes:b.length,costs:[P.length,L.length],source_deletion_models:delF,guard_deletion_models:delG,all_signed_flips_sat:[flipF,flipG],malformed_rejected:malformed,corrupt_rejected:bad};
}
if(typeof require!=='undefined'&&typeof module!=='undefined'&&require.main===module)console.log(JSON.stringify(run(),null,2));
