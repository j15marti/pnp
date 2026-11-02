'use strict';
// Independent compact logical-control/scheduling reproducer. Node >=18.
// The machine-space theorem is symbolic; this is NOT a native FLMV trace.
const assert=require('assert');
function clauses(src){
 let lines=src.trimEnd().split('\n');let h=lines.shift().trim().split(/\s+/);
 if(h.length!==4||h[0]!=='p'||h[1]!=='cnf'||!h.slice(2).every(s=>/^\d+$/.test(s)))throw Error('header');
 let n=+h[2],m=+h[3],arr=[],cur=[];
 if(n>14)throw Error('toy bound');
 for(let tok of lines.join(' ').trim().split(/\s+/)){
  if(tok===''){continue;}
  if(tok==='0'){arr.push(cur);cur=[];continue;}
  if(!/^-?[1-9]\d*$/.test(tok)||Math.abs(+tok)>n)throw Error('literal');cur.push(+tok);
 }
 if(arr.length!==m||cur.length)throw Error('length');return [n,arr];
}
function models(src){let [n,cc]=clauses(src),count=0;
 for(let a=0;a<2**n;a++)if(cc.every(c=>c.some(l=>((a>>(Math.abs(l)-1))&1)===(l>0?1:0))))count++;
 return count;
}
function k4(odd){let es=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],c=[];
 for(let v=0;v<4;v++){let incident=es.flatMap((e,i)=>e.includes(v)?[i+1]:[]);
 for(let a=0;a<8;a++)if(((a.toString(2).replace(/0/g,'').length)%2)!==(v===0&&odd?1:0))c.push(incident.map((e,k)=>(a>>k)&1?-e:e));}
 return 'p cnf 6 16\n'+c.map(x=>x.join(' ')+' 0\n').join('');
}
function schedule(gs,B){let state=gs.map(g=>({...g,used:0,stopped:false})),ops=0,sw=0;
 for(let r=0;r<45;r++){
  for(let g of state){if(g.stopped)continue;sw++;let limit=g.space>B?Math.min(g.steps,B+1):g.steps;
   let d=Math.min(2**r,limit-g.used);g.used+=d;ops+=d;
   if(g.used===limit){g.stopped=true;if(g.space<=B)return {label:g.label,ops,sw,indexCopies:2*B*sw};}
  }
  if(state.every(g=>g.stopped))return {label:'UNRESOLVED',ops,sw,indexCopies:2*B*sw};
 }
 throw Error('nontermination');
}
const sat='p cnf 1 1\n1 0\n',unsat='p cnf 1 2\n1 0\n-1 0\n';
assert.equal(models(sat),1);assert.equal(models(unsat),0);
assert.equal(models(k4(true)),0);assert.equal(models(k4(false)),8);
for(let s of ['p cnf 1 1\n2 0\n','p cnf 1 2\n1 0\n','p cnf 1 1\n1\n'])assert.throws(()=>clauses(s));
const high=[{name:'eager0',space:2000,steps:2400,label:'SAT'},{name:'eager1',space:3000,steps:3300,label:'SAT'}];
const cap=schedule(high,31);assert.equal(cap.label,'UNRESOLVED');
const full=schedule(high,4000);assert.equal(full.label,'SAT');
const mixed=schedule([{name:'stream',space:16,steps:73,label:'UNSAT'},...high.map(x=>({...x,label:'UNSAT'}))],31);
assert.equal(mixed.label,'UNSAT');
const N=1e6,B=1000,m=3,T=1e4;
const summary={run:'LSPV4_SPACE_CAPPED_PORTFOLIO344',scope:'abstract step/bit event controls, not native FLMV',k4_models:{odd:models(k4(true)),even:models(k4(false))},capouts:{high_only:cap.label,mixed:mixed.label},wide:full.label,budgets:{N,B,m,T,guestStepsUpper:2*m*T,indexCopyBitsUpper:2*m*B*(1+Math.ceil(Math.log2(T+1))),flatIndexCopyBits:2*m*B*T,guestBitsUpper:m*B}};
console.log(JSON.stringify(summary,null,2));
