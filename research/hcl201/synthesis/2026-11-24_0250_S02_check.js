function experiment(){
let seed=0x2015026;const rnd=n=>{seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return (seed>>>0)%n;};
const pc=x=>{let c=0;while(x){x&=x-1;c++}return c};
const rank=xs=>{let b=[];for(let x of xs){while(x){let j=31-Math.clz32(x);if(b[j])x^=b[j];else{b[j]=x;break;}}}return b.filter(Boolean).length;};
const image=(D,m)=>D.reduce((x,v,j)=>m>>j&1?x^v:x,0);
const stats={seed:"0x2015026",instances:0,targets:0,sat:0,unsat:0,lifts:0,oracleCalls:0,augmentations:0,hallChecks:0,nonzeroNullityInstances:0,scaling:[]};
function intersection(T,M,n){
let E=[];for(let j=0;j<n;j++)if(T>>j&1)for(let i=0;i<M.length;i++)E.push([i,j]);
let I=new Set();
function good(S,which){stats.oracleCalls++;if(which===2){let z=0;for(let e of S){let j=E[e][1];if(z>>j&1)return false;z|=1<<j;}return true;}let z=M.map(()=>0);for(let e of S){let [i,j]=E[e];z[i]|=1<<j;}return z.every((x,i)=>M[i].has(x));}
function change(I,del,add){let s=new Set(I);if(del!==-1)s.delete(del);s.add(add);return s;}
while(true){let p=new Map(),Q=[];for(let y=0;y<E.length;y++)if(!I.has(y)&&good(change(I,-1,y),1)){p.set(y,-1);Q.push(y);}
let end=-1;for(let k=0;k<Q.length;k++){let x=Q[k];if(!I.has(x)&&good(change(I,-1,x),2)){end=x;break;}
for(let y=0;y<E.length;y++)if(!p.has(y)&&I.has(x)!==I.has(y)){
let a=I.has(x)?good(change(I,x,y),1):good(change(I,y,x),2);
if(a){p.set(y,x);Q.push(y);}
}}
if(end===-1)break;
while(end!==-1){if(I.has(end))I.delete(end);else I.add(end);end=p.get(end);}
stats.augmentations++;if(!good(I,1)||!good(I,2))throw Error("invalid exchange");
if(I.size===pc(T))break;
}
if(I.size!==pc(T))return null;
let out=M.map(()=>0);for(let e of I){let [i,j]=E[e];out[i]|=1<<j;}return out;
}
function affineLifts(D,t){
let b=[],v=[],ker=[];for(let j=0;j<D.length;j++){let x=D[j],z=1<<j;while(x){let k=31-Math.clz32(x);if(b[k]){x^=b[k];z^=v[k];}else{b[k]=x;v[k]=z;break;}}if(!x)ker.push(z);}
let a=0;while(t){let k=31-Math.clz32(t);if(!b[k])return [];t^=b[k];a^=v[k];}
let L=[a];for(let z of ker)L=L.concat(L.map(x=>x^z));return L;
}
function hall(T,M){for(let U=T;;U=(U-1)&T){let s=0;for(let m of M){let r=0;for(let x of m)if((x&U)===x)r=Math.max(r,pc(x));s+=r;}if(pc(U)>s)return false;if(!U)break;}return true;}
function run(D,M,a,d,all=true){let n=D.length;let support=new Set([a]);for(let m of M){let next=new Set();for(let x of support)for(let z of m)next.add(x^image(D,z));support=next;}
stats.instances++;if(rank(D)<n)stats.nonzeroNullityInstances++;
for(let t=0;t<1<<d;t++){if(!all&&t!==0&&t!==(1<<d)-1)continue;stats.targets++;let w=null;for(let T of affineLifts(D,t^a)){stats.lifts++;let q=intersection(T,M,n),h=hall(T,M);stats.hallChecks++;if(Boolean(q)!==h)throw Error("Hall mismatch");if(q){w=q;break;}}
if(Boolean(w)!==support.has(t))throw Error("decision mismatch");if(w){stats.sat++;let x=a;for(let i=0;i<w.length;i++){if(!M[i].has(w[i]))throw Error("bad lift");x^=image(D,w[i]);}if(x!==t)throw Error("bad target");}else stats.unsat++;}
}
for(let trial=0;trial<180;trial++){let n=3+rnd(5),d=2+rnd(5),h=2+rnd(4);let D=Array.from({length:n},(_,j)=>trial%3===0&&n<=d?1<<j:rnd(1<<d));let M=[];for(let i=0;i<h;i++){let cols=Array.from({length:n},()=>rnd(1<<(1+rnd(3))));let m=new Set();for(let z=0;z<1<<n;z++){let a=cols.filter((_,j)=>z>>j&1);if(rank(a)===a.length)m.add(z);}M.push(m);}run(D,M,rnd(1<<d),d);}
for(let n of [4,6,8,10,12,14,16]){let M=Array.from({length:n-1},(_,j)=>new Set([0,1<<j,1<<(j+1)]));let D=Array.from({length:n},(_,j)=>1<<j),t=(1<<n)-1;let q=intersection(t,M,n),p=intersection(t^1,M,n);if(q||!p)throw Error("path controls");stats.scaling.push({n,RT02_min_variation_rank:n/2,unsat_full:true,sat_delete:true,witness:p});}
return stats;
}
console.log(JSON.stringify(experiment(),null,2));
