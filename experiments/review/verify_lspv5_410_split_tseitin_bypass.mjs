#!/usr/bin/env node
// Independent replay for LSPV-5/410. Not the historical R_mix341 checker.
import fs from 'node:fs';
import crypto from 'node:crypto';

const rawPath='results/raw/review/2026-11-07_0551_LSPV5_SPLIT_TSEITIN410.json';
const bytes=fs.readFileSync(rawPath), d=JSON.parse(bytes);
let checks=0;
const ok=(x,m)=>{checks++;if(!x)throw new Error(m);};

function graphFixtures(){
  const k4=[]; for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)k4.push([i,j]);
  const k33=[]; for(let i=0;i<3;i++)for(let j=3;j<6;j++)k33.push([i,j]);
  const cube=[]; for(let v=0;v<8;v++)for(const b of [1,2,4])if(v<(v^b))cube.push([v,v^b]);
  const p=[]; for(let i=0;i<5;i++){p.push([i,(i+1)%5]);p.push([5+i,5+(i+2)%5]);p.push([i,5+i]);}
  return {K4:[4,k4],'K3,3':[6,k33],cube:[8,cube],Petersen:[10,p]};
}

function pop(x){let n=0;while(x){n+=x&1;x>>=1;}return n;}
function tseitin(nv,edges,odd){
  const inc=Array.from({length:nv},()=>[]);
  edges.forEach(([u,v],i)=>{inc[u].push(i+1);inc[v].push(i+1);});
  ok(inc.every(x=>x.length===3),'cubic');
  const cs=[];
  inc.forEach((es0,v)=>{const es=[...es0].sort((a,b)=>a-b), charge=odd&&v===0?1:0;
    for(let bits=0;bits<8;bits++)if((pop(bits)&1)!==charge)
      cs.push(es.map((e,i)=>((bits>>i)&1)?-e:e));
  });
  return cs;
}
function split(base,n){
  const cs=[], pairs=[];
  base.forEach((c,i)=>{const a=n+i+1,p=[c[0],c[1],a],q=[c[0],c[2],-a];cs.push(p,q);pairs.push({target:c,aux:a,p,q});});
  return [cs,pairs];
}
function resolve(p,q,a){
  if(!p.includes(a)||!q.includes(-a))return null;
  const out=[];
  for(const l of [...p,...q]){if(Math.abs(l)===a)continue;if(out.includes(-l))return null;if(!out.includes(l))out.push(l);}
  return out;
}
function litTrue(l,a,aux){const v=Math.abs(l),bit=aux.has(v)?aux.get(v):((a>>(v-1))&1);return Boolean(bit)===(l>0);}
function clauseTrue(c,a,aux=new Map()){return c.some(l=>litTrue(l,a,aux));}
function sourceBytes(cs){const n=Math.max(...cs.flat().map(Math.abs));return `p cnf ${n} ${cs.length}\n`+cs.map(c=>`${c.join(' ')} 0\n`).join('');}
function support(c){return c.map(Math.abs).sort((a,b)=>a-b).join(',');}
function auxFor(pair,a,aux){for(const bit of [0,1]){aux.set(pair.aux,bit);if(clauseTrue(pair.p,a,aux)&&clauseTrue(pair.q,a,aux))return bit;}aux.delete(pair.aux);return null;}

// Exhaustive local projection under all target signs.
for(let signs=0;signs<8;signs++){
  const c=[1,2,3].map((v,i)=>((signs>>i)&1)?-v:v),p=[c[0],c[1],4],q=[c[0],c[2],-4];
  ok(JSON.stringify(resolve(p,q,4))===JSON.stringify(c),'local resolvent');
  for(let a=0;a<8;a++){
    const target=clauseTrue(c,a), ext=[0,1].some(bit=>{const m=new Map([[4,bit]]);return clauseTrue(p,a,m)&&clauseTrue(q,a,m);});
    ok(target===ext,'local projection');
  }
}

