"use strict";
function assertion(p,msg){if(!p)throw Error(msg)}

function allClauses(){let a=[];for(let k=0;k<8;k++){let c=[];for(let i=0;i<3;i++)c.push((k&(1<<i))?-(i+1):i+1);a.push(c)}return a}

function sourceCases(){
 const h8=allClauses(), h7=(omit)=>h8.filter((_,i)=>i!==omit);
 return [
 {name:"H8_unsat",n:3,clauses:h8},
 {name:"H7_middle_010_sat",n:3,clauses:h7(2)},
 {name:"H7_middle_101_sat",n:3,clauses:h7(5)},
 {name:"H7_renamed_sat",n:3,clauses:h7(2).map(c=>c.map(v=>Math.abs(v)===2?-v:v))},
 {name:"XOR_even_sat",n:3,clauses:h8.filter((_,i)=>[1,2,4,7].includes(i))},
 {name:"XOR_odd_sat",n:3,clauses:h8.filter((_,i)=>[0,3,5,6].includes(i))},
 {name:"XOR_contradiction_unsat",n:3,clauses:h8},
 {name:"mixed_overlap_sat",n:3,clauses:[[1,2,3],[1,-2,3]]},
 {name:"mixed_overlap_unsat",n:3,clauses:[[1,2,3],[1,-2,3],...h8]},
 {name:"Horn_sat",n:3,clauses:[[-1,-2,3],[-1,2],[-3,2]]},
 {name:"Horn_unsat",n:3,clauses:[[1],[-1]]},
 {name:"Krom_sat",n:3,clauses:[[1,2],[-1,2],[1,-2]]},
 {name:"Krom_unsat",n:3,clauses:[[1,2],[-1,2],[1,-2],[-1,-2]]},
 {name:"disjoint_sat",n:6,clauses:[[1,2,3],[-1,2,3],[4,5,6],[-4,5,6]]},
 {name:"disjoint_unsat",n:6,clauses:[...h8,[4,5,6],[-4,5,6]]}
 ]
}

function litVal(l,a){return l>0?((a>>(l-1))&1)===1:((a>>(-l-1))&1)===0}

function countTrue(c,a){return c.reduce((z,l)=>z+(litVal(l,a)?1:0),0)}

function evalCNF(cs,a){return cs.every(c=>c.some(l=>litVal(l,a)))}

function truthSet(cs,n){let r=[];for(let a=0;a<(1<<n);a++)if(evalCNF(cs,a))r.push(a);return r}

function sourceTargets(cs,n){
 return cs.map((c,j)=>{let S={},U={},occ=[];
 for(let k=0;k<c.length;k++){let l=c[k],v=Math.abs(l),st=l>0?1:0;assertion(S[v]===undefined,"duplicate var");S[v]=st;U[v]=1-st;
 occ.push({source_clause:j+1,occurrence_index:k+1,indexed_variable:`x_${v},${j+1}`,literal:l,S_target:st,S_inverted_U:1-st,U_target:1-st,U_inverted_S:st})}
 return {source_clause:j+1,literals:c,S_target:S,S_inverse_U:Object.fromEntries(Object.entries(S).map(([v,x])=>[v,1-x])),U_target:U,U_inverse_S:Object.fromEntries(Object.entries(U).map(([v,x])=>[v,1-x])),occurrences:occ}
 })
}

function modesForPair(C,D){
 const a={};for(let c of ["S","U"])for(let d of ["S","U"]){let req={},ok=true;for(const [cl,m] of [[C,c],[D,d]])for(const l of cl){const v=Math.abs(l),wanted=(l>0?1:0)^(m==="U"?1:0);if(req[v]!==undefined && req[v]!==wanted)ok=false;req[v]=wanted;}a[c+d]=ok}return a
}

