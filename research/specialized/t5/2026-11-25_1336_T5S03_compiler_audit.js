// Independent strict-C compilation and radius-one noncoverage audit.
const Z=[0,1,2,3,4],mod=x=>(x+20)%5;
const C=(...x)=>new Set(x).size===3&&Z.some(k=>x.every(v=>[k,mod(k+1),mod(k+2)].includes(v)));
let checks=0;function ok(x){checks++;if(!x)throw Error('check '+checks);}
function compile(circuit){let clauses=Z.map(i=>[i,mod(i+1),mod(i+2)]),n=5,wire=[],heads=[],gates=[];
function addWire(){let v=n++;wire.push(v);for(const j of [2,3,4]){let h=n++;clauses.push([j,v,h]);heads.push([j,v,h]);}return v;}
for(let i=0;i<circuit.inputs;i++)addWire();
for(const [type,p,q] of circuit.gates){let x=addWire();if(type==='N'){clauses.push([2,wire[p],x]);gates.push([type,wire[p],null,x]);}else{let y=n++,z=n++;clauses.push([1,2,y],[0,1,z],[4,wire[p],y],[3,wire[q],z],[x,y,z]);gates.push([type,wire[p],wire[q],x,y,z]);}}
let output=wire.at(-1);let d=clauses.length;clauses.push([0,2,output]);ok(clauses.every(t=>new Set(t).size===3));
function lift(input,s=0,e=1){let a=Array(n).fill(null);for(let i=0;i<5;i++)a[i]=i;
input.forEach((v,i)=>a[wire[i]]=v);
for(const [t,p,q,x,y,z] of gates){if(t==='N')a[x]=1-a[p];else{a[x]=a[p]||a[q];a[y]=a[p]?0:3;a[z]=a[q]?2:4;}}
for(const [j,v,h] of heads)a[h]=Z.find(w=>C(j,a[v],w));
let b=a.map(x=>mod(s+e*x));ok(b.every(x=>Z.includes(x)));let defects=clauses.map((t,i)=>C(...t.map(v=>b[v]))?-1:i).filter(i=>i!==-1);ok(JSON.stringify(defects)===JSON.stringify(a[output]?[ ]:[d]));return b;}
return {n,clauses,d,wire,gates,lift};}
let same=compile({inputs:1,gates:[['O',0,0]]}),near=same.lift([0]),full=same.lift([1]),dist=(a,b)=>Math.min(mod(a-b),mod(b-a));
const [,,,out,y,z]=same.gates[0];ok(near[y]===3&&near[z]===4&&full[y]===0&&full[z]===2);
let frameAudit=[];
for(let s=0;s<5;s++)for(const e of [1,-1]){let fullFrame=same.lift([1],s,e);let anchorOK=Z.every(i=>dist(near[i],fullFrame[i])<=1),yzOK=[y,z].every(i=>dist(near[i],fullFrame[i])<=1);ok(!anchorOK||!yzOK);frameAudit.push({s,e,anchorOK,yzOK});}
// The same anchor proof implies these ten frames are exhaustive: check all permutations.
function* perm(xs){if(!xs.length){yield [];return;}for(let i=0;i<xs.length;i++)for(const p of perm(xs.filter((_,j)=>j!==i)))yield [xs[i],...p];}
let frames=0;for(const a of perm(Z)){let legal=Z.every(i=>C(a[i],a[mod(i+1)],a[mod(i+2)]));if(legal)frames++;ok(legal===([1,-1].some(e=>Z.every(i=>a[i]===mod(a[0]+e*i)))));}ok(frames===10);
// Guarded circuit SAT/UNSAT controls: H=p or not p (SAT); H=p and not p (UNSAT).
let srcs=[{inputs:2,gates:[['N',0],['O',0,2],['N',1],['N',3],['O',4,5],['N',6]]},{inputs:2,gates:[['N',0],['O',0,2],['N',3],['N',1],['N',4],['O',5,6],['N',7]]}];
let controls=[];for(let i=0;i<srcs.length;i++){let f=compile(srcs[i]),sat=0;for(const p of [0,1])for(const g of [0,1]){let b=f.lift([p,g]);let yes=f.clauses.every(t=>C(...t.map(v=>b[v])));ok(yes===(i===0&&g===1));sat+=+yes;}ok(sat===(i===0?2:0));controls.push({n:f.n,m:f.clauses.length,sourceSatisfyingAssignments:sat,near:f.lift([0,0])});}
const results={checks,frames,noncoverage:{n:same.n,clauses:same.clauses,d:same.d,near,full,y,z,frameAudit},controls};
console.log(JSON.stringify(results,null,2));
