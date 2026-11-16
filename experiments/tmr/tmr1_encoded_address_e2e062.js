const audit=function audit(){
const seed=20261115;let state=seed>>>0,checks=0,cases=0,totalAddresses=0,totalFormalBits=0;
function rng(){state^=state<<13;state^=state>>>17;state^=state<<5;return state>>>0}
function rand(n){return rng()%n}
function assert(x,msg){checks++;if(!x)throw Error("ASSERT "+msg)}
const ops=["AND","OR","XOR","NOT","ZERO","ONE"];
function apply(op,a,b){switch(op){case"AND":return a&b;case"OR":return a|b;case"XOR":return a^b;case"NOT":return 1-a;case"ZERO":return 0;case"ONE":return 1;default:throw Error("op")}}
function bits(n,w){return Array.from({length:w},(_,i)=>(n>>>i)&1)}
function val(b){return b.reduce((v,x,i)=>v+(x<<i),0)}
function calc(C,x){const vv=x.slice();for(const g of C.gates)vv.push(apply(g.op,vv[g.a],vv[g.b]));return{out:vv[C.out],values:vv}}
function append(C,op,a,b=a){const id=C.q+C.gates.length;C.gates.push({op,a,b});return id}
function encodeCircuit(C){const G=C.gates.length,V=C.q+G,w=Math.floor(Math.log2(Math.max(2,V)))+1;let out="1".repeat(C.q)+"0"+"1".repeat(G)+"0";
for(const g of C.gates){out+=bits(g.a,w).join("")+bits(g.b,w).join("");for(let a=0;a<2;a++)for(let b=0;b<2;b++)out+=apply(g.op,a,b)}
out+=bits(C.out,w).join("");return out}
function decodeCircuit(src){let k=0;function unary(){let q=0;while(src[k]==="1"){k++;q++}if(src[k++]!=="0")throw Error("delimiter");return q}
const q=unary(),G=unary(),V=q+G,w=Math.floor(Math.log2(Math.max(2,V)))+1,C={q,gates:[],out:null};
function read(n){if(k+n>src.length)throw Error("truncated");const a=src.slice(k,k+n);k+=n;return a}
for(let j=0;j<G;j++){const a=val(read(w).split("").map(Number)),b=val(read(w).split("").map(Number)),tbl=read(4);assert(a<q+j&&b<q+j,"valid predecessors");const op=ops.find(t=>{let tr="";for(let u=0;u<2;u++)for(let v=0;v<2;v++)tr+=apply(t,u,v);return tr===tbl});if(!op)throw Error("unknown table");C.gates.push({op,a,b})}C.out=val(read(w).split("").map(Number));assert(k===src.length&&C.out<V,"source fully parsed");return C}
function randomAssignmentCircuit(v,g){const C={q:v,gates:[],out:0};for(let j=0;j<g;j++){const a=rand(v+j),b=rand(v+j);append(C,ops[rand(ops.length)],a,b)}C.out=rand(v+g);return C}
function makeDecoder(ell,v,clauses){
const C={q:ell,gates:[],out:0};const neg=Array.from({length:ell},(_,i)=>append(C,"NOT",i));
const tt=Array.from({length:1<<ell},(_,z)=>{const paths=Array.from({length:ell},(_,i)=>((z>>i)&1)?i:neg[i]);return paths.reduce((a,b)=>append(C,"AND",a,b))});
const zero=append(C,"ZERO",0);append(C,"ONE",0);
function rom(vals){let idx=zero;for(let z=0;z<vals.length;z++)if(vals[z])idx=append(C,"OR",idx,tt[z]);return idx}
const outputs=[];for(let s=0;s<3;s++){const p=rom(clauses.map(c=>c[s]!==null?1:0));
const id=Array.from({length:v},(_,j)=>rom(clauses.map(c=>c[s]!==null?((c[s].i>>j)&1):0)));
const sign=rom(clauses.map(c=>c[s]?.sign||0));outputs.push({p,id,sign})}
return {C,outputs}}
function buildB(ell,v,A,cls){
const D=makeDecoder(ell,v,cls),C=D.C;let vs=[];
for(const slot of D.outputs){let refs=slot.id.slice();for(const g of A.gates)refs.push(append(C,g.op,refs[g.a],refs[g.b]));const aVal=refs[A.out];const wrong=append(C,"XOR",aVal,slot.sign),missing=append(C,"NOT",slot.p);vs.push(append(C,"OR",wrong,missing))}
C.out=append(C,"AND",append(C,"AND",vs[0],vs[1]),vs[2]);return C}
function sourceCNF(C){const n=C.q+C.gates.length,cl=[];for(let j=0;j<C.gates.length;j++){const g=C.gates[j],z=C.q+j;for(let u=0;u<2;u++)for(let v=0;v<2;v++)cl.push([{i:g.a,sign:1-u},{i:g.b,sign:1-v},{i:z,sign:apply(g.op,u,v)}])}cl.push([{i:C.out,sign:1}]);
const uses=new Set(cl.flatMap(c=>c.map(l=>l.i)));for(let i=0;i<C.q;i++)if(!uses.has(i))cl.push([{i,sign:1},{i,sign:0},{i,sign:1}]);
const seen=new Set();const out=cl.filter(c=>{const key=JSON.stringify(c);if(seen.has(key))return false;seen.add(key);return true});return {n,clauses:out}}
function totalize(H){const n=H.n,cl=H.clauses.slice(),used=new Set(cl.flatMap(c=>c.map(l=>l.i)));let u=0;for(let i=0;i<n;i++)if(!used.has(i)){cl.push([{i,sign:1},{i,sign:0}]);u++}
const m0=H.clauses.length,d=Math.max(1,4-n,Math.ceil((m0+u+1-4*n)/3));for(let i=0;i<d;i++)cl.push([{i:n+i,sign:0}]);cl.push([{i:n,sign:1},{i:n,sign:0}]);return {n:n+d,clauses:cl,d,sourceN:n}}
function holds(F,vals){return F.clauses.every(c=>c.some(l=>vals[l.i]===l.sign))}
function formal(F){const w=Math.floor(Math.log2(2*F.n))+1;let raw="1110"+"1".repeat(F.n)+"0";for(const c of F.clauses){for(let s=0;s<3;s++){let code=s<c.length?2*c[s].i+1+c[s].sign:0;raw+=bits(code,w).join("")}}return {raw,w}}
function decodeFormal(F,raw){let k=0;assert(raw.startsWith("1110"+"1".repeat(F.n)+"0"),"unary formal header");k=F.n+5;const cls=[];for(let z=0;z<F.clauses.length;z++){let cl=[];for(let s=0;s<3;s++){const code=val(raw.slice(k,k+Math.floor(Math.log2(2*F.n))+1).split("").map(Number));k+=Math.floor(Math.log2(2*F.n))+1;if(code>0)cl.push({i:Math.floor((code-1)/2),sign:(code-1)%2})}cls.push(cl)}assert(k===raw.length,"formal full size");return cls}
for(let trial=0;trial<84;trial++){
const ell=1+rand(4),v=1+rand(3),U=1<<v;const A=randomAssignmentCircuit(v,rand(9)),clauses=Array.from({length:1<<ell},()=>Array.from({length:3},()=>rand(5)===0?null:{i:rand(U),sign:rand(2)}));
if(trial%7===0)for(let z=0;z<clauses.length;z++)clauses[z]=[null,null,null];
if(trial%7===1)for(let z=0;z<clauses.length;z++)clauses[z]=[{i:0,sign:1},{i:0,sign:0},null];
if(trial%7===2)for(let z=0;z<clauses.length;z++)clauses[z]=[{i:0,sign:1},null,null];
const C=buildB(ell,v,A,clauses),source=encodeCircuit(C),B=decodeCircuit(source);assert(source.length>=B.gates.length,"genuine encoded B");const H=sourceCNF(B),F=totalize(H),enc=formal(F);
assert(F.n>=4&&F.clauses.length>=2&&F.clauses.length<=4*F.n,"normalizer promises");
assert(JSON.stringify(decodeFormal(F,enc.raw))===JSON.stringify(F.clauses),"low-first formal roundtrip");
let bCount=0,declCount=0;
for(let z=0;z<(1<<ell);z++){const address=bits(z,ell),assignment=Array.from({length:U},(_,j)=>calc(A,bits(j,v)).out);const direct=clauses[z].every(t=>t===null||assignment[t.i]!==t.sign)?1:0;
const run=calc(B,address);assert(run.out===direct,"real gate-DAG violation equals direct literal semantics");const augmented=run.values.concat(Array(F.d).fill(0));assert(holds(F,augmented)===(direct===1),"unique extension CNF matches");
for(let j=0;j<B.gates.length&&j<4;j++){const fake=augmented.slice();fake[B.q+j]^=1;assert(!holds(F,fake),"functional gate constraints reject wrong internal gate")}
bCount+=run.out;declCount+=direct;totalAddresses++}
assert(bCount===declCount,"exact addressed violation count");
if(trial%7===0)assert(bCount===(1<<ell),"empty clause counts every address");
if(trial%7===1)assert(bCount===0,"tautology counts no addresses");
totalFormalBits+=enc.raw.length;cases++}
return {revision:"tmr1-c1f-address-verifier062.v2",seed,case_count:cases,address_evaluations:totalAddresses,formal_input_bits:totalFormalBits,assertions:checks,unexpected_failures:0,controls:"empty,tautology,repeated,missing slots,unused address,random shared-gate A; exact source and formal roundtrip",status:"COMPUTATIONAL only"};
};
const result=audit();
console.log(JSON.stringify(result,null,2));