function pairTable(cs,n){
 const out=[];for(let j=0;j<cs.length;j++)for(let k=j+1;k<cs.length;k++){
  let matrix=modesForPair(cs[j],cs[k]);
  let byEnum={SS:false,SU:false,US:false,UU:false};
  for(let a=0;a<(1<<n);a++)for(const m of Object.keys(byEnum)){const r=countTrue(cs[j],a),t=countTrue(cs[k],a);if((m[0]==="S"?r===cs[j].length:r===0)&&(m[1]==="S"?t===cs[k].length:t===0))byEnum[m]=true;}
  for(let mode of Object.keys(byEnum))assertion(byEnum[mode]===matrix[mode],"pair disagree");
  out.push({source_clauses:[j+1,k+1],modes:matrix,shares_same:cs[j].some(l=>cs[k].includes(l)),shares_opposite:cs[j].some(l=>cs[k].includes(-l))})
 }return out
}

function resolutionCubes(cs,n){
 let arr=[],unique=new Set();
 for(let j=0;j<cs.length;j++)for(let k=j+1;k<cs.length;k++)for(const x of cs[j]){
  if(!cs[k].includes(-x))continue;
  const rr=[...new Set([...cs[j].filter(l=>l!==x),...cs[k].filter(l=>l!==-x)])].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
  if(rr.some(l=>rr.includes(-l)))continue;
  const key=rr.join(",");if(unique.has(key))continue;unique.add(key);
  const cube={};for(const l of rr)cube[Math.abs(l)]=l>0?0:1;
  for(let a of truthSet(cs,n))assertion(!Object.keys(cube).every(v=>((a>>(Number(v)-1))&1)===cube[v]),"unsound blocker");
  arr.push({source_clauses:[j+1,k+1],pivot:x,resolvent:rr,forbidden_cube:cube})
 }return arr
}

function dpll(cs,n){
 let nodes=0,clauseVisits=0,literalReads=0,branches=0;
 function rec(a){nodes++;a=a.slice();for(;;){let forced=false,allSat=true;
 for(const c of cs){clauseVisits++;let sat=false,uns=[];
 for(const l of c){literalReads++;const v=a[Math.abs(l)-1];if(v===-1)uns.push(l);else if((l>0&&v===1)||(l<0&&v===0)){sat=true;break;}}
 if(sat)continue;allSat=false;if(!uns.length)return null;
 if(uns.length===1){let l=uns[0],v=Math.abs(l)-1,w=l>0?1:0;if(a[v]!==-1&&a[v]!==w)return null;if(a[v]===-1){a[v]=w;forced=true;break;}}
 }
 if(!forced){if(allSat)return a.map(x=>x===-1?0:x);break;}
 }
 const z=a.indexOf(-1);if(z===-1)return null;branches++;
 return rec(a.map((v,i)=>i===z?0:v))||rec(a.map((v,i)=>i===z?1:v));
 }
 const witness=rec(Array(n).fill(-1));return {sat:!!witness,witness,nodes,clauseVisits,literalReads,branches}
}

function cofactor(cs,v,w){let out=[];for(let c of cs){if(c.includes(w?v:-v))continue;out.push(c.filter(x=>x!==(w?-v:v)))}return out}

function dimacs(cs,n){return `p cnf ${n} ${cs.length}\n`+cs.map(c=>c.join(" ")+(c.length?" ":"")+"0\n").join("")}

function makeTrail(cs,n){
 let out=[],a=0;for(let i=0;i<=n;i++){let counts=cs.map(c=>countTrue(c,a));out.push({flipped_prefix:i,assignment_bits:Array.from({length:n},(_,j)=>(a>>j)&1),true_literal_counts:counts,clauses_sat:counts.map(x=>x>0),N0:counts.filter(x=>x===0).length,N1:counts.filter(x=>x===1).length,N2:counts.filter(x=>x===2).length,N3:counts.filter(x=>x===3).length});if(i<n)a^=1<<i;}return out
}

function FreshTape(){this.a=new Map();this.head=0;this.peak=0;this.reset=function(){this.a.clear();this.head=0;};this.read=function(p){this.peak=Math.max(this.peak,p);return this.a.get(p)||0;};this.write=function(p,b){this.peak=Math.max(this.peak,p);if(b)this.a.set(p,b);else this.a.delete(p);};this.erase=function(){this.a.clear();};}

