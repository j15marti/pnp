function main(){
let seed=20812026, assertions=0, gauss=0, localWords=0, globalWords=0, pins=0;
function rand(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}
function ok(x){assertions++;if(!x)throw Error("assertion "+assertions)}
function basis(rows){gauss++;let b=[];for(let v of rows){for(let i=0;i<b.length;i++)v=Math.min(v,v^b[i]);if(v){b.push(v);b.sort((a,b)=>b-a)}}return b}
function reduce(x,b){for(const v of b)x=Math.min(x,x^v);return x}
function addEq(q,row,b){return basis([...q,(row<<1)|b])}
function parity(x){let t=0;while(x){t^=1;x&=x-1}return t}
function good(e,w,relax){const bits=e.map(v=>(w>>>v)&1);return relax?bits.some(Boolean):!(bits.every(x=>x===0)||bits.every(x=>x===1))}
function row(e){return [(1<<e[0])^(1<<e[1]),(1<<e[0])^(1<<e[2])]}
function closure(n,E,relax,q){q=basis(q);while(true){if(reduce(1,q)===0)return null;let changed=false;for(let i=0;i<E.length;i++){let e=E[i],S=[];for(let w=0;w<8;w++){localWords++;let z=0,Q=q;for(let j=0;j<3;j++){let bit=(w>>j)&1;z|=bit<<e[j];Q=addEq(Q,1<<e[j],bit)}if(reduce(1,Q)!==0&&good(e,z,i===relax))S.push(w)}if(!S.length)return null;
for(let a=1;a<8;a++){let b=parity(a&S[0]);if(S.every(w=>parity(a&w)===b)){let v=0;for(let j=0;j<3;j++)if(a>>j&1)v^=1<<e[j];if(reduce((v<<1)|b,q)!==0){q=addEq(q,v,b);pins++;changed=true;break}}}
if(changed)break;}if(!changed)return q;}}
function degree(n,E){return Math.max(...Array.from({length:n},(_,i)=>E.filter(e=>e.includes(i)).length))}
function graphStars(n,edges){return Array.from({length:n},(_,i)=>edges.map((e,j)=>e.includes(i)?j:-1).filter(j=>j>=0))}
function verifyLocal(E,G){let vs=[...new Set(G.flatMap(i=>E[i]))],k=vs.length,allowed=[];for(let x=0;x<(1<<k);x++){let w=0;for(let j=0;j<k;j++)if(x>>j&1)w|=1<<vs[j];allowed[x]=G.every(i=>good(E[i],w,false))}
let period=0;for(let d=0;d<(1<<k);d++){let is=allowed.every((v,x)=>v===allowed[x^d]);let w=0;for(let j=0;j<k;j++)if(d>>j&1)w|=1<<vs[j];let expect=G.every(i=>row(E[i]).every(r=>parity(r&w)===0));ok(is===expect);if(is)period++}ok(period===2**(k-2*G.length))}
function run(name,n,E,b,g,relax,guardTrials){let D=degree(n,E),count=0;for(let w=0;w<(1<<n);w++){globalWords++;if(E.every((e,i)=>good(e,w,i===relax)))count++}let live=E.map((_,i)=>i).filter(i=>i!==relax),out={name,n,m:E.length,b,g,D,models:count,guards:0,closedContradiction:0,obstructions:0,other:0,rootObstruction:false,largestCleanGroup:0};
for(let i=0;i<live.length;i++){verifyLocal(E,[live[i]]);if(b>=2)for(let j=i+1;j<live.length;j++)verifyLocal(E,[live[i],live[j]])}
for(let trial=0;trial<guardTrials;trial++){let q=[];if(trial){let h=(trial%4)+1;for(let j=0;j<h;j++)q=addEq(q,1+rand((1<<n)-1),rand(2))}
q=closure(n,E,relax,q);out.guards++;if(q===null){out.closedContradiction++;continue}let H=basis(q.map(v=>v>>1)),h=H.length,P=H.reduce((p,v)=>p|(1<<Math.floor(Math.log2(v))),0);ok(basis(H.map(v=>v&P)).length===h);let L=live.slice();for(let i=L.length-1;i>0;i--){let j=rand(i+1);[L[i],L[j]]=[L[j],L[i]]}let groups=[];while(L.length)groups.push(L.splice(0,trial===0?b:1+rand(b)));let clean=groups.filter(G=>G.every(i=>E[i].every(v=>!(P>>v&1))));let sizes=clean.reduce((s,G)=>s+G.length,0);ok(sizes>=live.length-b*D*h);
let spaces=clean.map(G=>basis(G.flatMap(i=>row(E[i])).map(v=>reduce(v,H))));for(let i=0;i<spaces.length;i++){ok(spaces[i].length===2*clean[i].length);out.largestCleanGroup=Math.max(out.largestCleanGroup,clean[i].length);for(let j=0;j<i;j++)ok(basis([...spaces[i],...spaces[j]]).length===spaces[i].length+spaces[j].length)}
let sum=spaces.reduce((s,v)=>s+v.length,0),rank=basis(spaces.flat()).length;ok(rank<=n-h);if(2*(live.length-b*D*h)>n-h)ok(sum>rank);if(sum>rank){out.obstructions++;if(!trial)out.rootObstruction=true;}else out.other++}
ok(out.rootObstruction);return out}
let F=[];for(let a=1;a<=7;a++)for(let b=a+1;b<=7;b++){let c=a^b;if(c>b)F.push([a-1,b-1,c-1])}
let pe=[];for(let i=0;i<5;i++){pe.push([i,(i+1)%5],[i,5+i],[5+i,5+(i+2)%5])}
let P=graphStars(10,pe);let he=[];for(let i=0;i<7;i++)for(let j of [0,1,3])he.push([i,7+(i+j)%7]);let H=graphStars(14,he);
let cases=[run("Fano root",7,F,1,3,-1,201)];for(let j=0;j<7;j++)cases.push(run("Fano one-sided "+j,7,F,1,3,j,81));cases.push(run("Petersen star SAT",15,P,2,5,-1,201),run("Heawood star SAT",21,H,2,6,-1,81));ok(cases[0].models===0);ok(cases.slice(1,8).every(c=>c.models===5));ok(cases.slice(8).every(c=>c.models>0));return {seed:20812026,cases,assertions,gauss,localWords,globalWords,pins}}
console.log(JSON.stringify(main(),null,2));
