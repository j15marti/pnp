#!/usr/bin/env node
'use strict';
/* LSPV-2/585: two-premise entailment theorem regression and unchanged /386 CLI.
 * REFERENCE SEM2/WEAKEN rules below are NOT historical R_mix341 rules.
 * Execute from evidence root: node lspv2_585_sem2_replay.cjs [case-directory]
 */
const fs=require('fs'),cp=require('child_process'),os=require('os'),path=require('path');
const crypto=require('crypto'),assert=require('assert/strict');
const SHA=x=>crypto.createHash('sha256').update(x).digest('hex');
const base='results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json';
const cnf='results/raw/arc/574_k01_SIGNED_SOURCE.cnf';
const checker='experiments/arc/lspv2_386_independent_verify.js';
const seedRaw=fs.readFileSync(base),sourceRaw=fs.readFileSync(cnf),checkRaw=fs.readFileSync(checker),seed=JSON.parse(seedRaw);
assert.equal(SHA(checkRaw),'22d12f665fecede1a047ea20c0c2d3f245c7195ce5df44f342891198ea04a113');
assert.equal(SHA(seedRaw),'0d8b1894f91d00c554727a92fed35b2bb58f2b1602f2a3cfcb949effda43ceb0');
assert.equal(SHA(sourceRaw),'3b94f215568099b24756872b0391db550092fb24ef6e67f05ee024bf9330f35c');
const signedSource=sourceRaw.toString('utf8').trim().split('\n').slice(1).map(s=>s.trim().split(' ').map(Number).slice(0,-1));
const orig=seed.records.filter(r=>r.kind==='SOURCE').map(r=>r.c);
assert.equal(signedSource.length,17);assert.deepEqual(signedSource,orig);
const ordered=a=>[...a].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);
const subset=(a,b)=>a.every(x=>b.includes(x));
function cl(n){const out=[];for(let k=0;k<3**n;k++){let a=[],t=k;for(let v=1;v<=n;v++){const s=t%3;t=Math.floor(t/3);if(s)a.push(s===1?v:-v);}out.push(a);}return out;}
function mask(C,n){let x=0n;for(let a=0;a<2**n;a++)if(C.some(l=>Boolean(a&(1<<(Math.abs(l)-1)))===(l>0)))x|=1n<<BigInt(a);return x;}
function witness(A,B,C){for(const p of A)if(B.includes(-p)){
 const R=ordered([...new Set(A.filter(x=>x!==p).concat(B.filter(x=>x!==-p)))]);
 if(!R.some(x=>R.includes(-x))&&subset(R,C))return {pivot:p,resolvent:R};
}return null;}
function criterion(A,B,C){return subset(A,C)||subset(B,C)||!!witness(A,B,C);}
function exact(A,B,C,a,b,c){return (a&b&~c)===0n;}
const all4=cl(4),mask4=all4.map(C=>mask(C,4));
let checks4=0,entailed4=0,nontrivial4=0;
for(let i=0;i<81;i++)for(let j=0;j<81;j++)for(let k=0;k<81;k++){
 const truth=exact(all4[i],all4[j],all4[k],mask4[i],mask4[j],mask4[k]);
 assert.equal(criterion(all4[i],all4[j],all4[k]),truth,'n4 witness '+i+'/'+j+'/'+k);
 checks4++;if(truth){entailed4++;if(!subset(all4[i],all4[k])&&!subset(all4[j],all4[k]))nontrivial4++;}
}
const all7=cl(7),mask7=all7.map(C=>mask(C,7)),sourceMask=orig.map(C=>mask(C,7));
let pairs=0,checks7=0,entailed7=0,nontrivial7=0,emptyImplied=0;
for(let i=0;i<orig.length;i++)for(let j=i+1;j<orig.length;j++){
 pairs++;if((sourceMask[i]&sourceMask[j])===0n)emptyImplied++;
 for(let k=0;k<all7.length;k++){
  const truth=exact(orig[i],orig[j],all7[k],sourceMask[i],sourceMask[j],mask7[k]);
  assert.equal(criterion(orig[i],orig[j],all7[k]),truth,'source witness '+i+'/'+j+'/'+k);
  checks7++;if(truth){entailed7++;if(!subset(orig[i],all7[k])&&!subset(orig[j],all7[k]))nontrivial7++;}
 }
}
assert.equal(pairs,136);assert.equal(emptyImplied,0);
const outdir=process.argv[2]||null;if(outdir)fs.mkdirSync(outdir,{recursive:true});
function run(name,P,expected){const b=Buffer.from(JSON.stringify(P)+'\n'),dir=fs.mkdtempSync(path.join(os.tmpdir(),'pnp585-'));
 const f=path.join(dir,'packet.json');fs.writeFileSync(f,b);
 const x=cp.spawnSync(process.execPath,[checker,f],{encoding:'utf8',timeout:12000});
 fs.rmSync(dir,{recursive:true,force:true});assert.equal(x.status===0,expected,name);
 if(outdir)fs.writeFileSync(path.join(outdir,name+'.json'),b);
 const found=(x.stderr||'').match(/Error: ([^\n]+)/);let native=null;
 if(x.status===0){native=JSON.parse(x.stdout);delete native.file;}
 return {name,accepted:x.status===0,bytes:b.length,sha256:SHA(b),native,error:found?found[1]:null};
}
const packets=[run('baseline_W29',seed,true)];
function append(name,r,recognized){const P=structuredClone(seed),last=P.records.pop();P.records.push(r,last);
 P.summary.live_records++;
 if(recognized){P.summary.resolution++;P.summary.paid_total++;}
 packets.push(run(name,P,recognized));}
const a=orig[0],b=orig[4],R=witness(a,b,[2,3,4,5,-7]);
assert(R);assert.deepEqual(R.resolvent,[2,3,4,5,-7]);
append('native_paid_RES_W30',{kind:'RES',c:R.resolvent,parents:[0,4],pivot:R.pivot},true);
append('valid_semantic_WEAKEN_rejected',{kind:'WEAKEN',c:ordered([...a,4]),parents:[0]},false);
append('valid_semantic_SEM2_rejected',{kind:'SEM2',c:R.resolvent,parents:[0,4]},false);
assert(!exact(a,orig[16],[-7],sourceMask[0],sourceMask[16],mask([-7],7)));
append('invalid_semantic_SEM2_rejected',{kind:'SEM2',c:[-7],parents:[0,16]},false);
const result={run:'LSPV-2/585',source_sha256:SHA(sourceRaw),checker_sha256:SHA(checkRaw),seed_sha256:SHA(seedRaw),n4:{clauses:81,triples:checks4,entailed:entailed4,nontrivial_resolution_weakening:nontrivial4},guarded_K4:{source_clauses:17,pairs,clauses:2187,triples:checks7,entailed:entailed7,nontrivial_resolution_weakening:nontrivial7,one_step_empty_entailments:emptyImplied},positive_witness:{parents:[a,b],pivot:R.pivot,resolvent:R.resolvent},native_packets:packets,scope:'Two-clause semantic consequence normal form is a mathematical theorem, NOT a historical mixed-rule authorization. The /386 sibling checker supports SOURCE/DEF/RES only. P2-D1/P2-C3/B1/B3 OPEN; P versus NP OPEN.'};
console.log(JSON.stringify(result,null,2));
