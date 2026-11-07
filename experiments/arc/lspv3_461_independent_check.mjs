#!/usr/bin/env node
// LSPV-3/461 independent verifier, no producer imports; original-source sha, all SAT/UNSAT, typed binary RES, and hostile mutations.
import fs from 'node:fs';import crypto from 'node:crypto';import assert from 'node:assert/strict';
let checks=0;function check(x,msg='assertion failed'){checks++;assert.ok(x,msg)}
function sha(x){return crypto.createHash('sha256').update(x).digest('hex')}
function stream(seed){let c=0n, s=Buffer.alloc(4);s.writeUInt32BE(seed,0);return function(bound){let hi=(1n<<64n)/BigInt(bound)*BigInt(bound);while(true){let b=Buffer.alloc(8);b.writeBigUInt64BE(c++,0);let x=crypto.createHash('sha256').update(Buffer.concat([s,b])).digest().readBigUInt64BE(0);if(x<hi)return Number(x%BigInt(bound));}}}
function generate(n,seed,sat=false){let rnd=stream(seed),xs=[];let witness=0;for(let i=0;i<n;i++)if((i*13+seed)%7<3)witness|=(1<<i);while(xs.length<8*n){let ids=[];while(ids.length<3){let v=rnd(n)+1;if(!ids.includes(v))ids.push(v);}ids.sort((a,b)=>a-b);let mask=rnd(8);let c=ids.map((v,i)=>(mask&(1<<i))?-v:v);if(!sat||evalClause(c,witness))xs.push(c)}return [xs,witness];}
function evalClause(c,a){return c.some(l=>((a>> (Math.abs(l)-1))&1)===Number(l>0))}
function satWitness(clauses,n){for(let a=0;a<(1<<n);a++){if(clauses.every(c=>evalClause(c,a)))return a;}return null;}
function canonical(c){let set=new Set(c);if(c.some(x=>set.has(-x)))return null;return [...set].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);}
function dimacs(n,cs){return 'p cnf '+n+' '+cs.length+'\n'+cs.map(c=>c.join(' ')+' 0\n').join('')}
function strictParse(src){
 if(!src.endsWith('\n'))throw Error('missing final newline');
 const lines=src.trimEnd().split('\n');const head=/^p cnf ([1-9][0-9]*) ([1-9][0-9]*)$/.exec(lines[0]);if(!head)throw Error('bad header');
 const n=Number(head[1]),m=Number(head[2]);if(n>100000||m>100000||lines.length!==m+1)throw Error('bad length');
 const cs=[];for(let line of lines.slice(1)){
 const xs=line.split(' ');if(xs.length!==4||xs[3]!=='0')throw Error('bad clause fields');
 let c=xs.slice(0,3).map(z=>{if(!/^-?[1-9][0-9]*$/.test(z))throw Error('bad literal');return Number(z)});
 if(c.some(x=>Math.abs(x)>n)||new Set(c.map(Math.abs)).size!==3)throw Error('not proper3');cs.push(c);
 }return {n,m,cs};
}
function validate(d){
 check(d.test==='LSPV3_461');check(Number.isInteger(d.n)&&d.n>=3&&d.n<=18);check(Number.isInteger(d.seed));
 let n=d.n,[cs]=generate(n,d.seed);check(JSON.stringify(cs)===JSON.stringify(d.original_clauses),'source mismatch');
 let s=dimacs(n,cs);check(s===d.source_dimacs,'DIMACS mismatch');let parsed=strictParse(d.source_dimacs);check(parsed.n===n&&parsed.m===8*n&&JSON.stringify(parsed.cs)===JSON.stringify(cs));check(sha(s)===d.original_dimacs_sha256,'SHA mismatch');
 check(satWitness(cs,n)===null,'original must be UNSAT');
 let active=d.core_source_ids;check(active.length>0&&new Set(active).size===active.length&&active.every(i=>Number.isInteger(i)&&i>=0&&i<cs.length));
 let core=active.map(i=>cs[i]);check(satWitness(core,n)===null,'MUS core UNSAT');
 for(let i of active){let w=d.core_deletion_witnesses[String(i)],others=active.filter(j=>j!==i).map(j=>cs[j]);check(Number.isInteger(w)&&w>=0&&w<(1<<n),'malformed witness');check(others.every(c=>evalClause(c,w)),'invalid deletion witness');check(!evalClause(cs[i],w),'removed source not falsified');}
 let refs=new Map();cs.forEach((c,i)=>refs.set('s'+i,c));let seen=new Set();
 for(const node of d.resolution_dag){
   check(/^d\d+$/.test(node.id)&&!seen.has(node.id));seen.add(node.id);check(Number.isInteger(node.pivot)&&node.pivot>=1&&node.pivot<=n);
   check(refs.has(node.left)&&refs.has(node.right),'unknown or forward reference');let c=refs.get(node.left),e=refs.get(node.right),v=node.pivot;
   check(c.includes(v)&&e.includes(-v),'illegal oriented pivot');let out=canonical([...c.filter(x=>x!==v),...e.filter(x=>x!==-v)]);
   check(out!==null,'tautological resolution');check(JSON.stringify(out)===JSON.stringify(node.clause),'wrong resolvent');refs.set(node.id,out);
 }
 check(refs.has(d.root)&&refs.get(d.root).length===0,'root is not empty');check(d.resolution_inference_nodes===d.resolution_dag.length);
 check(d.source_count_lower_bound===active.length-1);check(d.resolution_dag.length>=active.length-1);
 let walk=new Set(),todo=[d.root],usedS=new Set(),nodeIndex=new Map(d.resolution_dag.map(x=>[x.id,x]));
 while(todo.length){let id=todo.pop();if(walk.has(id))continue;walk.add(id);if(id.startsWith('s')){usedS.add(Number(id.slice(1)));continue;}let node=nodeIndex.get(id);check(!!node,'unreachable node');todo.push(node.left,node.right);}
 check(usedS.size===active.length&&active.every(id=>usedS.has(id)),'missing essential source ancestry');
 check(walk.size===active.length+d.resolution_dag.length,'unpruned proof nodes');
 const sat=d.sat_control;let [sc,expected]=generate(n,sat.seed,true);check(JSON.stringify(sc)===JSON.stringify(sat.clauses),'SAT control source mismatch');check(sha(dimacs(n,sc))===sat.dimacs_sha256,'SAT hash mismatch');check(sat.witness_bits===expected);check(sc.every(c=>evalClause(c,sat.witness_bits)),'SAT control invalid');
 return {n,seed:d.seed,source_count:cs.length,core_count:active.length,paid_res_nodes:d.resolution_dag.length,proof_total_ancestor_nodes:walk.size,original_sha:d.original_dimacs_sha256};
}
let outputs=[];for(let file of process.argv.slice(2)){
let d=JSON.parse(fs.readFileSync(file,'utf8'));let base=checks;let info=validate(d);info.assertions=checks-base;outputs.push(info);
const invalid=[d.source_dimacs.replace(/^p cnf/, 'p fake'),d.source_dimacs.replace(/^p cnf (\d+) (\d+)/, (_,a,b)=>'p cnf '+a+' '+(Number(b)+1)),d.source_dimacs.replace(/ 0\n/, ' 0 0\n'),d.source_dimacs.slice(0,-2),d.source_dimacs.replace(/ 0\n/, ' 99999 0\n')];for(let bad of invalid){let rejected=false;try{strictParse(bad)}catch(e){rejected=true;}check(rejected,'malformed DIMACS accepted');}
const clone=()=>structuredClone(d);let mutations=[
 ['sha',(x)=>x.original_dimacs_sha256='0'.repeat(64)],
 ['source',(x)=>x.original_clauses[0][0]*=-1],
 ['witness',(x)=>x.core_deletion_witnesses[String(x.core_source_ids[0])]=-1],
 ['wrongpivot',(x)=>x.resolution_dag[0].pivot=0],
 ['brokenparent',(x)=>x.resolution_dag[0].left='s999999'],
 ['nonemptyroot',(x)=>x.root='s0'],
 ['satcontrol',(x)=>x.sat_control.witness_bits=0],
 ['invalidweight',(x)=>x.source_count_lower_bound=-1]
];for(const [name,fn] of mutations){let z=clone();fn(z);let bad=false;try{validate(z)}catch(e){bad=true;}check(bad,'hostile mutation not rejected '+name);}
}
console.log(JSON.stringify({status:'PASS',assertion_groups:checks,fixtures:outputs,mutations_rejected:outputs.length*8},null,2));
