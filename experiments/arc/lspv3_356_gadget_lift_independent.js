// LSPV-3 GADGET-LIFT356 independent no-import evaluator. Node.js >=16.
// Rebuilds AND2 canonical sources, gate definitions and local DP RES elimination.
"use strict";
const assert=require('assert');
function norm(v){let s=new Set(v);for(let x of s)if(s.has(-x))return null;return [...s].sort((x,y)=>Math.abs(x)-Math.abs(y)||(x-y));}
function key(c){return c.join(',')}
function edgesFor(label){if(label==='K4'){let e=[];for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)e.push([i,j]);return [4,e]}let r=Number(label.replace('PRISM',''));let edges=[];for(let i=0;i<r;i++)edges.push([i,(i+1)%r]);for(let i=0;i<r;i++)edges.push([i+r,(i+1)%r+r]);for(let i=0;i<r;i++)edges.push([i,i+r]);return [2*r,edges]}
function sat(c,mask){return c.some(x=>((mask>>(Math.abs(x)-1))&1)===(x>0?1:0))}
function fixture(label,odd){let [h,edges]=edgesFor(label),E=edges.length,inc=Array.from({length:h},()=>[]);edges.forEach(([a,b],i)=>{inc[a].push(i);inc[b].push(i)});assert(inc.every(v=>v.length===3));const a=e=>2*e+1,b=e=>2*e+2,p=e=>2*E+e+1;
 let defs=[];for(let e=0;e<E;e++)defs[e]=[norm([-p(e),a(e)]),norm([-p(e),b(e)]),norm([p(e),-a(e),-b(e)])];
 let sources=[],steps=[];
 for(let v=0;v<h;v++){
   let vars=inc[v].flatMap(e=>[a(e),b(e)]),charge=(odd&&v===0)?1:0, local=[];
   for(let mask=0;mask<64;mask++){
     const bits=vars.map((_,j)=>(mask>>j)&1),par=inc[v].reduce((acc,_,j)=>acc^(bits[2*j]&bits[2*j+1]),0);
     if(par===charge)continue;
     const clause=norm(vars.map((t,j)=>bits[j]?-t:t));sources.push(clause);local.push(clause);
   }
   let active=new Map();for(let c of local)active.set(key(c),c);
   for(let e of inc[v])for(let c of defs[e])active.set(key(c),c);
   let count=0;
   for(let e of inc[v])for(let pivot of [a(e),b(e)]){
     let P=[],M=[],next=new Map();for(let c of active.values())if(c.includes(pivot))P.push(c);else if(c.includes(-pivot))M.push(c);else next.set(key(c),c);
     for(let c of P)for(let d of M){let r=norm(c.filter(x=>x!==pivot).concat(d.filter(x=>x!==-pivot)));if(!r)continue;
       if(!steps.some(s=>s.v===v && key(s.clause)===key(r)) && !local.some(s=>key(s)===key(r)) && !inc[v].some(e=>defs[e].some(s=>key(s)===key(r)))) {steps.push({v,pivot,clause:r});count++}
       next.set(key(r),r)
     }
     active=next;
   }
   assert.strictEqual(active.size,4);
   for(let c of active.values()){
      assert(c.length===3 && c.every(x=>Math.abs(x)>2*E));
      let bad=inc[v].map(e=>c.includes(-p(e))?1:0);
      assert.strictEqual(bad[0]^bad[1]^bad[2],1^charge);
   }
 }
 return {graph:label,charge:odd?'odd':'even',h,E,sources:sources.length,resolution_nodes:steps.length,def_nodes:E,conditional_total:E+steps.length+4*h-1,source_clauses:sources};
}
const results=[];let controls=0;
for(let name of ['K4','PRISM3','PRISM4'])for(let odd of [true,false]){let f=fixture(name,odd);results.push({graph:f.graph,charge:f.charge,sources:f.sources,resolution_nodes:f.resolution_nodes,def_nodes:f.def_nodes,conditional_total:f.conditional_total});
   if(name==='K4'&&odd){const width=2*f.E,ss=f.source_clauses;let valid=0,sign=0;
      for(let i=0;i<ss.length;i++){let witness=-1;for(let a=0;a<(1<<width);a++)if(ss.every((c,j)=>i===j||sat(c,a))){witness=a;break}assert(witness>=0);assert(!sat(ss[i],witness));valid++;
      for(let x of ss[i]){let swapped=norm(ss[i].map(y=>y===x?-y:y));assert(sat(swapped,witness));sign++} }
      assert(valid===120&&sign===720);controls+=valid+sign;
   }
   if(!odd){assert(f.source_clauses.every(c=>sat(c,0)));controls++}
}
for(let bad of [[1,-1],[0,1],[null],['x']]){let n=bad.every(x=>Number.isInteger(x)&&x!==0)&&norm(bad)!==null;assert(!n);controls++}
// Strict independent DIMACS grammar, separate from logical witness tests.
function parseDimacs(src){
  let declared=null,clauses=[],current=[];
  for(const line0 of src.split(/\r?\n/)){
    const line=line0.trim();if(!line||line.startsWith('c '))continue;
    if(!declared){let m=/^p cnf (\d+) (\d+)$/.exec(line);assert(m,'invalid header');declared={n:Number(m[1]),m:Number(m[2])};continue;}
    const tokens=line.split(/\s+/);
    for(const x of tokens){assert(/^-?(0|[1-9]\d*)$/.test(x)&&x!=='-0','invalid literal');
      const l=Number(x);assert(Number.isSafeInteger(l),'big literal');
      if(l===0){clauses.push(current);current=[]}else{assert(Math.abs(l)<=declared.n,'out-of-bounds variable');current.push(l)}
    }
  }
  assert(declared,'header missing');assert(current.length===0,'unterminated clause');
  assert(clauses.length===declared.m,'clause count mismatch');return {n:declared.n,clauses};
}
const invalidDimacs=['1 0\n','p cnf 2 1\n1 0\n-1 0\n','p cnf 2 1\n1 2\n',
  'p cnf 1 1\n2 0\n','p cnf 2 1\nx 0\n','p cnf 2 1\np cnf 2 1\n1 0\n',
  'p cnf 2 0\n1 0\n','p cnf 2 1\n1 0\nbogus\n'];
for(const bad of invalidDimacs){assert.throws(()=>parseDimacs(bad));controls++}
assert.strictEqual(parseDimacs('p cnf 2 1\n0\n').clauses.length,1);
console.log(JSON.stringify({run:'GADGET-LIFT356/no-import-referee',controls,results},null,2));
