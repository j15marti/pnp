"use strict";
function audit059(){
"use strict";
const REV="tmr4-long-edge-spill059.v2",SEED=20261115;
let assertions=0,assignments=0,stepChecks=0,rankChecks=0,totalNodes=0,totalArcs=0;
function check(v,msg){assertions++;if(!v)throw Error("FAIL "+msg);}
function canonical(v){if(Array.isArray(v))return "["+v.map(canonical).join(",")+"]";if(v&&typeof v==="object")return "{"+Object.keys(v).sort().map(k=>JSON.stringify(k)+":"+canonical(v[k])).join(",")+"}";return JSON.stringify(v);}
function ref(v){if(typeof v!=="string"||!/^(x|g)(0|[1-9]\d*)$/.test(v))throw Error("bad reference");let j=Number(v.slice(1));if(!Number.isSafeInteger(j))throw Error("large index");return [v[0],j];}
function parse(s){
let o=JSON.parse(s);if(canonical(o)!==s)throw Error("not canonical");
if(!o||Array.isArray(o)||Object.keys(o).sort().join(",")!=="gates,n,out"||!Number.isSafeInteger(o.n)||o.n<1||!Array.isArray(o.gates)||!o.gates.length)throw Error("shape");
let g=o.gates.length,n=o.n;if(n>2*g)throw Error("invalid huge declared arity");
let G=new Map();
for(let rec of o.gates){
if(!rec||Array.isArray(rec)||Object.keys(rec).sort().join(",")!=="a,b,id,op"||!Number.isInteger(rec.op)||rec.op<0||rec.op>15)throw Error("gate record");
let [t,j]=ref(rec.id);if(t!=="g"||j>=g||G.has(rec.id))throw Error("gate ids");G.set(rec.id,rec);
}
if(G.size!==g||!G.has(o.out))throw Error("output");
let usedInputs=new Set(),fanout=new Map();
for(let rec of G.values())for(let v of [rec.a,rec.b]){let [t,j]=ref(v);if(t==="x"){if(j>=n)throw Error("x index");usedInputs.add(v);}else if(!G.has(v))throw Error("g ref");fanout.set(v,(fanout.get(v)||0)+1);}
if(usedInputs.size!==n)throw Error("unused input");
let gray=new Set(),depth=new Map(),reach=new Set();
function visit(v){
if(v[0]==="x")return 0;
if(gray.has(v))throw Error("cycle");if(depth.has(v))return depth.get(v);
gray.add(v);reach.add(v);let z=G.get(v);let d=1+Math.max(visit(z.a),visit(z.b));gray.delete(v);depth.set(v,d);return d;
}
let D=visit(o.out);if(reach.size!==g)throw Error("dead gate");
let intro=new Map();for(let rec of G.values())for(let v of [rec.a,rec.b])if(v[0]==="x")intro.set(v,Math.min(intro.get(v)??Infinity,depth.get(rec.id)));
let layers=new Map();
function layer(d){if(!layers.has(d))layers.set(d,{inputs:[],gates:[]});return layers.get(d);}
for(let [x,d] of intro)layer(d).inputs.push(x);
for(let [v,d] of depth)layer(d).gates.push(v);
let events=[],birth=new Map(),birthLevel=new Map();
let k=0;
for(let d=1;d<=D;d++){
let l=layer(d);l.inputs.sort((a,b)=>Number(a.slice(1))-Number(b.slice(1)));l.gates.sort((a,b)=>Number(a.slice(1))-Number(b.slice(1)));
k=Math.max(k,l.inputs.length,l.gates.length);
for(let v of l.inputs){birth.set(v,events.length);birthLevel.set(v,d);events.push({type:"input",v,level:d});}
for(let v of l.gates){birth.set(v,events.length);birthLevel.set(v,d);events.push({type:"gate",v,level:d});}
}
check(events.length===n+g,"events every real identity exactly once");
let last=new Map([...birth.keys()].map(v=>[v,birth.get(v)]));
for(let i=0;i<events.length;i++){let e=events[i];if(e.type==="gate")for(let operand of [G.get(e.v).a,G.get(e.v).b]){check(birth.get(operand)<i,"topological original predecessor");last.set(operand,Math.max(last.get(operand),i));}}
last.set(o.out,events.length);
let lastLevel=new Map([...last.keys()].map(v=>[v,last.get(v)===events.length?D+1:events[last.get(v)].level]));
let w=0;
for(let i=0;i<events.length;i++){let alive=[...birth.keys()].filter(v=>birth.get(v)<=i&&last.get(v)>i);w=Math.max(w,alive.length);}
let c=0,cOld=0;
for(let d=1;d<=D;d++){
let old=[...birth.keys()].filter(v=>birthLevel.get(v)<=d-1&&lastLevel.get(v)>=d&&!(v[0]==="g"&&birthLevel.get(v)===d-1));
let omitted=[...birth.keys()].filter(v=>birthLevel.get(v)<=d-2&&lastLevel.get(v)>=d);
c=Math.max(c,old.length);cOld=Math.max(cOld,omitted.length);
}
check(c>=cOld,"correct spill includes previous-layer retained inputs");
check(w<=3*k+c,"spill frontier theorem");
return {o,G,depth,events,birth,last,k,c,cOld,w,D,fanout,order:events.filter(e=>e.type==="input").map(e=>e.v)};
}
function gate(op,a,b){return (op>>(a*2+b))&1;}
function direct(P,bits){
let memo=new Map(bits.map((bit,i)=>["x"+i,bit]));
function value(v){if(memo.has(v))return memo.get(v);let z=P.G.get(v);let b=gate(z.op,value(z.a),value(z.b));memo.set(v,b);return b;}
let out=value(P.o.out);
return {out,memo};
}
function compile(P){
let {events,G,birth,last}=P;
let inp=events.map((e,i)=>e.type==="input"?i:-1).filter(i=>i>=0),all=events.length,states=new Map([["",{reg:{},count:1n}]]),arcs=[],sizes=[1];
function key(reg){return Object.keys(reg).sort().map(x=>x+"="+reg[x]).join("|");}
for(let j=0;j<inp.length;j++){
let first=inp[j],end=j+1<inp.length?inp[j+1]:all;
let next=new Map(),edges=new Map();
for(let [oldKey,state] of states){
let paths=[];
for(let bit=0;bit<=1;bit++){
let reg={...state.reg};
for(let t=first;t<end;t++){
let e=events[t];
if(e.type==="input")reg[e.v]=bit;
else {let z=G.get(e.v);check(Object.hasOwn(reg,z.a)&&Object.hasOwn(reg,z.b),"real gate reads retained operands");reg[e.v]=gate(z.op,reg[z.a],reg[z.b]);stepChecks++;}
for(let v of Object.keys(reg))if(last.get(v)<=t)delete reg[v];
}
let newKey=key(reg);
if(!next.has(newKey))next.set(newKey,{reg,count:0n});
next.get(newKey).count+=state.count;
paths.push(newKey);totalArcs++;
}
edges.set(oldKey,paths);
}
arcs.push(edges);states=next;sizes.push(states.size);
check(BigInt(states.size)<=2n**BigInt(P.w),"stage count bound");
}
let yes=0n;for(let st of states.values()){check(Object.hasOwn(st.reg,P.o.out),"output retained");if(st.reg[P.o.out]===1)yes+=st.count;}
totalNodes+=sizes.slice(0,-1).reduce((a,b)=>a+b,0);
return {yes,arcs,sizes,terminal:states};
}
function rank(a,p){
a=a.map(row=>row.map(v=>v%p));let h=a.length,w=a[0].length,r=0;
function inv(x){for(let z=1;z<p;z++)if(x*z%p===1)return z;throw Error("no inverse");}
for(let j=0;j<w&&r<h;j++){
let z=r;while(z<h&&a[z][j]===0)z++;if(z===h)continue;
[a[z],a[r]]=[a[r],a[z]];
let q=inv(a[r][j]);for(let c=j;c<w;c++)a[r][c]=a[r][c]*q%p;
for(let i=0;i<h;i++)if(i!==r&&a[i][j]!==0){let mult=a[i][j];for(let t=j;t<w;t++)a[i][t]=(a[i][t]-mult*a[r][t]%p+p)%p;}
r++;
}return r;
}
let random=SEED>>>0;function rnd(){random^=random<<13;random^=random>>>17;random^=random<<5;return random>>>0;}
let samples=[],allSources=[],correctionCases=0,seenSpill=0,seenShared=0,seenInputSpan=0,seenGateSpan=0;
function run(o,label){
let source=canonical(o),P=parse(source),C=compile(P);
let n=P.o.n,brute=0n;
for(let mask=0;mask<(1<<n);mask++){
let bits=Array.from({length:n},(_,i)=>(mask>>i)&1);
let A=direct(P,bits);brute+=BigInt(A.out);
let reg={};
for(let t=0;t<P.events.length;t++){
let e=P.events[t];
if(e.type==="input"){reg[e.v]=bits[Number(e.v.slice(1))];}
else {let z=P.G.get(e.v);check(reg[z.a]!==undefined&&reg[z.b]!==undefined,"gate replay operands");reg[e.v]=gate(z.op,reg[z.a],reg[z.b]);check(reg[e.v]===A.memo.get(e.v),"all original gate step values");stepChecks++;}
for(let v of Object.keys(reg))if(P.last.get(v)<=t)delete reg[v];
}
check(reg[o.out]===A.out,"terminal bit");
let st="";for(let j=0;j<n;j++){let bit=bits[Number(P.order[j].slice(1))];st=C.arcs[j].get(st)[bit];check(st!==undefined,"labelled source path");}
let final=C.terminal.get(st);check(final.reg[o.out]===A.out,"compiled assignment path same output");
assignments++;
}
check(brute===C.yes,"exact input assignment count (including edge multiplicity)");
for(let j=0;j<=n;j++){
let matrix=[],rows=1<<j,cols=1<<(n-j);
for(let a=0;a<rows;a++){let row=[];for(let b=0;b<cols;b++){
let bits=Array(n).fill(0);for(let v=0;v<j;v++)bits[Number(P.order[v].slice(1))]=(a>>v)&1;for(let v=j;v<n;v++)bits[Number(P.order[v].slice(1))]=(b>>(v-j))&1;
row.push(direct(P,bits).out);
}matrix.push(row);}
for(let f of [2,101]){let r=rank(matrix,f);rankChecks++;check(r<=C.sizes[j],"cofactor cut rank bound");}
}
if(P.c>0)seenSpill++;if(P.c>P.cOld)correctionCases++;
if([...P.fanout.values()].some(z=>z>=2))seenShared++;
for(let v of P.order){let uses=[...P.G.values()].filter(g=>g.a===v||g.b===v).map(g=>P.depth.get(g.id));if(Math.max(...uses)>Math.min(...uses))seenInputSpan++;}
for(let [v,d] of P.depth){let uses=[...P.G.values()].filter(g=>g.a===v||g.b===v).map(g=>P.depth.get(g.id));if(uses.some(z=>z>d+1))seenGateSpan++;}
samples.push({name:label,n,P_g:o.gates.length,k:P.k,c:P.c,cOld:P.cOld,w:P.w,states:C.sizes,yes:String(C.yes),bits:source.length*8});
allSources.push(source);
}
for(let n=2;n<=6;n++)for(let rep=0;rep<10;rep++){
let g=n+3+rep%3,gs=[{id:"g0",a:"x0",b:"x1",op:rnd()%16}];
for(let i=1;i<g;i++){
let b=i<n-1?"x"+(i+1):(i>=3&&i%3===0?"g"+(i-3):(i%2===1?"x0":"g0"));
gs.push({id:"g"+i,a:"g"+(i-1),b,op:rnd()%16});
}
if(rep%2)gs.reverse();
run({n,gates:gs,out:"g"+(g-1)},"chain"+n+"_"+rep);
}
run({n:5,gates:[{id:"g6",a:"g1",b:"g5",op:6},{id:"g0",a:"x0",b:"x1",op:8},{id:"g3",a:"g0",b:"x4",op:14},{id:"g5",a:"g4",b:"x0",op:7},{id:"g1",a:"x2",b:"x3",op:6},{id:"g4",a:"g2",b:"g3",op:8},{id:"g2",a:"g0",b:"g1",op:14}],out:"g6"},"reconvergent_long");
run({n:2,gates:[{id:"g0",a:"x0",b:"x1",op:8},{id:"g1",a:"g0",b:"x0",op:6}],out:"g1"},"adjacent_input_reuse");
let disj={n:6,gates:[{id:"g0",a:"x0",b:"x3",op:7},{id:"g1",a:"x1",b:"x4",op:7},{id:"g2",a:"x2",b:"x5",op:7},{id:"g3",a:"g0",b:"g1",op:8},{id:"g4",a:"g3",b:"g2",op:8}],out:"g4"};
run(disj,"DISJ3");
let rankDisj=[];let Pd=parse(canonical(disj));
for(let a=0;a<8;a++){let row=[];for(let b=0;b<8;b++)row.push(direct(Pd,[(a>>0)&1,(a>>1)&1,(a>>2)&1,(b>>0)&1,(b>>1)&1,(b>>2)&1]).out);rankDisj.push(row);}
check(rank(rankDisj,2)===8&&rank(rankDisj,101)===8,"DISJ3 rank 8 with compact circuit");
let reject=[
{n:1000000000000,gates:[{id:"g0",a:"x0",b:"x0",op:8}],out:"g0"},
{n:1,gates:[{id:"g0",a:"g1",b:"x0",op:8},{id:"g1",a:"g0",b:"x0",op:6}],out:"g1"},
{n:1,gates:[{id:"g0",a:"x0",b:"x0",op:8},{id:"g1",a:"x0",b:"x0",op:8}],out:"g0"},
{n:2,gates:[{id:"g0",a:"x0",b:"x0",op:8}],out:"g0"},
{n:1,gates:[{id:"g0",a:"x0",b:"x0",op:18}],out:"g0"},
{n:1,gates:[{id:"g0",a:"x0",b:"g9",op:8}],out:"g0"}
];for(let z of reject){let threw=false;try{parse(canonical(z));}catch(e){threw=true;}check(threw,"malformed source rejected");}
let dup='{"gates":[{"a":"x0","b":"x0","id":"g0","op":8}],"n":1,"n":2,"out":"g0"}';let threw=false;try{parse(dup);}catch(e){threw=true;}check(threw,"duplicate key rejected");
check(correctionCases>=1&&seenSpill>0&&seenGateSpan>0&&seenInputSpan>0&&seenShared>0,"all new long-edge source controls exercised");
return {revision:REV,seed:SEED,valid:samples.length,rejected:7,assertions,assignments,stepChecks,rankChecks,totalNodes,totalArcs,correctionCases,seenSpill,seenShared,seenInputSpan,seenGateSpan,disjGroupedRank:8,failures:0,cases:samples,canonicalSources:allSources};
}
if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(audit059(),null,2));
