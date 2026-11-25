/* Run: node DA18.js GD24_deductions.json BS17_stalled.json */
const fs=require('fs');
function experiment(g,b){
const wt=x=>{let n=0;while(x){x&=x-1;n++}return n}, hi=x=>x.toString(2).length-1;
let stats={evals:0,xors:0,checks:0,closure:0};
const bit=(x,i)=>(x>>BigInt(i))&1n;
function border(k,rows){
 if(!rows.length)return {eq:[[0]],basis:[],degree:0};
 let B=[],eq=[],p=new Map(),leads=[],todo=new Set([0]),done=new Set();
 while(todo.size){
  let m=[...todo].sort((a,b)=>wt(a)-wt(b)||a-b)[0];todo.delete(m);if(done.has(m))continue;done.add(m);
  if(leads.some(l=>(l&m)===l))continue;
  let y=0n;for(let i=0;i<rows.length;i++){stats.evals++;if((rows[i]&m)===m)y|=1n<<BigInt(i)}
  let c=0n;while(y&&p.has(hi(y))){let [v,h]=p.get(hi(y));y^=v;c^=h;stats.xors++}
  if(y){p.set(hi(y),[y,c^(1n<<BigInt(B.length))]);B.push(m);for(let i=0;i<k;i++)if(!(m&(1<<i))&&!done.has(m|(1<<i)))todo.add(m|(1<<i))}
  else{let r=[m];for(let j=0;j<B.length;j++)if(bit(c,j))r.push(B[j]);eq.push(r);leads.push(m)}
 }
 if(B.length!==rows.length)throw Error("dimension");
 let set=new Set(rows);for(let x=0;x<1<<k;x++){let valid=eq.every(r=>r.reduce((z,m)=>z^Number((x&m)===m),0)===0);stats.checks++;if(valid!==set.has(x))throw Error("table mismatch")}
 return {eq,basis:B,degree:Math.max(0,...eq.map(r=>wt(r[0])))};
}
function globalAffine(tables,pins){
 let polys=[];for(let t of tables)for(let r of t.alg.eq)polys.push(r.map(m=>t.v.filter((_,i)=>m&(1<<i)).sort((a,b)=>a-b).join(",")));
 for(let [v,x] of pins)polys.push(x?[String(v),""]:[String(v)]);
 let keys=[...new Set(polys.flat())].sort((a,b)=>(a?a.split(",").length:0)-(b?b.split(",").length:0)||a.localeCompare(b)), ids=new Map(keys.map((k,i)=>[k,i])), pivot=new Map();
 for(let r of polys){let y=r.reduce((a,k)=>a^(1n<<BigInt(ids.get(k))),0n);while(y&&pivot.has(hi(y))){y^=pivot.get(hi(y));stats.xors++}if(y)pivot.set(hi(y),y)}
 let aff=[];for(let [i,y] of pivot){if(keys[i].includes(","))continue;let a=[];for(let j=0;j<=i;j++)if(bit(y,j))a.push(keys[j]);aff.push(a)}
 return {rank:pivot.size,aff};
}
function close(tables,pins,n){
 let history=[];for(;;){stats.closure++;for(let t of tables)t.alg=border(t.v.length,t.a);
 let a=globalAffine(tables,pins);let eq=a.aff.map(r=>r.reduce((z,k)=>z^(k===""?1n<<BigInt(n):1n<<BigInt(Number(k))),0n));
 function consistent(extra){let piv=new Map();for(let y of [...eq,...extra]){while(y){let mask=y&((1n<<BigInt(n))-1n);if(!mask)return false;let i=hi(mask);if(!piv.has(i)){piv.set(i,y);break}y^=piv.get(i);stats.xors++}}return true}
 let degrees={},terms=0,rows=0,rowbits=0,eqbits=0,maxdegree=0;
 for(let t of tables){rows+=t.a.length;rowbits+=t.a.length*t.v.length;maxdegree=Math.max(maxdegree,t.alg.degree);degrees[t.alg.degree]=(degrees[t.alg.degree]||0)+1;for(let r of t.alg.eq){terms+=r.length;eqbits+=r.length*t.v.length}}
 if(!consistent([])){history.push({rank:a.rank,aff:a.aff,contradiction:true});break}
 let dropped=0;for(let t of tables){let old=t.a.length;t.a=t.a.filter(x=>consistent(t.v.map((v,i)=>(1n<<BigInt(v))^((x&(1<<i))?1n<<BigInt(n):0n))));dropped+=old-t.a.length}
 history.push({tables:tables.length,rows,rowbits,terms,eqbits,maxdegree,degrees,rank:a.rank,aff:a.aff,dropped});if(!dropped)break;
 }
 return history;
}
let jobs=[];
for(let i=0;i<g.jobs.length;i++){let j=g.jobs[i],s=b.snapshots[i];if(j.id!==s.id||JSON.stringify(j.guard)!==JSON.stringify(s.guard))throw Error("identity");let pins=s.p.flatMap((v,i)=>v<0?[]:[[i,v]]);let pre=close(s.remaining.map(t=>({v:t.v,a:[...t.a]})),pins,s.n);let post=close(j.final.map(t=>({v:t.v,a:t.a.map(r=>[...r].reduce((z,c,i)=>z+(Number(c)<<i),0))})),pins,s.n);jobs.push({id:j.id,guard:j.guard,pins,pre,post})}
let fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]], controls=[];
for(let flip of [false,true]){let t=fano.map((v,i)=>({v,a:[1,2,3,4,5,6].map(x=>x^(flip&&i===0?1:0))}));let h=close(t,[],7),models=0;for(let x=0;x<128;x++)if(t.every(q=>q.a.includes(q.v.reduce((z,v,i)=>z+(((x>>v)&1)<<i),0))))models++;controls.push({flip,models,history:h})}
return {jobs,controls,stats};
}
console.log(JSON.stringify(experiment(JSON.parse(fs.readFileSync(process.argv[2])),JSON.parse(fs.readFileSync(process.argv[3]))),null,2));
