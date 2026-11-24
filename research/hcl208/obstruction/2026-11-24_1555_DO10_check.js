'use strict';
function main(){
let seed=20261124;function rand(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed;}
const out={seed:20261124,rootCases:0,SAT:0,UNSAT:0,projectionWordChecks:0,guardCases:0,consistentCharts:0,closedCharts:0,localContradictions:0,rootPins:0,conditionalPins:0,closureScans:0,cutChecks:0,injectiveChecks:0,badBoundChecks:0,referenceWords:0,walshButterflies:0,rankCalls:0,maxBad:0,maxObservedLoss:0,assertions:0,fano:[],examples:[]};
function ok(x){out.assertions++;if(!x)throw Error("assertion "+out.assertions);}
function pc(x){let p=0;while(x){x&=x-1;p++;}return p;}
function dot(x,y){return pc(x&y)&1;}
function bas(rows,n){out.rankCalls++;const a=Array(n).fill(0);for(let x of rows){for(let i=n-1;i>=0&&x;i--)if(x&(1<<i)){if(a[i])x^=a[i];else{a[i]=x;break;}}}return a;}
function red(x,a){for(let i=a.length-1;i>=0;i--)if((x&(1<<i))&&a[i])x^=a[i];return x;}
function rank(rows,n){return bas(rows,n).filter(Boolean).length;}
function chart(n,eq){let a=bas(eq.map(e=>e[0]),n);const free=[];for(let i=0;i<n;i++)if(!a[i])free.push(i);const words=[];for(let z=0;z<(1<<n);z++){out.referenceWords++;if(eq.every(([r,b])=>dot(r,z)===b)){let k=0;free.forEach((v,i)=>k|=((z>>v)&1)<<i);words[k]=z;}}if(!words.length)return null;ok(words.length===1<<free.length && words.every(x=>x!==undefined));let dirs=free.map((_,j)=>words[1<<j]^words[0]);return {a,free,words,dirs,h:n-free.length};}
function obs(r,C){let q=0;C.dirs.forEach((v,i)=>q|=dot(r,v)<<i);return q;}
function spectrum(f,C){let a=C.words.map(z=>+f.eval(z));for(let k=1;k<a.length;k*=2)for(let i=0;i<a.length;i+=2*k)for(let j=0;j<k;j++){let p=a[i+j],q=a[i+j+k];a[i+j]=p+q;a[i+j+k]=p-q;out.walshButterflies++;}return bas(a.map((v,i)=>v?i:0),C.free.length).filter(Boolean);}
function overlap(A,B,n){return rank(A,n)+rank(B,n)-rank([...A,...B],n);}
function mk(e,mask){const scope=e.reduce((a,v)=>a|(1<<v),0);return {scope,eval:z=>{let p=z&scope;return !(p===0&&(mask&1))&&!(p===scope&&(mask&2));}};}
function project(F,S){let used=new Set(),G=[];for(let v of S){let I=F.filter((f,i)=>{if(f.scope&(1<<v)){ok(!used.has(i));used.add(i);return true;}return false;});G.push({scope:I.reduce((a,f)=>a|f.scope,0)&~(1<<v),eval:z=>[0,1].some(b=>I.every(f=>f.eval((z&~(1<<v))|(b<<v))))});}F.forEach((f,i)=>{if(!used.has(i))G.push(f);});return G;}
function close(n,F,eq){eq=eq.map(e=>e.slice());let pins=0;while(true){let C=chart(n,eq);if(!C)return {eq,C,pins,contr:true};let changed=false;for(let f of F){out.closureScans++;let legal=C.words.filter(z=>f.eval(z));if(!legal.length)return {eq,C,pins,contr:true};for(let v=0;v<n;v++){let row=1<<v;if(!(f.scope&row)||!red(row,C.a))continue;let b=dot(row,legal[0]);if(legal.every(z=>dot(row,z)===b)){eq.push([row,b]);pins++;changed=true;break;}}if(changed)break;}if(!changed)return {eq,C,pins,contr:false};}}
function check(n,F,W,eq,s,B){const C=chart(n,eq);if(!C)return;out.consistentCharts++;const V=F.map(f=>spectrum(f,C));let bad=0;for(let i=0;i<F.length;i++){const im=W[i].map(r=>obs(r,C));if(rank(im,C.free.length)<W[i].length)bad++;else{out.injectiveChecks++;ok(overlap(im,V[i],C.free.length)===W[i].length&&rank(V[i],C.free.length)===W[i].length);}}out.maxBad=Math.max(out.maxBad,bad);out.badBoundChecks++;ok(bad<=s*B*C.h);
let r=Math.max(...W.map(a=>a.length),0),max0=0,max1=0;for(let mask=1;mask<(1<<F.length)-1;mask++){if(!(mask&1))continue;let A=[],B0=[],A1=[],B1=[];for(let i=0;i<F.length;i++){if(mask&(1<<i)){A.push(...W[i]);A1.push(...V[i]);}else{B0.push(...W[i]);B1.push(...V[i]);}}let x=overlap(A,B0,n),y=overlap(A1,B1,C.free.length);out.cutChecks++;ok(y>=x-C.h-r*bad);max0=Math.max(max0,x);max1=Math.max(max1,y);out.maxObservedLoss=Math.max(out.maxObservedLoss,x-y);}return {h:C.h,bad,max0,max1};}
const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
const specs=[];for(let j=-1;j<14;j++)specs.push({n:7,edges:fano,j,name:"Fano"});for(let k=3;k<=4;k++)specs.push({n:2*k,edges:Array.from({length:k},(_,i)=>[i,(i+1)%k,k+i]),j:-1,name:"loose-cycle"});
for(const {n,edges,j,name} of specs){const F=edges.map((e,i)=>mk(e,j>=0&&Math.floor(j/2)===i?1+(j%2):3));const full=chart(n,[]);const models=full.words.filter(z=>F.every(f=>f.eval(z)));out.rootCases++;out[models.length?"SAT":"UNSAT"]++;if(name==="Fano"){ok(models.length===(j<0?0:5));out.fano.push({owner:j,models:models.length});}
const root=close(n,F,[]);out.rootPins+=root.pins;ok(root.pins===0&&!root.contr);
const choices=[[],[0]];if(name==="loose-cycle")choices.push([n-2,n-1]);
for(let S of choices){const G=project(F,S),priv=S.reduce((a,v)=>a|(1<<v),0),live=((1<<n)-1)^priv;const support=new Set(models.map(z=>z&live));for(let z of full.words){out.projectionWordChecks++;ok(G.every(f=>f.eval(z))===support.has(z&live));}const W=G.map(f=>spectrum(f,full));let s=Math.max(...G.map(f=>pc(f.scope))),B=Math.max(...Array.from({length:n},(_,v)=>G.filter(f=>f.scope&(1<<v)).length));
for(let k=0;k<6;k++){let eq=[];for(let i=0;i<k;i++){let row=(rand()>>>12)&live;if(!row)row=live&-live;eq.push([row,(rand()>>>16)&1]);}out.guardCases++;let a=check(n,G,W,eq,s,B);let C0=chart(n,eq);if(!C0)continue;let before=C0.words.filter(z=>G.every(f=>f.eval(z)));let c=close(n,G,eq);out.conditionalPins+=c.pins;out.localContradictions+=+c.contr;out.closedCharts++;let after=c.C?c.C.words.filter(z=>G.every(f=>f.eval(z))):[];ok(before.length===after.length&&before.every(z=>after.includes(z)));if(c.contr)ok(!before.length);if(c.pins){let b=check(n,G,W,c.eq,s,B);if(out.examples.length<6)out.examples.push({name,owner:j,S,before:a,after:b});}}
}}
return out;
}
console.log(JSON.stringify(main(),null,2));
