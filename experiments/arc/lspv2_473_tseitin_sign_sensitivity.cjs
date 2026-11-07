const summary = (function run(){
let assertions=0,mutantChecks=0,deletedChecks=0;
function check(v,m){assertions++;if(!v)throw new Error("ASSERT: "+m);}
function xor3(x){return ((x&1)^((x>>1)&1)^((x>>2)&1));}
function mk(n,edges){
 const inc=Array.from({length:n},()=>[]);
 const pairs=new Set();
 edges.forEach(([u,v],i)=>{check(u!==v,"loop");let key=[u,v].sort((a,b)=>a-b).join(":");check(!pairs.has(key),"parallel "+key);pairs.add(key);inc[u].push(i);inc[v].push(i);});
 inc.forEach((a,i)=>check(a.length===3,"degree "+i));return {n,edges,inc};
}
const E4=[];for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)E4.push([i,j]);
const k4=mk(4,E4);
const cubeEdges=[];for(let v=0;v<8;v++)for(let bit=0;bit<3;bit++)if(!(v&(1<<bit)))cubeEdges.push([v,v^(1<<bit)]);
const cube=mk(8,cubeEdges);
const pEdges=[];for(let i=0;i<5;i++){pEdges.push([i,(i+1)%5]);pEdges.push([i,i+5]);pEdges.push([i+5,((i+2)%5)+5]);}
const petersen=mk(10,pEdges);
const bEdges=E4.filter(([u,v])=>!(u===0&&v===1)).concat([[0,4],[1,4]],E4.filter(([u,v])=>!(u===0&&v===1)).map(([u,v])=>[u+5,v+5]),[[5,9],[6,9],[4,9]]);
const bridge=mk(10,bEdges);
function formula(g,charges){let cs=[];for(let v=0;v<g.n;v++)for(let a=0;a<8;a++)if(xor3(a)!==charges[v])cs.push({v,a,lits:g.inc[v].map((e,j)=>((a>>j)&1)?-(e+1):(e+1))});check(cs.length===4*g.n,"formula length");return cs;}
function sat(cs,bits,flipC=-1,flipJ=-1,remove=-1){for(let i=0;i<cs.length;i++){if(i===remove)continue;let f=false;for(let j=0;j<3;j++){let lit=cs[i].lits[j];if(i===flipC&&j===flipJ)lit=-lit;let value=bits[Math.abs(lit)-1];if((lit>0&&value===1)||(lit<0&&value===0)){f=true;break;}}if(!f)return false;}return true;}
function graphConnectedExcept(g,v){let start=0===v?1:0,queue=[start],seen=new Set([start]);for(let h=0;h<queue.length;h++){let u=queue[h];for(let e of g.inc[u]){let [s,t]=g.edges[e],w=s===u?t:s;if(w!==v&&!seen.has(w)){seen.add(w);queue.push(w)}}}return seen.size===g.n-1;}
function witness(g,charges,v,a){let bits=Array(g.edges.length).fill(null),par=Array(g.n).fill(-1);g.inc[v].forEach((eid,j)=>bits[eid]=(a>>j)&1);
let root=(v===0?1:0),queue=[root],seen=new Set([root]);for(let h=0;h<queue.length;h++){let u=queue[h];for(let e of g.inc[u]){let [s,t]=g.edges[e],w=(s===u?t:s);if(w===v||seen.has(w))continue;seen.add(w);par[w]=e;queue.push(w)}}
if(seen.size!==g.n-1)return null;
const tree=new Set(par.filter(e=>e>=0));for(let i=0;i<bits.length;i++)if(bits[i]===null&&!tree.has(i))bits[i]=0;
for(let i=queue.length-1;i>0;i--){let u=queue[i],p=par[u],z=charges[u];for(let e of g.inc[u])if(e!==p){check(bits[e]!==null,"unresolved");z^=bits[e]}bits[p]=z;}
for(let u of queue){let z=0;for(let e of g.inc[u])z^=bits[e];check(z===charges[u],"wrong parity "+u);}
return bits;}
const summaries=[];
for(let [name,g] of [["K4",k4],["cube",cube],["Petersen",petersen]]){
 for(let [mode,charges] of [["single",Array.from({length:g.n},(_,v)=>+(v===0))],["triple",Array.from({length:g.n},(_,v)=>+(v<3))]]){
 check(!((charges.reduce((a,b)=>a^b,0))===0),"charge parity");check(Array.from({length:g.n},(_,v)=>graphConnectedExcept(g,v)).every(Boolean),"not 2connected");
 const cs=formula(g,charges);let sensitive=0;
 for(let i=0;i<cs.length;i++){let {v,a}=cs[i];const w=witness(g,charges,v,a);check(w!==null,"witness missing");
 check(!sat(cs,w),"odd source SAT");check(sat(cs,w,-1,-1,i),"deleting one clause failed");deletedChecks++;
 for(let j=0;j<3;j++){check(sat(cs,w,i,j),"polarity flip not SAT");mutantChecks++;sensitive++;}
 }
 // An explicit one-bit polarity edit preserves strict-3CNF record structure and all other sign positions.
 check(sensitive===12*g.n,"sign count");
 // exhaustive original odd UNSAT for the three finite graph controls.
 let allSat=false;
 for(let x=0;x<(1<<g.edges.length);x++){let vec=g.edges.map((_,e)=>(x>>e)&1);if(sat(cs,vec)){allSat=true;break;}}
 check(!allSat,"odd source has assignment");
 summaries.push({graph:name,mode,vertices:g.n,edges:g.edges.length,clauses:cs.length,individuallyEssentialClauses:cs.length,individuallySensitiveSignBits:sensitive});
 }
}
const bc=Array(bridge.n).fill(0);bc[4]=1;let bcForm=formula(bridge,bc);let brYes=0,brNo=0;
check(!graphConnectedExcept(bridge,4),"bridge unexpectedly 2connected");
for(let i=0;i<bcForm.length;i++)if(bcForm[i].v===4)for(let j=0;j<3;j++){
 let found=false;for(let x=0;x<(1<<bridge.edges.length);x++){let vec=bridge.edges.map((_,e)=>(x>>e)&1);if(sat(bcForm,vec,i,j)){found=true;break;}}
 if(found)brYes++;else brNo++;
}
check(brYes===6&&brNo===6,"countercontrol mismatch "+brYes+"/"+brNo);
const total=summaries.reduce((a,x)=>a+x.individuallySensitiveSignBits,0);
check(total===528,"total sign count");
return {status:"PASS",assertions,mutantChecks,deletedChecks,totalSensitiveSignFlips:total,summary:summaries,bridgeCutVertexCountercontrol:{flipsSAT:brYes,flipsStillUNSAT:brNo},scope:"Only strict signed 3CNF of odd-charge connected cubic G with G-v connected; no unrestricted SAT or FLMV theorem.",algorithm:"Postorder GF(2) parity completion on a spanning tree of G-v; finite baseline exhaustive UNSAT and cutvertex mutation controls"};
})();
console.log(JSON.stringify(summary,null,2));
