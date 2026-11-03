#!/usr/bin/env node
/* Independent no-import verifier for REFEREE307.  It deliberately reimplements
   truth tables, relaxed rules, source-tree DP, unicycle normal form, exact
   Resolution certificate checking, both-label controls, and strict parsing. */
"use strict";
const fs = require("fs"), crypto = require("crypto");
const N = 6;
const SOURCES = [[1,2],[3,4],[5,6],[-1,-3],[-1,-5],[-3,-5],[-2,-4],[-2,-6],[-4,-6]];
let assertions = 0;
function ok(x,m){ assertions++; if(!x) throw new Error(m||"assertion"); }
function canon(c){
  const s = new Set(c); if(s.has(0)) throw Error("zero");
  for(const x of s) if(s.has(-x)) throw Error("tautology");
  return [...s].sort((a,b)=>Math.abs(a)-Math.abs(b)||(a<0)-(b<0));
}
function clauseTT(c){ let t=0n; for(let a=0;a<(1<<N);a++){
  let sat=false; for(const l of c){ const b=!!(a&(1<<(Math.abs(l)-1))); if(b===(l>0)){sat=true;break;} }
  if(sat)t|=1n<<BigInt(a);
} return t; }
function affineTT(mask,rhs){ let t=0n; for(let a=0;a<(1<<N);a++){
  let x=a&mask,p=0; while(x){p^=1;x&=x-1;} if(p===rhs)t|=1n<<BigInt(a);
} return t; }
function support(t){ let s=0; for(let v=0;v<N;v++){ const bit=1<<v; for(let a=0;a<(1<<N);a++){
  if(a&bit)continue; if(Number((t>>BigInt(a))&1n)!==Number((t>>BigInt(a|bit))&1n)){s|=bit;break;}
}} return s; }
function pop(x){let n=0;while(x){n++;x&=x-1;}return n;}
const CLAUSE=new Map(), AFFINE=new Map();
function genStates(pos,arr){ if(pos===N){const c=[];for(let i=0;i<N;i++)if(arr[i])c.push(arr[i]>0?i+1:-(i+1));const t=clauseTT(c);if(!CLAUSE.has(t))CLAUSE.set(t,c);return;}
  for(const z of [-1,0,1]){arr[pos]=z;genStates(pos+1,arr);} }
genStates(0,Array(N).fill(0));
for(let m=0;m<(1<<N);m++)for(const r of [0,1]){const t=affineTT(m,r);if(!AFFINE.has(t))AFFINE.set(t,[m,r]);}
const LOCAL_SET=new Set();for(let sm=0;sm<(1<<N);sm++){if(pop(sm)>3)continue;const vs=[];for(let v=0;v<N;v++)if(sm&(1<<v))vs.push(v);for(let allow=0;allow<(1<<(1<<vs.length));allow++){let lift=0n;for(let a=0;a<(1<<N);a++){let p=0;for(let j=0;j<vs.length;j++)if(a&(1<<vs[j]))p|=1<<j;if(allow&(1<<p))lift|=1n<<BigInt(a);}LOCAL_SET.add(lift);}}
const LOCAL=[...LOCAL_SET], ALL=(1n<<64n)-1n;
const freeMemo=new Map();let freeHits=0,freeMisses=0;
function freeConverts(t){if(freeMemo.has(t)){freeHits++;return freeMemo.get(t);}freeMisses++;const sm=support(t);if(pop(sm)>3){const z=[t];freeMemo.set(t,z);return z;}
  const z=LOCAL.filter(g=>(t&(ALL^g))===0n);freeMemo.set(t,z);return z;}