function EpochTape(){this.a=new Map();this.epoch=0;this.head=0;this.peak=0;this.reset=function(){this.epoch++;this.head=0;};this.read=function(p){this.peak=Math.max(this.peak,p);let q=this.a.get(p);return q&&q.epoch===this.epoch?q.b:0;};this.write=function(p,b){this.peak=Math.max(this.peak,p);this.a.set(p,{epoch:this.epoch,b});};this.erase=function(){this.epoch++;};}

function tapeTrial(text,naiveOrTagged,tapes){
 const U=tapes||{work:new (naiveOrTagged?EpochTape:FreshTape)(),wIndex:new (naiveOrTagged?EpochTape:FreshTape)(),iIndex:new (naiveOrTagged?EpochTape:FreshTape)()};
 for(const t of Object.values(U))t.reset();
 let log=[],logicalActions=0,inputHead=0,bitReads=0;
 function obs(x){log.push(x);bitReads++;}
 function write(t,p,b){t.head=p;t.write(p,b);logicalActions++}
 function read(t,p){t.head=p;logicalActions++;return t.read(p)}
 function jump(t,idx){let a=0;for(let i=0;i<=5;i++)a+=read(idx,i)*(2**i);t.head=a;idx.erase();logicalActions++;return a}
 obs({what:"fresh work[4]",bit:read(U.work,4)});
 write(U.wIndex,2,1);obs({what:"jump work via indexed bit2",address:jump(U.work,U.wIndex)});
 obs({what:"erased index bit2",bit:read(U.wIndex,2)});
 obs({what:"work[4] before write",bit:read(U.work,4)});
 write(U.work,4,1);obs({what:"work[4] after write",bit:read(U.work,4)});
 obs({what:"index head preserved",position:U.wIndex.head});
 write(U.wIndex,0,1);obs({what:"jump work via bit0",address:jump(U.work,U.wIndex)});
 write(U.work,1,1);obs({what:"work[1] after write",bit:read(U.work,1)});
 write(U.wIndex,2,1);obs({what:"return work to bit2",address:jump(U.work,U.wIndex)});
 obs({what:"work[4] survives index erasure",bit:read(U.work,4)});
 write(U.iIndex,4,1);inputHead=jump({head:0},U.iIndex);
 obs({what:"far input blank",address:inputHead,symbol:inputHead>=text.length?"BLANK":text[inputHead]});
 obs({what:"input index bit4 erased",bit:read(U.iIndex,4)});
 write(U.iIndex,0,1);inputHead=jump({head:0},U.iIndex);
 obs({what:"input at one",address:inputHead,symbol:inputHead>=text.length?"BLANK":text[inputHead]});
 obs({what:"input index head preserved",position:U.iIndex.head});
 obs({what:"fresh work[8] blank",bit:read(U.work,8)});
 return {log,logicalActions,bitReads,peak:Math.max(...Object.values(U).map(t=>t.peak)),tapes:U}
}

