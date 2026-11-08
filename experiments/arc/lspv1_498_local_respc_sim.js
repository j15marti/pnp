// LSPV-1/498: explicit syntactic Res(PC_1/F2) local-3 proof compiler.
// Lines are arrays of unique "mask:rhs" equation strings over 3 variables.
'use strict';
const assert=require('node:assert/strict');
const fs=require('node:fs');
const pop=(x)=>{let r=0;while(x){r+=x&1;x>>=1;}return r};
const eq=(m,b)=>String(m)+":"+String(b);
const val=(a,e)=>{const [m,b]=e.split(':').map(Number);return (pop(a&m)&1)===b};
const D=a=>[0,1,2].map(i=>eq(1<<i,1-((a>>i)&1))).sort();
const uniq=a=>[...new Set(a)].sort();
const bool=i=>[eq(1<<i,0),eq(1<<i,1)].sort();
const entails=(src,e)=>Array.from({length:8},(_,a)=>src.some(C=>!C.some(x=>val(a,x)))||val(a,e)).every(Boolean);
class Proof{
 constructor(src){this.src=src;this.nodes=[];this.source=[];this.ax=[];src.forEach((c,i)=>this.source.push(this.add('src',c,[],{i})));for(let i=0;i<3;i++)this.ax.push(this.add('ax',bool(i),[],{i}))}
 add(k,c,p=[],x={}){c=uniq(c);assert.ok(p.every(id=>Number.isInteger(id)&&id>=0&&id<this.nodes.length));
  if(k==='src')assert.deepEqual(c,this.src[x.i]);
  else if(k==='ax')assert.deepEqual(c,bool(x.i));
  else if(k==='weak')assert.ok(this.nodes[p[0]].c.every(z=>c.includes(z)));
  else if(k==='sum'){
    const f=x.f,g=x.g, A=this.nodes[p[0]].c,B=this.nodes[p[1]].c;
    assert.ok(A.includes(f)&&B.includes(g));const [fm,fb]=f.split(':').map(Number),[gm,gb]=g.split(':').map(Number);
    assert.deepEqual(c,uniq([...A.filter(z=>z!==f),...B.filter(z=>z!==g),eq(fm^gm,fb^gb)]));
  }else if(k==='del'){
    assert.ok(this.nodes[p[0]].c.includes(eq(0,1)));
    assert.deepEqual(c,this.nodes[p[0]].c.filter(z=>z!==eq(0,1)));
  }else throw Error('rule');
  const id=this.nodes.length;this.nodes.push({id,k,c,p,x});return id;
 }
}
function build(src,target){assert.ok(entails(src,target));assert.notEqual(target.split(':')[0],'0');const P=new Proof(src);let active={};
 for(let a=0;a<8;a++){
  const d=D(a);
  if(!val(a,target)){const idx=src.findIndex(C=>JSON.stringify(C)===JSON.stringify(d));assert.ok(idx>=0);active[a]=P.add('weak',uniq([...d,target]),[P.source[idx]])}
  else {
   const [m,b]=target.split(':').map(Number);let terms=[];
   for(let i=0;i<3;i++)if(m&(1<<i)){const lit=eq(1<<i,(a>>i)&1);terms.push([P.add('weak',uniq([...d,lit]),[P.ax[i]]),lit])}
   while(terms.length>1){const [[u,f],[v,g]] = terms;const [fm,fb]=f.split(':').map(Number),[gm,gb]=g.split(':').map(Number);const sum=eq(fm^gm,fb^gb);terms=[[P.add('sum',uniq([...d,sum]),[u,v],{f,g}),sum],...terms.slice(2)]}
   assert.equal(terms[0][1],target);active[a]=terms[0][0];
  }
 }
 for(let bit=2;bit>=0;bit--){const out={};for(const str of Object.keys(active)){const a=+str;if(a&(1<<bit))continue;const b=a^(1<<bit);const f=eq(1<<bit,1-((a>>bit)&1)),g=eq(1<<bit,1-((b>>bit)&1));
   const A=P.nodes[active[a]].c,B=P.nodes[active[b]].c;assert.ok(A.includes(f)&&B.includes(g));const c=uniq([...A.filter(z=>z!==f),...B.filter(z=>z!==g)]);
   const u=P.add('sum',uniq([...c,eq(0,1)]),[active[a],active[b]],{f,g});out[a]=P.add('del',c,[u]);
  }active=out;assert.equal(Object.keys(active).length,1<<bit)
 }
 assert.deepEqual(P.nodes[active[0]].c,[target]);return P;
}
let compiled=0,checkedNodes=0,maxNodes=0,card={};
for(let bits=0;bits<256;bits++){const src=Array.from({length:8},(_,i)=>i).filter(i=>bits&(1<<i)).map(D);for(let m=1;m<8;m++)for(let b=0;b<2;b++){
 const target=eq(m,b);if(!entails(src,target))continue;const P=build(src,target);compiled++;checkedNodes+=P.nodes.length;maxNodes=Math.max(maxNodes,P.nodes.length);card[src.length]=(card[src.length]||0)+1;
}}
assert.equal(compiled,224);assert.equal(checkedNodes,8224);assert.equal(maxNodes,49);
const examples=[];for(let rhs=0;rhs<2;rhs++){const src=Array.from({length:8},(_,i)=>i).filter(a=>!val(a,eq(7,rhs))).map(D),P=build(src,eq(7,rhs));assert.equal(P.nodes.length,45);const counts={};for(let x of P.nodes)counts[x.k]=(counts[x.k]||0)+1;examples.push({rhs,total:45,counts})}
const src=Array.from({length:8},(_,i)=>i).filter(a=>!val(a,eq(7,1))).map(D),P=build(src,eq(7,1));let rejected=0;
for(const f of [()=>P.add('weak',[],[0]),()=>P.add('sum',[eq(7,1)],[0,1],{f:eq(1,0),g:eq(1,1)}),()=>P.add('del',[],[0]),()=>P.add('weak',src[0],[P.nodes.length+1]),()=>P.add('ax',src[0],[],{i:0}),()=>build(src,eq(7,0))]){try{f();throw Error('bad certificate accepted')}catch(e){if(e.message==='bad certificate accepted')throw e;rejected++}}
const raw={model:'syntactic Res(PC_1/F2), source-local three variables',sourceSubsets:256,affineTargets:14,acceptedImplications:compiled,checkedNodes,maxNodes,bySourceSize:card,examples,hostileRejected:rejected,status:'PASS; finite/restricted only'};
if(require.main===module){fs.writeFileSync(process.argv[2]||'lspv1_498_local_respc_raw_js.json',JSON.stringify(raw,null,2)+'\n');console.log(JSON.stringify(raw,null,2))}
module.exports={build,raw};
