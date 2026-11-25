function run(){
let checks=0, scans=0,words=0;const assert=(b)=>{checks++;if(!b)throw Error("assertion "+checks)};
const par=x=>{let p=0;while(x){p^=1;x&=x-1}return p};
const hit=(p,x)=>p.every(([a,b])=>par(a&x)===b);
const ok=(F,x)=>!F.some(p=>hit(p,x));
function rank(rows){const b=[];for(let x of rows){for(const y of b)x=Math.min(x,x^y);if(x){b.push(x);b.sort((a,b)=>b-a)}}return b.length}
const hull=(xs)=>xs.length?rank(xs.map(x=>x^xs[0])):-1;
function gate(F,n,k){return F.map(p=>p.concat(Array.from({length:k},(_,i)=>[1<<(n+i),1])))}
function scan(F){scans++;for(const p of F)assert(rank(p.map(r=>r[0]))>=2)}
const data={controls:0,sourceSAT:0,sourceUNSAT:0,sourceModelCounts:{},projection:{true:0,false:0}};
function test(name,F,n,nu){
 const sat=[];for(let x=0;x<1<<n;x++){words++;if(ok(F,x))sat.push(x)}
 data.controls++;data[sat.length?"sourceSAT":"sourceUNSAT"]++;data.sourceModelCounts[name]=sat.length;
 const G=gate(F,n,2), B=[[[1<<n,1],[1<<(n+1),1]]], H=gate(F,n,1);
 scan(G);scan(B);scan(H);
 const gs=[],bs=[],hs=[];let diff=0;
 for(let x=0;x<1<<(n+2);x++){words++;const g=ok(G,x),b=ok(B,x);assert(g===(b||ok(F,x&((1<<n)-1))));if(g)gs.push(x);if(b)bs.push(x);if(g!==b)diff++}
 assert(diff===sat.length);assert(hull(gs)===n+2);assert(hull(bs)===n+2);assert(ok(G,0)&&ok(B,0));
 for(let x=0;x<1<<(n+1);x++){words++;if(ok(H,x))hs.push(x)}
 assert(hs.length===(1<<n)+sat.length);assert(hs.every(x=>!(x&(1<<n)))===!sat.length);assert(hull(hs)===n+(sat.length?1:0));
 // Keep the conditional gate fixed: never promote its deductions to the root.
 const proj=new Set(gs.map(x=>(x&((1<<nu)-1))|((x>>n)<<nu)));
 const sourceProj=new Set(sat.map(x=>x&((1<<nu)-1)));
 const full=sourceProj.size===1<<nu;
 assert((proj.size===1<<(nu+2))===full);
 assert(proj.size===3*(1<<nu)+sourceProj.size);
 assert(hull([...proj])===nu+2);
 data.projection[full?"true":"false"]++;
}
const E=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
const nae=(e,s=[0,0,0])=>[[(1<<e[0])|(1<<e[1]),s[0]^s[1]],[(1<<e[0])|(1<<e[2]),s[0]^s[2]]];
const F=E.map(e=>nae(e));test("Fano",F,7,3);
for(let i=0;i<7;i++){for(let j=0;j<3;j++){const s=[0,0,0];s[j]=1;test("sign"+i+"_"+j,F.map((p,k)=>k===i?nae(E[i],s):p),7,3)}
for(let b=0;b<2;b++)test("budget"+i+"_"+b,F.map((p,k)=>k===i?E[i].map(v=>[1<<v,b]):p),7,3)}
assert(data.sourceModelCounts.Fano===0);for(const [k,v] of Object.entries(data.sourceModelCounts)){if(k.startsWith("sign"))assert(v===10);if(k.startsWith("budget"))assert(v===5)}
// forall u exists v (u=v), and a neighbor requiring u=1.
test("QBFtrue",[[[3,1]]],2,1);test("QBFfalse",[[[3,1]],[[1,0]]],2,1);
let state=20261124;const rng=()=>{state=(Math.imul(state,1664525)+1013904223)>>>0;return state};
for(let i=0;i<80;i++){const n=5, m=4+(rng()%24), f=[];for(let j=0;j<m;j++){const vars=[];while(vars.length<3){const v=rng()%n;if(!vars.includes(v))vars.push(v)}f.push(vars.map(v=>[1<<v,rng()>>>31]))}test("random"+i,f,n,2)}
return {...data,checks,scans,words,seed:20261124,notes:"exhaustive finite support reference; rank-only singleton closure at ungated roots (all packet ranks >=2, no guard); no general solver, kernel verification or measured CM"};
}
console.log(JSON.stringify(run(),null,2));
