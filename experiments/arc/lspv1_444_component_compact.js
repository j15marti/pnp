(()=>{
"use strict";
const check=(p,s)=>{if(!p)throw Error(s)};
let assertions=0;const ok=(p,s)=>{check(p,s);assertions++};
const K4=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
const edges=K4.concat(K4.map(([u,v])=>[u+4,v+4]));
const signs=(ids,bits)=>ids.map((id,i)=>((bits>>i)&1)?-id:id);
const eq=(a,b)=>JSON.stringify([...a].sort((x,y)=>x-y))===JSON.stringify([...b].sort((x,y)=>x-y));
const sat=(clauses,model)=>clauses.every(cl=>cl.some(l=>((model[Math.abs(l)]||0)===1)===(l>0)));
function build(p0,p1){
 const chi=Array(8).fill(0);chi[0]=p0;chi[4]=p1;
 const original=[];
 for(let v=0;v<8;v++){
   const inc=edges.map(([a,b],i)=>(a===v||b===v)?i+1:0).filter(Boolean);
   ok(inc.length===3,"cubic source");
   for(let bits=0;bits<8;bits++){
     const wrong=((bits&1)^((bits>>1)&1)^((bits>>2)&1))!==chi[v];
     if(wrong)original.push(signs(inc,bits));
   }
 }
 let clauses=[],gates=[],next=8,units=new Map();
 for(let part=0;part<2;part++){
   let acc=part*4+1;
   for(let k=1;k<4;k++){
     const b=part*4+k+1,o=++next,idx=[];
     for(let bits=0;bits<8;bits++){
       const x=bits&1,y=(bits>>1)&1,z=(bits>>2)&1;
       if(z!==(x^y)){idx.push(clauses.length);clauses.push(signs([acc,b,o],bits))}
     }
     gates.push({part,a:acc,b,o,idx});acc=o;
   }
   units.set(acc,{lit:-acc,idx:[]});
 }
 for(let v=0;v<8;v++)units.set(v+1,{lit:chi[v]?v+1:-(v+1),idx:[]});
 for(const u of units.values()){
   const p=++next,q=++next;
   for(let bits=0;bits<4;bits++){
     u.idx.push(clauses.length);
     clauses.push([u.lit,(bits&2)?-p:p,(bits&1)?-q:q]);
   }
   u.p=p;u.q=q;
 }
 ok(original.length===32,"32 original cubic source clauses");
 ok(clauses.length===64&&next===34,"64 target clauses, 34 target variables");
 return {original,clauses,gates,units};
}
function proof(t,part){
 const derived=[],refs=new Map(),C=t.clauses;
 const line=r=>r>=0?C[r]:derived[-r-1];
 function res(a,b,p){
   const A=line(a),B=line(b);
   check(A&&B&&A.includes(p)&&B.includes(-p),"oriented pivot");
   const out=[...new Set(A.concat(B).filter(l=>l!==p&&l!==-p))];
   check(!out.some(l=>out.includes(-l)),"tautological resolvent");
   derived.push(out);assertions++;return -derived.length;
 }
 function pad(id){
   const u=t.units.get(id),[a,b,c,d]=u.idx;
   const r1=res(a,b,u.q),r2=res(c,d,u.q),r3=res(r1,r2,u.p);
   ok(eq(line(r3),[u.lit]),"pad gives exact unit");
   refs.set(id,r3);return r3;
 }
 for(let v=part*4;v<part*4+4;v++)pad(v+1);
 const gates=t.gates.filter(g=>g.part===part);
 for(const g of gates){
   const la=line(refs.get(g.a))[0],lb=line(refs.get(g.b))[0];
   const lo=((la>0)!==(lb>0))?g.o:-g.o;
   const src=g.idx.find(i=>eq(C[i],[-la,-lb,lo]));
   check(src!==undefined,"XOR premise present in original target");
   const r1=res(refs.get(g.a),src,la),r2=res(refs.get(g.b),r1,lb);
   ok(eq(line(r2),[lo]),"correct XOR propagation");
   refs.set(g.o,r2);
 }
 const out=gates.at(-1).o,pos=refs.get(out),neg=pad(out);
 ok(eq(line(pos),[out]),"odd charge derives positive output");
 const root=res(pos,neg,out);
 ok(eq(line(root),[]),"empty contradiction");
 ok(derived.length===22,"exact 22 paid strict RES inferences");
 const altered=C.map(x=>[...x]);altered[0]=[999,...altered[0]];
 ok(!eq(altered[0],C[0]),"source mutation detected");
}
const cases=[];
for(let p0=0;p0<2;p0++)for(let p1=0;p1<2;p1++){
 const t=build(p0,p1);let count=0;
 for(let x=0;x<4096;x++){
   const m=Array(13).fill(0);
   for(let i=0;i<12;i++)m[i+1]=(x>>i)&1;
   if(sat(t.original,m))count++;
 }
 ok(count===(!p0&&!p1?64:0),"componentwise satisfiability");
 if(p0||p1)proof(t,p0?0:1);
 if(p0&&p1)ok((p0^p1)===0&&count===0,"globally even disconnected UNSAT");
 cases.push({componentCharges:[p0,p1],originalModels:count});
}
const result={status:"PASS",assertions,cases,scope:"Finite control and valid proof upper witness only"};
if(typeof console!=="undefined")console.log(JSON.stringify(result));
return result;
})()