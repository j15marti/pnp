"use strict";
/* LSPV-3/492. SOURCE-EXACT ONE-HOT -> RES -> AND3 -> XOR.
   Distinct extensional typed calculus: clause outputs of RES may be viewed
   by AND3 as factors at no additional charge; historical acceptance OPEN.
   Prints replay summary when run in Node >=18. */
function ok(b,m){if(!b)throw Error(m)}
function norm(a){return [...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y)}
function resolve(a,b,p){
 ok(a.includes(-p)&&b.includes(p),"wrong RES pivot");
 const out=norm([...a.filter(x=>x!==-p),...b.filter(x=>x!==p)]);
 ok(!out.some(x=>out.includes(-x)),"tautological RES");return out;
}
function truth(c,s){let t=0;for(let j=0;j<1<<s.length;j++){let sat=c.some(x=>{
  let bit=(j>>s.indexOf(Math.abs(x)))&1;return x>0?bit:!bit
 });if(sat)t|=1<<j;}return t}
function join(a,b,s){let t=0;for(let j=0;j<1<<s.length;j++){
 function evalx(f){let idx=0;f.s.forEach((z,i)=>idx|=((j>>s.indexOf(z))&1)<<i);return (f.t>>idx)&1}
 if(evalx(a)&&evalx(b))t|=1<<j;
}return t}
function build(name,edges,charge){
 const h=charge.length,E=edges.length,inc=Array.from({length:h},()=>[]);
 ok(edges.length*2===3*h&&charge.reduce((a,b)=>a^b,0)===1,"graph/charge");
 edges.forEach(([u,v],e)=>{inc[u].push(e);inc[v].push(e)});
 ok(inc.every(a=>a.length===3),"noncubic");
 let src=[],nodes=[],m=new Map(),pos=[];
 function source(c){let id="s"+src.length,o={id,c:norm(c)};src.push(o);m.set(id,{rule:"SOURCE",c:o.c});return id}
 function step(rule,parents,rest){let id="d"+nodes.length,n={id,rule,parents,...rest};nodes.push(n);m.set(id,n);return id}
 for(let e=0;e<E;e++){pos[e]=source([2*e+1,2*e+2]);source([-2*e-1,-2*e-2])}
 let vr=[];
 for(let v=0;v<h;v++){
  let leaves=[];
  for(let pat=0;pat<8;pat++){
   let bits=[pat&1,(pat>>1)&1,(pat>>2)&1];
   if((bits[0]^bits[1]^bits[2])===charge[v])continue;
   let c=inc[v].map((e,j)=>-(2*e+bits[j]+1)),parent=source(c);
   for(let j=0;j<3;j++)if(bits[j]===0){
    let pivot=2*inc[v][j]+1,b=m.get(pos[inc[v][j]]).c,after=resolve(c,b,pivot);
    parent=step("RES",[parent,pos[inc[v][j]]],{pivot,c:after});c=after;
   }
   const s=inc[v].map(e=>2*e+2).sort((a,b)=>a-b);
   ok(c.length===3&&c.every(x=>s.includes(Math.abs(x))),"bit width");
   leaves.push({id:parent,s,t:truth(c,s)});
  }
  ok(leaves.length===4,"wrong parity clause count");
  function and(a,b,final){
   let s=[...new Set([...a.s,...b.s])].sort((x,y)=>x-y);ok(s.length===3,"AND support");
   let t=join(a,b,s),extra={s,t};
   if(final){
    let mask=inc[v].reduce((a,e)=>a^(1n<<BigInt(2*e+1)),0n);
    extra.row={mask:String(mask),rhs:charge[v]};
   }
   let id=step("AND3",[a.id,b.id],extra);return {id,s,t,row:extra.row}
  }
  let a=and(leaves[0],leaves[1]),b=and(leaves[2],leaves[3]),f=and(a,b,true);
  for(let j=0;j<8;j++){let parity=((j&1)^((j>>1)&1)^((j>>2)&1));ok(((f.t>>j)&1)===(parity===charge[v]?1:0),"alias wrong")}
  vr.push({id:f.id,row:f.row});
 }
 while(vr.length>1){let next=[];
  for(let j=0;j<vr.length;j+=2){
   if(j+1===vr.length){next.push(vr[j]);continue}
   const a=vr[j],b=vr[j+1],row={mask:String(BigInt(a.row.mask)^BigInt(b.row.mask)),rhs:a.row.rhs^b.row.rhs};
   let id=step("XOR",[a.id,b.id],{row});next.push({id,row});
  }vr=next;
 }
 ok(BigInt(vr[0].row.mask)===0n&&vr[0].row.rhs===1,"noncontradictory sink");
 return {name,edges,charge,src,nodes};
}
function check(P){
 const E=P.edges.length,h=P.charge.length,inc=Array.from({length:h},()=>[]);
 ok(E*2===3*h&&P.charge.reduce((a,b)=>a^b,0)===1,"shape");
 P.edges.forEach(([a,b],e)=>{ok(a!==b&&a>=0&&b>=0&&a<h&&b<h,"edge");inc[a].push(e);inc[b].push(e)});
 ok(inc.every(x=>x.length===3),"degree");
 const want=[];for(let e=0;e<E;e++)want.push(norm([2*e+1,2*e+2]),norm([-2*e-1,-2*e-2]));
 for(let v=0;v<h;v++)for(let p=0;p<8;p++){
  const b=[p&1,(p>>1)&1,(p>>2)&1];
  if((b[0]^b[1]^b[2])!==P.charge[v])want.push(norm(inc[v].map((e,j)=>-(2*e+b[j]+1))));
 }
 ok(P.src.length===want.length,"clause count");
 let m=new Map();for(let i=0;i<P.src.length;i++){
  const a=P.src[i];ok(a.id==="s"+i&&JSON.stringify(a.c)===JSON.stringify(want[i]),"source not authenticated");m.set(a.id,{rule:"CLAUSE",c:a.c})}
 let types={RES:0,AND3:0,XOR:0},depth=new Map(P.src.map(x=>[x.id,0])),cost=0;
 for(let j=0;j<P.nodes.length;j++){
  const p=P.nodes[j];ok(p.id==="d"+j&&!m.has(p.id),"id");
  const a=m.get(p.parents[0]),b=m.get(p.parents[1]);
  ok(a&&b&&p.parents[0]!==p.parents[1],"parent");let entry;
  if(p.rule==="RES"){
   ok(a.rule==="CLAUSE"&&b.rule==="CLAUSE","RES type");
   let c=resolve(a.c,b.c,p.pivot);
   ok(JSON.stringify(c)===JSON.stringify(p.c),"invalid RES result");entry={rule:"CLAUSE",c};
  }else if(p.rule==="AND3"){
   function asFactor(x){if(x.rule==="FACTOR")return x;
    ok(x.rule==="CLAUSE","AND parent type");
    let s=[...new Set(x.c.map(Math.abs))].sort((a,b)=>a-b);
    ok(s.length<=3,"AND nonlocal input");return {rule:"FACTOR",s,t:truth(x.c,s)}
   }
   let x=asFactor(a),y=asFactor(b),s=[...new Set([...x.s,...y.s])].sort((a,b)=>a-b);
   ok(s.length<=3&&JSON.stringify(s)===JSON.stringify(p.s),"AND support");
   let t=join(x,y,s);ok(t===p.t,"AND table");
   if(p.row){
    let mask=BigInt(p.row.mask),rhs=p.row.rhs;
    ok(rhs===0||rhs===1,"rhs");ok(mask>=0n&&mask<(1n<<BigInt(2*E)),"invalid mask");
    for(let k=0;k<1<<s.length;k++){
     let sum=0;for(let i=0;i<s.length;i++)if(mask&(1n<<BigInt(s[i]-1)))sum^=(k>>i)&1;
     ok(((t>>k)&1)===(sum===rhs?1:0),"row not equivalent");
    }
   }
   entry={rule:"FACTOR",s,t,row:p.row};
  }else if(p.rule==="XOR"){
   ok(a.row&&b.row,"XOR type");
   ok(BigInt(p.row.mask)===(BigInt(a.row.mask)^BigInt(b.row.mask))&&p.row.rhs===(a.row.rhs^b.row.rhs),"XOR result");
   entry={rule:"AFFINE",row:p.row};
  }else ok(false,"unknown rule");
  types[p.rule]++;cost++;m.set(p.id,entry);
  depth.set(p.id,1+Math.max(depth.get(p.parents[0]),depth.get(p.parents[1])));
 }
 const end=m.get(P.nodes.at(-1).id);
 ok(end.rule==="AFFINE"&&BigInt(end.row.mask)===0n&&end.row.rhs===1,"sink");
 ok(P.src.length===7*h&&types.RES===6*h&&types.AND3===3*h&&types.XOR===h-1&&cost===10*h-1,"cost");
 let odd=0,even=0;
 if(E<=9)for(let assignment=0;assignment<1<<E;assignment++){
  let bits=Array(2*E+1).fill(0);
  for(let e=0;e<E;e++){bits[2*e+2]=(assignment>>e)&1;bits[2*e+1]=1-bits[2*e+2]}
  const sat=c=>c.some(l=>l>0?bits[l]===1:bits[-l]===0);
  if(P.src.every(x=>sat(x.c)))odd++;
  if(inc.every(arr=>arr.reduce((t,e)=>t^bits[2*e+2],0)===0))even++;
 }
 if(E<=9)ok(odd===0&&even===1<<(E-h+1),"models");
 return {name:P.name,h,sourceVariables:2*E,sourceClauses:P.src.length,paid:cost,types,span:depth.get(P.nodes.at(-1).id),oddModels:odd,evenModels:even,explicitBytes:JSON.stringify(P).length};
}
function run(){
 let graph=[{name:"K4",e:[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],h:4},
 {name:"K3,3",e:Array.from({length:9},(_,e)=>[Math.floor(e/3),3+e%3]),h:6}];
 let result=[],fixtures=[],reject=0;
 for(let {name,e,h} of graph){
  let p=build(name,e,[1,...Array(h-1).fill(0)]);result.push(check(p));fixtures.push(p);
  for(let f of [
   x=>x.src[2*e.length].c[0]*=-1,
   x=>x.nodes.find(y=>y.rule==="RES").pivot=999,
   x=>x.nodes.find(y=>y.rule==="RES").c=[999],
   x=>x.nodes.find(y=>y.rule==="AND3").t^=1,
   x=>x.nodes.find(y=>y.rule==="XOR").row.rhs^=1,
   x=>x.nodes[1].parents[0]="future",
   x=>x.charge[0]^=1
  ]){let x=JSON.parse(JSON.stringify(p));f(x);let did=false;try{check(x)}catch(e){did=true};ok(did,"corruption accepted");reject++}
 }
 return {result,rejectedControls:reject,fixtures,
    qualification:"CONDITIONAL extensional clause-to-factor typing; historical byte grammar RES/AND3 interface OPEN. No unrestricted lower bound."};
}
if(typeof module!=="undefined")module.exports={build,check,run};
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(run(),null,2));