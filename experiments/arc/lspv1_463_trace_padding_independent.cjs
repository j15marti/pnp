// LSPV-1/463 independent Node.js replay: strict-3 source and rejecting circuit control.
"use strict";
let checks=0; const ok=(p,s)=>{checks++;if(!p)throw Error(s)};
const norm=a=>[...new Set(a)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
const sat=(cl,env)=>cl.some(x=>env[Math.abs(x)]===(x>0));
let src={},proof=[],cls=[];
for(let b=0;b<8;b++){
 const c=norm([1,2,3].map((v,i)=>b&(1<<i)?-v:v));cls.push(c);src["F"+b]=c;
}
for(const c of cls){
 const env={};for(const lit of c)env[Math.abs(lit)]=lit<0;
 ok(!sat(c,env),"falsifies source");for(const d of cls)if(d!==c)ok(sat(d,env),"deletion witness");
}
for(let m=0;m<8;m++){
 const env={1:!!(m&1),2:!!(m&2),3:!!(m&4)};
 ok(cls.filter(c=>!sat(c,env)).length===1,"exact unsat control");
}
const get=id=>src[id]||proof.find(p=>p.id===id)?.cl;
const res=(a,b,p)=>{ok(a.includes(p)&&b.includes(-p),"oriented pivot");const c=norm([...a.filter(x=>x!==p),...b.filter(x=>x!==-p)]);ok(!c.some(x=>c.includes(-x)),"not tautological");return c};
function derive(a,b,p,section){
 const cl=res(get(a),get(b),p),id="R"+(proof.length+1);
 proof.push({id,a,b,p,cl,section});return id;
}
let fr=cls.map((cl,i)=>({id:"F"+i,cl}));
for(const v of [3,2,1]){
 let next=[];
 for(const u of fr.filter(x=>x.cl.includes(v))){
  const rem=norm(u.cl.filter(x=>x!==v));
  const neg=fr.find(x=>x.cl.includes(-v)&&JSON.stringify(norm(x.cl.filter(y=>y!==-v)))===JSON.stringify(rem));
  ok(!!neg,"elimination mate");const id=derive(u.id,neg.id,v,"source");
  next.push({id,cl:get(id)});
 }
 fr=next;
}
ok(proof.length===7&&get(fr[0].id).length===0,"seven paid source inferences");
let val={4:1,5:0,6:1};
for(const v of [4,5,6])src["I"+v]=[val[v]?v:-v];
const funcs={XOR:(a,b)=>a^b,AND:(a,b)=>a&b,OR:(a,b)=>a|b,NAND:(a,b)=>1-(a&b),NOT:a=>1-a};
const gates=[[7,"XOR",4,5],[8,"AND",7,6],[9,"NOT",8,null],[10,"OR",9,5],[11,"NAND",4,10],[12,"NOT",11,null]];
let known={4:"I4",5:"I5",6:"I6"};
for(const [y,op,a,b] of gates){
 const arity=b===null?1:2;
 val[y]=funcs[op](val[a],b===null?0:val[b]);
 for(let bits=0;bits<(1<<arity);bits++){
  const x=bits&1,z=arity===2?(bits>>1)&1:0;
  const cl=norm([x?-a:a,...(arity===2?[z?-b:b]:[]),funcs[op](x,z)?y:-y]);
  src["G"+y+"_"+x+(arity===2?z:"")]=cl;
 }
 let cur="G"+y+"_"+val[a]+(arity===2?val[b]:"");
 for(const v of arity===2?[a,b]:[a]){
   const unit=get(known[v]);ok(unit.length===1,"gate parent unit");
   cur=derive(known[v],cur,unit[0],"trace");
 }
 known[y]=cur;ok(JSON.stringify(get(cur))===JSON.stringify([val[y]?y:-y]),"gate propagated");
}
ok(val[12]===0&&proof.filter(p=>p.section==="trace").length===10,"rejecting trace");
const trail=proof.slice();src.BAD_OUT=[12];
derive("BAD_OUT",known[12],12,"extra_output_axiom");
ok(proof.length===18&&get("R18").length===0,"augmented contradiction");
function replay(S,P){
 const h={...S};
 for(const p of P){if(h[p.id]||!h[p.a]||!h[p.b]||!h[p.a].includes(p.p)||!h[p.b].includes(-p.p))return false;
 let c=norm([...h[p.a].filter(x=>x!==p.p),...h[p.b].filter(x=>x!==-p.p)]);
 if(c.some(x=>c.includes(-x))||JSON.stringify(c)!==JSON.stringify(p.cl))return false;h[p.id]=c;}
 return P.length>0&&P[P.length-1].cl.length===0;
}
ok(replay(src,proof),"full source-checked replay");
ok(replay(src,proof.slice(0,7)),"strict three-source replay");
ok(!replay(Object.fromEntries(Object.entries(src).filter(([x])=>x!=="BAD_OUT")),proof.slice(7)),"no false-output source");
const circuitVals=Object.fromEntries(Object.entries(val).map(([k,v])=>[k,!!v]));
for(const [id,c] of Object.entries(src))if(id.startsWith("G")||id.startsWith("I"))ok(sat(c,circuitVals),"trace has a model");
for(const mode of ["pivot","parent","conclusion","gate_source","bad_out","missing"]){
 let S=JSON.parse(JSON.stringify(src)),P=JSON.parse(JSON.stringify(proof));
 if(mode==="pivot")P.at(-1).p=77;
 if(mode==="parent")P.at(-1).a="MISSING";
 if(mode==="conclusion")P.at(-1).cl=[99];
 if(mode==="gate_source")S.G12_1=[-4,12];
 if(mode==="bad_out")S.BAD_OUT=[-12];
 if(mode==="missing")P.splice(-2,1);
 ok(!replay(S,P),"reject "+mode);
}
console.log(JSON.stringify({checked:true,assertions:checks,source_clauses:8,exact_min_resolution_nodes:7,gate_clauses:20,gate_nodes:10,augmented_bad_output_nodes:18,corruptions_rejected:6,source_only_requires_no_bad_output_axiom:true}));
