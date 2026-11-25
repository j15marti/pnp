const H={"n":36,"owners":[{"p":0,"t":[26,32,29],"bad":[0,7]},{"p":0,"t":[27,14,31],"bad":[0,7]},{"p":0,"t":[2,28,25],"bad":[0,7]},{"p":0,"t":[34,8,13],"bad":[0,7]},{"p":0,"t":[10,6,7],"bad":[0,7]},{"p":0,"t":[21,4,30],"bad":[0,7]},{"p":0,"t":[18,11,3],"bad":[0,7]},{"p":0,"t":[9,24,23],"bad":[0,7]},{"p":0,"t":[12,15,35],"bad":[0,7]},{"p":0,"t":[20,0,19],"bad":[0,7]},{"p":0,"t":[5,16,17],"bad":[0,7]},{"p":0,"t":[22,33,1],"bad":[0,7]},{"p":1,"t":[8,17,9],"bad":[0,7]},{"p":1,"t":[12,19,21],"bad":[0,7]},{"p":1,"t":[23,29,6],"bad":[0,7]},{"p":1,"t":[4,0,13],"bad":[0,7]},{"p":1,"t":[34,15,18],"bad":[0,7]},{"p":1,"t":[1,2,3],"bad":[0,7]},{"p":1,"t":[35,14,28],"bad":[0,7]},{"p":1,"t":[16,22,25],"bad":[0,7]},{"p":1,"t":[24,30,27],"bad":[0,7]},{"p":1,"t":[20,31,32],"bad":[0,7]},{"p":1,"t":[33,5,10],"bad":[0,7]},{"p":1,"t":[26,7,11],"bad":[0,7]},{"p":2,"t":[34,31,30],"bad":[0,7]},{"p":2,"t":[11,4,24],"bad":[0,7]},{"p":2,"t":[6,5,15],"bad":[0,7]},{"p":2,"t":[0,2,35],"bad":[0,7]},{"p":2,"t":[9,32,21],"bad":[0,7]},{"p":2,"t":[1,12,20],"bad":[0,7]},{"p":2,"t":[26,19,27],"bad":[0,7]},{"p":2,"t":[16,23,13],"bad":[0,7]},{"p":2,"t":[28,17,3],"bad":[0,7]},{"p":2,"t":[29,10,22],"bad":[0,7]},{"p":2,"t":[25,33,14],"bad":[0,7]},{"p":2,"t":[8,7,18],"bad":[0,7]},{"p":3,"t":[23,0,17],"bad":[0,7]},{"p":3,"t":[2,16,29],"bad":[0,7]},{"p":3,"t":[25,10,8],"bad":[0,7]},{"p":3,"t":[22,27,21],"bad":[0,7]},{"p":3,"t":[32,33,15],"bad":[0,7]},{"p":3,"t":[4,26,3],"bad":[0,7]},{"p":3,"t":[34,19,1],"bad":[0,7]},{"p":3,"t":[13,28,11],"bad":[0,7]},{"p":3,"t":[9,5,30],"bad":[0,7]},{"p":3,"t":[31,12,18],"bad":[0,7]},{"p":3,"t":[24,7,14],"bad":[0,7]},{"p":3,"t":[35,6,20],"bad":[0,7]}]};
const hunt=function(H){
let n=H.n,O=H.owners,stats={nodes:0,scans:0,checks:0};let rows=[];
function job(k,pin,d,pol,cap){
let side=o=>o.p===0||o.p===k?0:1;let own=Array.from({length:n},(_,j)=>O.filter(o=>o.t.includes(j)));
let q=Array(n).fill(-1),nodes=0;if(pin>=0)q[0]=pin;
function set(p,j,v){if(p[j]!==-1&&p[j]!==v)return false;p[j]=v;return true}
if(!set(q,d,pol))return{status:"INCONSISTENT"};
for(let o of own[d])for(let j of o.t)if(j!==d&&!set(q,j,1^pol^side(o)))return{status:"INCONSISTENT"};
const actual=(p,j,o)=>p[j]===-1?-1:p[j]^(j===d?side(o):0);
function propagate(p){
let ch=true;while(ch){let before=p.filter(x=>x!==-1).length;
for(let o of O){stats.scans++;let b=o.t.map(j=>actual(p,j,o));let known=b.filter(v=>v!==-1);
if(known.length===3&&known.every(v=>v===known[0]))return false;
if(known.length===2&&known[0]===known[1]){let j=o.t[b.indexOf(-1)];if(!set(p,j,1^known[0]^(j===d?side(o):0)))return false}}
for(let j=0;j<n;j++){if(j===d||pin>=0&&j===0)continue;let cand=[];
for(let o of own[j])for(let b=0;b<2;b++){stats.scans++;if(o.t.every(i=>{let a=actual(p,i,o);return a===-1||a===(i===j?b:1-b)}))cand.push([o,b])}
if(!cand.length)return false;
if(cand.length===1){let [o,b]=cand[0];for(let i of o.t)if(!set(p,i,(i===j?b:1-b)^(i===d?side(o):0)))return false}}
ch=p.filter(x=>x!==-1).length>before}return true}
function rec(p){if(++nodes>cap)return null;stats.nodes++;if(!propagate(p))return null;let j=p.indexOf(-1);if(j<0)return p;for(let b=0;b<2;b++){let a=p.slice();a[j]=b;let r=rec(a);if(r)return r;if(nodes>cap)return null}return null}
let r=rec(q);if(!r)return{status:nodes>cap?"CAP":"NO SUCH TRAP UNDER TEST GUARD",nodes};
let x=r.reduce((a,b,i)=>a|(BigInt(b)<<BigInt(i)),0n),y=x^(1n<<BigInt(d));
function ok(x,y){return O.every(o=>{stats.checks++;let w=side(o)?y:x,b=o.t.map(i=>Number(w>>BigInt(i)&1n));return b.some(z=>z!==b[0])})}
if(!ok(x,y))throw Error("bad");
for(let s=0;s<3;s++)for(let j=-1;j<n;j++){if(j===d||s===2&&j<0||pin>=0&&j===0)continue;let f=(1n<<BigInt(d))^(j<0?0n:1n<<BigInt(j));let a=x,b=y;if(s===0)a^=f;if(s===1)b^=f;if(s===2){a^=1n<<BigInt(j);b^=1n<<BigInt(j)}if(ok(a,b))throw Error("nonisolated")}
return{status:"ISOLATED",nodes,x:x.toString(),y:y.toString(),d}
}
for(let k=1;k<=3;k++)for(let pin of [-1,0,1]){let ds=pin<0?[0,1,2,3]:[1,2,3,4];for(let d of ds){let r=job(k,pin,d,0,3000);rows.push({k,pin,d,...r});if(r.status==="ISOLATED")break}}
return{rows,stats,scope:"Finite auxiliary guard search for isolated states only; no universal solver, capped at 3000 nodes per test."}
};
console.log(JSON.stringify(hunt(H),null,2));
