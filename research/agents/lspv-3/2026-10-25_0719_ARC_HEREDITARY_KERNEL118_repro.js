"use strict";
// ARC-HEREDITARY-KERNEL118: executable Node/V8, no dependencies, deterministic.
// Logical byte traffic is NOT a physical FLMV primitive-operation trace.
const raw={run_id:"ARC-HEREDITARY-KERNEL118",seed:"none",assertions:0,partitions:0,root_masks:16,parent_join_cases:0,hereditary_join_cases:0,ordinary_encodings:0,ordinary_satisfiability_checks:0,ordinary_two_level_roots:0,first_children:0,grandchildren:0,sat_ordinary_formulas:0,unsat_ordinary_formulas:0,logical_bits_written:0,logical_bits_read:0,peak_single_encoded_child_bits:0,failures:0};
function ck(x,msg){raw.assertions++;if(!x){raw.failures++;throw Error(msg)}}
function pinMask(i,v){let m=0;for(let b=0;b<4;b++)if(((b>>i)&1)===v)m|=1<<b;return m}
function pc(m){let n=0;for(let b=0;b<4;b++)n+=(m>>b)&1;return n}
function fam(m){const a=[m];for(let x=0;x<2;x++){const c=m&pinMask(0,x);a.push(c);for(let y=0;y<2;y++)a.push(c&pinMask(1,y))}return a}
function parts(){let out=[];function visit(a,m){if(a.length===4){out.push(a.slice());return}for(let j=0;j<=m+1;j++){a.push(j);visit(a,Math.max(m,j));a.pop()}}visit([0],0);ck(out.length===15,"Bell(4)");return out}
function satFiber(m,h){for(let b=0;b<4;b++)for(let c=0;c<4;c++)if(h[b]===h[c]&&Boolean(m&(1<<b))!==Boolean(m&(1<<c)))return false;return true}
function join(p,q){return (p&q)!==0}
function coarse(p,q,h){for(let b=0;b<4;b++)if(p&(1<<b))for(let c=0;c<4;c++)if((q&(1<<c))&&h[b]===h[c])return true;return false}
function clone(f){return {maxvar:f.maxvar,clauses:f.clauses.map(c=>c.slice())}}
function clause(f,a){ck(a.length===3&&new Set(a.map(Math.abs)).size===3,"proper signed ternary clause");f.clauses.push(a.slice());f.maxvar=Math.max(f.maxvar,...a.map(Math.abs))}
function maskCNF(m,start=3){let f={maxvar:start-1,clauses:[]},next=start;for(let b=0;b<4;b++)if(!(m&(1<<b))){let l1=(b&1)?-1:1,l2=(b&2)?-2:2,z=next++;clause(f,[l1,l2,z]);clause(f,[l1,l2,-z])}let a=next++,b=next++,c=next++,d=next++;clause(f,[1,a,b]);clause(f,[2,c,d]);return f}
function pin(f,i,v){let lit=v===1?i+1:-(i+1),a=f.maxvar+1,b=f.maxvar+2;for(let x of [1,-1])for(let y of [1,-1])clause(f,[lit,x*a,y*b])}
function encode(f){let s="p cnf "+f.maxvar+" "+f.clauses.length+"\n";for(const c of f.clauses)s+=c.join(" ")+" 0\n";raw.ordinary_encodings++;raw.logical_bits_written+=8*s.length;return s}
function decode(s){const lines=s.trimEnd().split("\n");const h=/^p cnf ([1-9][0-9]*) ([0-9]+)$/.exec(lines[0]);if(!h)throw Error("bad header");const n=Number(h[1]),m=Number(h[2]);if(lines.length!==m+1)throw Error("bad clause count");const f={maxvar:n,clauses:[]};for(const line of lines.slice(1)){const a=line.split(" ");if(a.length!==4||a[3]!=="0")throw Error("bad clause row");const cl=a.slice(0,3).map(Number);if(cl.some(x=>!Number.isInteger(x)||x===0||Math.abs(x)>n)||new Set(cl.map(Math.abs)).size!==3)throw Error("improper clause");f.clauses.push(cl)}raw.logical_bits_read+=8*s.length;return f}
function feasibility(f,b){const ns=Array.from(new Set(f.clauses.flat().map(Math.abs))).filter(x=>x!==1&&x!==2);ck(ns.length<=20,"small exhaustive control");for(let bits=0;bits<(1<<ns.length);bits++){const a=new Map([[1,b&1],[2,(b>>1)&1]]);for(let i=0;i<ns.length;i++)a.set(ns[i],(bits>>i)&1);let ok=true;for(const cl of f.clauses){if(!cl.some(l=>l>0?a.get(l)===1:a.get(-l)===0)){ok=false;break}}if(ok)return true}return false}
function support(f){let m=0;for(let b=0;b<4;b++)if(feasibility(f,b))m|=1<<b;return m}
function joinsOrdinary(p,q){const f={maxvar:Math.max(p.maxvar,q.maxvar),clauses:p.clauses.concat(q.clauses)};return support(decode(encode(f)))!==0}
function suffix(word,start){let f={maxvar:start-1,clauses:[]};pin(f,0,word&1);pin(f,1,(word>>1)&1);return f}
const partitions=parts();raw.partitions=partitions.length;
for(let mask=0;mask<16;mask++){
 const D=fam(mask),signatures=[0,1,2,3].map(b=>D.map(d=>(d>>b)&1).join(""));
 const classes=new Set(signatures).size;
 ck(classes===pc(mask)+(mask!==15?1:0),"pin-tree signature count");
 for(const h of partitions){
  let pOK=true,allOK=true;
  for(let q=0;q<16;q++){const eq=join(mask,q)===coarse(mask,q,h);raw.parent_join_cases++;if(!eq)pOK=false;if(satFiber(mask,h))ck(eq,"single prefix saturated")}
  ck(pOK===satFiber(mask,h),"prefix universal-suffix criterion");
  const allSat=D.every(d=>satFiber(d,h));
  for(const d of D)for(let q=0;q<16;q++){const eq=join(d,q)===coarse(d,q,h);raw.hereditary_join_cases++;if(!eq)allOK=false;if(allSat)ck(eq,"descendant exactness")}
  ck(allOK===allSat,"hereditary quotient iff");
  if(allSat)for(let b=0;b<4;b++)for(let c=0;c<4;c++)if(h[b]===h[c])ck(signatures[b]===signatures[c],"classes refine signatures");
 }
 const r=maskCNF(mask),list=[r],expected=[mask];
 for(let x=0;x<2;x++){const c=clone(r);pin(c,0,x);list.push(c);expected.push(mask&pinMask(0,x));for(let y=0;y<2;y++){const g=clone(c);pin(g,1,y);list.push(g);expected.push(mask&pinMask(0,x)&pinMask(1,y))}}
 ck(list.length===7,"actual root/children/grandchildren");
 for(let i=0;i<list.length;i++){const s=encode(list[i]),f=decode(s),got=support(f);raw.ordinary_satisfiability_checks+=4;ck(got===expected[i],"ordinary real descendant support "+mask+" "+i);if(got)raw.sat_ordinary_formulas++;else raw.unsat_ordinary_formulas++;if(i>0)raw.peak_single_encoded_child_bits=Math.max(raw.peak_single_encoded_child_bits,8*s.length)}
 raw.ordinary_two_level_roots++;raw.first_children+=2;raw.grandchildren+=4;
}
const h=[0,1,0,1],r=maskCNF(15),c=clone(r);pin(c,0,0);const g=clone(c);pin(g,1,0);
ck(satFiber(support(r),h)&&satFiber(support(c),h)&&!satFiber(support(g),h),"inherited certificate fails on real second level");
raw.hostile_cases=[];
for(const [name,parent,word,expected,expected_coarse] of [["UNSAT_false_positive",g,2,false,true],["SAT_agreement",g,0,true,true],["UNSAT_other_fiber",g,1,false,false],["SAT_parent_valid",r,2,true,true],["SAT_first_child_valid",c,2,true,true]]){
 const q=suffix(word,g.maxvar+1),p=decode(encode(parent)),s=decode(encode(q));
 const exact=joinsOrdinary(p,s),relaxed=coarse(support(p),support(s),h);
 ck(exact===expected&&relaxed===expected_coarse,"real same-name gluing "+name);
 raw.hostile_cases.push({name,exact_sat:exact,coarse_sat:relaxed,parent_bits:8*encode(parent).length,suffix_bits:8*encode(q).length});
}
for(const [name,mask] of [["full_easy",15],["empty_unsat",0],["affine_equal",9],["Horn_implication",11],["singleton",1]]){const f=decode(encode(maskCNF(mask)));ck(support(f)===mask,"control "+name)}
try{decode("p cnf 5 99\n1 2 3 0\n");ck(false,"invalid header accepted")}catch(e){ck(/bad clause count/.test(String(e)),"reject malformed header")}
raw.status={restricted_theorem:"PROVED/EXACT",finite_experiments:"COMPUTATIONAL",arc_edge_90:"OPEN",p_vs_np:"OPEN"};
console.log(JSON.stringify(raw,null,2));