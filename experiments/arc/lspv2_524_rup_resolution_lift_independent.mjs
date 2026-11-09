#!/usr/bin/env node
// LSPV-2/524 independent Node.js replay. Restricted RUP only, no RAT/ER/XOR.
import { createHash } from 'node:crypto';
let tests=0;
function check(cond,msg='failed') { ++tests; if(!cond) throw new Error(msg); }
function norm(xs) {
  const y=[...new Set(xs.map(Number))].sort((a,b)=>Math.abs(a)-Math.abs(b)||b-a);
  if(y.some(x=>x===0||y.includes(-x))) throw new Error('invalid/tautological clause');
  return y;
}
function dimacs(n,cs) {
  return 'p cnf '+n+' '+cs.length+'\n'+cs.map(c=>c.join(' ')+(c.length?' ':'')+'0\n').join('');
}
function parse(s) {
  if(!s) throw new Error('empty source');
  const ls=s.trimEnd().split('\n'), h=ls[0].split(' ');
  if(h.length!==4||h[0]!=='p'||h[1]!=='cnf'||!/^\d+$/.test(h[2])||!/^\d+$/.test(h[3]))throw new Error('bad header');
  const n=+h[2],m=+h[3];
  if(n<1||m<1||ls.length!==m+1)throw new Error('bad dimensions');
  const clauses=ls.slice(1).map(line=>{
    const toks=line.trim().split(/\s+/);
    if(toks.pop()!=='0'||toks.some(tok=>!/^-[1-9]\d*$|^[1-9]\d*$/.test(tok)))throw new Error('bad tokens');
    const c=norm(toks.map(Number));
    if(c.some(x=>Math.abs(x)>n))throw new Error('out-of-range literal');
    return c;
  });
  return {n,clauses,sha256:createHash('sha256').update(s).digest('hex')};
}
function resolve(a,b,p) {
  check(a.includes(p)&&b.includes(-p),'bad oriented pivot');
  return norm([...a.filter(x=>x!==p),...b.filter(x=>x!==-p)]);
}
function key(c){return c.join(',');}
function rup(db,goal,n) {
  const assumptions=norm(goal);
  if(assumptions.some(x=>Math.abs(x)>n))throw new Error('bad proof literal');
  const assign=new Map(),prop=[], scans={clauses:0,literals:0};
  for(const x of assumptions)assign.set(Math.abs(x),-x);
  for(;;) {
    let progress=false;
    for(let j=0;j<db.length;j++) {
      const c=db[j];scans.clauses++;
      let good=false,unknown=[];
      for(const l of c) {
        scans.literals++;
        if(assign.get(Math.abs(l))===l){good=true;break;}
        if(!assign.has(Math.abs(l)))unknown.push(l);
      }
      if(good)continue;
      if(unknown.length===0)return {conflict:j,prop,scans};
      if(unknown.length===1){
        const x=unknown[0]; assign.set(Math.abs(x),x);
        prop.push({lit:x,reason:j});
        progress=true;break;
      }
    }
    if(!progress)return null;
  }
}
function dp(n,source) {
  let active=source.slice(), db=source.slice(), known=new Set(source.map(key)),proof=[];
  for(let p=1;p<=n;p++) {
    const pos=active.filter(c=>c.includes(p)), neg=active.filter(c=>c.includes(-p));
    const next=active.filter(c=>!c.includes(p)&&!c.includes(-p)),nextSeen=new Set(next.map(key));
    for(const a of pos)for(const b of neg) {
      let c;try{c=resolve(a,b,p);}catch(e){if(e.message.includes('tautological'))continue;throw e;}
      const k=key(c);
      if(!known.has(k)){
        check(rup(db,c,n)!==null,'DP derivation lacks RUP witness');
        proof.push(c);db.push(c);known.add(k);
      }
      if(!nextSeen.has(k)){next.push(c);nextSeen.add(k);}
    }
    active=next;
    if(known.has(''))break;
  }
  check(known.has(''),'DP missed empty');
  return proof;
}
function compile(n,source,proof) {
  if(!proof.length||proof[proof.length-1].length)throw new Error('not refutation');
  let db=source.slice();
  const nodes=db.map((c,i)=>({op:'source',clause:c,source:i})),ids=db.map((c,i)=>i);
  let scans=0,literalChecks=0,units=0,resCount=0,weakCount=0;
  for(const goal0 of proof) {
    const goal=norm(goal0);const run=rup(db,goal,n);
    if(!run)throw new Error('invalid RUP step');
    scans+=run.scans.clauses;literalChecks+=run.scans.literals;units+=run.prop.length;
    let id=ids[run.conflict],cur=db[run.conflict];
    for(let j=run.prop.length-1;j>=0;j--) {
      const {lit,reason}=run.prop[j];
      if(!cur.includes(-lit))continue;
      const next=resolve(db[reason],cur,lit);
      nodes.push({op:'res',left:ids[reason],right:id,pivot:lit,clause:next});
      id=nodes.length-1;cur=next;resCount++;
    }
    check(cur.every(x=>goal.includes(x)),'bad learned subsumption');
    if(key(cur)!==key(goal)){
      nodes.push({op:'weak',parent:id,clause:goal});
      id=nodes.length-1;weakCount++;
    }
    ids.push(id);db.push(goal);
  }
  const pure=[],mapped=new Map();
  let pureRes=0;
  for(let i=0;i<nodes.length;i++){
    const x=nodes[i];
    if(x.op==='source'){mapped.set(i,pure.length);pure.push({op:'source',source:x.source,clause:x.clause});continue;}
    if(x.op==='weak'){mapped.set(i,mapped.get(x.parent));continue;}
    const leftId=mapped.get(x.left),rightId=mapped.get(x.right);
    const a=pure[leftId].clause,b=pure[rightId].clause,p=x.pivot;
    let id;
    if(a.includes(p)&&b.includes(-p)){
      pure.push({op:'res',left:leftId,right:rightId,pivot:p,clause:resolve(a,b,p)});
      id=pure.length-1;pureRes++;
    } else {id=a.includes(p)?rightId:leftId;}
    mapped.set(i,id);
    check(pure[id].clause.every(l=>x.clause.includes(l)),'strengthening induction');
  }
  for(let i=0;i<pure.length;i++){
    const x=pure[i];
    if(x.op==='source'){check(key(x.clause)===key(source[x.source]),'source corruption');continue;}
    check(x.left<i&&x.right<i,'bad DAG order');
    check(key(resolve(pure[x.left].clause,pure[x.right].clause,x.pivot))===key(x.clause),'RES corruption');
  }
  check(pure[mapped.get(ids[ids.length-1])].clause.length===0,'no pure-RES empty goal');
  check(pureRes<=resCount&&resCount<=n*proof.length,'bound violated');
  return {rup_records:proof.length,res_nodes:resCount,pure_res_nodes:pureRes,
    weakenings:weakCount,source_clause_scans_plus_learned:scans,
    literal_tests:literalChecks,rup_assignment_steps:units,
    rup_log_bits_ascii:8*proof.map(c=>c.join(' ')+(c.length?' ':'')+'0\n').join('').length,
    max_database_clauses:db.length,terminal_pure_node:mapped.get(ids[ids.length-1]),
    upper_bound:(n+1)*proof.length};
}
function horn(n) {return [[1],...Array.from({length:n-1},(_,i)=>[-(i+1),i+2]),[-n]];}
function k4(charge) {
  const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]], cs=[];
  for(let v=0;v<4;v++){
    const inc=edges.map((e,j)=>e.includes(v)?j+1:0).filter(Boolean);
    for(let q=0;q<8;q++){
      const bits=[(q>>2)&1,(q>>1)&1,q&1];
      if(((bits[0]^bits[1]^bits[2])!==(v===0?charge:0)))
        cs.push(inc.map((e,j)=>bits[j]?-e:e));
    }
  }
  return cs;
}
function sat(n,cs) {
  for(let m=0;m<2**n;m++)
    if(cs.every(c=>c.some(l=>l>0?!!(m&(1<<(l-1))):!(m&(1<<(-l-1))))))
      return true;
  return false;
}
const results=[],controls={};
for(let n=1;n<=12;n++) {
  const p=parse(dimacs(n,horn(n)));
  check(!sat(n,p.clauses),'Horn UNSAT');
  const r=compile(n,p.clauses,[[]]);
  check(r.rup_records===1&&r.res_nodes===n,'Horn exact');
  results.push({family:'Horn',n,source_sha256:p.sha256,...r});
}
for(const odd of [0,1]) {
  const p=parse(dimacs(6,k4(odd)));
  check(sat(6,p.clauses)===(odd===0),'K4 classification');
  check(rup(p.clauses,[],6)===null,'K4 empty RUP must fail initially');
  if(odd===1){
    const proof=dp(6,p.clauses);
    results.push({family:'K4-Tseitin-odd',n:4,source_sha256:p.sha256,...compile(6,p.clauses,proof)});
  } else controls.sat_k4_reject_empty=1;
}
const satSrc=parse(dimacs(3,[[1],[-1,2],[-2,3]]));
check(sat(3,satSrc.clauses),'SAT control');
check(rup(satSrc.clauses,[],3)===null,'invalid empty RUP on SAT');
const h=parse(dimacs(3,horn(3)));
const nontrivial=compile(3,h.clauses,[[2,3],[]]);
check(nontrivial.weakenings===1,'missing weakening witness');
controls.weakening_eliminated=1;
const badSources=['','p cnf 2 1\n1 0\n2 0\n','p cnf 2 1\n3 0\n',
  'p cnf 2 1\n1 -1 0\n','p cnf 2 1\n1\n','p cnf -2 1\n1 0\n',
  'p cnf 2 1\n1 1\n'];
controls.malformed_rejections=0;
for(const s of badSources) {
  try{parse(s);}catch(e){controls.malformed_rejections++;continue;}
  throw new Error('accepted malformed source '+JSON.stringify(s));
}
controls.corrupt_proof_rejections=0;
for(const goal of [[4],[-1],[]]){
  try{compile(3,satSrc.clauses,[goal]);}catch(e){controls.corrupt_proof_rejections++;continue;}
  throw new Error('accepted bogus proof');
}
const del=horn(4).slice(0,-1);
check(sat(4,del)&&rup(del,[],4)===null,'deleted-source false proof');
controls.deleted_source_rejection=1;
console.log(JSON.stringify({run:'LSPV-2/524',checks:tests,controls,results,
    scope:'SOURCE-AUTHENTICATED RUP-only with no added variables, RAT, GF(2), ER or semantic oracle'},null,2));
