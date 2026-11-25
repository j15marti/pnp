// node checker.js S27_results.json DA22_results.json
const fs=require('fs');
function run(s,d){
let checks=0, localWords=0, scans=0;
const assert=(v)=>{checks++;if(!v)throw Error("assertion "+checks)};
const bit=(x,i)=>(x>>i)&1, parity=x=>{let v=0;while(x){v^=1;x&=x-1}return v};
const ok=(o,x)=>!o.bad.includes(o.t.reduce((a,v,i)=>a|(bit(x,v)<<i),0));
function closure(n,reg,guard,width){
 let p=Array.from({length:n},(_,i)=>i),z=Array(n).fill(0),cuts=[];
 function find(i){if(p[i]===i)return [i,0];let [r,b]=find(p[i]);return [r,b^z[i]]}
 function join(a,b,v){let [i,s]=find(a),[j,t]=find(b);if(i===j)return (s^t)===v?0:-1;p[i]=j;z[i]=v^s^t;return 1}
 for(let [a,b,v] of guard)if(join(a,b,v)<0)return {status:"UNSAT",cuts};
 let blocks=[];function rec(a,start,k){if(!k){blocks.push(a);return}for(let i=start;i<=reg.length-k;i++)rec([...a,i],i+1,k-1)}
 for(let k=1;k<=width;k++)rec([],0,k);
 for(;;){let progress=false;for(let ids of blocks){
 scans++;let vars=[...new Set(ids.flatMap(i=>reg[i].t.map(t=>find(t)[0])))], pos=new Map(vars.map((v,i)=>[v,i])), support=[];
 for(let w=0;w<(1<<vars.length);w++){localWords++;if(ids.every(i=>{let o=reg[i],b=o.t.reduce((a,t,j)=>{let [r,v]=find(t);return a|((bit(w,pos.get(r))^v)<<j)},0);return !o.bad.includes(b)}))support.push(w)}
 if(!support.length)return {status:"UNSAT",cuts,block:ids};
 for(let i=0;i<vars.length&&!progress;i++)for(let j=i+1;j<vars.length&&!progress;j++){let v=bit(support[0],i)^bit(support[0],j);if(support.every(w=>(bit(w,i)^bit(w,j))===v)){assert(join(vars[i],vars[j],v)===1);cuts.push([vars[i],vars[j],v,ids]);progress=true}}
 if(progress)break;
 }if(!progress)return {status:"OPEN",cuts}}
}
const peer=[];
for(const x of s.controls.filter(x=>x.neighbor))for(const [label,reg] of [["UNSAT",x.neighbor.root],["SAT",x.neighbor.satRegistry]]){
 let rows=d.results.find(a=>a.id===`S27-${x.n}-${label}`).runs.find(a=>a.mode===2).cuts.map(a=>a.cut);
 let gs=[[]];if(rows.length)gs.push(rows.slice(0,1),rows);
 for(const g of gs){let ref=[];for(let w=0;w<1<<x.n;w++)if(g.every(([a,b,v])=>(bit(w,a)^bit(w,b))===v)&&reg.every(o=>ok(o,w)))ref.push(w);
 let a=closure(x.n,reg,g,1),b=closure(x.n,reg,g,3);
 for(let t of [a,b]){assert(t.status!=="UNSAT"||!ref.length);for(let [i,j,v] of t.cuts)assert(ref.every(w=>(bit(w,i)^bit(w,j))===v))}
 peer.push({n:x.n,label,guard:g,referenceModels:ref.length,single:a,triple:b});
 }}
// Relative XOR block: invalid f, clause l_i=u_i xor f_i; l=0 at f.
function makeBlock(charge){let owners=[],invalid=[];for(let f=0;f<8;f++)if(parity(f)!==charge){let y=4+invalid.length;invalid.push(f);owners.push({t:[0,1,y],bad:[f&3,(f&3)^7]});let v=1|(bit(f,2)<<1);owners.push({t:[y,2,3],bad:[v,v^7]})}return {owners,invalid}}
const block=[];
for(let charge=0;charge<2;charge++){let {owners,invalid}=makeBlock(charge),proj=[];for(let x=0;x<16;x++){let support=[];for(let y=0;y<16;y++){let w=x|(y<<4);if(owners.every(o=>ok(o,w)))support.push(y)}assert(!!support.length===(parity(x)===charge));if(support.length){proj.push({x,lift:support[0],count:support.length});let phase=bit(x,3),yy=invalid.reduce((a,f,i)=>a|((phase^Number((bit(x,0)^phase^bit(f,0))===0&&(bit(x,1)^phase^bit(f,1))===0))<<i),0);assert(support.includes(yy))}}block.push({charge,projection:proj})}
// Petersen graph and K4: true local laws of at most two stars, NOT a global moment check.
let graphs=[{n:4,edges:Array.from({length:4},(_,a)=>Array.from({length:4-a-1},(_,i)=>[a,a+i+1])).flat()},{n:10,edges:[...Array.from({length:5},(_,i)=>[i,(i+1)%5]),...Array.from({length:5},(_,i)=>[i,i+5]),...Array.from({length:5},(_,i)=>[i+5,5+(i+2)%5])]}];
const graphResults=[];
for(const {n,edges} of graphs){let stars=Array.from({length:n},(_,v)=>edges.map((e,i)=>e.includes(v)?i:-1).filter(i=>i>=0));assert(stars.every(t=>t.length===3));
 for(let odd of [0,1]){let charge=Array(n).fill(0);charge[0]=odd;
 let funcs=[{vars:[],eval:()=>0},...edges.map((e,i)=>({vars:[i],eval:w=>bit(w,i)}))];
 for(let v=0;v<n;v++)for(let f=0;f<8;f++)if(parity(f)!==charge[v])funcs.push({owner:v,vars:stars[v].slice(0,2),eval:w=>Number(bit(w,stars[v][0])===bit(f,0)&&bit(w,stars[v][1])===bit(f,1))});
 let pairs=0,max=0;
 for(let i=0;i<funcs.length;i++)for(let j=i+1;j<funcs.length;j++){let a=funcs[i],b=funcs[j],vs=[...new Set([a.owner,b.owner].filter(x=>x!==undefined))],es=[...new Set([...a.vars,...b.vars,...vs.flatMap(v=>stars[v])])],num=0,den=0;for(let x=0;x<1<<es.length;x++){let w=es.reduce((t,e,k)=>t|(bit(x,k)<<e),0);if(!vs.every(v=>stars[v].reduce((t,e)=>t^bit(w,e),0)===charge[v]))continue;den++;num+=a.eval(w)===b.eval(w)?1:-1}assert(den>0&&Math.abs(num)<den);max=Math.max(max,Math.abs(num/den));pairs++}
 // Gaussian XOR via elimination of incidence rows, independently check all source edge assignments on small graph.
 let count=0,witness=null;for(let w=0;w<1<<edges.length;w++)if(stars.every((t,v)=>t.reduce((r,e)=>r^bit(w,e),0)===charge[v])){count++;witness=w}
 assert((count===0)===!!odd);if(!odd)assert(count===2**(edges.length-n+1));
 graphResults.push({n,odd,compiledVariables:funcs.length,pairs,maxAbsCorrelation:max,baseModels:count,witness});
 }}
return {checks,localWords,scans,peer,block,graphResults};
}
console.log(JSON.stringify(run(JSON.parse(fs.readFileSync(process.argv[2])),JSON.parse(fs.readFileSync(process.argv[3]))),null,2));