const combineMemo=new Map(); let combineHits=0,combineMisses=0;
function combine(a,b){const key=a.toString()+":"+b.toString();if(combineMemo.has(key)){combineHits++;return combineMemo.get(key);}combineMisses++;
  const out=new Set(),ca=CLAUSE.get(a),cb=CLAUSE.get(b);
  if(ca&&cb) for(const l of ca)if(cb.includes(-l)){const raw=[...new Set([...ca,...cb].filter(x=>x!==l&&x!==-l))];let taut=false;for(const x of raw)if(raw.includes(-x))taut=true;if(!taut)out.add(clauseTT(canon(raw)));}
  const aa=AFFINE.get(a),ab=AFFINE.get(b); if(aa&&ab)out.add(affineTT(aa[0]^ab[0],aa[1]^ab[1]));
  const conj=a&b;if(pop(support(conj))<=3)out.add(conj);
  const ans=[...out];combineMemo.set(key,ans);return ans;
}
function models(cs){let n=0;for(let a=0;a<(1<<N);a++){let yes=true;for(const c of cs)if(((clauseTT(c)>>BigInt(a))&1n)===0n){yes=false;break;}if(yes)n++;}return n;}
function treeBank(atomTables){const k=atomTables.length,bank=Array.from({length:1<<k},()=>new Set());for(let i=0;i<k;i++)bank[1<<i].add(atomTables[i]);
  let tests=0,outs=0;for(let cnt=2;cnt<=k;cnt++)for(let whole=1;whole<(1<<k);whole++){if(pop(whole)!==cnt)continue;const least=whole&-whole;for(let left=(whole-1)&whole;left;left=(left-1)&whole){const right=whole^left;if(right&&(left&least))for(const a of bank[left])for(const b of bank[right]){tests++;const made=combine(a,b);outs+=made.length;for(const z of made)bank[whole].add(z);}}}
  return {bank,tests,outs};}
function oneUnaryTree(){const k=9,b0=Array.from({length:1<<k},()=>new Set()),b1=Array.from({length:1<<k},()=>new Set());for(let i=0;i<k;i++){b0[1<<i].add(atoms[i]);for(const z of freeConverts(atoms[i]))b1[1<<i].add(z);}let tests=0,outs=0;
  for(let cnt=2;cnt<=k;cnt++)for(let whole=1;whole<(1<<k);whole++){if(pop(whole)!==cnt)continue;const least=whole&-whole;for(let left=(whole-1)&whole;left;left=(left-1)&whole){const right=whole^left;if(!right||!(left&least))continue;
    for(const a of b0[left])for(const b of b0[right]){tests++;const made=combine(a,b);outs+=made.length;for(const z of made){b0[whole].add(z);for(const w of freeConverts(z))b1[whole].add(w);}}
    for(const [aa,bb] of [[b1[left],b0[right]],[b0[left],b1[right]]])for(const a of aa)for(const b of bb){tests++;const made=combine(a,b);outs+=made.length;for(const z of made)b1[whole].add(z);}
  }}return {contradiction_found:b1[(1<<k)-1].has(0n),pair_tests:tests,outputs:outs,terminal_functions:b1[(1<<k)-1].size};}
const atoms=SOURCES.map(clauseTT), trees=treeBank(atoms); const FULL=(1<<9)-1;
const extMemo=new Map();let extendCalls=0,extendHits=0;
function extend(shared,mask){const key=shared.toString()+":"+mask;if(extMemo.has(key)){extendHits++;return extMemo.get(key);}extendCalls++;
  const ts=[shared];for(let i=0;i<9;i++)if(mask&(1<<i))ts.push(atoms[i]);const ans=treeBank(ts).bank[(1<<ts.length)-1];extMemo.set(key,ans);return ans;}
let rootTests=0,rootOuts=0,found=false;
outer: for(let sm=1;sm<=FULL;sm++){const rest=FULL^sm;for(let tail=rest;;tail=(tail-1)&rest){const cycRest=rest^tail;for(let left=cycRest;;left=(left-1)&cycRest){const right=cycRest^left;if(left<=right)for(const sh of trees.bank[sm])for(const a of extend(sh,left))for(const b of extend(sh,right)){rootTests++;const made=combine(a,b);rootOuts+=made.length;for(const z of made)if(extend(z,tail).has(0n)){found=true;break outer;}}
      if(left===0)break;}if(tail===0)break;}}
