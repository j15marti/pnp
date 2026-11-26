function redteam(){
let seed=20261126,check=0;
const rand=n=>{seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return (seed>>>0)%n}, range=n=>Array.from({length:n},(_,i)=>i), assert=(b,m)=>{check++;if(!b)throw Error(m)};
const data={random:0,randomYes:0,randomNo:0,exteriorNo:0,exteriorYes:0,strictPeels:0,profiles:0,assignments:0,explicit:[]};
function test(n,cs,B,label){
let m=cs.length,free=new Set(range(n).filter(v=>!B.includes(v))),d=-1,intersection=(1<<m)-1;
for(let s=0;s<1<<m;s++){let rows=range(m).filter(i=>s>>i&1),nb=new Set(rows.flatMap(i=>cs[i].map(t=>t[0])).filter(v=>free.has(v))),v=rows.length-nb.size;if(v>d){d=v;intersection=s}else if(v===d)intersection&=s}
let U=range(m).filter(i=>intersection>>i&1),V=new Set(U.flatMap(i=>cs[i].map(t=>t[0])).filter(v=>free.has(v))),out=range(m).filter(i=>!U.includes(i)),rep=new Map(),used=new Set([...V,...B]);
function assign(j){if(j===out.length)return true;let i=out[j];for(let [v] of cs[i])if(!used.has(v)){rep.set(i,v);used.add(v);if(assign(j+1))return true;used.delete(v);rep.delete(i)}return false}assert(assign(0),"outside SDR");
let arcs=range(n).map(()=>[]),reps=new Set(rep.values());for(let i of out){let u=rep.get(i),s=cs[i].find(t=>t[0]===u)[1];for(let [v,t] of cs[i])if(v!==u)arcs[u].push([v,1^s^t])}
// Independent alternative: mark every vertex that can reach a root or a balanced simple cycle.
let good=new Set(range(n).filter(v=>!reps.has(v)));
for(let start of reps){function visit(u,p,path){for(let [v,b] of arcs[u])if(v===start&&!(p^b)){for(let z of path)good.add(z)}else if(!path.includes(v)&&reps.has(v))visit(v,p^b,[...path,v])}visit(start,0,[start])}
let changed=true;while(changed){changed=false;for(let u of reps)if(!good.has(u)&&arcs[u].some(([v])=>good.has(v))){good.add(u);changed=true}}
let feasible=[...reps].every(u=>good.has(u)),keep=[...new Set([...B,...V])],ext=new Set(),full=new Set(),inner=new Set();for(let w=0;w<1<<n;w++){let pass=cs.map(c=>{let a=c.map(([v,s])=>(w>>v&1)^s);return a.some(t=>t!==a[0])}),key=keep.map(v=>w>>v&1).join("");if(out.every(i=>pass[i]))ext.add(key);if(U.every(i=>pass[i]))inner.add(key);if(pass.every(Boolean))full.add(key);data.assignments++}
assert(ext.size===(feasible?2**keep.length:0),"root or balanced cycle characterization");assert(full.size===(feasible?inner.size:0)&&[...full].every(k=>inner.has(k)),"projection equality");data.profiles+=2**keep.length;data.exteriorNo+=!feasible;data.exteriorYes+=feasible;data.strictPeels+=U.length>0&&out.length>0;
if(label)data.explicit.push({label,n,m,delta:d,core:U.length,exterior:feasible,sat:full.size>0});else{data.random++;data.randomYes+=full.size>0;data.randomNo+=full.size===0}}
const pos=cs=>cs.map(c=>c.map(v=>[v,0]));
let fano=[];for(let a=1;a<=7;a++)for(let b=a+1;b<=7;b++){let c=a^b;if(c>b)fano.push([a-1,b-1,c-1])}
test(7,pos(fano),[],"Fano: perfect SDR but no balanced simple cycle");
test(3,pos([[0,1],[1,2],[2,0]]),[],"odd cycle: no even simple cycle although even closed walks exist");
test(3,[[[0,0],[1,0]],[[1,0],[2,0]],[[2,0],[0,1]]],[],"signed balanced triangle");
test(4,pos([[0,1,2],[0,1,3]]),[0,1],"two protected boundary phases");
test(6,pos([[0,1],[1,2],[2,0],[3,4],[4,5],[5,3]]),[0,1,2],"infeasible exterior independent of protected core");
for(let j=0;j<500;j++){let n=3+rand(5),m=1+rand(11),B=range(n).filter(()=>rand(5)===0),cs=range(m).map(()=>{let vs=range(n),k=2+rand(2),c=[];for(let i=0;i<k;i++)c.push([vs.splice(rand(vs.length),1)[0],rand(2)]);return c});test(n,cs,B,"")}
return {...data,checks:check,seed:20261126}}
console.log(JSON.stringify(redteam(),null,2));
