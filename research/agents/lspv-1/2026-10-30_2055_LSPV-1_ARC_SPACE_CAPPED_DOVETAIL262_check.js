/* ARC_SPACE_CAPPED_DOVETAIL262 independent ground-truth checker.
   Standard JavaScript, node >=16; does not import Python producer.
   Checks source labels, coherent complementary assignments, occurrence
   S/U targets, pair/triple extrema and source resolution forbidden cubes.
   Event timings are retained as measured producer values, not remeasured.
*/
'use strict';
function assign(n) {
  let a=[];
  for(let k=0;k<(1<<n);k++) a.push(Array.from({length:n},(_,i)=>(k>>i)&1));
  return a;
}
function val(x,a){let b=a[Math.abs(x)-1];return x>0?b:1-b;}
function t(c,a){return c.reduce((s,x)=>s+val(x,a),0);}
function sat(F,a){return F.every(c=>t(c,a)>0);}
function parity(p) {
  return assign(3).filter(a=>a.reduce((s,x)=>s+x,0)%2===p)
                  .map(a=>a.map((b,i)=>b?i+1:-(i+1)));
}
let eight=assign(3).map(a=>a.map((b,i)=>b?i+1:-(i+1)));
const controls=[
 ['seven_sat',eight.slice(0,7),3,true,31,124,16],
 ['eight_unsat',eight,3,false,99,480,22],
 ['xor_even_sat',parity(0),3,true,19,112,16],
 ['xor_both_unsat',parity(0).concat(parity(1)),3,false,99,480,22],
 ['xor_renamed_sat',parity(0).map(c=>c.map(x=>[1,3].includes(Math.abs(x))?-x:x)),3,true,19,112,16],
 ['horn_sat',[[-1,-2,3],[1],[2]],3,true,21,114,16],
 ['horn_unsat',[[-1,-2,3],[1],[2],[-3]],3,false,25,118,16],
 ['2sat_sat',[[1,2],[-1,2]],2,true,9,54,13],
 ['2sat_unsat',[[1,2],[-1,2],[-2]],2,false,21,75,14],
 ['scoped_guard_sat',[[1,2],[1,-2]],2,true,14,59,13],
 ['dense_3cnf_sat',[[1,2,3],[-1,2,3],[1,-2,3],[1,2,-3]],3,true,32,155,17],
 ['dense_3cnf_unsat',eight,3,false,99,480,22]
];
function target(c,sign){let obj={};for(let x of c)obj[Math.abs(x)]=Number((x>0)=== (sign==='S'));return obj;}
function compatible(a,b){return Object.keys(a).every(k=>!(k in b)||a[k]===b[k]);}
function ext(c,a,mode){return t(c,a)===(mode==='S'?c.length:0);}
function claim(x,msg){if(!x)throw Error(msg);}
let stats={cases:0,SAT:0,UNSAT:0,assignments:0,pairs:0,triples:0,blockers:0,trials:0};
for(let [name,F,n,truth,base,portfolio,trials] of controls){
  let A=assign(n), M=A.filter(a=>sat(F,a));
  claim((M.length>0)===truth,name+' SAT label');
  stats[truth?'SAT':'UNSAT']++;stats.cases++;stats.assignments+=A.length;
  stats.trials+=trials;
  for(let c of F) for(let a of A) {
    let b=a.map(x=>1-x);
    claim(t(c,a)+t(c,b)===c.length,name+' complement');
  }
  if(F.every(c=>c.length===3)){
    for(let c of F){
      for(let mode of ['S','U']){
        let tar=target(c,mode), co=Object.assign(new Array(n).fill(0),Object.keys(tar).reduce((o,k)=>{o[k-1]=tar[k];return o;},{}));
        claim(ext(c,co,mode),name+' occurrence target');
      }
    }
    for(let j=0;j<F.length;j++)for(let k=j+1;k<F.length;k++){
      for(let m1 of ['S','U'])for(let m2 of ['S','U']){
        let cp=compatible(target(F[j],m1),target(F[k],m2));
        let enumeration=A.some(a=>ext(F[j],a,m1)&&ext(F[k],a,m2));
        claim(cp===enumeration,name+' pair '+j+','+k+','+m1+m2);
        stats.pairs++;
      }
      for(let x of F[j])if(F[k].includes(-x)){
        let C=new Set([...F[j].filter(y=>y!==x),...F[k].filter(y=>y!==-x)]);
        if([...C].some(y=>C.has(-y)))continue;
        claim(M.every(a=>[...C].some(y=>val(y,a))),name+' source-derived resolution blocker');
        stats.blockers++;
      }
    }
    for(let i=0;i<F.length;i++)for(let j=i+1;j<F.length;j++)for(let k=j+1;k<F.length;k++){
      for(let z=0;z<8;z++){
        let modes=[0,1,2].map(h=>(z>>h)&1?'U':'S'), ids=[i,j,k];
        let feasible=ids.every((u,h)=>ids.every((v,l)=>h>=l||compatible(target(F[u],modes[h]),target(F[v],modes[l]))));
        let actual=A.some(a=>ids.every((v,h)=>ext(F[v],a,modes[h])));
        claim(feasible===actual,name+' triple '+i+','+j+','+k);
        stats.triples++;
      }
    }
  }
  claim(portfolio<12*Math.max(1,base),name+' abstract budget');
}
claim(sat([[1,2],[1,-2]],[1,0]),'source SAT');
claim(!sat([[1,2],[1,-2]],[0,0]),'source restricted NO');
for(let [k,v] of Object.entries({cases:12,SAT:7,UNSAT:5,assignments:84,pairs:492,triples:1720,blockers:48,trials:203}))
  claim(stats[k]===v, 'mismatch '+k+' '+stats[k]+' != '+v);
if(typeof console!=='undefined')console.log(JSON.stringify({run:'ARC_SPACE_CAPPED_DOVETAIL262',pass:true,stats}));
