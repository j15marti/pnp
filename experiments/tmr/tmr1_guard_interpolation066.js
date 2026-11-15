"use strict";
const audit=function audit(){
"use strict";
let checks=0;
function must(ok,label){checks++;if(!ok)throw Error("FAIL: "+label)}
function norm(c){const s=[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);must(s.every(x=>x!==0),"zero literal");must(s.every(x=>!s.includes(-x)),"tautological clause");return s}
function key(c){return norm(c).join(",")}
function resolve(a,b,p){must(a.includes(p)&&b.includes(-p),"pivot orientations");return norm([...a.filter(x=>x!==p),...b.filter(x=>x!==-p)])}
function verify(proof,axioms){
const allow=new Set(axioms.map(key));
for(let i=0;i<proof.length;i++){
const r=proof[i];must(JSON.stringify(r.c)===JSON.stringify(norm(r.c)),"canonical line");
if(r.ax){must(allow.has(key(r.c)),"authenticated source");continue}
must(r.parents&&r.parents.length===2&&r.parents.every(j=>j>=0&&j<i),"earlier parents");
const [j,k]=r.parents;must(key(resolve(proof[j].c,proof[k].c,r.pivot))===key(r.c),"legitimate resolution");
}
must(proof.length>0&&proof[proof.length-1].c.length===0,"terminal empty");
}
function base(n){
const pf=[];const m=1<<n;
for(let a=0;a<m;a++){const clause=[];for(let i=1;i<=n;i++)clause.push((a>>(i-1)&1)?-i:i);pf.push({c:norm(clause),ax:true})}
let active=Array.from({length:m},(_,i)=>i);
for(let p=n;p>=1;p--){
const half=1<<(p-1),next=[];
for(let t=0;t<half;t++){let j=active[t],k=active[t+half],c=resolve(pf[j].c,pf[k].c,p);next.push(pf.length);pf.push({c,parents:[j,k],pivot:p})}
active=next;
}
must(pf[active[0]].c.length===0,"base root");
return pf;
}
function lift(baseProof,n){
const z=n+1;
const out=baseProof.map(q=>q.ax?{c:norm([...q.c,z]),ax:true}:{c:norm([...q.c,z]),parents:q.parents.slice(),pivot:q.pivot});
const bidx=out.length;out.push({c:[-z],ax:true});
const ridx=baseProof.length-1;out.push({c:resolve(out[ridx].c,out[bidx].c,z),parents:[ridx,bidx],pivot:z});
return out;
}
function satisfies(clause,mask){return clause.some(l=>!!(mask>>(Math.abs(l)-1)&1)===(l>0))}
function sat(clauses,n){for(let mask=0;mask<(1<<n);mask++)if(clauses.every(c=>satisfies(c,mask)))return true;return false}
function interpolation(A,B,z){const good=[];for(let f=0;f<4;f++){
let ok=true;
for(let mask=0;mask<(1<<z);mask++){
const Iz=!!(f>>(mask>>(z-1)&1)&1);
if(A.every(c=>satisfies(c,mask))&&!Iz)ok=false;
if(B.every(c=>satisfies(c,mask))&&Iz)ok=false;
}
if(ok)good.push(f)
}return good}
function guard(F,z){return F.map(c=>norm([...c,z]))}
const cases=[];
for(const n of [2,3,4]){
const p=base(n);const F=p.filter(q=>q.ax).map(q=>q.c);const z=n+1,A=guard(F,z),B=[[-z]],lp=lift(p,n);
verify(p,F);verify(lp,[...A,...B]);
must(!sat(F,n),"base UNSAT");must(sat(A,z),"guard A SAT");must(sat(B,z),"side B SAT");must(!sat([...A,...B],z),"joint UNSAT");
const allowed=interpolation(A,B,z);must(allowed.length===1&&allowed[0]===2,"unique interpolant z");
must(lp.length===p.length+2,"source-inclusive proof +2");
must(lp.filter(x=>!x.ax).length===p.filter(x=>!x.ax).length+1,"resolution steps +1");
for(let j=0;j<p.length;j++)must(key(lp[j].c.filter(l=>Math.abs(l)!==z))===key(p[j].c),"restriction line");
const mangled=lp.map(q=>({...q,c:q.c.slice()}));mangled[mangled.length-1].pivot=1;
let rejected=false;try{verify(mangled,[...A,...B])}catch(e){rejected=true}must(rejected,"mutated derivation rejected");
cases.push({name:"all_signs_"+n,variables:n,base_width:n,base_sources:1<<n,base_resolution_steps:(1<<n)-1,guard_sources:(1<<n)+1,guard_resolution_steps:1<<n,base_proof_lines:p.length,guard_proof_lines:lp.length,interpolant_truth_table:"01",status:"finite control"});
}
const controls=[
{name:"contradictory_units",n:1,F:[[1],[-1]],want_unsat:true},
{name:"contradictory_horn",n:2,F:[[1,2],[-1],[-2]],want_unsat:true},
{name:"satisfiable_2sat",n:2,F:[[1,2]],want_unsat:false},
{name:"satisfiable_singleton",n:1,F:[[1]],want_unsat:false},
{name:"affine_inconsistent_units",n:2,F:[[1],[-1],[2]],want_unsat:true}
];
for(const v of controls){
const z=v.n+1,A=guard(v.F,z),B=[[-z]],u=sat(v.F,v.n);
must(u!==v.want_unsat,"control truth expected");
must(sat(A,z)&&sat(B,z),"both sides SAT");
must(sat([...A,...B],z)===u,"guard conjunction equals F sat");
const inter=interpolation(A,B,z);
if(!u)must(inter.length===1&&inter[0]===2,"unique z for UNSAT base");
if(u)must(inter.length===0,"no interpolant when joint SAT");
cases.push({name:v.name,base_unsat:!u,interpolants:inter.length,joint_unsat:!u});
}
function k4(){
const edges=[],at=Array.from({length:4},()=>[]);
for(let u=0;u<4;u++)for(let v=u+1;v<4;v++){const id=edges.length+1;edges.push([u,v]);at[u].push(id);at[v].push(id)}
const F=[];
for(let v=0;v<4;v++){for(let a=0;a<8;a++){const parity=((a&1)+((a>>1)&1)+((a>>2)&1))&1;const charge=v===0?1:0;if(parity!==charge)F.push(norm(at[v].map((x,j)=>(a>>j&1)?-x:x))) }}
return {F,edges};
}
const graph=k4();const z=7,A=guard(graph.F,z),B=[[-z]];
must(graph.F.length===16&&graph.edges.length===6,"authentic K4 odd charge source cardinality");
must(!sat(graph.F,6),"K4 odd XOR UNSAT");
must(sat(A,z)&&sat(B,z)&&!sat([...A,...B],z),"K4 guard sides");
must(JSON.stringify(interpolation(A,B,z))===JSON.stringify([2]),"K4 interpolant z");
cases.push({name:"odd_K4_Tseitin",sources:16,edge_variables:6,charge_parity:1,interpolant_truth_table:"01",status:"finite nonexpander control"});
return {experiment:"GUARD_INTERPOLANT_RESTRICTION066",timestamp_label:"2026-11-14 23:10 PST",checks,failures:0,cases,
theorem_scope:"For any UNSAT CNF F: A=and_{C in F}(z or C), B=not z. A,B individually SAT, unique Craig interpolant on z is z. Resolution complexity of A and B is between that of F and +2 lines; base F of width w yields guard width w+1. Published exponential source only for cubic expander Tseitin F, not finite tested K4.",
limitations:["No native finite-state Turing machine execution","Finite all-sign and K4 examples not expander hardness witnesses","Guarded hard family is 4-CNF plus unit, not asserted proper 3-CNF","No SAT-machine-to-Resolution transfer","No new P-versus-NP lower bound"]};
};
console.log(JSON.stringify(audit(),null,2));
