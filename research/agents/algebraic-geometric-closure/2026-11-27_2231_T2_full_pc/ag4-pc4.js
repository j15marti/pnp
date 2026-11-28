function prove(x){
const F=x.dimacs.trimEnd().split("\n").slice(1).map(c=>c.split(" ").map(Number).slice(0,-1)),n=x.n,d=4,pop=m=>{let k=0;while(m){m&=m-1;k++}return k};
let ms=Array.from({length:2**n},(_,i)=>i).filter(i=>pop(i)<=d),M=new Map(ms.map((m,i)=>[m,1n<<BigInt(i)])),inv=new Map([...M].map(([m,b])=>[b,m]));
let lines=[],B=new Map(),events=0,sweeps=0;
function record(r,op){let i=lines.length;lines.push({r,op});return i}
function add(i){let r=lines[i].r;while(r){events++;let p=r&-r;if(!B.has(p)){B.set(p,i);return true}let j=B.get(p);r^=lines[j].r;i=record(r,["x",i,j])}return false}
function poly(c){let P=new Set([0]);for(let l of c){let Q=new Set(),v=1<<(Math.abs(l)-1);function t(m){if(Q.has(m))Q.delete(m);else Q.add(m)}for(let m of P){t(m|v);if(l>0)t(m)}P=Q}let z=0n;for(let m of P)z^=M.get(m);return z}
for(let i=0;i<F.length;i++)add(record(poly(F[i]),["a",i+1]));
function goal(){let r=1n,ls=[];while(r){let p=r&-r;if(!B.has(p))return -1;let j=B.get(p);ls.push(j);r^=lines[j].r}let i=ls[0];for(let j of ls.slice(1))i=record(lines[i].r^lines[j].r,["x",i,j]);return i}
let end=goal();while(end<0){let old=B.size;sweeps++;for(let i=0;i<n;i++){let v=1<<i,high=0n,mp=new Map(),H=new Map();for(let m of ms){events++;let b=M.get(m),t=M.get(m|v);if(t===undefined)high|=b;else mp.set(b,t)}
for(let j of [...B.values()]){let r=lines[j].r,h=r&high;while(h){events++;let p=h&-h;if(!H.has(p)){H.set(p,j);break}let k=H.get(p);r^=lines[k].r;j=record(r,["x",j,k]);h=r&high}if(!h&&r){let y=0n;while(r){events++;let b=r&-r;r^=b;y^=mp.get(b)}add(record(y,["m",j,i+1]))}if(events>1000000)throw Error("cap")}
end=goal();if(end>=0)break}if(end<0&&old===B.size)throw Error("no proof")}
let keep=new Set(),todo=[end];while(todo.length){let i=todo.pop();if(keep.has(i))continue;keep.add(i);let o=lines[i].op;if(o[0]==="x")todo.push(o[1],o[2]);if(o[0]==="m")todo.push(o[1])}
let order=[...keep].sort((a,b)=>a-b),map=new Map(order.map((x,i)=>[x,i]));let proof=order.map(i=>{let o=lines[i].op.slice();if(o[0]==="x"){o[1]=map.get(o[1]);o[2]=map.get(o[2])}if(o[0]==="m")o[1]=map.get(o[1]);return o});
return {proof,events,generated:lines.length,rank:B.size,sweeps}
}
function verify(x,P){
let F=x.dimacs.trimEnd().split("\n").slice(1).map(c=>c.split(" ").map(Number).slice(0,-1)),R=[],events=0,peakMonomials=0,stored=0;const pop=m=>{let k=0;while(m){m&=m-1;k++}return k};function toggle(S,m){events++;if(S.has(m))S.delete(m);else S.add(m)}
for(let o of P){let s=new Set();if(o[0]==="a"){if(!F[o[1]-1])throw Error("axiom");s.add(0);for(let l of F[o[1]-1]){let t=new Set();for(let m of s){toggle(t,m|(1<<(Math.abs(l)-1)));if(l>0)toggle(t,m)}s=t}}else if(o[0]==="x"){if(!R[o[1]]||!R[o[2]])throw Error("order");for(let m of R[o[1]])toggle(s,m);for(let m of R[o[2]])toggle(s,m)}else if(o[0]==="m"){if(!R[o[1]]||o[2]<1||o[2]>x.n)throw Error("mul");for(let m of R[o[1]])toggle(s,m|(1<<(o[2]-1)))}else throw Error("op");if([...s].some(m=>pop(m)>4))throw Error("degree");R.push(s);stored+=s.size;peakMonomials=Math.max(peakMonomials,s.size)}
if(R.at(-1).size!==1||!R.at(-1).has(0))throw Error("not one");return {events,peakMonomials,stored,lines:R.length}
}
module.exports={prove,verify};
