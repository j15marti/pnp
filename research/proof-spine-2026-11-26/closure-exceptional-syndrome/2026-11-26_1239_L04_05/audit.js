// L04-05 finite audit. Node.js; no packages. Not a SAT implementation.
function run(){
let checks=0;const assert=(v)=>{checks++;if(!v)throw Error("assert "+checks)};
const bin=n=>n.toString(2),frame=s=>"1".repeat(s.length)+"0"+s;
function encode(rules,x,t,N){let p=frame(rules.map(r=>r.map(z=>frame(bin(z))).join("")).join(""))+frame(x)+frame(bin(t));if(N!==undefined){assert(p.length<=N);p+="0".repeat(N-p.length)}return p}
function decode(w,h){let p=0;function get(s,at){let z=at;while(s[z]==="1")z++;if(s[z]!=="0"||z+1+z-at>s.length)throw Error("frame");return [s.slice(z+1,z+1+z-at),z+1+z-at]}let a,x,t;[a,p]=get(w,p);[x,p]=get(w,p);[t,p]=get(w,p);assert(/^0*$/.test(w.slice(p)));let rows=[];let j=0;while(j<a.length){let r=[];for(let k=0;k<8;k++){let b;[b,j]=get(a,j);assert(/^(0|1[01]*)$/.test(b));r.push(parseInt(b,2))}rows.push(r)}let T=parseInt(t,2);assert(BigInt(T)<=BigInt(w.length)**BigInt(h));return {rows,x,T}}
function machine(bits){let rows=[]; // two writes per output cell, last is correct
for(let i=0;i<bits.length;i++){let q=i===0?0:2*i,mid=2*i+1+1; // distinct states: use 2i+2, but next initial overlaps; corrected below
q=i===0?0:2*i+2;mid=2*i+3;let nxt=i===bits.length-1?1:2*i+4;let v=1+bits[i];
rows.push([q,0,0,mid,3-v,0,2,2],[mid,3-v,0,nxt,v,0,1,2]);}
return rows}
function replay(w,h){let {rows,x,T}=decode(w,h),q=0,p=[0,0],maps=[new Map([...x].map((b,i)=>[i,1+Number(b)])),new Map()],E=[[],[]],i=0;
for(;i<T&&q!==1;i++){let a=maps.map((m,k)=>m.get(p[k])||0),r=rows.filter(z=>z[0]===q&&z[1]===a[0]&&z[2]===a[1]);if(r.length!==1)break;let z=r[0];for(let k=0;k<2;k++){E[k].push({pos:p[k],time:i,read:a[k],write:z[4+k]});maps[k].set(p[k],z[4+k]);p[k]+=[-1,1,0][z[6+k]]}q=z[3]}
return {yes:q===1,E,maps,l:i}}
function sortedExtract(E,j){let P=E.map((_,i)=>i).sort((a,b)=>E[a].pos-E[b].pos||a-b),I=Array(E.length);P.forEach((i,r)=>I[i]=r);for(let r=0;r<P.length;r++){assert(I[P[r]]===r);assert(P[I[r]]===r);let cur=E[P[r]],prev=r?E[P[r-1]]:null;if(prev)assert(prev.pos<cur.pos||prev.pos===cur.pos&&prev.time<cur.time);assert(cur.read===(prev&&prev.pos===cur.pos?prev.write:0))}
let lo=0,hi=P.length;for(let z=0;z<Math.ceil(Math.log2(P.length+1));z++){if(lo<hi){let mid=Math.floor((lo+hi)/2);if(E[P[mid]].pos<=j)lo=mid+1;else hi=mid}}
assert(lo===hi);return lo&&E[P[lo-1]].pos===j?E[P[lo-1]].write:0}
function allFunctions(m,S){let L=1<<m,mask=(1<<L)-1,init=[0,mask];for(let i=0;i<m;i++){let a=0;for(let j=0;j<L;j++)if((j>>i)&1)a|=1<<j;init.push(a)}let found=new Set();function dfs(v,k){v.forEach(x=>found.add(x));if(!k)return;let next=new Set();for(let a of v){next.add(mask^a);for(let b of v){next.add(a&b);next.add(a|b)}}for(let x of next)if(!v.includes(x))dfs([...v,x],k-1)}dfs(init,S);return found}
let controls=[],pairs=0;for(let m=1;m<=3;m++){let L=1<<m,S=m===1?0:m===2?1:2,F=allFunctions(m,S);let miss=null;for(let v=0;v<(1<<L);v++)if(!F.has(v)){miss=v;break}controls.push({m,S,reachable:F.size,missing:miss});if(miss!==null)assert(!F.has(miss));
for(let v=0;v<(1<<L);v++){let bits=Array.from({length:L},(_,i)=>(v>>i)&1),rules=machine(bits),yes=encode(rules,"",2*L),no=encode(rules,"",2*L-1,yes.length),A=replay(yes,2),B=replay(no,2);assert(A.yes&&!B.yes);assert(yes.length===no.length);for(let i=0;i<L;i++){assert(A.maps[0].get(i)===1+bits[i]);assert(sortedExtract(A.E[0],i)===1+bits[i])}assert(sortedExtract(A.E[0],L)===0);pairs++}}
return {checks,pairs,controls,scope:"finite hardcoded tables; exact deterministic source YES/deadline NO, not conditional hard-table generator or circuit minimization at scale"};
}

console.log(JSON.stringify(run(),null,2));
