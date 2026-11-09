#!/usr/bin/env node
/* Independent LSPV-5/456 red-team audit of the proposed LSPV-3/528
 * ER2-OWNER verifier. This is not the historical R_mix341 checker. */
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import {createRequire} from 'node:module';
import {fileURLToPath} from 'node:url';

const here=path.dirname(fileURLToPath(import.meta.url));
const arc=process.env.LSPV456_ARC || path.resolve(here,'../arc');
const require=createRequire(import.meta.url);
const peer=require(path.join(arc,'lspv3_528_dual_zero_source_reconvergence.cjs'));
const baseProducer=require(path.join(arc,'lspv3_526_core_zero_splice.cjs'));
const clone=x=>JSON.parse(JSON.stringify(x));
const norm=a=>[...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);
const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const sha=s=>crypto.createHash('sha256').update(s).digest('hex');

function expectedSources(){
  const out=[];
  for(let i=0;i<3;i++)for(let j=0;j<3;j++)for(let k=0;k<3;k++)
    if((i+j+k)%3!==0)out.push(norm([-1-i,-4-j,-7-k]));
  return out.concat([[1,2,3],[4,5,6],[7,8,9]]);
}

function strictVerify(q){
  assert.equal(q.model,'ER2-OWNER only, historical R_mix341 unverified');
  assert.equal(q.lines.length,459);assert.equal(q.defs.length,68);assert.equal(q.joins.length,3);
  const L=q.lines,G=q.defs,facetClaims=new Map(),counts={SOURCE:0,FACET:0,RES:0};
  for(let i=0;i<G.length;i++){
    const g=G[i];
    assert.equal(g.owner,i,`owner ${i}`);assert.equal(g.id,13+i,`DEF id ${i}`);
    for(const x of [g.a,g.b]){
      assert(Number.isSafeInteger(x)&&x!==0,`DEF input 0/noninteger owner ${i}`);
      assert(Math.abs(x)<g.id,`DEF freshness owner ${i}`);
    }
    assert.notEqual(Math.abs(g.a),Math.abs(g.b),`DEF repeated input owner ${i}`);
    assert(Array.isArray(g.facets)&&g.facets.length===3,`facet arity owner ${i}`);
    assert.equal(new Set(g.facets).size,3,`facet alias owner ${i}`);
    for(let k=0;k<3;k++){
      const f=g.facets[k];assert(Number.isSafeInteger(f)&&f>=0&&f<L.length,`facet id owner ${i}`);
      assert(!facetClaims.has(f),`facet multiply claimed ${f}`);facetClaims.set(f,{owner:i,k});
    }
  }
  const src=expectedSources();
  for(let i=0;i<L.length;i++){
    const n=L[i];assert.equal(n.id,i,`line id ${i}`);assert(n.kind in counts,`kind ${i}`);counts[n.kind]++;
    assert(Array.isArray(n.clause)&&n.clause.length>0,`empty clause ${i}`);
    for(const lit of n.clause)assert(Number.isSafeInteger(lit)&&lit!==0,`zero/noninteger literal line ${i}`);
    assert.equal(new Set(n.clause).size,n.clause.length,`duplicate literal line ${i}`);
    assert(!n.clause.some(x=>n.clause.includes(-x)),`tautology line ${i}`);
    assert(same(n.clause,norm(n.clause)),`noncanonical line ${i}`);
    if(n.kind==='SOURCE'){
      assert(i<21,`late source ${i}`);assert(same(n.clause,src[i]),`source position ${i}`);
    }else if(n.kind==='FACET'){
      const c=facetClaims.get(i);assert(c,`unclaimed facet ${i}`);assert.equal(n.owner,c.owner,`facet owner ${i}`);
      const g=G[c.owner],expect=[[-g.id,g.a],[-g.id,g.b],[g.id,-g.a,-g.b]][c.k];
      assert(same(n.clause,norm(expect)),`facet clause ${i}`);
    }else{
      assert(Number.isSafeInteger(n.left)&&Number.isSafeInteger(n.right)&&n.left>=0&&n.right>=0&&n.left<i&&n.right<i,`RES ancestry ${i}`);
      assert(Number.isSafeInteger(n.pivot)&&n.pivot>0,`RES pivot type ${i}`);
      const a=L[n.left].clause,b=L[n.right].clause;
      assert(a.includes(n.pivot)&&b.includes(-n.pivot),`RES orientation ${i}`);
      const expect=norm([...a.filter(x=>x!==n.pivot),...b.filter(x=>x!==-n.pivot)]);
      assert(same(n.clause,expect),`RES consequent ${i}`);
    }
  }
  assert.equal(facetClaims.size,204);assert.deepEqual(counts,{SOURCE:21,FACET:204,RES:234});
  for(const t of q.joins){
    assert.equal(t.input,10+t.k);assert(same(L[t.forward].clause,norm([-t.bit1,t.bit2])));assert(same(L[t.backward].clause,norm([-t.bit2,t.bit1])));
  }
  return {PASS:true,counts,defs:G.length,paid:G.length+counts.RES,records:L.length};
}

