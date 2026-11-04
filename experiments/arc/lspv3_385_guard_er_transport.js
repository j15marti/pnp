"use strict";
// LSPV-3/385: typed ER guard transport finite fixture. Run: node this-file.js
const test=(ok,msg)=>{if(!ok)throw Error(msg);};
const norm=c=>[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
const eq=(a,b)=>JSON.stringify(norm(a))===JSON.stringify(norm(b));
const yes=(cl,as)=>cl.some(l=>as[Math.abs(l)]===(l>0));
function resolve(a,b,p){
  test(a.includes(p)&&b.includes(-p),"invalid signed pivot");
  let v=norm([...a.filter(x=>x!==p),...b.filter(x=>x!==-p)]);
  test(!v.some(x=>v.includes(-x)),"tautological inference excluded");
  return v;
}
function data(p,q){
 const S=[norm([p,q]),[-p],[-q]];
 const D=[norm([-p,3]),norm([-q,3]),norm([p,q,-3])];
 const ops=[["S0","D0",p],["R0","D1",q],["S1","D2",-p],["R2","S2",q],["R1","R3",3]];
 return {p,q,S,D,ops};
}
function replay(f,guard){
  const db={};f.S.forEach((c,i)=>db["S"+i]=guard?norm([-4,...c]):c);
  f.D.forEach((c,i)=>db["D"+i]=c);
  const rows=f.ops.map(([a,b,p],i)=>{
    test(db[a]&&db[b],"missing antecedent");
    const c=resolve(db[a],db[b],p);db["R"+i]=c;
    return {id:"R"+i,parent1:a,parent2:b,pivot:p,clause:c};
  });
  test(eq(db.R4,guard?[-4]:[]),"not a contradiction/guard unit");
  return rows;
}
function run(){
 let checks=0,corrupt=0,fixtures=[];
 for(let p of [1,-1])for(let q of [2,-2]){
  const f=data(p,q), P=replay(f,false),G=replay(f,true);
  for(let i=0;i<5;i++){test(eq(G[i].clause,[-4,...P[i].clause]),"transport mismatch");checks++;}
  for(let bits=0;bits<16;bits++){
   const a={1:!!(bits&1),2:!!(bits&2),3:!!(bits&4),4:!!(bits&8)};
   const def=f.D.every(c=>yes(c,a));
   const value=yes([p,q],a);
   test(def===(a[3]===value),"DEF truth table wrong");
   const sat=f.S.every(c=>yes(c,a));
   const guarded=f.S.every(c=>yes([-4,...c],a));
   test(!sat&&guarded===(!a[4]||sat),"guard semantic failure");checks+=2;
  }
  for(let i=0;i<3;i++){
   let witness=false;
   for(let x=0;x<4;x++){
    const a={1:!!(x&1),2:!!(x&2),3:false,4:true};
    if(f.S.filter((_,j)=>j!==i).every(c=>yes(c,a)))witness=true;
   }
   test(witness,"SAT deletion neighbor missing");checks++;
  }
  fixtures.push({p,q,sources:f.S,def_output:3,def_input:[p,q],
    paid_definition_clauses:f.D,plain_P:P,guarded_G:G,
    charged_definition_nodes:1,charged_resolution_nodes:5});
 }
 // The single guard bit becomes a RES pivot if DEF is allowed to depend on it.
 const tdep=[[-3,4],[-3,1],[3,-4,-1]];
 for(let t=0;t<2;t++)for(let x=0;x<2;x++){
   const a={1:!!x,4:!!t,3:!!(t&&x)};
   test(tdep.every(c=>yes(c,a)),"t-dependent DEF invalid");checks++;
 }
 test(eq(resolve([-4,1],[-3,4],-4),[1,-3]),"t-pivot failure");checks++;
 const invalid=[[[1],[2],1],[[1],[-2],2],[[1],[-1],2],
                [[1,2],[-1,-2],1],[[],[-1],1]];
 for(let [a,b,p] of invalid){try{resolve(a,b,p);}catch(e){corrupt++;}}
 test(corrupt===invalid.length,"bad pivot accepted");checks+=corrupt;
 return {status:"PASS",scope:"signed RES plus one paid t-free OR2 DEF; sample not global optimum",
        configurations:4, charged_nodes_per_fixture:6,
        assertions:checks,corrupted_inferences_rejected:corrupt,
        guarded_to_plain_step_by_step:true,t_dependent_def_blocks_guard_isometry:true,
        records:fixtures};
}
if(typeof module!=="undefined"&&require.main===module)
 console.log(JSON.stringify(run(),null,2));