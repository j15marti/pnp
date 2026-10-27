// Self-contained Node.js LSPV-3 reproducibility audit. Run: node this_filename.js
function audit145(){
const c={};function test(v,k){c[k]=(c[k]||0)+1;if(!v)throw Error(k+" "+c[k]);}
function sat(F,n,y=-1,b=0){for(let a=0;a<2**n;a++){if(y>0&&+!!(a&(2**(y-1)))!==b)continue;let ok=true;for(const row of F){if(!row.some(l=>+!!(a&(2**(Math.abs(l)-1)))===+(l>0))){ok=false;break;}}if(ok)return true;}return false;}
function prop(F){return F.every(x=>x.length===3&&new Set(x.map(Math.abs)).size===3)&&new Set(F.map(x=>x.join(","))).size===F.length;}
function balance(F,n){return Array.from({length:n},(_,i)=>i+1).every(v=>F.filter(x=>x.includes(v)).length===2&&F.filter(x=>x.includes(-v)).length===2);}
function conn(F){let g=new Map();const add=(u,v)=>{if(!g.has(u))g.set(u,[]);g.get(u).push(v)};F.forEach((row,j)=>row.forEach(l=>{let a="c"+j,b="v"+Math.abs(l);add(a,b);add(b,a)}));let seen=new Set(["c0"]),todo=["c0"];for(let k=0;k<todo.length;k++)for(let t of g.get(todo[k])||[])if(!seen.has(t)){seen.add(t);todo.push(t)}return seen.size===g.size;}
function pin(y,u,v){return [[-y,u,v],[-y,u,-v],[-y,-u,v],[-y,-u,-v]];}
function compile(F,n){let y=n+1,G=[];F.forEach((row,j)=>{let t=n+2+j;G.push([y,row[0],t],[-t,row[1],row[2]])});return {G,P:pin(y,n+2+F.length,n+3+F.length),n:n+F.length+3,y};}
function xor(x,y,z,b){let F=[];for(let i=0;i<8;i++){let bits=[i&1,(i>>1)&1,(i>>2)&1];if(((bits[0]+bits[1]+bits[2])&1)!==b)F.push([x,y,z].map((v,j)=>bits[j]?-v:v))}return F;}
function quartets(F){let g=new Map();for(let row of F){let key=row.map(Math.abs).sort((a,b)=>a-b).join(",");if(!g.has(key))g.set(key,[]);g.get(key).push(row.join(","));}let out=[];for(let [key,rows] of g){if(rows.length!==4)continue;let ids=key.split(",").map(Number),s=new Set(rows);if([0,1].some(b=>xor(...ids,b).every(row=>s.has(row.join(",")))))out.push(key)}return out;}
let rows=[];for(let mask=0;mask<8;mask++)rows.push([1,2,3].map((v,i)=>(mask&(1<<i))?-v:v));
let valid=0,satcases=0,unsatcases=0;
for(let mask=1;mask<256;mask++){let F=rows.filter((_,i)=>mask&(1<<i)),o=compile(F,3),H=o.G.concat(o.P),label=sat(F,3);test(prop(H)&&conn(H)&&H.length===2*F.length+4,"compiled_proper_connected_size");test(sat(o.G,o.n,o.y,1),"all_projections_contain_one");test(sat(o.G,o.n,o.y,0)===label,"rank_zero_iff_F_SAT");test(sat(o.P,o.n,o.y,0)&&!sat(o.P,o.n,o.y,1),"pin_forces_zero");test(sat(H,o.n)===label,"joined_label_preserved");valid++;label?satcases++:unsatcases++;}
test(satcases===254&&unsatcases===1,"three_variable_cube_exact_labels");
const W=[[-1,3,-14],[2,-8,9],[10,-13,14],[3,7,-13],[-4,-9,-11],[5,8,-14],[4,-8,-11],[1,7,13],[1,-7,10],[-5,-6,-15],[-2,-6,12],[-4,9,-10],[-2,5,-12],[-3,6,-15],[6,-7,11],[2,-9,11],[4,8,-10],[-3,12,15],[-5,-12,15],[-1,13,14]];
test(prop(W)&&balance(W,15)&&conn(W)&&!sat(W,15),"W1_strict22_connected_UNSAT");
test(quartets(W).length===0,"W1_no_XOR3_source_quartet");
let counts=[];
for(let a=0;a<=1;a++)for(let b=0;b<=1;b++){let F=W.map(row=>row.slice());if(!a)for(let [i,j] of [[6,0],[11,0]])F[i][j]*=-1;if(!b)for(let [i,j] of [[9,2],[17,2]])F[i][j]*=-1;let count=0;for(let m=0;m<1<<15;m++)if(F.every(row=>row.some(l=>+!!(m&(1<<(Math.abs(l)-1)))===+(l>0))))count++;test(count===((a&&b)?0:(!a&&!b)?772:272)&&prop(F)&&balance(F,15)&&!quartets(F).length,"W1_signed_variants");counts.push([a,b,count]);}
for(let b=0;b<=1;b++){let Q=xor(1,2,3,b);test(prop(Q)&&balance(Q,3)&&quartets(Q).length===1&&sat(Q,3),"single_XOR_quartet_exact22_SAT");}
let A=xor(1,2,3,0),B=xor(4,5,6,1);
test(balance(A.concat(B),6)&&!conn(A.concat(B))&&quartets(A.concat(B)).length===2,"two_XOR_components");
let swaps=0;
for(let i=0;i<4;i++)for(let j=0;j<4;j++){let ia=A[i].findIndex(l=>l>0),ib=B[j].findIndex(l=>l>0);if(ia<0||ib<0)continue;let X=A.map(r=>r.slice()),Y=B.map(r=>r.slice());[X[i][ia],Y[j][ib]]=[Y[j][ib],X[i][ia]];let F=X.concat(Y);test(prop(F)&&balance(F,6)&&conn(F),"swapped_connected_exact22");test(!quartets(F).length&&sat(F,6),"swapped_no_quartet_SAT");swaps++;}
let edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
for(let odd=0;odd<2;odd++){let F=[];for(let v=0;v<4;v++)F.push(...xor(...edges.map((e,j)=>e.includes(v)?j+1:0).filter(Boolean),+(odd&&v===0)));test(prop(F)&&conn(F)&&quartets(F).length===4,"K4_Tseitin_four_quartets");test(Array.from({length:6},(_,i)=>i+1).every(v=>F.filter(r=>r.includes(v)).length===4&&F.filter(r=>r.includes(-v)).length===4),"K4_not_exact22");test(sat(F,6)===(odd===0),"K4_Tseitin_odd_parity");}
for(let mask of [1,255]){let F=rows.filter((_,i)=>mask&(1<<i)),o=compile(F,3),H=o.G.concat(o.P),n=o.n;for(let lev=1;lev<=2;lev++){H=H.concat(pin(o.y,n+1,n+2));n+=2;test(prop(H)&&conn(H)&&H.length===2*F.length+4+4*lev,"two_real_3CNF_descendants_expanding");if(mask===1)test(sat(H,n),"SAT_descendant_explicit_model");}}
return {run:"AFFINE_PROMISE_HARDNESS145",seed:"deterministic exhaustive",exhaustive_proper_3variable_sources:valid,SAT:satcases,UNSAT:unsatcases,connected_signed22_swaps:swaps,W1_model_counts:counts,checks:c,total_assertions:Object.values(c).reduce((a,b)=>a+b,0),failures:0,scope:"Only proper connected 3CNF hardness; signed exact22 isolated-XOR theorem and hostile controls; not a general SAT lower bound",status:{projection_affine_rank:"RESTRICTED_PROVED_PENDING_REVIEW",quartet_isolation:"RESTRICTED_PROVED_PENDING_REVIEW",all_UNSAT_coverage:"OPEN",ARC_EDGE_90:"OPEN",P_vs_NP:"OPEN"}};
}
console.log(JSON.stringify(audit145(),null,2));