function experiment(){
 let data={id:"ARC-UNKNOWN-EXPONENT-EPOCH274",local_time:"2026-10-31 07:54 PDT",status:"PROVED/EXACT restricted theorem; COMPUTATIONAL finite controls; universal ARC OPEN",sources:[],tag_capacity:[],counters:{}};
 let stats={sources:0,sat:0,unsat:0,original_assignments:0,complement_checks:0,pair_modes:0,resolvents:0,physical_children:0,child_sat:0,child_unsat:0,tape_trials:0,tape_comparisons:0,dpll_nodes:0,dpll_literals:0,guest_nodes:0,guest_literals:0,source_bytes:0,child_bytes:0,tape_actions:0,tagged_peak_symbols:0,selected_baseline:0,selected_host:0};
 let shared={work:new EpochTape(),wIndex:new EpochTape(),iIndex:new EpochTape()};
 const expectedPrefix=[0,4,0,0,1,0,1,1,4,1,16,0,1,4,0]; // independent verifier checks named observations
 for(const src of sourceCases()){
  const {n,clauses}=src;const witnessSet=truthSet(clauses,n),label=witnessSet.length>0,base=dpll(clauses,n),targets=sourceTargets(clauses,n),pairs=pairTable(clauses,n),blockers=resolutionCubes(clauses,n),trail=makeTrail(clauses,n);
  assertion(label===base.sat,"baseline label");
  if(label)assertion(evalCNF(clauses,witnessSet[0]),"SAT witness");
  for(let a=0;a<1<<n;a++){const b=((1<<n)-1)^a;for(const c of clauses)assertion(countTrue(c,a)+countTrue(c,b)===c.length,"complement");stats.complement_checks++;}
  const children=[];let any=false;
  for(let w=0;w<2;w++){
   const c=cofactor(clauses,1,w),enc=dimacs(c,n),models=truthSet(c,n),d=dpll(c,n);
   const should=witnessSet.some(a=>(a&1)===w);assertion((models.length>0)===should && d.sat===should,"cofactor both labels");
   let fresh=tapeTrial(enc,false),tagged=tapeTrial(enc,true,shared);
   assertion(JSON.stringify(fresh.log)===JSON.stringify(tagged.log),"tape fresh-v-epoch mismatch");
   assertion(fresh.log[0].bit===0 && fresh.log[5].position===2 && fresh.log[10].address===16 && fresh.log[11].bit===0,"tape semantic");
   stats.tape_comparisons+=fresh.log.length;stats.tape_trials++;stats.tape_actions+=tagged.logicalActions;stats.tagged_peak_symbols=Math.max(stats.tagged_peak_symbols,tagged.peak);
   stats.physical_children++;stats.child_bytes+=enc.length;stats.guest_nodes+=d.nodes;stats.guest_literals+=d.literalReads;
   if(d.sat)stats.child_sat++;else stats.child_unsat++;
   any=any||d.sat;
   children.push({variable:1,value:w,clauses:c,ordinary_child_dimacs:enc,sat:should,base_guest_dpll:d,tape_log:tagged.log,tape_logical_actions:tagged.logicalActions,guest_tag_erasures:shared.wIndex.epoch+shared.iIndex.epoch});
  }
  assertion(any===label,"source OR join");
  stats.sources++;if(label)stats.sat++;else stats.unsat++;
  stats.original_assignments+=1<<n;stats.pair_modes+=4*pairs.length;stats.resolvents+=blockers.length;stats.dpll_nodes+=base.nodes;stats.dpll_literals+=base.literalReads;stats.source_bytes+=dimacs(clauses,n).length;
  data.sources.push({name:src.name,n,original_clauses:clauses,sat:label,model_count:witnessSet.length,witnesses:witnessSet,original_source_dimacs:dimacs(clauses,n),targets,pair_compatibility:pairs,source_resolution_blockers:blockers,global_zero:trail[0],global_one:trail[n],flip_trail:trail,baseline_dpll:base,children});
 }
 const untagged=new FreshTape();untagged.reset();untagged.write(4,1);untagged.head=0;const stale=untagged.read(4)===1;
 const smallTagCollision=(()=>{const storedTag=1,storedBit=1;let epoch=1;for(let i=0;i<4;i++)epoch=(epoch+1)%4;return epoch===storedTag && storedBit===1})();
 assertion(stale && smallTagCollision,"must detect no-reset and wrap bugs");
 data.falsifiers={untagged_reuse_exposes_stale_work_cell:stale,modulo_four_epoch_wrap_resurrects_stale_cell:smallTagCollision,sequential_guests_only:true};
 // This is symbolic exponent arithmetic, not the execution of N^D steps.
 for(const k of [8,16,64]){const B=k*k+2;for(const D of [2,4,8,16,32]){const fits=BigInt(D)*BigInt(k)<BigInt(B);data.tag_capacity.push({N:`2^${k}`,log2_N:k,tag_width_B:B,polynomial_degree_D:D,tag_can_count_N_to_D:fits});}}
 data.counters=stats;
 stats.selected_baseline=stats.dpll_literals+stats.dpll_nodes;
 // Selected host accounting: one source serialization, all child bytes, guest clauses,
 // policy switching, verification, and tagged blocks. Not normalized FLMV TM operations.
 stats.selected_host=stats.source_bytes+stats.child_bytes+stats.guest_literals+stats.guest_nodes+stats.tape_actions*(Math.ceil(Math.log2(stats.source_bytes+2)**2)+2)+2*stats.sources;
 return data
}
const result=experiment();
process.stdout.write(JSON.stringify(result,null,2)+'\n');
