function run(){
 const assert=(b,msg)=>{if(!b)throw Error(msg)};
 const R={wheelMasks:0,wheelRimAssignments:0,packBoundaryCases:0,packShadowCases:0,fanoCases:[],strictCases:[],strictAssignments:0,strictSatLifts:0,localSignatureChecks:0,graphLifts:0,edgeChecks:0,closurePins:0,closureRejects:0};
 function rim(mask,L){let witness=null,count=0;for(let t=0;t<3**L;t++){let v=[],z=t;for(let i=0;i<L;i++){v.push(z%3);z=Math.floor(z/3)}if(v.every((c,i)=>c!==v[(i+1)%L]&&(c!==2||((mask>>i)&1)))){count++;witness=v}}return {count,witness}}
 let tables={};for(let L of [3,5,7,9])for(let mask=0;mask<8;mask++){let r=rim(mask,L);R.wheelMasks++;R.wheelRimAssignments+=3**L;assert(!!r.count===!!mask,"wheel projection");tables[L+":"+mask]=r.witness}
 const choice=(a,b,x,y)=>[a,b].find(c=>c!==x&&c!==y);
 function packSpec(a,b){let specs=[];for(let j=0;j<2;j++){let bit=j===0?a:b;let c=2+bit;for(let s=0;s<2;s++){let ok=choice(2,1,c,s)!==undefined&&choice(3,0,c,s)!==undefined;R.packShadowCases++;assert(ok===(s===bit),"shadow sync")}}}
 for(let a=0;a<2;a++)for(let b=0;b<2;b++){packSpec(a,b);for(let h=0;h<4;h++){let ok=true;for(let j=0;j<2;j++){let bit=j===0?a:b;for(let color=0;color<4;color++){let want=(color>>(1-j))&1;let f=(color<2?2:0)+1-want;let carrier=(color<2?2:0)+bit;ok&&=choice(color,f,h,carrier)!==undefined}}R.packBoundaryCases++;assert(ok===(h===2*a+b),"pack decode")}}
 function graph(n,clauses,dup=1,L=5,packed=true){
  let edges=[],names=[],pal=[],car=[],neg=[],packs=[],wheels=[];
  const node=name=>{names.push(name);return names.length-1};
  const edge=(a,b)=>{assert(a!==b,"loop");edges.push([a,b])};
  for(let i=0;i<4;i++)pal.push(node("p"+i));
  for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)edge(pal[i],pal[j]);
  const list=(v,colors)=>{for(let c=0;c<4;c++)if(!colors.includes(c))edge(v,pal[c])};
  const aux=(a,b,x,y)=>{let z=node("aux");list(z,[a,b]);edge(z,x);edge(z,y);return [z,a,b,x,y]};
  for(let i=0;i<n;i++){let a=node("x"+i),b=node("not"+i);car.push(a);neg.push(b);list(a,[2,3]);list(b,[2,3]);edge(a,b)}
  if(packed)for(let i=0;i+1<n;i+=2){let h=node("packed"+i),sh=[],as=[];for(let j=0;j<2;j++){let c=car[i+j],s=node("shadow");sh.push(s);list(s,[0,1]);as.push(aux(2,1,c,s),aux(3,0,c,s));for(let color=0;color<4;color++){let want=(color>>(1-j))&1;let f=(color<2?2:0)+1-want;as.push(aux(color,f,h,color<2?c:s))}}packs.push({i,h,sh,as})}
  for(let k=0;k<clauses.length;k++)for(let d=0;d<dup;d++){let h=node("wheelhub"),tri=[node("eq"),node("eq"),node("eq")];for(let i=0;i<3;i++){edge(tri[i],h);edge(tri[i],pal[3]);for(let j=i+1;j<3;j++)edge(tri[i],tri[j])}let vs=Array.from({length:L},()=>node("rim"));for(let i=0;i<L;i++){edge(vs[i],h);edge(vs[i],vs[(i+1)%L]);let lit=clauses[k][i];edge(vs[i],lit===undefined?pal[2]:(lit>0?car[lit-1]:neg[-lit-1]))}wheels.push({k,h,tri,vs})}
  let keys=edges.map(([a,b])=>Math.min(a,b)+":"+Math.max(a,b));assert(new Set(keys).size===keys.length,"duplicate edge");
  function project(bits){return clauses.every(c=>c.some(l=>bits[Math.abs(l)-1]===(l>0?1:0)))}
  function lift(bits){let out=Array(names.length).fill(-1);pal.forEach((v,i)=>out[v]=i);car.forEach((v,i)=>{out[v]=2+bits[i];out[neg[i]]=3-bits[i]});for(let p of packs){out[p.h]=2*bits[p.i]+bits[p.i+1];p.sh.forEach((v,j)=>out[v]=bits[p.i+j]);for(let [v,a,b,x,y] of p.as){out[v]=choice(a,b,out[x],out[y]);assert(out[v]!==undefined,"pack lift")}}for(let w of wheels){let mask=clauses[w.k].reduce((m,l,i)=>m|((bits[Math.abs(l)-1]===(l>0?1:0)?1:0)<<i),0);let row=tables[L+":"+mask];if(!row)return null;out[w.h]=3;w.tri.forEach((v,i)=>out[v]=i);w.vs.forEach((v,i)=>out[v]=row[i])}assert(out.every(c=>c>=0&&c<4),"unassigned");for(let [a,b] of edges){R.edgeChecks++;assert(out[a]!==out[b],"invalid graph edge")}R.graphLifts++;return out}
  return {lift,project,V:names.length,E:edges.length}
 }
 function closure(n,cs){let a=Array(n).fill(-1),changed=true;while(changed){changed=false;for(let c of cs){if(c.some(l=>a[Math.abs(l)-1]===(l>0?1:0)))continue;let left=[...new Set(c.filter(l=>a[Math.abs(l)-1]===-1))];if(left.some(l=>left.includes(-l)))continue;if(!left.length){R.closureRejects++;return null}if(left.length===1){let l=left[0];a[Math.abs(l)-1]=l>0?1:0;changed=true;R.closurePins++;break}}}return a}
 const bits=(k,n)=>Array.from({length:n},(_,i)=>(k>>i)&1);
 const edges=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
 const fano=edges.flatMap(e=>[e.map(x=>x+1),e.map(x=>-x-1)]);
 for(let del=-1;del<14;del++){let cs=fano.filter((_,i)=>i!==del),g=graph(7,cs,2,5,true),cl=closure(7,cs),sat=0;for(let k=0;k<128;k++){let x=bits(k,7),expected=cs.every(c=>c.some(l=>x[Math.abs(l)-1]===(l>0?1:0))),out=g.lift(x);assert(!!out===expected,"Fano gluing");if(expected){sat++;assert(cl&&cl.every((v,i)=>v<0||v===x[i]),"closure removed model")}}assert(sat===(del<0?0:5),"Fano count");R.fanoCases.push({deleted:del,sat,assignments:128,vertices:g.V,edges:g.E})}
 // Strict signed K5 graphs: 4 ports per vertex, 10 signed edges.
 let seed=7102026;function rand(){seed=(Math.imul(1664525,seed)+1013904223)>>>0;return seed}
 function equality(a,b,s){return s?[[a,b],[-a,-b]]:[[-a,b],[a,-b]]}
 function sig(p,bal){if(!bal)return p.slice(1).flatMap(q=>equality(p[0],q,0));let cs=[];for(let skip=0;skip<4;skip++){let c=p.filter((_,i)=>i!==skip);cs.push(c,c.map(x=>-x))}return cs}
 for(let bal of [false,true])for(let k=0;k<16;k++){let x=bits(k,4),c=sig([1,2,3,4],bal),good=bal?x.reduce((a,b)=>a+b,0)===2:x.every(v=>v===x[0]);assert(c.every(t=>t.some(l=>x[Math.abs(l)-1]===(l>0?1:0)))===good,"signature");R.localSignatureChecks++}
 for(let s=0;s<2;s++)for(let k=0;k<4;k++){let x=bits(k,2);assert(equality(1,2,s).every(c=>c.some(l=>x[Math.abs(l)-1]===(l>0?1:0)))===((x[0]^x[1])===s),"signed edge");R.localSignatureChecks++}
 for(let t=0;t<20;t++){let p=Array.from({length:5},()=>[]),es=[],q=0;for(let i=0;i<5;i++)for(let j=i+1;j<5;j++){let a=++q,b=++q,s=t===0?0:(rand()>>>16)&1;p[i].push(a);p[j].push(b);es.push([a,b,s])}let types=p.map(()=>t===0?false:t===1?true:!!((rand()>>>16)&1)),cs=es.flatMap(e=>equality(...e)).concat(p.flatMap((row,i)=>sig(row,types[i]))),g=graph(20,cs,1,5,true),cl=closure(20,cs),sat=0;for(let k=0;k<1024;k++){let x=Array(20).fill(0);es.forEach(([a,b,s],i)=>{x[a-1]=(k>>i)&1;x[b-1]=x[a-1]^s});let good=p.every((row,i)=>{let v=row.map(a=>x[a-1]);return types[i]?v.reduce((a,b)=>a+b,0)===2:v.every(a=>a===v[0])});assert(g.project(x)===good,"strict CNF");R.strictAssignments++;if(good){sat++;assert(cl&&cl.every((v,i)=>v<0||v===x[i]),"strict closure");assert(g.lift(x),"strict witness");R.strictSatLifts++}}R.strictCases.push({case:t,sat,vertices:g.V,edges:g.E,clauses:cs.length})}
 R.strictSatCases=R.strictCases.filter(x=>x.sat>0).length;R.strictUnsatCases=20-R.strictSatCases;R.discrepancies=0;return R
}
console.log(JSON.stringify(run(), null, 2));