function peerResult(packet){
  try{return {accepted:true,result:peer.verify(packet)}}catch(e){return {accepted:false,error:String(e.message)}}
}
function strictResult(packet){
  try{return {accepted:true,result:strictVerify(packet)}}catch(e){return {accepted:false,error:String(e.message)}}
}

const base=peer.splice(baseProducer.build());
const basePeer=peerResult(clone(base)),baseStrict=strictResult(clone(base));
if(!basePeer.accepted||!baseStrict.accepted)throw new Error(`base replay failed: ${JSON.stringify({basePeer,baseStrict})}`);

// Accepted malformed witness A: owner 22 has only its L facet used by RES.
// The peer verifier permits literal 0 as the unused b input and in its R/B facets.
const zero=clone(base),zg=zero.defs[22];
assert.deepEqual(zg,{id:35,owner:22,a:-29,b:10,label:'term_1_0',facets:[174,175,176]});
zg.b=0;
zero.lines[zg.facets[1]].clause=norm([-zg.id,0]);
zero.lines[zg.facets[2]].clause=norm([zg.id,-zg.a,0]);

// Accepted malformed witness B: canonicality is tested with an equality that
// normalizes both operands, so a duplicate literal in a terminal RES survives.
const duplicate=clone(base),terminal=duplicate.joins.at(-1).backward;
duplicate.lines[terminal].clause.push(duplicate.lines[terminal].clause[0]);

// Accepted malformed witness C: the owner facet list is not closed to exactly
// its three FACET records; an unrelated RES line can be appended as an alias.
const alias=clone(base),aliasedLine=alias.joins[0].forward;
alias.defs[0].facets.push(aliasedLine);

const acceptedMalformed={
  zero_literal_def:{peer:peerResult(zero),strict:strictResult(zero),owner:22,changed_lines:[175,176]},
  duplicate_terminal_literal:{peer:peerResult(duplicate),strict:strictResult(duplicate),line:terminal},
  extra_owner_facet_alias:{peer:peerResult(alias),strict:strictResult(alias),owner:0,aliased_line:aliasedLine}
};
for(const x of Object.values(acceptedMalformed))assert(x.peer.accepted&&!x.strict.accepted);

// Controls that the peer checker does reject.
const rejected={};
function reject(name,mutate){const q=clone(base);mutate(q);const r=peerResult(q);assert(!r.accepted,name);rejected[name]=r.error}
reject('foreign_source',q=>q.lines[0].clause=[-999]);
reject('colliding_def_id',q=>q.defs[1].id=q.defs[0].id);
reject('bad_facet_owner',q=>q.lines[q.defs[0].facets[0]].owner=67);
reject('future_parent',q=>{const n=q.lines.find(x=>x.kind==='RES');n.left=n.id;});
reject('bad_pivot',q=>{const n=q.lines.find(x=>x.kind==='RES');n.pivot=999;});
reject('changed_join_output',q=>q.lines[q.joins[0].forward].clause=[1]);

const zeroBytes=JSON.stringify(zero);
const result={
  id:'LSPV5_456_ER2_OWNER_MALFORMED_ACCEPTANCE',
  timestamp_pst:'2026-11-09 02:15 PST',
  status:'FALSIFIED_CHECKER_COMPLETENESS_BASE_PACKET_SURVIVES',
  audited_node:'P2-L3-528',
  model:'published proposed ER2-OWNER JavaScript verifier, not historical R_mix341',
  dependency_mode:process.env.LSPV456_ARC?'ephemeral exact-content reconstruction with final-newline hash adaptation':'clean repository dependencies',
  base:{peer:basePeer,strict:baseStrict,paid:302,records:459},
  accepted_malformed:acceptedMalformed,
  peer_rejected_controls:rejected,
  exact_zero_literal_packet:{utf8_bytes:Buffer.byteLength(zeroBytes),sha256:sha(zeroBytes),packet:zero},
  classification:{
    logical_composition_lemma:'survives; the unmodified packet passes the strict verifier',
    computational_checker_claim:'narrowed; its negative controls do not establish malformed-packet rejection',
    historical_accepted_bytes:'still OPEN and not tested by this proposed checker',
    p_vs_np:'OPEN'
  },
  resource_ledger:{logical_nodes_added:0,peer_verifier_runs:10,strict_verifier_runs:4,construction_search:'deterministic mutation and exact replay',discovery_cost_excluded_from_W:true}
};

const out=process.argv[2]||'results/raw/arc/2026-11-09_0215_LSPV5_456_ER2_OWNER_MALFORMED_RAW.json';
fs.mkdirSync(path.dirname(out),{recursive:true});fs.writeFileSync(out,JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({status:result.status,base_paid:302,zero_packet_sha256:result.exact_zero_literal_packet.sha256,
  malformed:Object.fromEntries(Object.entries(acceptedMalformed).map(([k,v])=>[k,{peer:v.peer.accepted,strict:v.strict.accepted,error:v.strict.error}])),
  peer_rejected:Object.keys(rejected),out},null,2));