const unary=oneUnaryTree();ok(!trees.bank[FULL].has(0n),"cost8 contradiction");ok(!found,"cost9 unicycle contradiction");ok(!unary.contradiction_found,"cost9 unary contradiction");ok(models(SOURCES)===0,"PHP UNSAT");
const del=SOURCES.map((_,i)=>models(SOURCES.filter((_,j)=>i!==j)));ok(del.every(x=>x>0),"deletion controls");
let flips=[];for(let i=0;i<9;i++)for(let j=0;j<2;j++){const z=SOURCES.map(c=>c.slice());z[i][j]*=-1;flips.push(models(z));}ok(flips.every(x=>x>0),"sign flips");
function resolve(a,b,p){if(!(a.includes(p)&&b.includes(-p))){if(a.includes(-p)&&b.includes(p))return resolve(b,a,p);throw Error("pivot");}return canon([...new Set([...a,...b].filter(x=>x!==p&&x!==-p))]);}
const steps=[[1,3,3],[2,4,5],[9,8,4],[11,10,6],[1,6,4],[2,7,6],[13,5,3],[15,14,5],[0,12,1],[17,16,2]];
let lines=SOURCES.map(canon);for(const [l,r,p] of steps){ok(l<lines.length&&r<lines.length,"index");lines.push(resolve(lines[l],lines[r],p));}ok(lines.at(-1).length===0,"upper certificate");
function parityCNF(rows,charges){const out=[];for(let i=0;i<rows.length;i++)for(let z=0;z<8;z++){if((pop(z)&1)!==charges[i]){const c=[];for(let j=0;j<3;j++)c.push((z&(1<<j))?-rows[i][j]:rows[i][j]);out.push(c);}}return out;}
const K4=[[1,2,3],[1,4,5],[2,4,6],[3,5,6]];ok(models(parityCNF(K4,[1,0,0,0]))===0,"odd K4");ok(models(parityCNF(K4,[0,0,0,0]))===8,"even K4");
function strictDimacs(s){const ls=s.split(/\n/);const h=ls[0].trim().split(/\s+/);if(h.length!==4||h[0]!=="p"||h[1]!=="cnf")throw Error("header");const n=+h[2],m=+h[3];if(n<0||m<0||ls.length!==m+1)throw Error("counts");for(const line of ls.slice(1)){const xs=line.trim().split(/\s+/).map(Number);if(!xs.length||xs.at(-1)!==0||xs.slice(0,-1).includes(0))throw Error("term");const c=xs.slice(0,-1);if(c.some(x=>Math.abs(x)<1||Math.abs(x)>n)||new Set(c).size!==c.length||c.some(x=>c.includes(-x)))throw Error("clause");}return true;}
const malformed=["","p cnd 1 1\n1 0","p cnf 1\n1 0","p cnf 1 2\n1 0","p cnf 1 1\n2 0","p cnf 1 1\n1","p cnf 1 1\n1 0 0","p cnf 1 1\n1 -1 0","p cnf 1 1\n1 1 0"];
let rejected=0;for(const s of malformed){try{strictDimacs(s)}catch{rejected++;}}ok(rejected===9,"malformed");
const rawPath=process.argv[2]||"results/raw/arc/2026-11-02_2348_LSPV5_PHP32_EXACT_MIXED_REFEREE307_raw.json";const raw=JSON.parse(fs.readFileSync(rawPath,"utf8"));
ok(raw.exact_cost===10,"raw cost");ok(raw.search.root_pair_tests===rootTests,"root tests");ok(raw.search.root_outputs===rootOuts,"root outputs");ok(raw.search.tree_pair_tests===trees.tests,"tree tests");ok(raw.search.tree_outputs===trees.outs,"tree outs");ok(raw.source.models===0,"raw label");ok(raw.malformed.rejected===9,"raw malformed");ok(raw.corrupted_certificates.rejected===3,"raw corruptions");
ok(raw.search.one_unary_tree.pair_tests===unary.pair_tests,"unary tests");ok(raw.search.one_unary_tree.outputs===unary.outputs,"unary outputs");ok(raw.search.one_unary_tree.terminal_functions===unary.terminal_functions,"unary terminals");
const report={run_id:"PHP32-EXACT-MIXED-REFEREE307-INDEPENDENT",status:"PASS",assertions,search:{tree_pair_tests:trees.tests,tree_outputs:trees.outs,tree_terminal_functions:trees.bank[FULL].size,tree_contains_false:false,one_unary_tree:unary,root_pair_tests:rootTests,root_outputs:rootOuts,extend_calls:extendCalls,extend_hits:extendHits,combine_misses:combineMisses,combine_hits:combineHits,free_convert_misses:freeMisses,free_convert_hits:freeHits,contradiction_found:false},controls:{php_models:0,deletion_model_counts:del,sign_flip_model_counts:flips,odd_K4_models:0,even_K4_models:8,malformed_rejected:rejected,upper_cost:steps.length},producer_payload_sha256:raw.payload_sha256,producer_file_sha256:crypto.createHash("sha256").update(fs.readFileSync(rawPath)).digest("hex")};
const out=process.argv[3]||"results/raw/arc/2026-11-02_2348_LSPV5_PHP32_EXACT_MIXED_REFEREE307_verify.json";fs.writeFileSync(out,JSON.stringify(report,null,2)+"\n");console.log(JSON.stringify(report,null,2));
