'use strict';
// Independent verification; does not import producer's proof checker or optimizer.
const fs=require('fs');
function ckey(cl){return [...new Set(cl)].sort((a,b)=>a-b).join(':');}
function simplify(a,b,p){
  if(!a.includes(p)||!b.includes(-p))return null;
  const r=[...new Set([...a.filter(z=>z!==p),...b.filter(z=>z!==-p)])];
  if(r.some(x=>r.includes(-x)))return null;
  return r;
}
function modelCount(formula){const v=[...new Set(formula.flat().map(Math.abs))], vars=v.sort((a,b)=>a-b);let sum=0;
  for(let mask=0;mask<2**vars.length;mask++){
    const value=new Map(vars.map((x,i)=>[x,!!(mask&(1<<i))]));
    if(formula.every(cl=>cl.some(lit=>lit>0?value.get(lit):!value.get(-lit))))sum++;
  }
  return sum;
}
function replay(F,pi){const lines=F.map(c=>[...c]);if(F.some(c=>c.length===0))return pi.length===0;
  for(const d of pi){if(!Number.isInteger(d.i)||!Number.isInteger(d.j)||d.i<0||d.j<0||d.i>=lines.length||d.j>=lines.length||d.i===d.j)return false;
    const r=simplify(lines[d.i],lines[d.j],d.p);if(!r||ckey(r)!==ckey(d.out))return false;
    lines.push(r);
  }
  return pi.length>0&&lines.at(-1).length===0;
}
function lowerBoundCheck(F,budget){ // no Resolution DAG with at most budget derived nodes
  const memo=new Set();const seed=F.map(x=>[...x]);
  function walk(extra,left){const known=[...seed,...extra];
    if(known.some(c=>!c.length))return false;
    if(left===0)return true;
    const sig=extra.map(ckey).sort().join('|')+'#'+left;if(memo.has(sig))return true;memo.add(sig);
    for(let i=0;i<known.length;i++)for(let j=0;j<known.length;j++)if(i!==j){
      for(const lit of known[i])if(lit>0&&known[j].includes(-lit)){
        const r=simplify(known[i],known[j],lit);if(r&&!known.some(c=>ckey(c)===ckey(r))&&!walk([...extra,r],left-1))return false;
      }
    }
    return true;
  }
  return walk([],budget);
}
function run(raw){let checks=0, certified=[];
  for(const c of raw.cases){if(modelCount(c.source)!==c.models)throw Error('models mismatch '+c.name);checks++;
    if(c.minimum===null){if(c.models===0)throw Error('false SAT');checks++;}
    else {if(c.models!==0)throw Error('false UNSAT');checks++;
      if(!replay(c.source,c.proof)||c.proof.length!==c.minimum)throw Error('replay fail '+c.name);checks++;
      if(c.minimum>0&&!lowerBoundCheck(c.source,c.minimum-1))throw Error('shorter proof exists '+c.name);checks++;
    }
    certified.push({name:c.name,minimum:c.minimum,independent_model_count:c.models});
  }
  const contradictory=[[1],[-1]],valid=[{i:0,j:1,p:1,out:[]}];
  if(!replay(contradictory,valid))throw Error('valid proof rejected');checks++;
  for(const broken of [[{i:0,j:1,p:2,out:[]}],[{i:4,j:1,p:1,out:[]}],[{i:0,j:1,p:1,out:[1]}]]){
    if(replay(contradictory,broken))throw Error('corruption accepted');checks++;
  }
  function isValidSource(x){return Array.isArray(x)&&x.every(cl=>Array.isArray(cl)&&cl.every(l=>Number.isInteger(l)&&l!==0&&Math.abs(l)<=30));}
  for(const x of [null,{},[[0]],[[1.5]],'x']){if(isValidSource(x))throw Error('bad accepted');checks++;}
  if(raw.parity.odd_models!==0||raw.parity.even_models!==8)throw Error('parity control');checks+=2;
  return {id:'LSPV1_364_INDEPENDENT',pass:true,assertions:checks,certified,broken_rejected:3,malformed_rejected:5};
}
if(require.main===module)console.log(JSON.stringify(run(JSON.parse(fs.readFileSync(process.argv[2],'utf8'))),null,2));
module.exports={run};
