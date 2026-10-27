// FIRST-READ-TAPE-FOOLING146, dependency-free exhaustive verifier.
// Execute with: node 2026-10-27_0624_FIRST_READ_TAPE_FOOLING146_compact_audit.js
// Mathematical unbounded conclusions require the separately supplied formal proof.
"use strict";
const W=[[-1,3,-14],[2,-8,9],[10,-13,14],[3,7,-13],[-4,-9,-11],
[5,8,-14],[4,-8,-11],[1,7,13],[1,-7,10],[-5,-6,-15],
[-2,-6,12],[-4,9,-10],[-2,5,-12],[-3,6,-15],[6,-7,11],
[2,-9,11],[4,8,-10],[-3,12,15],[-5,-12,15],[-1,13,14]];
const A=[6,11],B=[9,17],BD=[2,4,7,14,15];
let assertions=0;
function ck(x,msg){assertions++;if(!x)throw Error(msg+" #"+assertions);}
function H(a,b){let F=W.map(r=>r.slice());if(!a)for(let i of A)F[i][0]*=-1;
if(!b)for(let i of B)F[i][2]*=-1;return F;}
function truth(F,z){return F.every(r=>r.some(l=>!!(z & (1<<(Math.abs(l)-1)))==(l>0)));}
function balance(F,n){let p=Array(n+1).fill(0),q=p.slice(),seen=new Set();
for(let r of F){if(r.length!==3||new Set(r.map(Math.abs)).size!==3)return false;
let key=r.join(",");if(seen.has(key))return false;seen.add(key);
for(let l of r){if(Math.abs(l)>n||!l)return false;(l>0?p:q)[Math.abs(l)]++;}}
return F.length*3===4*n&&Array.from({length:n},(_,i)=>i+1).every(i=>p[i]===2&&q[i]===2);}
function S(m,a,b){let aa=[],xx=[],bb=[];
for(let i=0;i<m;i++){let F=H((a>>i)&1,(b>>i)&1);
for(let j=0;j<20;j++){let r=F[j].map(l=>Math.sign(l)*(Math.abs(l)+15*i));
let z={i,j,row:r};(A.includes(j)?aa:B.includes(j)?bb:xx).push(z);}}
return aa.concat(xx,bb).map((x,i)=>Object.assign({source_id:i+1},x));}
function reachable(g,u,v){let todo=[u],seen=new Set([u]);for(let x of todo){
if(x===v)return true;for(let y of (g[x]||[]))if(!seen.has(y)){seen.add(y);todo.push(y);}}return false;}
function leaf(bits){let as={};BD.forEach((v,j)=>as[v]=(bits>>j)&1);
let edges={};for(let [i,row] of W.entries()){
if(row.some(l=>as[Math.abs(l)]!==undefined&&as[Math.abs(l)]===(l>0?1:0)))continue;
let sub=row.filter(l=>as[Math.abs(l)]===undefined);
ck(sub.length<=2,"W1 2CNF leaf");
if(sub.length===0)return true;
let add=(x,y)=>{if(!edges[x])edges[x]=[];edges[x].push(y);};
if(sub.length===1)add(-sub[0],sub[0]);else{add(-sub[0],sub[1]);add(-sub[1],sub[0]);}}
return Array.from({length:15},(_,i)=>i+1).some(v=>reachable(edges,v,-v)&&reachable(edges,-v,v));}
function satp(m,a,b,p){for(let i=0;i<m;i++)if((p>>i)&1){if((b>>i)&1)return false;
}else if((a>>i)&1)return false;return true;}
function rectangle(m){let k=1<<m,total=0;for(let u=1;u<(1<<k);u++)
for(let v=1;v<(1<<k);v++){let okay=true,diag=0;
for(let a=0;a<k;a++)if((u>>a)&1){for(let b=0;b<k;b++)if((v>>b)&1&&((a&b)!==0))okay=false;
if((v>>((k-1)^a))&1)diag++;}
if(okay){ck(diag<=1,"DISJ fooling rectangle");total++;}}
return total;}
function real(P,x,bits){let q=[],v={};
function get(a){let z=(bits>>a)&1;if(v[a]===undefined){v[a]=z;q.push([a,z]);}else ck(v[a]===z,"alias");return z;}
let a=x%P,z0=get(a),b=(a+1+z0)%P,z1=get(b),c=(2*b+(z1^(x&1)))%P,z2=get(c);
return {out:!!((z0^z1)|z2),queries:q};}
function virt(P,x,bits){let q=[],v={};
function get(a){if(v[a]===undefined){let z=bits[q.length];if(z===undefined)return null;
v[a]=z;q.push([a,z]);}return v[a];}
let a=x%P,z0=get(a);if(z0===null)return null;
let b=(a+1+z0)%P,z1=get(b);if(z1===null)return null;
let c=(2*b+(z1^(x&1)))%P,z2=get(c);if(z2===null)return null;
return {out:!!((z0^z1)|z2),queries:q};}
function audit(){
let counts=[];for(let a=0;a<2;a++)for(let b=0;b<2;b++){let F=H(a,b),num=0;
for(let z=0;z<(1<<15);z++)if(truth(F,z))num++;
ck(balance(F,15),"W1 exact22");ck((num===0)===(a===1&&b===1),"W1 truth");counts.push([a,b,num]);}
ck(JSON.stringify(counts.map(x=>x[2]))==="[772,272,272,0]","W1 expected counts");
for(let bits=0;bits<32;bits++)ck(leaf(bits),"32 SCC contradiction leaves");
let sources=0,sats=0,unsats=0,unsatLocal=0,sourceSizes=[];
for(let m=1;m<=5;m++){let lengths=new Set(),s0=0,u0=0;for(let a=0;a<(1<<m);a++)
for(let b=0;b<(1<<m);b++){let E=S(m,a,b),F=E.map(x=>x.row);
ck(balance(F,15*m),"product strict exact22");ck(E.length===20*m,"physical clause count");
E.forEach((e,j)=>{ck(e.source_id===j+1,"source ID");let expected=H((a>>e.i)&1,(b>>e.i)&1)[e.j].map(l=>Math.sign(l)*(Math.abs(l)+15*e.i));ck(JSON.stringify(e.row)===JSON.stringify(expected),"real source row");});
let w=Math.ceil(Math.log2(15*m+1));
lengths.add(("p b3 "+(15*m)+" "+(20*m)+" "+w+"\n").length+20*m*(3*(w+1)+1));
let sat=((a&b)===0),found=false;for(let p=0;p<(1<<m);p++)found ||=satp(m,a,b,p);
ck(found===sat,"sound and complete SAT word");
let has=false;for(let i=0;i<m;i++)if(((a>>i)&1)&&((b>>i)&1)){has=true;unsatLocal++;}
ck(has===!sat,"UNSAT local module index");
sources++;if(sat){sats++;s0++;}else{unsats++;u0++;}}
ck(lengths.size===1,"fixed-length selector");
sourceSizes.push({m,SAT:s0,UNSAT:u0,source_bit_length:[...lengths][0]});}
let fool=[];for(let m=1;m<=9;m++){let mask=(1<<m)-1;for(let a=0;a<(1<<m);a++){
let b=mask^a,hits=[];for(let p=0;p<(1<<m);p++)if(satp(m,a,b,p))hits.push(p);
ck(hits.length===1&&hits[0]===a,"one SAT proof for each fooling pair");}fool.push({m,pairs:1<<m});}
let rectangles=[1,2,3].map(m=>({m,nonempty_sound_rectangles:rectangle(m)}));
for(let P=1;P<=5;P++)for(let x=0;x<=2*P;x++)for(let pi=0;pi<(1<<P);pi++){
let v=real(P,x,pi),p=v.queries.map(pair=>pair[1]),v2=virt(P,x,p);
ck(JSON.stringify(v)===JSON.stringify(v2),"first-read honest replay");
for(let q=0;q<=3;q++)for(let bits=0;bits<(1<<q);bits++){
let seq=Array.from({length:q},(_,i)=>(bits>>i)&1),vv=virt(P,x,seq);
if(vv!==null){let good=false;for(let full=0;full<(1<<P);full++)
if(JSON.stringify(real(P,x,full))===JSON.stringify(vv))good=true;
ck(good,"virtual partial map extends to genuine proof");}}}
return {run:"FIRST_READ_TAPE_FOOLING146_GITHUB_COMPACT",status:"COMPUTATIONAL",
W1_model_counts:counts,authenticated_2CNF_backdoor_leaves:32,sourceSizes,
sources,sats,unsats,authenticated_local_UNSAT_modules:unsatLocal,fooling:fool,rectangles,
max_virtual_proof_length:5,assertions,failures:0,
warnings:["Finite tests not an asymptotic TM lower bound","UNSAT local index does not imply global ordinary UNSAT coverage","No RAM crossing transfer","Full two-level ordinary 3CNF tests are in separately generated Python audit"]};}
if (typeof module!=="undefined" && require.main===module)console.log(JSON.stringify(audit(),null,2));
