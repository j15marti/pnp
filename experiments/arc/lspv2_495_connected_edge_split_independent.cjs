'use strict';
// LSPV-2/495 independent standalone Node.js test of exact signed original 3-CNF.
// This is NOT an execution of the FLMV TM or the native mixed-calculus checker.
const crypto=require('node:crypto'),fs=require('node:fs');
let count=0;
function ok(cond,msg){if(!cond)throw Error(msg||'failed check '+count);count++}
const graphSet=[
 {name:'K3,3',H:6,edges:Array.from({length:9},(_,i)=>[Math.floor(i/3),3+(i%3)])},
 {name:'Q3',H:8,edges:Array.from({length:8},(_,i)=>Array.from({length:3},(_,b)=>[i,i^(1<<b)]).filter(e=>e[0]<e[1])).flat().sort((a,b)=>a[0]-b[0]||a[1]-b[1])},
 {name:'Heawood',H:14,edges:Array.from({length:7},(_,i)=>[0,1,3].map(s=>[i,7+((i+s)%7)])).flat().sort((a,b)=>a[0]-b[0]||a[1]-b[1])}
];
function key(e){return e[0]+','+e[1]}
function fields(g){let {H,edges}=g;let neigh=Array.from({length:H},()=>[]);
 for(let [a,b] of edges){neigh[a].push(b);neigh[b].push(a)}
 ok(edges.length===3*H/2,'noncubic edges');ok(neigh.every(z=>z.length===3),'noncubic degrees');
 let col=Array(H).fill(-1);for(let s=0;s<H;s++){if(col[s]>=0)continue;let q=[s];col[s]=0;for(let i=0;i<q.length;i++)for(let w of neigh[q[i]]){if(col[w]<0){col[w]=1-col[q[i]];q.push(w)}else ok(col[w]!==col[q[i]],'nonbipartite')}}
 const left=Array.from({length:H},(_,i)=>i).filter(i=>col[i]===0),right=Array.from({length:H},(_,i)=>i).filter(i=>col[i]===1);
 ok(left.length===right.length,'unequal sides');
 const match=[],used=new Set();function choose(i){if(i===left.length)return true;for(let w of neigh[left[i]])if(!used.has(w)){used.add(w);match.push([Math.min(left[i],w),Math.max(left[i],w)]);if(choose(i+1))return true;match.pop();used.delete(w)}return false}
 ok(choose(0),'no matching');return {left,right,match,neigh}
}
function emit(g,f,A,B,even=false){const {H,edges}=g,{left,right,match,neigh}=f;const M=match.length;
 let mi=new Map(match.map((e,i)=>[key(e),i]));let fixed=new Map();let num=H+1;
 for(let e of edges)if(!mi.has(key(e)))fixed.set(key(e),num++);
 ok(num===2*H+1,'bad fixed namespace');
 let incident=Array.from({length:H},()=>[]);
 for(let e of edges){let k=key(e),idx=mi.get(k);if(idx!==undefined){incident[e[0]].push(2*idx+1+Number(((left.includes(e[0])?A:B)>>idx)&1));incident[e[1]].push(2*idx+1+Number(((left.includes(e[1])?A:B)>>idx)&1))}else{incident[e[0]].push(fixed.get(k));incident[e[1]].push(fixed.get(k))}}
 const charge=Array(H).fill(0);if(!even)charge[0]=1;
 const clauses=[];for(let v of [...left,...right]){const vars=incident[v].sort((a,b)=>a-b);ok(new Set(vars).size===3,'local alias');
 for(let a=0;a<8;a++)if(((a>>2)&1 ^ (a>>1)&1 ^ (a>>0)&1)!==charge[v]){
  clauses.push(vars.map((id,j)=>((a>>(2-j))&1)?-id:id));
 }}
 ok(clauses.length===4*H,'incorrect clause count');ok(new Set(clauses.map(x=>x.join(','))).size===4*H,'repeated clause');
 const W=Math.ceil(Math.log2(2*H+1));let bits='11100011'+'1'.repeat(H)+'0'+'1'.repeat(2*H)+'0';
 for(let C of clauses)for(let l of C)bits+=(l<0?'1':'0')+Math.abs(l).toString(2).padStart(W,'0');bits+='10';
 ok(bits.length===8+(H+1)+(2*H+1)+12*H*(W+1)+2,'length');
 return {clauses,bits,incident,charge}
}
function rank(vec){let b=new Map(),r=0;for(let x0 of vec){let x=x0;while(x){let p=x.toString(2).length-1; if(b.has(p))x^=b.get(p);else{b.set(p,x);r++;break}}}return r}
function counts(g,dat){let {H,edges}=g,{incident,charge}=dat;const names=[...new Set(incident.flat())].sort((a,b)=>a-b);let ix=new Map(names.map((id,i)=>[id,i]));let rows=incident.map(a=>a.reduce((v,id)=>v^(1<<ix.get(id)),0));let r=rank(rows),ar=rank(rows.map((x,i)=>x ^ (charge[i]<<(names.length))));return {rank:r,aug:ar,models:ar>r?0:2**(names.length-r),variables:names.length}}
function brute(dat){let ids=[...new Set(dat.clauses.flat().map(Math.abs))].sort((a,b)=>a-b),ix=new Map(ids.map((id,i)=>[id,i]));let masks=dat.clauses.map(C=>{let m=0,z=0;for(let l of C){let b=2**ix.get(Math.abs(l));m+=b;if(l<0)z+=b}return [m,z]});let models=0;for(let a=0;a<2**ids.length;a++)if(masks.every(([m,z])=>(a&m)!==z))models++;return models}
let results=[];for(let g of graphSet){let f=fields(g),m=f.match.length;const pairs=[];
 if(m<=4){for(let a=0;a<2**m;a++)for(let b=0;b<2**m;b++)pairs.push([a,b])}
 else{for(let a=0;a<2**m;a++)pairs.push([a,a]);for(let a=0;a<12;a++)pairs.push([a,(a^1)]);}
 let seenSat=0,seenUnsat=0,bruteCases=0;
 for(let [a,b] of pairs){let dat=emit(g,f,a,b),C=counts(g,dat),d=((a^b).toString(2).match(/1/g)||[]).length;
 ok(C.variables===3*g.H/2+d,'wrong vars');ok(C.rank===(d===0?g.H-1:g.H),'wrong rank');ok((C.models===0)===(a===b),'sat iff NEQ');
 if(d>0)ok(C.models===2**(g.H/2+d),'offdiag count');
 if(g.H===6 || (g.H===8 && [[0,0],[0,1],[2,3],[5,5],[15,0],[15,15]].some(([x,y])=>a===x&&b===y))){ok(brute(dat)===C.models,'independent truth table');bruteCases++}
 if(C.models)seenSat++;else seenUnsat++;
 }
 for(let [a,b] of [[0,0],[0,1]]){let C=counts(g,emit(g,f,a,b,true));ok(C.models>0,'even-charge control')}
 let d0=emit(g,f,0,0);results.push({graph:g.name,H:g.H,word_bits:m,pairs:pairs.length,sat:seenSat,unsat:seenUnsat,bruteCases,bitlength:d0.bits.length,sha256:crypto.createHash('sha256').update(d0.bits).digest('hex')});
}
const result={artifact:'LSPV2_495_INDEPENDENT_NODE',seed:495,checks:count,results,native_FLMV:false,historical_Rmix341:false};
console.log(JSON.stringify(result,null,2));fs.writeFileSync(__dirname+'/LSPV2_495_NODE_RAW.json',JSON.stringify(result,null,2)+'\n');
