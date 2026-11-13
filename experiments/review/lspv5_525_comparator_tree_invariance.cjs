'use strict';
// LSPV-5/525 independent red-team audit of LSPV-4/584 weighted SOURCE-alias frontier.
// (1) Recomputes Q/S/J, the 167 conflicting clauses and 49-kink histogram DIRECTLY from the
//     archived /341 packet (no Tseitin regeneration, no GF(2) solver; witnesses read from packet).
// (2) Enumerates EVERY non-redundant comparison decision tree sorting 3 distinct keys and
//     recomputes the frontier per tree: the conflict set is a property of the chosen tree.
// (3) Free per-clause tree choice (the W_R "free optimal choice" principle) and a fixed
//     3-comparator network both give ZERO conflict.
// (4) Emits the min-S and lambda=1 joint endpoint packets and runs the UNCHANGED original
//     checker on them as separate OS processes.
// Usage: node experiments/review/lspv5_525_comparator_tree_invariance.cjs [--out FILE]
const fs=require('node:fs'),path=require('node:path'),os=require('node:os'),crypto=require('node:crypto');
const cp=require('node:child_process'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const checkerPath=path.join(root,'experiments/arc/lspv2_341_independent_verify.js');
const packetPath=path.join(root,'results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json');
const raw584Path=path.join(root,'results/raw/arc/2026-11-13_0436_LSPV4_584_WEIGHTED_SOURCE_ALIAS_FRONTIER_RAW.json');
const gitBlob=b=>crypto.createHash('sha1').update('blob '+b.length+'\0').update(b).digest('hex');
const C=fs.readFileSync(checkerPath),P=fs.readFileSync(packetPath);
assert.equal(gitBlob(C),'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0');
assert.equal(gitBlob(P),'fe27fe1011d0021e721ccaeb747ed58da65d7464');
const packet=JSON.parse(P);
let checks=0;const ok=(b,m)=>{checks++;assert(b,m);};

// ---- permutations and rank patterns
const PERMS=[[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]];
const rankKey=lits=>{const a=lits.map(Math.abs);return a.map(x=>a.filter(y=>y<x).length).join('');};
// ---- witness probes (short-circuit OR evaluation)
function probes(lits,bits){let n=0;for(const l of lits){n++;if(l>0?bits[l-1]===1:bits[-l-1]===0)return n;}return n;}
// ---- 584 insertion sort, re-implemented
function insertion(lits){const a=lits.map(Math.abs);let n=0;for(let i=1;i<3;i++){const x=a[i];let j=i-1;while(j>=0){n++;if(a[j]<=x)break;a[j+1]=a[j];j--;}a[j+1]=x;}return n;}
// ---- enumerate all non-redundant decision trees over rank patterns; tree => map pattern->depth
const ALLPAT=PERMS.map(p=>p.join(''));
function trees(set){
  if(set.length===1)return [{[set[0]]:0}];
  const out=[];
  for(const [i,j] of [[0,1],[0,2],[1,2]]){
    const L=set.filter(s=>s[i]<s[j]),R=set.filter(s=>s[i]>s[j]);
    if(!L.length||!R.length)continue;
    for(const a of trees(L))for(const b of trees(R)){const m={};for(const k in a)m[k]=a[k]+1;for(const k in b)m[k]=b[k]+1;out.push(m);}
  }
  return out;
}
const ALLT=trees(ALLPAT);
for(const t of ALLT){ok(Object.keys(t).length===6,'tree covers');ok(Object.values(t).every(d=>d===2||d===3),'depth 2/3');ok(Object.values(t).filter(d=>d===2).length===2,'two depth-2 leaves');}
const insTree={};for(const p of ALLPAT){const lits=p.split('').map(c=>Number(c)+1);insTree[p]=insertion(lits);}
const insIdx=ALLT.findIndex(t=>ALLPAT.every(p=>t[p]===insTree[p]));ok(insIdx>=0,'insertion sort is an enumerated tree');
const leafSets=[...new Set(ALLT.map(t=>ALLPAT.filter(p=>t[p]===2).sort().join('|')))].sort();

// ---- per-clause cost table from packet
const clauses=[];
for(const f of packet.fixtures){
  const ws=f.deleted.filter(d=>d.assignment!==null).map(d=>Array.from(d.assignment,Number));
  for(const c of f.clauses){
    ok(c.literals.length===3&&new Set(c.literals.map(Math.abs)).size===3,'distinct ternary');
    const opts=PERMS.map(p=>{const lits=p.map(i=>c.literals[i]);return {lits,q:ws.reduce((s,b)=>s+probes(lits,b),0),pat:rankKey(lits)};});
    clauses.push({fixture:f.graph.name,id:c.id,opts,wcount:ws.length});
  }
}
ok(clauses.length===328,'328 sources');
const nWit=packet.fixtures.reduce((n,f)=>n+f.deleted.filter(d=>d.assignment!==null).length,0);ok(nWit===324,'324 witnesses');
function frontier(depthOf){ // depthOf(clauseIndex, pattern) -> s
  let Q=0,S=0,J=0;const sav=[];const qArgminPats=[];
  clauses.forEach((c,ci)=>{const o=c.opts.map(x=>({q:x.q,s:depthOf(ci,x.pat)}));
    const qmin=Math.min(...o.map(x=>x.q)),smin=Math.min(...o.map(x=>x.s));
    const qAtS=Math.min(...o.filter(x=>x.s===smin).map(x=>x.q));
    Q+=qmin;S+=smin;J+=Math.min(...o.map(x=>x.q+x.s));
    // exact two-level structure check: lambda-frontier per clause = smin*l + qmin + min(l*(s'-smin), d)
    const sv=new Set(o.map(x=>x.s));if(sv.size===2){ok(Math.max(...sv)===smin+1,'unit step');}
    if(qAtS>qmin){sav.push(qAtS-qmin);qArgminPats.push(ci);}});
  const hist={};for(const d of sav)hist[d]=(hist[d]||0)+1;
  const gap=J-Q-S;
  ok(gap===sav.length,'exact lemma: lambda=1 nonadditivity gap equals the conflict count');
  return {Q,S,J,gap,conflicts:sav.length,conflictClauses:qArgminPats,sumSavings:sav.reduce((a,b)=>a+b,0),kinks:Object.keys(hist).length,hist};
}
// (1) insertion-sort frontier == 584
const ins=frontier((ci,p)=>insTree[p]);
const r584=JSON.parse(fs.readFileSync(raw584Path));
ok(ins.Q===29238&&ins.S===656&&ins.J===30061&&ins.conflicts===167&&ins.kinks===49&&ins.sumSavings===9462,'584 metrics reproduced');
ok(JSON.stringify(Object.fromEntries(Object.entries(ins.hist).map(([k,v])=>[k,v])))===JSON.stringify(Object.fromEntries(Object.entries(r584.histogram).map(([k,v])=>[k,v]))),'584 histogram identical');
// exact parametric formula at many lambdas (rational check at integer and half-integer lambda)
const val=(fr,l)=>fr.Q+fr.S*l+Object.entries(fr.hist).reduce((s,[d,m])=>s+m*Math.min(l,Number(d)),0);
for(let l2=0;l2<=480;l2++){const l=l2/2;const direct=clauses.reduce((s,c)=>s+Math.min(...c.opts.map(x=>x.q+l*insTree[x.pat])),0);ok(Math.abs(direct-val(ins,l))<1e-9,'formula at lambda '+l);}
// (2) every tree
const perTree=ALLT.map((t,ti)=>{const fr=frontier((ci,p)=>t[p]);return {tree:ti,depth2:ALLPAT.filter(p=>t[p]===2).sort(),Q:fr.Q,S:fr.S,J:fr.J,gapAtLambda1:fr.J-fr.Q-fr.S,conflicts:fr.conflicts,kinks:fr.kinks,sumSavings:fr.sumSavings};});
for(const r of perTree){ok(r.Q===29238&&r.S===656,'Q,S minima tree-invariant');}
// exact characterization: a clause conflicts under tree T iff NO q-minimizing order of that
// clause has a rank pattern among T's two depth-2 leaves.
ALLT.forEach((t,ti)=>{const d2=new Set(ALLPAT.filter(p=>t[p]===2));
  const predicted=[];clauses.forEach((c,ci)=>{const qmin=Math.min(...c.opts.map(x=>x.q));
    if(!c.opts.some(x=>x.q===qmin&&d2.has(x.pat)))predicted.push(ci);});
  const actual=frontier((ci,p)=>t[p]).conflictClauses;
  ok(JSON.stringify(predicted)===JSON.stringify(actual),'depth-2 leaf characterization, tree '+ti);});
const gaps=perTree.map(r=>r.gapAtLambda1),confl=perTree.map(r=>r.conflicts),sums=perTree.map(r=>r.sumSavings);
// (3a) free per-clause tree choice: put argmin-q order at depth 2
const free=frontier((ci,p)=>{const best=clauses[ci].opts.reduce((a,b)=>b.q<a.q?b:a);return p===best.pat?2:3;});
ok(free.conflicts===0&&free.J===29238+656,'free tree choice: zero conflict');
// every pattern is a depth-2 leaf of some tree (so the per-clause choice is legal within the tree family)
for(const p of ALLPAT)ok(ALLT.some(t=>t[p]===2),'pattern realizable at depth 2');
// (3b) fixed 3-comparator network
const net=frontier(()=>3);ok(net.conflicts===0&&net.J===29238+984,'network: zero conflict');
// (4) OS replay of endpoint packets with unchanged checker
function emit(choose){const pk=JSON.parse(JSON.stringify(packet));let k=0;let Q=0,S=0;
  for(const f of pk.fixtures)for(const c of f.clauses){const o=choose(clauses[k]);c.literals=o.lits;Q+=o.q;S+=insTree[o.pat];k++;}
  return {bytes:Buffer.from(JSON.stringify(pk,null,2)+'\n'),Q,S};}
const cmp=(a,b)=>a.lits.join(',').localeCompare(b.lits.join(','));
const minS=emit(c=>c.opts.filter(x=>insTree[x.pat]===2).sort((a,b)=>a.q-b.q||cmp(a,b))[0]);
const joint=emit(c=>[...c.opts].sort((a,b)=>(a.q+insTree[a.pat])-(b.q+insTree[b.pat])||a.q-b.q||cmp(a,b))[0]);
const minQ=emit(c=>[...c.opts].sort((a,b)=>a.q-b.q||insTree[a.pat]-insTree[b.pat]||cmp(a,b))[0]);
ok(minS.Q===38700&&minS.S===656,'min-S endpoint');ok(joint.Q+joint.S===30061,'lambda=1 joint');ok(minQ.Q===29238&&minQ.S===823,'min-Q endpoint (S-tiebroken)');
function run(bytes,label){const file=path.join(os.tmpdir(),'lspv5_525_'+process.pid+'_'+label+'.json');fs.writeFileSync(file,bytes);
  const r=cp.spawnSync(process.execPath,[checkerPath,file],{encoding:'utf8',maxBuffer:1<<26});fs.unlinkSync(file);
  return {accepted:r.status===0,checks:r.status===0?JSON.parse(r.stdout).checks:null,blob:gitBlob(bytes),bytes:bytes.length};}
const os1=run(P,'baseline'),os2=run(minS.bytes,'minS'),os3=run(joint.bytes,'joint'),os4=run(minQ.bytes,'minQ');
// hostile control: a cross-clause literal swap must be rejected
const bad=JSON.parse(P);const t0=bad.fixtures[0].clauses[0].literals[0];bad.fixtures[0].clauses[0].literals[0]=bad.fixtures[0].clauses[1].literals[0];bad.fixtures[0].clauses[1].literals[0]=t0;
const os5=run(Buffer.from(JSON.stringify(bad,null,2)+'\n'),'hostile');
for(const o of [os1,os2,os3,os4])ok(o.accepted&&o.checks===30714,'checker accepts');
ok(!os5.accepted,'hostile cross-clause swap rejected');
const result={schema:'LSPV5_525_COMPARATOR_TREE_INVARIANCE/v1',date:'2026-11-13 America/Los_Angeles',
 pins:{checker:'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0',packet:'fe27fe1011d0021e721ccaeb747ed58da65d7464',raw584blob:gitBlob(fs.readFileSync(raw584Path))},
 reproduced584:{Q:ins.Q,S:ins.S,J:ins.J,conflicts:ins.conflicts,kinks:ins.kinks,sumSavings:ins.sumSavings,lambdaGridPoints:481},
 trees:{count:ALLT.length,distinctDepth2LeafSets:leafSets.length,insertionSortTreeIndex:insIdx,
   gapAtLambda1:{min:Math.min(...gaps),max:Math.max(...gaps)},conflicts:{min:Math.min(...confl),max:Math.max(...confl)},sumSavings:{min:Math.min(...sums),max:Math.max(...sums)},perTree},
 freePerClauseTree:{J:free.J,conflicts:free.conflicts},fixedNetwork3:{J:net.J,S:net.S,conflicts:net.conflicts},
 osReplay:{baseline:os1,minS:{...os2,Q:minS.Q,S:minS.S},jointLambda1:{...os3,Q:joint.Q,S:joint.S},minQ:{...os4,Q:minQ.Q,S:minQ.S},hostileCrossClauseSwap:os5},
 checks,
 conclusion:'584 exact frontier reproduced from packet bytes; its 167-clause conflict and 49 kinks depend on the chosen comparison tree and vanish under free per-clause tree choice or a fixed network. Q,S minima are tree-invariant. S is not checker-authenticated.',
 open:['P2-D1','P2-C3','P2-B1','P2-B2','P2-B3'],P_versus_NP:'OPEN'};
const oi=process.argv.indexOf('--out');if(oi>=0)fs.writeFileSync(process.argv[oi+1],JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({status:'PASS',checks,trees:ALLT.length,leafSets:leafSets.length,gap:result.trees.gapAtLambda1,conflicts:result.trees.conflicts,free:result.freePerClauseTree,net:result.fixedNetwork3,os:[os1.accepted,os2.accepted,os3.accepted,os4.accepted,os5.accepted]}));
