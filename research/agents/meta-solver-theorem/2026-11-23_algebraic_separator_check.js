#!/usr/bin/env node
// HCL algebraic separator; exact BigInt GF(2) arithmetic; no dependency.
function main(){
const assert=(x,msg="assertion failed")=>{if(!x)throw Error(msg)};
const bit=i=>1n<<BigInt(i), pivot=x=>x.toString(2).length-1;
function par(x){let p=0;while(x){x&=x-1n;p^=1}return p}
function elim(rows){const P=new Map(),deps=[];for(let i=0;i<rows.length;i++){let v=rows[i],t=bit(i);while(v){let p=pivot(v);if(!P.has(p)){P.set(p,[v,t]);break}const [w,s]=P.get(p);v^=w;t^=s}if(!v)deps.push(t)}return {P,deps}}
const bas=rs=>[...elim(rs).P.values()].map(x=>x[0]);
function coord(v,rs){const {P}=elim(rs);let t=0n;while(v){const q=P.get(pivot(v));assert(q,"not in span");v^=q[0];t^=q[1]}return t}
function meet(A,B){A=bas(A);B=bas(B);return bas(elim([...A,...B]).deps.map(t=>A.reduce((s,v,i)=>s^((t&bit(i))?v:0n),0n)))}
function factor(forms,allowed,offset=0){return {forms,allowed,offset,V:bas(forms)}}
function tree(a){assert(a.length);if(a.length===1)return a[0];const m=a.length>>1,l=tree(a.slice(0,m)),r=tree(a.slice(m));return {l,r,V:bas([...l.V,...r.V])}}
function val(forms,rows,s){return forms.reduce((t,v,i)=>t|(BigInt(par(coord(v,rows)&s))<<BigInt(i)),0n)}
function dp(root){let width=0,pairs=0,states=0;function go(n,out){const W=meet(n.V,out),R=new Set();width=Math.max(width,W.length);
if(!n.l){for(let s=0n;s<bit(n.V.length);s++)if(n.allowed.includes(Number(val(n.forms,n.V,s))^n.offset))R.add(val(W,n.V,s))}
else{const A=go(n.l,bas([...out,...n.r.V])),B=go(n.r,bas([...out,...n.l.V])),C=meet(n.l.V,n.r.V);
const ac=C.map(v=>coord(v,A.W)),bc=C.map(v=>coord(v,B.W)),pc=W.map(v=>coord(v,[...A.W,...B.W]));
for(const a of A.R)for(const b of B.R){pairs++;if(!ac.every((q,i)=>par(q&a)===par(bc[i]&b)))continue;const s=a|(b<<BigInt(A.W.length));R.add(pc.reduce((z,q,i)=>z|(BigInt(par(q&s))<<BigInt(i)),0n))}}
states+=R.size;return {W,R}}const r=go(root,[]);return {sat:r.R.size>0,width,pairs,states}}
function brute(f,d){for(let u=0n;u<bit(d);u++)if(f.every(g=>g.allowed.includes(g.forms.reduce((t,v,i)=>t|(par(v&u)<<i),0)^g.offset)))return true;return false}
function rankCons(rows){const P=new Map();for(const [a,b] of rows){let v=a,r=b;while(v){let p=pivot(v);if(!P.has(p)){P.set(p,[v,r]);break}v^=P.get(p)[0];r^=P.get(p)[1]}if(!v&&r)return {sat:false,rank:P.size}}return {sat:true,rank:P.size}}
let seed=20261123;function rng(n){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return (seed>>>0)%n}
let sat=0,unsat=0;const widths=new Set();
for(let d=1;d<=8;d++)for(let rep=0;rep<60;rep++){const f=Array.from({length:2+rng(8)},()=>{const k=1+rng(3),forms=Array.from({length:k},()=>BigInt(rng(1<<d)));return factor(forms,Array.from({length:1<<k},(_,i)=>i).filter(()=>rng(7)<3),rng(1<<k))});const a=dp(tree(f)),b=brute(f,d);assert(a.sat===b);b?sat++:unsat++;widths.add(a.width)}
function edges(t,kind){const e=new Set();const add=(a,b)=>{if(a!==b)e.add([Math.min(a,b),Math.max(a,b)].join(","))};for(let i=0;i<t;i++)add(i,(i+1)%t);if(kind==="cubic"){assert(t>=4&&t%2===0);for(let i=0;i<t/2;i++)add(i,i+t/2)}if(kind==="four"){assert(t>=5);for(let i=0;i<t;i++)add(i,(i+2)%t)}return [...e].map(x=>x.split(",").map(Number))}
function family(t,k,kind,charge,blocked,extra,deleted=-1){
const E=edges(t,kind), A=[],x=(i,j)=>i*k+j,p=(i,j)=>(i+j)%2;
for(let e=0;e<E.length;e++)for(let j=0;j<k;j++){const [a,b]=E[e];A.push([bit(x(a,j))^bit(x(b,j)),p(a,j)^p(b,j)^((e===0&&j===0)?charge:0)])}
const ac=rankCons(A);if(charge){assert(!ac.sat);return {t,k,kind,charge,blocked,extra,sat:false,affine:false}}
assert(ac.sat&&ac.rank===k*(t-1));const groups=[];
for(let i=0;i<t;i++){const local=[];for(let j=0;j<k;j++){const q=k+2*(i*k+j);local.push(factor([bit(j),bit(q),bit(q+1)],[1,2,4]))}
if(i===0)local.push(factor([1n,2n,4n],[1,2,4]));
if(i===t-1){if(blocked){for(const v of [1,2,4])if(v!==deleted)local.push(factor([1n,2n,4n],Array.from({length:8},(_,q)=>q).filter(q=>q!==v)))}else local.push(factor([1n,2n,4n],[1,2,4]));if(extra)local.push(factor([1n,bit(k+2*t*k)],[1,2,3]))}groups.push(tree(local))}
const a=dp(tree(groups));assert(a.sat===(!blocked||deleted>=0));assert(a.width===k,"family width");
let found=false;for(let z=0;z<(1<<k);z++){const b=z&7;if(![1,2,4].includes(b))continue;if(blocked&&b!==deleted)continue;found=true}assert(a.sat===found);
return {t,k,kind,charge,blocked,extra,deleted,affine:true,rank:ac.rank,nullity:3*t*k+extra-ac.rank,sourceEdges:E.length,...a}}
const F=[];
for(const [t,kind] of [[3,"cycle"],[4,"cycle"],[5,"cycle"],[6,"cycle"],[4,"cubic"],[6,"cubic"],[5,"four"],[6,"four"]])for(const k of [3,4,5,6])for(const extra of [0,1]){
F.push(family(t,k,kind,0,false,extra),family(t,k,kind,0,true,extra),family(t,k,kind,1,false,extra));for(const v of [1,2,4])F.push(family(t,k,kind,0,true,extra,v))}
const A=[0,1,2,4],B=[3,5,6,7];assert(bas(A.map(BigInt)).length===3&&bas(B.map(v=>BigInt(v^7))).length===3);
assert(!dp(tree([factor([1n,2n,4n],A),factor([1n,2n,4n],B)])).sat);
return {random:{cases:sat+unsat,sat,unsat,widths:[...widths].sort((a,b)=>a-b)},family:{cases:F.length,sat:F.filter(r=>r.sat).length,unsat:F.filter(r=>!r.sat).length,affineRejects:F.filter(r=>!r.affine).length,maxWidth:Math.max(...F.map(r=>r.width||0)),examples:F.filter(r=>r.affine&&r.deleted===-1).slice(0,6)},hullCollision:"verified"};
}
console.log(JSON.stringify(main(),null,2));
