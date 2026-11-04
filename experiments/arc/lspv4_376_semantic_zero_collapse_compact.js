'use strict';
const assert=require('assert'),fs=require('fs');
function validate(F){
 if(!Array.isArray(F)||!F.length)throw Error('empty CNF');
 let n=0;for(const c of F){if(!Array.isArray(c)||!c.length)throw Error('bad clause');
  const a=new Set();for(const x of c){if(!Number.isSafeInteger(x)||!x)throw Error('bad literal');
   if(a.has(x)||a.has(-x))throw Error('dup or tautology');a.add(x);n=Math.max(n,Math.abs(x));}}
 if(n>12)throw Error('finite checker cap');return n;
}
function direct(F,b){return F.every(c=>c.some(x=>Boolean((b>>(Math.abs(x)-1))&1)===(x>0)));}
function compile(F){
 const n=validate(F);let k=0,res=0;const gates=[];
 function lit(x){return{t:'lit',x};}
 function gate(t,a,b){const z={t,a,b,id:++k};gates.push(z);return z;}
 let roots=[];for(const c of F){let q=lit(c[0]);for(let j=1;j<c.length;j++){q=gate('OR',q,lit(c[j]));res+=2;}roots.push(q);}
 let root=roots[0];for(let j=1;j<roots.length;j++){root=gate('AND',root,roots[j]);res+=2;}
 return{n,root,gates,charged:k+res+1};
}
function evalC(C,b){
 let a=new Map();
 function get(z){if(z.t==='lit')return Boolean((b>>(Math.abs(z.x)-1))&1)===(z.x>0);
  if(a.has(z.id))return a.get(z.id);const x=get(z.a),y=get(z.b),out=z.t==='AND'?(x&&y):(x||y);a.set(z.id,out);return out;}
 return get(C.root);
}
function signed(n){let out=[];for(let m=1;m<3**n;m++){let code=m,c=[];for(let j=1;j<=n;j++){let d=code%3;code=Math.floor(code/3);if(d)c.push(d===1?j:-j);}out.push(c);}return out;}
function parity(odd){const ed=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],F=[];
 for(let v=0;v<4;v++){let ix=ed.map((e,i)=>e.includes(v)?i+1:0).filter(Boolean);
  for(let b=0;b<8;b++){let p=((b&1)?1:0)^((b&2)?1:0)^((b&4)?1:0);
   if(p!==(odd&&v===0?1:0))F.push(ix.map((x,j)=>(b>>j)&1?-x:x));}}return F;}
function run(){
 let results={valid:0,sat:0,unsat:0,malformed:0,assignments:0,gateEvals:0};
 const base=Array.from({length:8},(_,m)=>[1,2,3].map((x,j)=>(m>>j)&1?-x:x));
 let tests=[[[1],[-1]],[[1]],[[1,2],[-1],[-2]],parity(true),parity(false)];
 for(let mask=1;mask<256;mask++)tests.push(base.filter((_,j)=>(mask>>j)&1));
 for(let n=1;n<=4;n++){const c=signed(n);for(let i=0;i<Math.min(c.length,45);i++)tests.push([c[i],c[(i*7+3)%c.length]]);}
 for(const F of tests){const C=compile(F);let solutions=0;
  for(let b=0;b<(1<<C.n);b++){const x=evalC(C,b),y=direct(F,b);assert.strictEqual(x,y);solutions+=y;results.assignments++;results.gateEvals+=C.gates.length;}
  results.valid++;results[solutions?'sat':'unsat']++;
  assert.strictEqual(solutions===0,Array.from({length:1<<C.n},(_,i)=>evalC(C,i)).every(v=>!v));
 }
 const bad=[null,{},[],[[0]],[[1,1]],[[-1,1]],[[1.2]],[[Infinity]],[[1],[]],[[NaN]],[['x']]];
 for(const v of bad){assert.throws(()=>compile(v));results.malformed++;}
 let odd=parity(true),even=parity(false);
 const count=F=>{let C=compile(F),s=0;for(let a=0;a<1<<C.n;a++)s+=evalC(C,a);return s;};
 assert.strictEqual(count(odd),0);assert.strictEqual(count(even),8);
 assert.strictEqual(results.valid,341);
 return{run:'LSPV4-376',results,oddModels:0,evenModels:8,scope:'hypothetical Rsem, unchanged fixed Rmix341'};
}
if(require.main===module){const x=run();console.log(JSON.stringify(x,null,2));if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(x,null,2)+'\n');}
module.exports={compile,direct,evalC,parity,run};
