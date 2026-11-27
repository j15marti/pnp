// C08-18 cross-track check; node cooperative_audit.js (requires algebra_results.json in same directory)
function coopAudit(data){
let checks=0;function ok(v,msg){checks++;if(!v)throw Error(msg||"check "+checks)}function par(x){x^=x>>>16;x^=x>>>8;x^=x>>>4;return(0x6996>>>(x&15))&1}
function gf(d,rows=[]){let A=Array(d).fill(null),rank=0,bad=false;function red(a,b=0){for(let i=d-1;i>=0;i--)if(A[i]&&((a>>>i)&1)){a^=A[i][0];b^=A[i][1]}return[a,b]}function add(a,b){[a,b]=red(a,b);if(!a){bad||=!!b;return b?-1:0}A[31-Math.clz32(a)]=[a,b];rank++;return 1}for(let [a,b] of rows)add(a,b);function solve(x=0){for(let i=0;i<d;i++)if(A[i]&&(par(A[i][0]&x)!==A[i][1]))x^=1<<i;return x}return{red,add,solve,get bad(){return bad},get rank(){return rank},get rows(){return A.filter(Boolean)}}}
function mul(a,b){let r=0;while(b){if(b&1)r^=a;b>>>=1;a<<=1;if(a&64)a^=67}return r}
let a=Array.from({length:64},(_,t)=>1|(t<<1)|(mul(mul(t,t),t)<<7)),b=a.map((_,i)=>((i<32?648477357:3348622548)>>>(i%32))&1),B=Array.from({length:32},(_,i)=>[4*i+1,4*i+3]),d=13;
function valid(z){let y=a.map((r,i)=>par(r&z)^b[i]);return B.every(([u,v])=>y[u>>1]===(u&1)||y[v>>1]===(v&1))}
function closure(rows){let H=gf(d,rows),rounds=[],total=0;for(;;){if(H.bad)return{status:"UNSAT",why:"linear contradiction",rounds,total,rows:H.rows};let L=B.slice(),R=new Map;
for(let i=0;i<a.length;i++){let [r,s]=H.red(a[i],b[i]);if(!r)L.push([2*i+s,2*i+s]);else if(R.has(r)){let[j,t]=R.get(r),u=t^s;L.push([2*i,2*j+(1^u)],[2*i+1,2*j+u])}else R.set(r,[i,s])}
let m=128,A=Array.from({length:m},()=>[]),P=Array.from({length:m},()=>[]);for(let [u,v] of L){A[u^1].push(v);A[v^1].push(u);P[v].push(u^1);P[u].push(v^1)}
let Reach=Array.from({length:m},(_,i)=>{let S=new Set([i]),q=[i];for(let j=0;j<q.length;j++)for(let v of A[q[j]])if(!S.has(v)){S.add(v);q.push(v)}return S});total++;
for(let i=0;i<64;i++)if(Reach[2*i].has(2*i+1)&&Reach[2*i+1].has(2*i))return{status:"UNSAT",why:"contradictory implication paths",rounds,total,rows:H.rows,contradictionObservation:i};
let r0=H.rank;for(let i=0;i<64;i++){for(let t of [0,1])if(Reach[2*i+(1^t)].has(2*i+t))H.add(a[i],b[i]^t);for(let j=0;j<i;j++)for(let t of [0,1])if(Reach[2*i].has(2*j+t)&&Reach[2*j+t].has(2*i))H.add(a[i]^a[j],b[i]^b[j]^t)}
rounds.push({rankBefore:r0,rankAfter:H.rank,consistent:!H.bad});if(H.bad)continue;if(H.rank===r0)return{status:valid(H.solve())?"SAT":"UNKNOWN",rounds,total,rows:H.rows};}}
const rows=data.results[0].tests[0].affineRows;
let initial=closure([]),after=closure(rows),profiles=0,accepted=0;for(let z=0;z<8192;z++)if(rows.every(([r,s])=>par(r&z)===s)){profiles++;if(valid(z))accepted++}
ok(initial.status==="UNKNOWN");ok(gf(13,rows).rank===7);ok(profiles===64&&!accepted);if(after.status==="UNSAT")ok(!accepted);return{checks,degree2Rows:rows,initial,after,profiles,accepted};
}
console.log(JSON.stringify(coopAudit(JSON.parse(require('fs').readFileSync(require('path').join(__dirname,'algebra_results.json'),'utf8'))),null,2));
