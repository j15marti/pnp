function audit(){
let checks=0,searchNodes=0;const ok=(b,m)=>{checks++;if(!b)throw Error(m||"check "+checks)};
const caps=[
 {mode:0,order:[0,1,2,3],colors:[0,0,1,2,0,1,2],T:[[0,5,3],[1,5,6],[4,2,3],[4,2,6],[4,5,6]],rot:{7:[0,3,5],0:[7,1,3],5:[8,7,11],3:[9,7,0,2],8:[1,5,6],1:[0,8,2],6:[11,10,8],9:[4,3,2],4:[10,11,9],2:[3,1,10,9],10:[6,4,2],11:[5,4,6]}},
 {mode:0,order:[0,2,1,3],colors:[0,0,1,2],T:[[0,2,3],[1,2,3]],rot:{7:[0,3,2],0:[7,2,3],2:[0,7,8,1],3:[8,7,0,1],8:[2,3,1],1:[3,2,8]}},
 {mode:1,order:[0,1,2,3],colors:[0,0,1,2,1,2],T:[[0,2,3],[0,4,5],[1,4,5]],rot:{7:[0,3,2],0:[7,8,1,3],2:[1,7,3],3:[2,7,0],8:[0,4,5],4:[8,9],5:[9,8],9:[4,1,5],1:[9,2,0]}},
 {mode:1,order:[0,2,1,3],colors:[0,0,1,2,1,2],T:[[0,4,3],[0,4,5],[1,2,5],[1,4,5]],rot:{7:[0,3,4],0:[7,8,2,3],4:[8,7,10],3:[1,7,0],8:[0,4,5],5:[10,9,8],9:[5,1,2],1:[9,10,3,2],2:[0,9,1],10:[4,1,5]}}
];
function rotation(C){let {rot,T,order}=C,G=new Map();function edge(u,v){if(!G.has(u))G.set(u,new Set());if(!G.has(v))G.set(v,new Set());G.get(u).add(v);G.get(v).add(u)}
 T.forEach((t,i)=>t.forEach(v=>edge(7+i,v)));order.forEach((v,i)=>edge(v,order[(i+1)%4]));
 let E=0;for(let [v,A] of G){ok(rot[v].length===A.size&&rot[v].every(w=>A.has(w)));E+=A.size}
 let used=new Set(),F=[];for(let [u,A] of G)for(let v of A){if(used.has(`${u},${v}`))continue;let face=[],a=u,b=v;do{ok(!used.has(`${a},${b}`));used.add(`${a},${b}`);face.push(a);let r=rot[b],c=r[(r.indexOf(a)+r.length-1)%r.length];a=b;b=c;}while(a!==u||b!==v);F.push(face)}
 ok(G.size-E/2+F.length===2);ok(F.some(f=>f.length===4&&order.every((v,i)=>f[(f.indexOf(order[0])+i)%4]===v)));return F.length
}
function exact(I,required,pins={}){let {T,colors}=I,n=colors.length,used=new Uint8Array(n),need=new Uint8Array(n),rows=Array.from({length:n},()=>[]),sel=[];
 required.forEach(v=>need[v]=1);
 for(let i=0;i<T.length;i++){let t=T[i];ok(t.map(v=>colors[v]).join("")==="012");if(pins[i]===0||t.some(v=>!need[v])){if(pins[i]===1)return null;continue}t.forEach(v=>rows[v].push(i))}
 for(let i in pins)if(pins[i]===1){let j=Number(i),t=T[j];if(t.some(v=>used[v]||!need[v]))return null;t.forEach(v=>used[v]=1);sel.push(j)}
 function rec(){searchNodes++;let best=null;for(let v of required)if(!used[v]){let a=rows[v].filter(j=>T[j].every(w=>!used[w]));if(!a.length)return false;if(best===null||a.length<best.length){best=a;if(best.length===1)break}}if(best===null)return true;for(let j of best){T[j].forEach(v=>used[v]=1);sel.push(j);if(rec())return true;sel.pop();T[j].forEach(v=>used[v]=0)}return false}
 return rec()?sel.slice():null
}
const req=(I,m)=>I.colors.map((_,i)=>i).filter(i=>i>=4||(m>>i&1));
function verify(I,required,S,pins={}){let count=Array(I.colors.length).fill(0),set=new Set(S);ok(set.size===S.length);S.forEach(i=>I.T[i].forEach(v=>count[v]++));let r=new Set(required);ok(count.every((c,i)=>c===+r.has(i)));for(let i in pins)ok(+set.has(+i)===pins[i])}
function support(I,pins={}){let A=[];for(let m=0;m<16;m++){let r=req(I,m),w=exact(I,r,pins);if(w!==null){verify(I,r,w,pins);A.push(m)}}return A}
function cap(R,order){if(R.length===0)return null;if(R.length===1)return {colors:[0,0,1,2],T:[],force:R[0]};let force=R.reduce((a,b)=>a&b),Q=R.map(m=>m^force);
 if(R.length===3){let mode=R.includes(0)?0:1;let C=caps.find(c=>c.mode===mode&&c.order.join()===order.join());return {...C,force:0}}
 ok(R.length===2);let [a,b]=Q;if(a===0||b===0){let w=a|b,t=[0,1,2,3].filter(i=>w>>i&1);ok(t.length===3&&t.map(i=>[0,0,1,2][i]).join("")==="012");return {colors:[0,0,1,2],T:[t],force}}
 ok(a+b===3&&(a===1||a===2)&&(b===1||b===2));return{colors:[0,0,1,2,1,2],T:[[0,4,5],[1,4,5]],force}
}
function capSupport(C){if(C===null)return[];let A=support(C).filter(m=>!(m&C.force));return A.map(m=>m|C.force).sort((a,b)=>a-b)}
function inflate(C,depth){let I={colors:C.colors.slice(),T:[]};function add(t,r){if(!r){I.T.push(t);return}let a=I.colors.length,b=a+1,c=a+2;I.colors.push(0,1,2);add([t[0],b,c],r-1);add([a,t[1],t[2]],r-1);add([a,b,c],r-1)}C.T.forEach(t=>add(t,depth));return I}
function outer(I,m){let J={colors:I.colors.slice(),T:I.T.map(t=>t.slice())};for(let v=0;v<4;v++)if(!(m>>v&1)){let t=[];for(let c=0;c<3;c++){if(c===J.colors[v])t.push(v);else{t.push(J.colors.length);J.colors.push(c)}}J.T.push(t)}return J}
function unit(I,pins){let D=I.T.map(()=>3);for(let i in pins)D[i]=pins[i]?2:1;let rows=I.colors.map((_,v)=>I.T.flatMap((t,i)=>t.includes(v)?[i]:[])),change=true;while(change){change=false;for(let r of rows){let one=r.filter(i=>D[i]===2),live=r.filter(i=>D[i]!==1);if(one.length>1||!live.length)return false;if(one.length){for(let i of live)if(i!==one[0]&&D[i]!==1){D[i]=1;change=true}}else if(live.length===1){D[live[0]]=2;change=true}}}return true}
let signatures=new Set(),subcases=0;for(let a=0;a<=4;a++)for(let b=0;b<=4;b++)for(let c=0;c<=4;c++){let L=[];for(let m=0;m<16;m++)if(a+(m&1)+((m>>1)&1)===b+((m>>2)&1)&&b+((m>>2)&1)===c+((m>>3)&1))L.push(m);ok(L.length<=3);for(let s=0;s<1<<L.length;s++){let R=L.filter((_,i)=>s>>i&1);for(let order of [[0,1,2,3],[0,2,1,3]]){let C=cap(R,order);ok(capSupport(C).join()===R.join(),JSON.stringify({R,order,C}));if(C)ok(C.T.length<=5);subcases++}signatures.add(R.join())}}
let faces=caps.map(rotation),scales=[],closureNo=0;for(let d=0;d<=4;d++){let jobs=0,largest=0;for(let C of caps){let I=inflate(C,d),R=support(I),expect=C.mode===0?[0,13,14]:[1,2,15];ok(R.join()===expect.join());for(let m of R){let w=exact(I,req(I,m));ok(w!==null);let forced=w.find(j=>exact(I,req(I,m),{[j]:0})===null);if(forced===undefined)continue;
 let J=outer(I,m),all=J.colors.map((_,i)=>i),nc=[0,0,0];J.colors.forEach(c=>nc[c]++);ok(nc[0]===nc[1]&&nc[1]===nc[2]);let yes=exact(J,all,{[forced]:1}),no=exact(J,all,{[forced]:0});ok(yes!==null&&no===null);verify(J,all,yes,{[forced]:1});if(!unit(J,{[forced]:0}))closureNo++;
 // acquire exact guarded support by original local solver, then solve independent cap+same exterior, discharge force by requiring cap's mask minus mandatory.
 for(let z of [0,1]){let A=support(I,{[forced]:z}),Q=cap(A,C.order);ok(capSupport(Q).join()===A.join());ok(A.includes(m)===(z===1));}
 jobs++;largest=Math.max(largest,J.T.length)
 }}scales.push({depth:d,pairs:jobs,largestTuples:largest})}
let recur=0;for(let n=20;n<=300;n++)for(let a=10;a<=n/2;a++){let N=BigInt(n),A=BigInt(a),B=N-A+5n;ok(3n*A**4n+B**4n<=N**4n-1n);recur++}
// Independent lower-side finite test: exact-four complement formula and dual-rail totalization.
let masks=0;for(let v=0;v<65536;v++){let bits=Array.from({length:16},(_,i)=>v>>i&1);if(bits.reduce((a,b)=>a+b,0)!==4)continue;masks++;for(let i=0;i<16;i++)ok(+(bits.reduce((a,b,j)=>a+(j===i?0:b),0)>=4)===1-bits[i])}
return {checks,searchNodes,signatures:signatures.size,subcases,faces,scales,closureNo,recurrenceCases:recur,exactFourMasks:masks}
}
console.log(JSON.stringify(audit(),null,2));
