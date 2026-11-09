'use strict';
/* LSPV-3/521: original-source two-defect test. No historical checker API. */
const mod=x=>((x%3)+3)%3, A=(ok,msg)=>{if(!ok)throw Error(msg)};
const graphs=()=>{
 const K4=[];for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)K4.push([i,j]);
 const K33=[];for(let i=0;i<3;i++)for(let j=3;j<6;j++)K33.push([i,j]);
 const cube=[];for(let i=0;i<8;i++)for(let j=i+1;j<8;j++)if((i^j).toString(2).split('1').length===2)cube.push([i,j]);
 const pet=[],prism=[];for(let i=0;i<5;i++)pet.push([i,(i+1)%5],[i,5+i],[5+i,5+(i+2)%5]);
 for(let i=0;i<8;i++)prism.push([i,(i+1)%8],[8+i,8+(i+1)%8],[i,8+i]);
 return [['K4',4,K4],['K33',6,K33],['cube',8,cube],['Petersen',10,pet],['prism16',16,prism]];
};
function source(h,input,sigma){
 const edges=input.map(e=>e.slice().sort((a,b)=>a-b)).sort((a,b)=>a[0]-b[0]||a[1]-b[1]);
 const b=Array(h).fill(0);b[0]=sigma;
 const C=[],info=[];
 edges.forEach((_,i)=>{C.push([3*i+1,3*i+2,3*i+3]);info.push({kind:'ALO',vertex:-1})});
 for(let v=0;v<h;v++){
  const inc=edges.map((e,i)=>e.includes(v)?i:-1).filter(i=>i>=0);
  A(inc.length===3,'degree');
  for(let a=0;a<3;a++)for(let c=0;c<3;c++)for(let d=0;d<3;d++){
   const t=[a,c,d],sum=mod(inc.reduce((z,i,j)=>z+(edges[i][0]===v?1:-1)*t[j],0));
   if(sum===b[v])continue;
   C.push(inc.map((i,j)=>-(3*i+t[j]+1)));
   info.push({kind:sum===mod(b[v]+sigma)?'wrong':'essential',vertex:v});
  }
 }
 A(C.length===39*h/2,'source count');
 return {edges,b,C,info};
}
function flow(h,edges,b,sigma,u,v){
 const want=b.slice();want[u]=mod(want[u]+sigma);want[v]=mod(want[v]+sigma);
 A(mod(want.reduce((a,b)=>a+b,0))===0,'charge');
 const adj=Array.from({length:h},()=>[]);
 edges.forEach(([a,b],i)=>{adj[a].push([b,i]);adj[b].push([a,i])});
 const par=Array(h).fill(-1),by=Array(h).fill(-1),order=[0];par[0]=0;
 for(let j=0;j<order.length;j++)for(const [w,i] of adj[order[j]])if(par[w]<0){par[w]=order[j];by[w]=i;order.push(w)}
 A(order.length===h,'connected');
 const lab=Array(edges.length).fill(0);
 for(let j=order.length-1;j>0;j--){
  const x=order[j],i=by[x],sign=edges[i][0]===x?1:-1;
  lab[i]=mod(sign*want[x]);want[par[x]]=mod(want[par[x]]+want[x]);
 }
 A(want[0]===0,'tree');
 return lab;
}
function falseSource(C,labels){
 const truth=new Set(labels.map((x,i)=>3*i+x+1));
 const bad=[];C.forEach((c,j)=>{if(c.every(l=>l>0?!truth.has(l):truth.has(-l)))bad.push(j)});
 return bad;
}
const summary={role:'LSPV-3/521',published_script:'original-source two-defect',pairs:0,families:[],full_checker_executed:false};
for(const [name,h,E] of graphs())for(const sigma of [1,2]){
 const s=source(h,E,sigma),counts={name,h,sigma,original_sources:s.C.length,pairs:0};
 for(let u=0;u<h;u++)for(let v=u+1;v<h;v++){
  const vals=flow(h,s.edges,s.b,sigma,u,v),bad=falseSource(s.C,vals);
  A(bad.length===2,'two false sources');A(bad.every(i=>s.info[i].kind==='wrong'),'wrong class');
  A(bad.map(i=>s.info[i].vertex).sort((a,b)=>a-b).join(',')===u+','+v,'fault vertices');
  counts.pairs++;summary.pairs++;
 }
 summary.families.push(counts);
}
A(summary.pairs===428,'total pairs');
console.log(JSON.stringify(summary));
