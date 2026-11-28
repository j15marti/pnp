function substitute(F,guard,sub){
 const A=new Map(guard),result=[];let tests=0,replay=0;
 for(const f of F){let vs=[...new Set(f.vs.filter(v=>!A.has(v)).map(v=>sub&&v===sub.from?sub.to:v))].sort((a,b)=>a-b);
  let rows=[];for(let w=0;w<2**vs.length;w++){let get=v=>A.has(v)?A.get(v):sub&&v===sub.from?((w>>vs.indexOf(sub.to))&1)^sub.flip:(w>>vs.indexOf(v))&1;let old=f.vs.reduce((a,v,j)=>a|(get(v)<<j),0);tests++;if(f.rows.includes(old))rows.push(w)}
  // independently replay by mapping allowed original words, not by enumerating output words
  let image=new Set();for(const w of f.rows){replay++;const a=new Map(f.vs.map((v,j)=>[v,(w>>j)&1]));if([...A].some(([v,b])=>a.has(v)&&a.get(v)!==b))continue;if(sub&&a.has(sub.from)){const b=a.get(sub.from)^sub.flip;if(a.has(sub.to)&&a.get(sub.to)!==b)continue;a.set(sub.to,b)}image.add(vs.reduce((n,v,j)=>n|(a.get(v)<<j),0))}
  if(JSON.stringify([...image].sort((a,b)=>a-b))!==JSON.stringify(rows))throw Error("substitute verify");
  result.push({vs,rows,owners:f.owners});
 }return {result,tests,replay}
}
module.exports=substitute;
