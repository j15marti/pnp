function run(){
let seed=20261124;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}
function parity(x){let p=0;while(x){p^=1;x&=x-1}return p}
function basis(a){let b=[];for(let x of a){for(let y of b)x=Math.min(x,x^y);if(x){b.push(x);b.sort((a,b)=>b-a)}}return b}
function has(b,x){return basis([...b,x]).length===b.length}
function orth(b,n){let rows=basis(b),piv=new Set(rows.map(x=>31-Math.clz32(x))),out=[];for(let j=0;j<n;j++)if(!piv.has(j)){let v=1<<j;for(let i=rows.length-1;i>=0;i--){let x=rows[i],k=31-Math.clz32(x);if(parity(x&v))v|=1<<k}out.push(v)}return basis(out)}
function inter(a,b,n){return orth(basis([...orth(a,n),...orth(b,n)]),n)}
function recognize(U,n){let V=Array.from({length:n},(_,i)=>1<<i),R=U.map(basis),out=[];while(V.length){let I=V,skip=[];for(let X of R){let T=inter(I,X,n);if(T.length)I=T;else skip.push(X)}let v=I[0],S=basis(skip.flat());if(has(S,v))return null;let f=orth(S,n).find(x=>parity(x&v));if(f===undefined)throw Error("separate");out.push(v);let H=orth([f],n);V=inter(V,H,n);R=R.map(X=>inter(X,H,n))}return out}
function adapted(U,B){return B!==null&&U.every(X=>B.filter(v=>has(X,v)).length===X.length)}
function bases(n){let out=[];function go(a,start){if(a.length===n){out.push(a);return}for(let x=start;x<1<<n;x++)if(!has(basis(a),x))go([...a,x],x+1)}go([],1);return out}
function spaces(n){let m=new Map();for(let B of bases(n))for(let z=0;z<1<<n;z++){let a=basis(B.filter((_,i)=>(z>>i)&1));let k=Array.from({length:1<<n},(_,i)=>i).filter(x=>has(a,x)).join(",");m.set(k,a)}return [...m.values()]}
let r={seed:20261124,arrangements3:0,arrangements3Accept:0,random4:0,random4Accept:0,mixedCoordinate:0,decisionCases:0,SAT:0,UNSAT:0,closurePins:0,closureContradictions:0,pointwiseChecks:0,witnesses:0};
let S=spaces(3).filter(x=>x.length>0&&x.length<3),B3=bases(3),B4=bases(4),S4=spaces(4);
for(let mask=0;mask<1<<S.length;mask++){let U=S.filter((_,i)=>(mask>>i)&1),B=recognize(U,3),ref=B3.some(x=>adapted(U,x));if(!!B!==ref||B&&!adapted(U,B))throw Error("arr3");r.arrangements3++;r.arrangements3Accept+=!!B}
for(let k=0;k<300;k++){let U=Array.from({length:1+rnd(8)},()=>S4[rnd(S4.length)]),B=recognize(U,4),ref=B4.some(x=>adapted(U,x));if(!!B!==ref||B&&!adapted(U,B))throw Error("arr4");r.random4++;r.random4Accept+=!!B}
function mix(n){let B=Array.from({length:n},(_,i)=>1<<i);for(let k=0;k<8*n;k++){let i=rnd(n),j=rnd(n);if(i!==j)B[i]^=B[j]}return B}
function evalEvent(E,x){return E.every(([a,b])=>parity(a&x)===b)}
function reduce(E,H,n){let out=[];let bH=basis(H.map(([a,b])=>a|(b<<n))); // use augmented elimination below, with coefficient pivots, not RHS pivot
let rows=[];for(let [a,b] of [...H,...E]){for(let [u,v] of rows)if((a>>(31-Math.clz32(u)))&1){a^=u;b^=v}if(!a){if(b)return null;continue}rows.push([a,b]);rows.sort((x,y)=>y[0]-x[0])}
let h=H.length;return rows.filter(([a])=>!has(basis(H.map(x=>x[0])),a)) // not used; quotient via chart below
}
function chart(H,n){let R=[];for(let [a,b] of H){for(let [u,v] of R)if((a>>(31-Math.clz32(u)))&1){a^=u;b^=v}if(!a){if(b)return null;continue}R.push([a,b]);R.sort((x,y)=>y[0]-x[0])}let x=0;for(let i=R.length-1;i>=0;i--){let [a,b]=R[i];if(parity(a&x)!==b)x|=1<<(31-Math.clz32(a))}return [x,orth(R.map(x=>x[0]),n)]}
function project(E,x,B){let R=[];for(let [a,b] of E){let u=0;for(let j=0;j<B.length;j++)u|=parity(a&B[j])<<j;b^=parity(a&x);for(let [v,w] of R)if((u>>(31-Math.clz32(v)))&1){u^=v;b^=w}if(!u){if(b)return null;continue}R.push([u,b]);R.sort((x,y)=>y[0]-x[0])}return R}
function closure(E,n){let H=[];while(true){let [x,B]=chart(H,n),P=[],pin=null;for(let a of E){let e=project(a,x,B);if(e===null)continue;if(!e.length){r.closureContradictions++;return null}if(e.length===1){ // choose actual original row nonconstant; forcing its opposite
pin=a.find(([u])=>B.some(v=>parity(u&v)));pin=[pin[0],pin[1]^1];break}P.push(e)}if(pin){H.push(pin);r.closurePins++;continue}return {x,B,P,H}}}
function test(E,n){r.decisionCases++;let orig=Array.from({length:1<<n},(_,x)=>x).filter(x=>E.every(e=>!evalEvent(e,x)));let C=closure(E,n);if(!C){if(orig.length)throw Error("closure");r.UNSAT++;return}let {x,B,P}=C,d=B.length,U=P.map(e=>basis(e.map(a=>a[0]))),D=recognize(U,d);if(!D)throw Error("coordinate promise after coordinate pins");let clauses=P.map((e,i)=>D.map((v,j)=>[v,j]).filter(([v])=>has(U[i],v)).map(([v,j])=>{let found=false,b;for(let z=0;z<1<<e.length;z++){let u=0,w=0;for(let k=0;k<e.length;k++)if(z>>k&1){u^=e[k][0];w^=e[k][1]}if(u===v){found=true;b=w;break}}if(!found)throw Error("row");return [j,b]}));let good=[];for(let z=0;z<1<<d;z++){let y=0;for(let j=0;j<d;j++)if(z>>j&1)y^=B[j];y^=x;let w=0;for(let j=0;j<d;j++)w|=parity(D[j]&z)<<j;let a=clauses.every(c=>c.some(([j,b])=>((w>>j)&1)!==b));let ref=E.every(e=>!evalEvent(e,y));if(a!==ref)throw Error("pointwise");r.pointwiseChecks++;if(a)good.push(y)}if(good.length!==orig.length)throw Error("count");if(good.length){r.SAT++;r.witnesses++}else r.UNSAT++}
for(let k=0;k<200;k++){let n=3+rnd(5),B=mix(n);let U=Array.from({length:2+rnd(12)},()=>B.filter(()=>rnd(7)<4));let X=recognize(U.map(basis),n);if(!adapted(U.map(basis),X))throw Error("mixed");r.mixedCoordinate++;let E=U.filter(u=>u.length).map(u=>u.map(a=>[a,rnd(3)&1]));test(E,n)}
for(let n=2;n<=7;n++){let B=mix(n),E=Array.from({length:1<<Math.min(n,3)},(_,z)=>B.slice(0,Math.min(n,3)).map((a,j)=>[a,(z>>j)&1]));test(E,n);test(E.slice(1),n)}
return r}
console.log(JSON.stringify(run(),null,2));
