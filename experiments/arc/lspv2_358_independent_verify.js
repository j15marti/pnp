// LSPV-2 DPLL-IMPLICATE-PRUNE358 independent proof-and-source verifier.
// To run locally with Node:
// const {main}=require("./lspv2_358_dpll_implicate_producer.js"); console.log(JSON.stringify(verifyAll(main())));
"use strict";
function vAssert(b,msg){if(!b)throw Error("independent verifier: "+msg);}
function vCanon(a){
  vAssert(Array.isArray(a),"clause not array");
  const out=[...a].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);
  for(let i=0;i<out.length;i++){
    vAssert(Number.isInteger(out[i])&&out[i]!==0,"invalid literal");
    if(i>0)vAssert(out[i]!==out[i-1],"duplicate literal");
    vAssert(!out.includes(-out[i]),"tautology");
  }
  return out;
}
function vSame(a,b){return a.length===b.length&&a.every((x,i)=>x===b[i]);}
function vClause(c,mask){for(const lit of c)if(((mask>>(Math.abs(lit)-1))&1)==(lit>0?1:0))return true;return false;}
function vSat(F,mask){for(const c of F)if(!vClause(c,mask))return false;return true;}
function vEntails(F,C,n){for(let m=0;m<(1<<n);m++)if(vSat(F,m)&&!vClause(C,m))return false;return true;}
function vResolve(left,right,p){
  vAssert(left.includes(p)&&right.includes(-p),"wrong pivot");
  return vCanon(left.filter(x=>x!==p).concat(right.filter(x=>x!==-p)));
}
function verifyOne(test) {
  const F=test.F,C=test.C,n=test.n,P=test.proof;
  vAssert(n>=1&&n<=10&&P.length>=F.length,"bad header");
  vAssert(vSame(vCanon(C),C),"bad target");
  F.forEach(c=>{vAssert(vSame(vCanon(c),c),"bad source");for(const l of c)vAssert(Math.abs(l)<=n,"source name");});
  vAssert(vEntails(F,C,n),"unentailed conclusion");
  const typed=[],gates=new Map(),used=new Set();let q=0,defs=0,res=0,reads=0;
  for(let i=0;i<P.length;i++){
    const item=P[i];vAssert(item&&typeof item==="object","not line");
    let current=null;
    if(item.op==="src"){
      vAssert(i<F.length&&item.source===i,"bad source index");
      current=F[i];
    }else if(item.op==="def"){
      vAssert(Number.isInteger(item.y)&&item.y>n&&!used.has(item.y),"bad fresh wire");
      vAssert(Number.isInteger(item.a)&&item.a!==0&&Number.isInteger(item.b)&&item.b!==0,"bad gate input");
      vAssert(Math.abs(item.a)<item.y&&Math.abs(item.b)<item.y,"cyclic gate");
      used.add(item.y);gates.set(i,{y:item.y,a:item.a,b:item.b});
      vAssert(item.clause.length===0,"definition must be typed not a clause");
      q++;defs++;
    }else if(item.op==="dc"){
      vAssert(Number.isInteger(item.def)&&item.def<i&&gates.has(item.def),"invalid DEF reference");
      const d=gates.get(item.def);
      vAssert(Number.isInteger(item.slot)&&item.slot>=0&&item.slot<3,"invalid slot");
      const expected=[
        vCanon([-d.y,d.a]),vCanon([-d.y,d.b]),vCanon([d.y,-d.a,-d.b])
      ][item.slot];current=expected;reads+=3;
    }else if(item.op==="res"){
      vAssert(Array.isArray(item.parents)&&item.parents.length===2,"bad parents");
      const [a,b]=item.parents;
      vAssert(Number.isInteger(a)&&Number.isInteger(b)&&a<i&&b<i&&a>=0&&b>=0,"future parent");
      vAssert(typed[a]!==null&&typed[b]!==null,"typed parent not a clause");
      current=vResolve(typed[a],typed[b],item.pivot);reads+=typed[a].length+typed[b].length;
      q++;res++;
    }else throw Error("unknown op "+item.op);
    if(current===null){vAssert(item.op==="def","missing clause");typed.push(null);}
    else{vAssert(vSame(vCanon(item.clause),current),"forged statement "+i);typed.push(current);}
  }
  vAssert(Number.isInteger(test.root)&&test.root<P.length&&test.root>=0,"bad root id");
  const result=typed[test.root];vAssert(result!==null,"root is not a clause");
  vAssert(result.length===0||vSame(result,C),"wrong final consequence");
  if(result.length===0)vAssert(!Array.from({length:1<<n},(_,x)=>x).some(m=>vSat(F,m)),"early contradiction from SAT");
  const t=n-C.length,bound=(1<<t)-1+3*Math.max(C.length-1,0);
  vAssert(q===test.cost&&q<=bound,"invalid cost bound");
  vAssert(test.bound===undefined||test.bound===bound,"incorrect reported bound");
  return {q,defs,res,reads,early:result.length===0};
}
function verifyAll(raw) {
  vAssert(raw.run_id==="LSPV-2_DPLL_IMPLICATE_PRUNE358","bad run");
  vAssert(raw.seed===3582026,"seed mismatch");
  const count={proofs:0,satSources:0,unsatSources:0,early:0,defs:0,res:0,charged:0,statementReads:0,corruptRejected:0,malformedRejected:0};
  const seen=new Set();let priorSource=null,priorN=null;
  for(const e of raw.cases){
    const v=verifyOne(e);count.proofs++;count.early+=v.early?1:0;
    count.defs+=v.defs;count.res+=v.res;count.charged+=v.q;count.statementReads+=v.reads;
    const key=e.n+"|"+JSON.stringify(e.F);
    if(key!==priorSource){priorSource=key;priorN=e.n; if(seen.has(key))throw Error("interleaved duplicated sources");seen.add(key);
      if(Array.from({length:1<<priorN},(_,i)=>i).some(m=>vSat(e.F,m)))count.satSources++;else count.unsatSources++;
    }
  }
  const sample=raw.cases.filter(x=>x.proof.some(p=>p.op==="res"||p.op==="def")).slice(0,30);
  for(const e of sample){
    const bad=JSON.parse(JSON.stringify(e));
    const idx=bad.proof.findIndex(p=>p.op==="res"||p.op==="def");
    if(bad.proof[idx].op==="res")bad.proof[idx].pivot=9999;
    else bad.proof[idx].y=-1;
    try{verifyOne(bad);}catch(err){count.corruptRejected++;continue;}throw Error("accepted corrupted proof");
  }
  for(const badF of [[[0]],[[1,-1]],[[1,1]],[[999]]]){
    const bad={F:badF,C:[],n:2,proof:[{op:"src",source:0,clause:badF[0]}],root:0,cost:0};
    try{verifyOne(bad);}catch(err){count.malformedRejected++;continue;}throw Error("accepted malformed source");
  }
  vAssert(count.proofs===raw.counts.claims,"proof tally");
  vAssert(count.defs===raw.counts.defNodes&&count.res===raw.counts.resNodes,"node tally");
  vAssert(count.early===raw.counts.early,"early tally");
  vAssert(count.satSources===raw.counts.satSources&&count.unsatSources===raw.counts.unsatSources,"label tally");
  return count;
}
if(typeof module!=="undefined"&&module&&module.exports)module.exports={verifyOne,verifyAll};
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module){
  const path=require("path"),prod=require("./lspv2_358_dpll_implicate_producer.js");
  console.log(JSON.stringify(verifyAll(prod.main()),null,2));
}
