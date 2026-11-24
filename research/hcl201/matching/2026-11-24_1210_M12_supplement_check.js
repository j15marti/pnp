function run(){
let seed=11241210;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};
const bit=(x,i)=>Number((x>>BigInt(i))&1n), parity=x=>{let s=0;while(x){s^=1;x&=x-1n}return s};
const stats={hist:0,localWords:0,convolutions:0,signChecks:0,closureScans:0,forcedPins:0,creditChecks:0,witnesses:0,random:{SAT:0,UNSAT:0,UNKNOWN:0,referenceSAT:0,referenceUNSAT:0,improved:0},scales:[],controls:{}};
function event(n,rows,H,w=rows.map(()=>2)){let par=Array.from({length:n},(_,i)=>i),find=i=>par[i]===i?i:par[i]=find(par[i]);let groups=new Map(),constant=[0,0];for(let [m] of rows){let v=[];for(let i=0;i<n;i++)if(bit(m,i))v.push(i);for(let i=1;i<v.length;i++)par[find(v[i])]=find(v[0]);}for(let i=0;i<n;i++){let j=find(i);if(!groups.has(j))groups.set(j,{v:[],r:[]});groups.get(j).v.push(i)}let net=w.reduce((a,b)=>a+b,0);for(let j=0;j<rows.length;j++){let [m,a]=rows[j],o=w[j]%2;if(m===0n){constant[0]+=a;constant[1]+=a^o;}else {let i=0;while(!bit(m,i))i++;groups.get(find(i)).r.push([m,a,o]);}}return {n,rows,w,H,net,constant,g:[...groups.values()],bad:(a,b)=>a>H||b>net-H};}
function local(g,pins,flip=-1){let base=0n,free=[];for(let i of g.v){if(i===flip)continue;if(pins[i]<0)free.push(i);else if(pins[i])base|=1n<<BigInt(i);}let out=new Map();for(let j=0;j<2**free.length;j++){let x=base;for(let k=0;k<free.length;k++)if((j>>k)&1)x|=1n<<BigInt(free[k]);let a=0,b=0,d=0,e=0;for(let [m,c,o] of g.r){let v=parity(m&x)^c, vv=v^(flip>=0?bit(m,flip):0);a+=v;b+=v^o;d+=vv;e+=vv^o;}let key=flip<0?`${a},${b}`:`${a},${b},${d},${e}`;out.set(key,(out.get(key)||0n)+1n);stats.localWords++;}return out}
function conv(A,B){let C=new Map();for(let [a,x] of A){let [i,j]=a.split(",").map(Number);for(let [b,y] of B){let [k,l]=b.split(",").map(Number),key=`${i+k},${j+l}`;C.set(key,(C.get(key)||0n)+x*y);stats.convolutions++;}}return C}
function hist(e,pins,skip=-1){stats.hist++;let h=new Map([[e.constant.join(","),1n]]);for(let i=0;i<e.g.length;i++)if(i!==skip)h=conv(h,local(e.g[i],pins));return h}
function mass(e,pins){let F=0n;for(let [k,v] of hist(e,pins)){let [a,b]=k.split(",").map(Number);if(e.bad(a,b))F+=v}return F}
function signs(e,pins){let s=Array(e.n).fill(3);for(let k=0;k<e.g.length;k++){let g=e.g[k];if(!g.r.length)continue;let outside=hist(e,pins,k);for(let i of g.v){if(pins[i]>=0)continue;let up=true,down=true;for(let [key] of local(g,pins,i)){let [a,b,d,f]=key.split(",").map(Number);for(let [v] of outside){let [j,l]=v.split(",").map(Number),x=e.bad(a+j,b+l),y=e.bad(d+j,f+l);if(x&&!y)up=false;if(y&&!x)down=false;stats.signChecks++;}}s[i]=(up?1:0)|(down?2:0);}}return s}
const M=p=>1n<<BigInt(p.filter(x=>x<0).length);
function masses(E,p){return E.map(e=>mass(e,p))}
function closure(E,p){while(true){stats.closureScans++;let m=M(p),f=masses(E,p);if(f.some(x=>x===m))return false;let done=false;for(let i=0;i<p.length;i++)if(p[i]<0){let a=p.slice(),b=p.slice();a[i]=0;b[i]=1;let mm=m/2n,fa=masses(E,a).some(x=>x===mm),fb=masses(E,b).some(x=>x===mm);if(fa&&fb)return false;if(fa||fb){p[i]=fa?1:0;stats.forcedPins++;done=true;break;}}if(!done)return true;}}
const max=(a,b)=>a>b?a:b;
function forest(E,p){let s=E.map(e=>signs(e,p)),f=masses(E,p),m=M(p),edges=[];for(let i=0;i<E.length;i++)for(let j=0;j<i;j++){let good=s[i].every((v,k)=>v===3||s[j][k]===3||!!(v&s[j][k]));let w=good?f[i]*f[j]:m*max(0n,f[i]+f[j]-m);edges.push({i,j,good,w});}edges.sort((a,b)=>a.w>b.w?-1:a.w<b.w?1:0);let par=E.map((_,i)=>i),find=i=>par[i]===i?i:par[i]=find(par[i]);let t=[];for(let e of edges)if(find(e.i)!==find(e.j)){par[find(e.i)]=find(e.j);t.push(e);}return t;}
function credit(E,p,t){stats.creditChecks++;let m=M(p),f=masses(E,p),U=f.reduce((a,b)=>a+b,0n),c=m*(m-U);for(let {i,j,good} of t)c+=good?f[i]*f[j]:m*max(0n,f[i]+f[j]-m);return {m,U,c,f};}
function bad(e,x){let a=0,b=0;for(let j=0;j<e.rows.length;j++){let [mask,k]=e.rows[j],v=parity(mask&x)^k;a+=v;b+=v^(e.w[j]%2);}return e.bad(a,b)}
function lift(E,p){let x=p.reduce((a,b,i)=>a|(BigInt(b)<<BigInt(i)),0n);for(let e of E){let a=e.rows.map(([m,k])=>parity(m&x)^k),left=e.H-a.reduce((s,v)=>s+v,0);if(left<0||left%2)throw Error("invalid parity");for(let i=0;i<a.length;i++){let add=Math.min(left,2*Math.floor((e.w[i]-a[i])/2));a[i]+=add;left-=add;}if(left||a.some((v,i)=>v<0||v>e.w[i]||v%2!==(parity(e.rows[i][0]&x)^e.rows[i][1]))||a.reduce((s,v)=>s+v,0)!==e.H)throw Error("bad lift");}stats.witnesses++;}
function solve(E,n){let p=Array(n).fill(-1);if(!closure(E,p))return {label:"UNSAT"};let t=forest(E,p),r=credit(E,p,t);if(r.c<=0n){if(!closure(E,p))return {label:"UNSAT"};return {label:"UNKNOWN"};}let improved=r.U>=r.m;while(p.includes(-1)){let i=p.indexOf(-1),a=p.slice(),b=p.slice();a[i]=0;b[i]=1;let A=credit(E,a,t),B=credit(E,b,t);if(2n*(A.c+B.c)<r.c)throw Error("superadditivity");p=A.c>0n?a:b;if(!closure(E,p))throw Error("positive credit rejected");r=credit(E,p,t);if(r.c<=0n)throw Error("lost credit");}lift(E,p);return {label:"SAT",improved};}
function check(E,n){let ref=0;for(let i=0;i<2**n;i++)if(!E.some(e=>bad(e,BigInt(i))))ref++;let res=solve(E,n);if(res.label==="SAT"&&!ref||res.label==="UNSAT"&&ref)throw Error("wrong label");return {ref,...res};}
for(let z=0;z<100;z++){let n=3+rnd(5),E=[];for(let j=0;j<2+rnd(4);j++){let rows=[];for(let k=0;k<2+rnd(6);k++){let mask=BigInt(1+rnd(2**n-1)),a=rnd(2);rows.push([mask,a],[mask,a]);}E.push(event(n,rows,2*rnd(rows.length+1)));}let r=check(E,n);stats.random[r.label]++;stats.random[r.ref?"referenceSAT":"referenceUNSAT"]++;if(r.improved)stats.random.improved++;}
function clause(n,mask){let rows=[];for(let i=0;i<3;i++)rows.push([1n<<BigInt(i),bit(BigInt(mask),i)^1]);rows.push([7n,rows.reduce((a,b)=>a^b[1],0)]);return event(n,rows,2);}
let cube=Array.from({length:8},(_,i)=>clause(3,i));stats.controls.cube=check(cube,3);stats.controls.deletions=cube.map((_,i)=>check(cube.filter((_,j)=>i!==j),3));
let E=[event(1,[[1n,0],[1n,0]],0),event(1,[[1n,1],[1n,1]],0)];stats.controls.opposite=check(E,1);
function scale(n){let m=n/3,rows=[[],[]];for(let j=0;j<m;j++){let sets=[[3*j,3*j+1,3*j+2],[3*j,3*((j+1)%m)+1,3*((j+2)%m)+2]];for(let k=0;k<2;k++)for(let h=1;h<8;h++){let mask=0n;for(let a=0;a<3;a++)if(h&(1<<a))mask|=1n<<BigInt(sets[k][a]);rows[k].push([mask,0]);}}let H=4*(Math.floor(7*m/8)-1),E=rows.map(r=>event(n,r,H));E.push(event(n,Array.from({length:4},(_,i)=>[[1n<<BigInt(i),1],[1n<<BigInt(i),1]]).flat(),6));let p=Array(n).fill(-1); // root scan: each branch has known legal witness with <=2 ones, so no coordinate forced; verify all 2n supports directly.
for(let i=0;i<n;i++)for(let b=0;b<2;b++){let x=(1n<<BigInt(i)) * BigInt(b);if(!b||i>=4)x|=1n<<BigInt(i===0?1:0);if(bit(x,i)!==b||E.some(e=>bad(e,x)))throw Error("scale closure support");}
let t=forest(E,p),r=credit(E,p,t);if(r.U<r.m||r.c<=0n)throw Error("scale no strict improvement");let x=Array(n).fill(0);x[0]=1;lift(E,x);stats.scales.push({n,localWidth:3,jointCycleRank:m+1,UoverM:Number(r.U)/Number(r.m),creditFraction:Number(r.c)/Number(r.m*r.m),exactPairQueries:0,rootSupportWitnesses:2*n});}
for(let n of [24,48,96])scale(n);

// Explicit small positive-correlation escape with conflicting orientations elsewhere.
let make=(inds,H,a=0)=>event(6,inds.flatMap(i=>[[1n<<BigInt(i),a],[1n<<BigInt(i),a]]),H);
let ee=[make([0,1,2],2),make([0,3,4],2),make([0,1,2,5],6,1)];
stats.controls.strictEscape=check(ee,6);
if(!stats.controls.strictEscape.improved||stats.controls.strictEscape.label!=="SAT")throw Error("strict escape failed");

return stats;
}


console.log(JSON.stringify(run(),null,2));
