const fs=require('fs');
function verify(o){
 const y=[1,0,0,0,-1,0,0,-1,3,0,-1,1,1,-3,-1,0,8,-5,3,0,-8,6,-4,0,9,-6,0,0,0,0,2,0,-1,1,0,-1,0,-3,4,2,-2,-3,0,-2,-1,0,-1,-1,0,1,-1,0,0,1,-1,3,0,-5,5,0,1,-3,-1,0,0,0,0,0,1,0,0,0,5,6,-6,0,0,-1,0,1,-1,0,0,0,0,2,-2,0,0,2,0,-2,0,-1,0,0];
 const O=o.O.map(q=>q.t.slice().sort((a,b)=>a-b)),key=(a,b)=>Math.min(a,b)+","+Math.max(a,b),edges=t=>[key(t[0],t[1]),key(t[0],t[2]),key(t[1],t[2])],E=[...new Set(O.flatMap(edges))].map(s=>s.split(",").map(Number)).sort((a,b)=>a[0]-b[0]||a[1]-b[1]).map(t=>t.join(","));
 let w=new Map(E.map((e,i)=>[e,y[i]])),owner=new Set(O.map(t=>t.join(","))),T=[],ck=(q,m)=>{if(!q)throw Error(m)},zero=0,positive=0,min=1200,extra=0,checks=0;
 ck(E.length===96&&y.length===96,"edge identity");for(let t of O){ck(edges(t).reduce((s,e)=>s+w.get(e),0)===0,"owner tangent");checks++}
 for(let a=0;a<o.n;a++)for(let b=a+1;b<o.n;b++)for(let c=b+1;c<o.n;c++){
  let t=[a,b,c],e=edges(t),isOwner=owner.has(t.join(","));T.push(t);
  if(!isOwner&&e.every(k=>w.has(k))){extra++;ck(e.reduce((s,k)=>s+w.get(k),0)<=-1,"strict extra");checks++}
  let corr=e.map(k=>w.has(k)?-50-w.get(k):0),p=[];
  for(let z=0;z<8;z++){let s=t.map((_,i)=>z>>i&1?-1:1),v=150+corr[0]*s[0]*s[1]+corr[1]*s[0]*s[2]+corr[2]*s[1]*s[2];ck(v>=0&&((v===0)===(isOwner&&(z===0||z===7))),"support exact");checks++;p.push(v);if(v){positive++;min=Math.min(min,v)}else zero++}
  ck(p.reduce((s,v)=>s+v,0)===1200,"normalization");checks++;
  for(let i=0;i<3;i++){ck(p.reduce((s,v,z)=>s+((z>>i&1)?v:0),0)===600,"single");checks++}
  [[0,1],[0,2],[1,2]].forEach(([i,j],k)=>{ck(p.reduce((s,v,z)=>s+((z>>i&1)!==(z>>j&1)?v:0),0)===600-4*corr[k],"pair");checks++});
 }
 return {ref:"9164cb11c6fcdf96d470de9d86b061e3201a591f",edgeOrder:E,tangent:y,denominator:1200,extra,triples:T.length,zero,positive,minPositiveNumerator:min,checks,status:"FULL_SOURCE_ALLOWED_SUPPORT_CERTIFIED"};
}
console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(process.argv[2],'utf8'))),null,2));
