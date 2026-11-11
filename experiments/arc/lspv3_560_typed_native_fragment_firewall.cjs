'use strict';
/* LSPV-3/560. Separate strict source-bound guard for recovered /341
 SOURCE/AND3/XOR fixture checker. NOT a full historical R_mix341 parser.
 Node: node experiments/arc/lspv3_560_typed_native_fragment_firewall.cjs [raw.json]
 Tests ORIGINAL producer and checker bodies unchanged inside node:vm.
 */
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const safe=x=>typeof x==='number'&&Number.isSafeInteger(x), bit=x=>safe(x)&&(x===0||x===1), array=Array.isArray;
const sid=x=>typeof x==='string'&&/^s(?:0|[1-9]\d*)$/.test(x);
const did=x=>typeof x==='string'&&/^d(?:0|[1-9]\d*)$/.test(x);
const hex=x=>typeof x==='string'&&/^0x(?:0|[1-9a-f][0-9a-f]*)$/.test(x);
function ck(x,msg){if(!x)throw Error('TYPED: '+msg);}
function guard(f,external){
 ck(f&&typeof f==='object'&&!array(f),'fixture');
 const g=f.graph;ck(g&&safe(g.n)&&g.n>=4&&array(g.edges),'graph');
 const V=g.n,E=g.edges.length;ck(2*E===3*V,'cubic dimensions');
 for(const e of g.edges)ck(array(e)&&e.length===2&&e.every(x=>safe(x)&&x>=0&&x<V)&&e[0]!==e[1],'edge type');
 ck(array(f.charges)&&f.charges.length===V&&f.charges.every(bit),'binary numeric charges');
 ck(array(f.clauses)&&array(external)&&f.clauses.length===4*V&&external.length===f.clauses.length,'source count');
 const ids=new Set();
 for(let i=0;i<f.clauses.length;i++){
  const c=f.clauses[i];ck(c&&sid(c.id)&&!ids.has(c.id),'source id');ids.add(c.id);
  ck(safe(c.vertex)&&c.vertex>=0&&c.vertex<V&&safe(c.pattern)&&c.pattern>=0&&c.pattern<8,'source vertex/pattern');
  ck(array(c.literals)&&c.literals.length===3&&c.literals.every(x=>safe(x)&&x!==0&&Math.abs(x)<=E),'signed numeric literals');
  ck(array(external[i])&&external[i].length===3&&c.literals.every((x,j)=>x===external[i][j]),'external source binding');
 }
 ck(array(f.proof),'proof records');
 for(const p of f.proof){
  ck(p&&did(p.id)&&!ids.has(p.id),'paid id');ids.add(p.id);
  ck(array(p.parents)&&p.parents.length===2&&p.parents.every(x=>sid(x)||did(x))&&p.parents[0]!==p.parents[1],'parent types');
  ck(p.rule==='AND3'||p.rule==='XOR','supported rule');
  if(p.rule==='AND3'){
   ck(p.kind==='factor'&&array(p.support)&&p.support.length<=3&&p.support.every(x=>safe(x)&&x>=0&&x<E)&&new Set(p.support).size===p.support.length,'numeric support');
   ck(safe(p.table)&&p.table>=0&&p.table<=255,'truth table');
  }else ck(p.kind==='affine','affine kind');
  if(p.row!=null){
   ck(typeof p.row==='object'&&!array(p.row)&&hex(p.row.mask)&&bit(p.row.rhs),'typed affine row');
   ck(BigInt(p.row.mask)<(1n<<BigInt(E)),'ghost coordinates');
  }else ck(p.rule!=='XOR','missing XOR row');
 }
 return {variables:E,vertices:V,source:4*V,paid:f.proof.length};
}
function externalCNF(g,ch){
 ck(ch.every(bit),'external charges');
 const inc=Array.from({length:g.n},()=>[]);
 g.edges.forEach(([a,b],i)=>{inc[a].push(i);inc[b].push(i);});
 const out=[];
 for(let v=0;v<g.n;v++)for(let p=0;p<8;p++)if(((p&1)^((p>>1)&1)^((p>>2)&1))!==ch[v])
  out.push(inc[v].map((e,j)=>(p>>j)&1?-(e+1):e+1));
 return out;
}
const clone=x=>JSON.parse(JSON.stringify(x));
function preflight(f,ext){try{return {accept:true,metrics:guard(f,ext)}}catch(e){return {accept:false,error:String(e.message)}}}
function originals(){
 const pp='experiments/arc/lspv2_341_mixed_tseitin_min_dag.js';
 const vp='experiments/arc/lspv2_341_independent_verify.js';
 const producer=fs.readFileSync(pp,'utf8'),checker=fs.readFileSync(vp,'utf8');
 let out=[];vm.runInNewContext(producer,{console:{log:s=>out.push(s)}});
 const packet=JSON.parse(out[0]);
 function verify(p){
  let logs=[];try{vm.runInNewContext(checker,{require:n=>n==='fs'?{readFileSync:()=>JSON.stringify(p)}:null,
   process:{argv:['node',vp,'fixture.json']},console:{log:s=>logs.push(s)}});
   return {accept:true,checks:JSON.parse(logs[0]).checks};
  }catch(e){return {accept:false,error:String(e.message)}}
 }
 return {packet,verify};
}
function audit(){
 const {packet,verify}=originals(),native=verify(packet);assert.equal(native.accept,true);
 const out={run:'LSPV-3/560',type:'separate sound sublanguage',nativeBaselineChecks:native.checks,valid:[],negative:[]};
 for(const f of packet.fixtures){
  const r=preflight(f,externalCNF(f.graph,f.charges));assert.equal(r.accept,true,f.graph.name);
  out.valid.push({graph:f.graph.name,...r.metrics});
 }
 const controls=[
 ['charge-string',p=>p.fixtures[0].charges[0]='1','binary numeric charges'],
 ['support-string',p=>p.fixtures[0].proof[0].support='012','numeric support'],
 ['numeric-id',p=>p.fixtures[0].proof[0].id=48,'paid id'],
 ['external-source',p=>p.fixtures[0].clauses[0].literals[0]*=-1,'external source binding'],
 ['mask-lexical',p=>p.fixtures[0].proof[2].row.mask='00','typed affine row'],
 ['ghost-mask',p=>{let q=p.fixtures[0].proof.find(x=>x.row);q.row.mask='0x'+(BigInt(q.row.mask)|(1n<<35n)).toString(16)},'ghost coordinates'],
 ['res-opcode',p=>p.fixtures[0].proof[0].rule='RES','supported rule']
 ];
 const ext=externalCNF(packet.fixtures[0].graph,packet.fixtures[0].charges);
 for(const [name,mutate,why] of controls){
  const p=clone(packet);mutate(p);
  const r=preflight(p.fixtures[0],ext);
  assert.equal(r.accept,false,name);assert(r.error.includes(why),name+' '+r.error);
  out.negative.push({name,rejected:true,why});}
 const bad=clone(packet);bad.fixtures[0].charges[0]='1';
 out.nativeStringCharge=verify(bad);
 const res=clone(packet);res.fixtures[0].proof[0].rule='RES';
 out.nativeRes=verify(res);assert.equal(out.nativeRes.accept,false);
 out.tests=1+out.valid.length+controls.length+1;
 return out;
}
if(require.main===module){const result=audit();if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result,null,2));}
module.exports={guard,externalCNF,preflight,audit};
