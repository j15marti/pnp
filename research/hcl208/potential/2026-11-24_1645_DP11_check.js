function run(){
const out={seed:20261124,rankCalls:0,exchangeTests:0,augmentations:0,closureScans:0,closurePins:0,referenceWords:0,lifts:0,assertions:0,small:{SAT:0,UNSAT:0},cube:{SAT:0,UNSAT:0},fano:{SAT:0,UNSAT:0},scales:[]};
const ok=(v)=>{out.assertions++;if(!v)throw Error("assertion "+out.assertions)};
let seed=out.seed>>>0;const rand=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};
const bit=i=>1<<i;const par=x=>{let y=x>>>0;y^=y>>>16;y^=y>>>8;y^=y>>>4;return (0x6996>>>(y&15))&1};
function basis(rows){out.rankCalls++;let b=[];for(let x of rows){for(const y of b)if(x&(1<<(31-Math.clz32(y))))x^=y;if(x){b.push(x);b.sort((a,c)=>(c>>>0)-(a>>>0))}}return b}
const rank=r=>basis(r).length;
function reduce(x,b){for(const y of b)if(x&(1<<(31-Math.clz32(y))))x^=y;return x}
function solve(rows){let b=new Map();for(let [x,y] of rows){while(x){let p=31-Math.clz32(x);if(!b.has(p)){b.set(p,[x,y]);break}let [a,c]=b.get(p);x^=a;y^=c}if(!x&&y)return null}let z=0;for(const p of [...b.keys()].sort((a,c)=>a-c)){let [x,y]=b.get(p);if(par(x&z)!==y)z|=bit(p)}return z}
const matches=(rows,z)=>rows.every(([x,y])=>par(x&z)===y);
const legal=(F,z)=>F.every(e=>!matches(e,z));
function closure(F,H){H=H.map(x=>x.slice());while(true){if(solve(H)===null)return {bad:true,H};let changed=false;for(const e of F){out.closureScans++;if(solve(H.concat(e))===null)continue;let b=basis(H.map(x=>x[0]));let d=rank(b.concat(e.map(x=>x[0])))-b.length;if(!d)return {bad:true,H};if(d===1){let row=e.find(x=>reduce(x[0],b));H.push([row[0],row[1]^1]);out.closurePins++;changed=true;break}}if(!changed)return {bad:false,H}}}
function maxmatch(F,Q,initial=[]){let b=basis(Q),rows=F.flatMap((e,i)=>e.map(([a,y])=>({i,a,y,v:reduce(a,b)})));let S=[];for(const o of initial){let j=rows.findIndex(x=>x.i===o.i&&x.a===o.a&&x.y===o.y);if(j>=0&&rank(S.map(k=>rows[k].v).concat(rows[j].v))>S.length)S.push(j)}
let initialSize=S.length;
while(true){let used=new Set(S),owners=new Set(S.map(j=>rows[j].i)),prev=new Map(),queue=[];for(let j=0;j<rows.length;j++)if(!used.has(j)&&!owners.has(rows[j].i)){prev.set(j,-1);queue.push(j)}let end=-1;for(let h=0;h<queue.length&&end<0;h++){let j=queue[h];if(!used.has(j)){out.exchangeTests++;if(rank(S.map(k=>rows[k].v).concat(rows[j].v))===S.length+1){end=j;break}for(let k of S){if(prev.has(k))continue;out.exchangeTests++;if(rank(S.filter(t=>t!==k).map(t=>rows[t].v).concat(rows[j].v))===S.length){prev.set(k,j);queue.push(k)}}}else{for(let k=0;k<rows.length;k++)if(!used.has(k)&&!prev.has(k)&&(rows[k].i===rows[j].i||!owners.has(rows[k].i))){prev.set(k,j);queue.push(k)}}}
if(end<0)break;let X=new Set(S);for(let j=end;j!==-1;j=prev.get(j)){if(X.has(j))X.delete(j);else X.add(j)}S=[...X];out.augmentations++;ok(new Set(S.map(j=>rows[j].i)).size===S.length&&rank(S.map(j=>rows[j].v))===S.length)}
return {t:S.length,rows:S.map(j=>rows[j]),initialSize}}
function core(F,Q){let t=maxmatch(F,Q).t,d=F.length-t,C=[];for(let i=0;i<F.length;i++){let K=F.filter((_,j)=>j!==i);if(K.length-maxmatch(K,Q).t<d)C.push(i)}return {C,d,t}}
function bruteCore(F,Q){let base=rank(Q),best=-1,intersection=0;for(let mask=0;mask<2**F.length;mask++){let J=F.filter((_,i)=>mask&bit(i));let d=J.length-(rank(Q.concat(J.flat().map(x=>x[0])))-base);if(d>best){best=d;intersection=mask}else if(d===best)intersection&=mask}return {d:best,C:F.map((_,i)=>i).filter(i=>intersection&bit(i))}}
function common(F,H,P,W=[]){let Q=H.map(x=>x[0]).concat(P,W),a=core(F,Q),C=a.C.map(i=>F[i]),K=F.filter((_,i)=>!a.C.includes(i));let sel=maxmatch(K,Q.concat(C.flat().map(x=>x[0])));ok(sel.t===K.length);return {...a,Cf:C,K,lift:sel.rows.map(x=>[x.a,x.y^1])}}
function audit(F,H,P,n,bucket){let root=closure(F,H);if(root.bad){let count=0;for(let z=0;z<2**n;z++){out.referenceWords++;if(matches(H,z)&&legal(F,z))count++}ok(count===0);bucket.UNSAT++;return}
H=root.H;let Q=H.map(x=>x[0]),parent=core(F,Q),base=common(F,H,P);ok(parent.C.every(i=>base.C.includes(i)));ok(base.d>=parent.d&&base.d<=parent.d+rank(Q.concat(P))-rank(Q));if(F.length<=9){let b=bruteCore(F,Q.concat(P));ok(b.d===base.d&&JSON.stringify(b.C)===JSON.stringify(base.C))}
for(let w=0;w<2**P.length;w++){let G=H.concat(P.map((a,i)=>[a,(w>>i)&1]));if(solve(G)===null)continue;let cl=closure(F,G),cc=closure(base.Cf,G),ref=false,projected=false;let R=F.map((e,i)=>({e,i})).filter(x=>solve(G.concat(x.e))!==null),rc=core(R.map(x=>x.e),Q.concat(P));ok(rc.C.every(i=>base.C.includes(R[i].i)));for(let z=0;z<2**n;z++){out.referenceWords++;if(!matches(G,z))continue;let r=legal(F,z),c=legal(base.Cf,z);ref||=r;projected||=c;if(c){let x=solve(G.concat(base.Cf.flat().map(([a])=>[a,par(a&z)]),base.lift));ok(x!==null&&matches(G,x)&&legal(F,x));out.lifts++}}ok(ref===projected);if(cl.bad||cc.bad)ok(!ref);if(ref)ok(!cl.bad&&!cc.bad);bucket[ref?"SAT":"UNSAT"]++}}
const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
const nae=tr=>[[bit(tr[0])^bit(tr[1]),0],[bit(tr[0])^bit(tr[2]),0]];
const mono=(tr,b)=>tr.map(i=>[bit(i),b]);
let ff=fano.map(nae);audit(ff,[],[],7,out.fano);for(let i=0;i<7;i++)for(let b=0;b<2;b++)audit(ff.map((e,j)=>i===j?mono(fano[i],b):e),[],[],7,out.fano);
for(let s=0;s<256;s++){let F=[];for(let w=0;w<8;w++)if(s&bit(w))F.push([0,1,2].map(i=>[bit(i),(w>>i)&1]));audit(F,[],[],3,out.cube)}
for(let z=0;z<90;z++){let n=5+rand(3),F=[];for(let i=0,m=2+rand(7);i<m;i++){let e=[];for(let j=0,l=2+rand(2);j<l;j++)e.push([1+rand((1<<n)-1),rand(2)]);F.push(e)}let P=[1+rand((1<<n)-1),1+rand((1<<n)-1)];audit(F,[],P,n,out.small)}
for(let n of [4,6,8,12,16,20]){let F=Array.from({length:n},(_,i)=>[[bit(i),0],[bit((i+1)%n),0]]),P=[bit(0)^bit(n/2)];let a=core(F,[]),b=core(F,P);ok(a.C.length===0&&a.d===0&&b.C.length===n&&b.d===1);let M=maxmatch(F,[]),M2=maxmatch(F,P,M.rows);ok(M.t===n&&M2.t===n-1&&M2.initialSize===n-1);
let pins=out.closurePins;for(let w=0;w<2;w++){let G=[[P[0],w]],cl=closure(F,G);ok(!cl.bad&&cl.H.length===1);let x=(1<<n)-1;if(w)x^=1;ok(matches(G,x)&&legal(F,x))}
ok(out.closurePins===pins);
let tail=F.map(e=>e.map(([a,y])=>[a<<7,y])),tP=P.map(a=>a<<7);let t=bit(n+7);let connected=ff.concat(tail,[[[t,0],[bit(7),0],[1,0]]]);let root=core(connected,[]),child=core(connected,tP);ok(root.C.length===7&&child.C.length===7+n&&child.d===root.d+1);let relaxed=connected.map((e,i)=>i===0?mono(fano[0],0):e);let rr=core(relaxed,[]),rc=core(relaxed,tP);ok(rr.C.length===0&&rc.C.length===n);let fa=[...Array(128).keys()].find(z=>legal(relaxed.slice(0,7),z));ok(fa!==undefined);for(let w=0;w<2;w++){let G=[[tP[0],w]],cl=closure(connected,G);ok(!cl.bad&&cl.H.length===1);let y=fa|(((1<<n)-1)<<7)|t;if(w)y^=bit(7);ok(matches(G,y)&&legal(relaxed,y));}out.scales.push({n,rootCore:root.C.length,childCore:child.C.length,SATneighborRootCore:rr.C.length,SATneighborChildCore:rc.C.length,rankLoss:M.t-M2.t,repairAugmentations:M2.t-M2.initialSize})}
return out;
}
console.log(JSON.stringify(run(),null,2));
