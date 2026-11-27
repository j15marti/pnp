function acquire(data){
let checks=0,ops=0,cap=1000000;function ck(v,m){checks++;if(!v)throw Error(m)}
function components(n,rows,skip){let a=Array.from({length:n},()=>[]);for(let i=0;i<rows.length;i++)if(!skip(i))for(let v of rows[i])for(let w of rows[i]){a[v].push(w);ops++}let id=Array(n).fill(-1),sets=[];for(let v=0;v<n;v++)if(id[v]<0){let q=[v];id[v]=sets.length;for(let i=0;i<q.length;i++)for(let w of a[q[i]]){ops++;if(id[w]<0){id[w]=sets.length;q.push(w)}}sets.push(q)}if(ops>cap)throw Error("cap");return {id,sets}}
let out=[];for(let c of data.cases){let {native,part}=c.source,n=c.variables,admitted=[];
for(let p=0;p<4;p++){let x=components(n,native,i=>part[i]===p),cut=native.map((t,i)=>i).filter(i=>part[i]===p&&new Set(native[i].map(v=>x.id[v])).size>1);
if(cut.length===0)continue;let cutset=new Set(cut),y=components(n,native,i=>cutset.has(i));if(y.sets.length!==cut.length)continue;
let degree=Array(y.sets.length).fill(0);for(let i of cut)for(let v of native[i])degree[y.id[v]]++;
ck(degree.every(d=>d===3),"balanced");admitted.push({partition:p,cut,componentSizes:y.sets.map(s=>s.length)});
}
let good=admitted.find(a=>a.cut.length===c.k&&a.cut.every((x,i)=>x===c.source.cross[i]));ck(!!good,"intended cut acquired");out.push({kind:c.kind,k:c.k,admitted});
}
return {out,ops,checks,cap}}
const fs=require('fs');console.log(JSON.stringify(acquire(JSON.parse(fs.readFileSync(process.argv[2]||'results.json','utf8'))),null,2));