ok(d.run==='LSPV-5/410','run');
ok(d.historical_checker.startsWith('NOT RUN'),'scope');
const fixtures=graphFixtures();
for(const row of d.rows){
  const [nv,edges]=fixtures[row.graph], base=tseitin(nv,edges,true), [cs,pairs]=split(base,edges.length);
  ok(cs.length===8*nv,'source clause count');
  ok(row.total_variables===edges.length+4*nv,'variables');
  ok(cs.every(c=>c.length===3&&new Set(c.map(Math.abs)).size===3),'strict proper');
  const counts=new Map(); for(const c of cs)counts.set(support(c),(counts.get(support(c))||0)+1);
  ok(Math.max(...counts.values())===1,'unique supports');
  const rec=pairs.map(x=>resolve(x.p,x.q,x.aux));
  ok(JSON.stringify(rec)===JSON.stringify(base),'all reconstruction');
  const derived=new Map();for(const c of rec)derived.set(support(c),(derived.get(support(c))||0)+1);
  ok([...derived.values()].every(x=>x===4)&&derived.size===nv,'derived packets');

  const deletion=Array(base.length).fill(null), oddModels=[];
  for(let a=0;a<(1<<edges.length);a++){
    const falseIds=[]; for(let i=0;i<base.length;i++)if(!clauseTrue(base[i],a))falseIds.push(i);
    if(falseIds.length===0)oddModels.push(a);
    if(falseIds.length===1&&deletion[falseIds[0]]===null)deletion[falseIds[0]]=a;
  }
  ok(oddModels.length===0,'odd unsat');
  ok(deletion.every(x=>x!==null),'base deletion witnesses');
  for(let si=0;si<cs.length;si++){
    const ti=Math.floor(si/2),a=deletion[ti],aux=new Map();
    for(let j=0;j<pairs.length;j++){
      if(j===ti)aux.set(pairs[j].aux,si%2===0?0:1);
      else ok(auxFor(pairs[j],a,aux)!==null,'other gadget extension');
    }
    ok(cs.every((c,i)=>i===si||clauseTrue(c,a,aux)),'split deletion witness');
    ok(!clauseTrue(cs[si],a,aux),'deleted split clause falsified');
  }

  const even=tseitin(nv,edges,false);let evenCount=0;
  for(let a=0;a<(1<<edges.length);a++)if(even.every(c=>clauseTrue(c,a)))evenCount++;
  ok(evenCount===2**(edges.length-nv+1),'even count');
  ok(row.even_base_models===evenCount,'raw even count');
  ok(row.split_source_deletion_witnesses===cs.length,'raw deletion count');
  ok(row.declared_Rmix341_paid_nodes.total===8*nv-1,'upper count');
  ok(row.declared_Rmix341_paid_nodes.source_capacity_lower_bound===8*nv-1,'lower count');
  ok(row.balanced_weighted_critical_path===3+(nv-1).toString(2).length,'span');
  const src=sourceBytes(cs),sha=crypto.createHash('sha256').update(src).digest('hex');
  ok(row.encoded_bytes===Buffer.byteLength(src),'bytes');ok(row.source_sha256===sha,'source hash');
}

// Independent malformed/forged controls.
ok(resolve([1,2,4],[1,3,4],4)===null,'same polarity');
ok(resolve([1,2,4],[-1,3,-4],4)===null,'tautology');
ok(resolve([1,2,4],[1,3,-4],3)===null,'wrong pivot');
const [mut]=split([[1,2,3],[1,-2,-3]],3);
mut[2]=[1,-2,4]; // maliciously reuse aux 4: duplicate-support/source-freshness failure
ok(new Set(mut.map(support)).size<mut.length,'aux reuse caught');
for(const [k,v] of Object.entries(d.hostile_controls))if(typeof v==='boolean')ok(v,`recorded control ${k}`);
ok(d.p_vs_np==='OPEN','status');
console.log(JSON.stringify({status:'PASS',checks,raw_sha256:crypto.createHash('sha256').update(bytes).digest('hex')}));
