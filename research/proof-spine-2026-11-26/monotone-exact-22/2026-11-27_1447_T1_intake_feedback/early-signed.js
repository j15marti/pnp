module.exports=function early(F,gauge){
 const vs=[...new Set(F.flatMap(a=>a.v))].sort((a,b)=>a-b),p=new Map([0,...vs].map(x=>[x,x])),s=new Map([0,...vs].map(x=>[x,0])),steps=[],work={rowChecks:0,find:0,relationTests:0,rounds:0};
 function find(x){let y=x,b=0;while(p.get(y)!==y){work.find++;b^=s.get(y);y=p.get(y)}return [y,b]}
 function join(x,y,b){let [u,i]=find(x),[v,j]=find(y);if(u===v)return (i^j)===b?0:-1;if(u>v){[u,v]=[v,u]}p.set(v,u);s.set(v,i^j^b);return 1}
 join(gauge,0,0);steps.push({kind:"complement gauge",v:gauge,b:0});
 function factor(a){const m=a.v.map(find),v=[...new Set(m.map(x=>x[0]).filter(Boolean))].sort((a,b)=>a-b),ok=[];
  for(let k=0;k<2**v.length;k++){work.rowChecks++;let w=m.reduce((z,[r,b],i)=>z|(((r?((k>>v.indexOf(r))&1):0)^b)<<i),0);if(a.ok.includes(w))ok.push(k)}return {v,ok,ids:a.ids}
 }
 let T=[],conflict=null;
 for(;;){work.rounds++;T=F.map(factor);let changes=0;for(let [i,t] of T.entries()){if(!t.ok.length){conflict={factor:i,ids:t.ids};break}
  // Rebuild snapshot relation before applying: unchanged row truth-table was certified under prior substitutions, valid under later restrictions.
  const q=[0,...t.v];for(let j=0;j<q.length;j++)for(let k=j+1;k<q.length;k++){
   const bit=(w,v)=>v?(w>>t.v.indexOf(v)&1):0,b=bit(t.ok[0],q[j])^bit(t.ok[0],q[k]);work.relationTests+=t.ok.length;
   if(!t.ok.every(w=>(bit(w,q[j])^bit(w,q[k]))===b))continue;
   let r=join(q[j],q[k],b);if(r<0){conflict={factor:i,ids:t.ids,relation:[q[j],q[k],b]};break}if(r>0){changes++;steps.push({kind:"forced signed relation",round:work.rounds,sourceB:t.ids,factor:i,scope:t.v,allowed:t.ok,relation:[q[j],q[k],b]})}
  }if(conflict)break
 }if(conflict||!changes)break}
 let map=vs.map(v=>[v,...find(v)]),free=new Set(map.map(x=>x[1]).filter(Boolean));
 const dedup=new Map();for(const a of T){const key=a.v.join(",");if(!dedup.has(key))dedup.set(key,{v:a.v,ok:a.ok.slice(),ids:a.ids.slice()});else{let b=dedup.get(key);b.ok=b.ok.filter(w=>a.ok.includes(w));b.ids.push(...a.ids)}}
 // Independent soundness: verify every original local assignment maps exactly to the reconstructed factor table.
 let verification=0;for(const [i,a] of F.entries()){let t=T[i],m=a.v.map(find);if(conflict)break;for(let k=0;k<2**t.v.length;k++){let z=m.reduce((z,[r,b],j)=>z|(((r?(k>>t.v.indexOf(r)&1):0)^b)<<j),0);verification++;if(t.ok.includes(k)!==a.ok.includes(z))throw Error("quotient check")}}
 const final=[...dedup.values()].filter(a=>a.ok.length!==2**a.v.length);
 return {before:{vars:vs.length,factors:F.length,rows:F.reduce((s,t)=>s+t.ok.length,0)},after:{vars:free.size,factors:final.length,rows:final.reduce((s,t)=>s+t.ok.length,0),fixed:map.filter(x=>!x[1]).length},forced:steps.length-1,steps,map,final,conflict,work,verification};
};
