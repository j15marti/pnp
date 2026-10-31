// ARC-SPARSE-EXTREME-LEDGER276: node v18+ standalone compact reproducer.
'use strict';
const W=[[-1,3,-14],[2,-8,9],[10,-13,14],[3,7,-13],[-4,-9,-11],[5,8,-14],[4,-8,-11],[1,7,13],[1,-7,10],[-5,-6,-15],[-2,-6,12],[-4,9,-10],[-2,5,-12],[-3,6,-15],[6,-7,11],[2,-9,11],[4,8,-10],[-3,12,15],[-5,-12,15],[-1,13,14]];
const SW=W.map(c=>c.slice());SW[7][0]=-1;SW[19][0]=1;
const H8=Array.from({length:8},(_,v)=>[1,2,3].map(i=>((v>>(i-1))&1)?i:-i)),H7=H8.slice(0,7);
function nv(F){return Math.max(...F.flat().map(Math.abs));}
function models(F){const n=nv(F);if(n>15)throw Error('limit');
let sum=0;for(let z=0;z<2**n;z++)if(F.every(C=>C.some(l=>((z>>(Math.abs(l)-1))&1)===(l>0?1:0))))sum++;return sum;}
function pairFlags(C,D){let same=false,opp=false;for(const x of C)for(const y of D){same ||= x===y;opp ||= x===-y;}
return {SS:!opp,SU:!same,US:!same,UU:!opp,same,opp};}
function brute(C,D,mode){const vv=[...new Set(C.concat(D).map(Math.abs))];
for(let z=0;z<2**vv.length;z++){const a=new Map(vv.map((v,k)=>[v,(z>>k)&1]));
const all=(E,s)=>E.every(l=>(a.get(Math.abs(l))===(l>0?1:0))===s);
if(all(C,mode[0]==='S')&&all(D,mode[1]==='S'))return true;}return false;}
function sparse(F,verify){const inc=new Map();let probes=0;
for(let j=0;j<F.length;j++){if(F[j].length!==3||new Set(F[j].map(Math.abs)).size!==3)throw Error('nonproper');
for(const l of F[j]){const v=Math.abs(l),a=inc.get(v)||[];a.push([j,l>0]);inc.set(v,a);}}
const dict=new Map();for(const [v,ls] of inc)for(let i=0;i<ls.length;i++)for(let j=i+1;j<ls.length;j++){
const [u,p]=ls[i],[w,q]=ls[j],key=Math.min(u,w)+':'+Math.max(u,w);
const f=dict.get(key)||{same:false,opp:false};f[p===q?'same':'opp']=true;dict.set(key,f);probes++;}
if(verify)for(let i=0;i<F.length;i++)for(let j=i+1;j<F.length;j++){
const exp=pairFlags(F[i],F[j]),got=dict.get(i+':'+j)||{same:false,opp:false};
if(exp.same!==got.same||exp.opp!==got.opp)throw Error('index mismatch');
for(const mode of ['SS','SU','US','UU'])if(brute(F[i],F[j],mode)!==exp[mode])throw Error('mode mismatch');}
return {full_pairs:F.length*(F.length-1)/2,sparse_pairs:dict.size,occurrence_pair_probes:probes,max_degree:Math.max(...[...inc.values()].map(a=>a.length))};}
function copy(F,b){const n=nv(F),out=[];for(let t=0;t<b;t++)for(const C of F)out.push(C.map(l=>Math.sign(l)*(Math.abs(l)+t*n)));return out;}
function star(F,k){const n=nv(F),out=F.map(c=>c.slice());for(let j=0;j<k;j++)out.push([n+1,n+2+2*j,n+3+2*j]);return out;}
function run(){const cases=[['W1_UNSAT',W],['W1_swapped_SAT',SW],['H8_UNSAT',H8],['H7_SAT',H7],['star_H8_UNSAT',star(H8,40)],['star_H7_SAT',star(H7,40)]];
const out=cases.map(([name,F])=>({name,n:nv(F),m:F.length,models:nv(F)<=15?models(F):null,...sparse(F,true)}));
if(out[0].models!==0||out[1].models!==168||out[2].models!==0||out[3].models!==1)throw Error('labels');
if(out[0].sparse_pairs!==73||out[4].sparse_pairs!==808||out[5].sparse_pairs!==801)throw Error('pairs');
const scaled=sparse(copy(W,64),false);if(scaled.full_pairs!==818560||scaled.sparse_pairs!==4672||scaled.occurrence_pair_probes!==5760)throw Error('scale');
return {run_id:'ARC-SPARSE-EXTREME-LEDGER276',status:'COMPUTATIONAL (finite, exact, restricted)',cases:out,disjoint_W1_copies_64:scaled,note:'Full producer, UNSAT proof replay and indexed raw are in the reproducibility ZIP.'};}
if(typeof module!=='undefined'&&require.main===module)process.stdout.write(JSON.stringify(run(),null,2)+'\n');
