/* LSPV-2/577: source-bound original-/386 S3 quotient; NOT the historical full R_mix341 checker.
   Reproduce: node experiments/arc/lspv2_577_native386_S3_quotient.cjs . /tmp/lspv2_577
   Generates 6 accepted and 5 rejected byte-exact packet files and 495-value potential.
*/
(function main(){
  'use strict';
  const fs=require('fs'),path=require('path'),os=require('os'),cp=require('child_process'),crypto=require('crypto'),assert=require('assert/strict');
  const root=path.resolve(process.argv[2]||'.'),out=path.resolve(process.argv[3]||path.join(os.tmpdir(),'lspv2_577'));
  fs.mkdirSync(out,{recursive:true});
  const get=(p)=>fs.readFileSync(path.join(root,p));
  const sum=b=>crypto.createHash('sha256').update(b).digest('hex');
  const gitblob=b=>crypto.createHash('sha1').update(Buffer.concat([Buffer.from(`blob ${b.length}\0`),b])).digest('hex');
  const F=get('results/raw/arc/2026-11-12_0836_LSPV2_577_SIGNED_SOURCE.cnf');
  const P=get('results/raw/arc/2026-11-12_0712_LSPV2_576_ACCEPTED_TREE_RES_W29.json');
  const H=get('results/raw/arc/2026-11-12_0712_LSPV2_576_POTENTIAL_2187.json');
  const checker=path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
  assert.equal(sum(F),'3b94f215568099b24756872b0391db550092fb24ef6e67f05ee024bf9330f35c');
  assert.equal(sum(P),'c753ef947e94d09dd278cfa958eb0eb7badbe3878ac9103be7f8549d8d289bac');
  assert.equal(sum(H),'82a2ad521043ff5e1e71e08904d57e88cf50f8e97abf1e3585e115243c0ff5dc');
  assert.equal(gitblob(fs.readFileSync(checker)),'338305c0ce101704205e57543756b8127074a986');
  const base=JSON.parse(P),h=JSON.parse(H),edges=base.spec.edges,indices=new Map(edges.map((e,i)=>[e.join(','),i+1]));
  const source=F.toString().trim().split('\n').slice(1).map(s=>s.trim().split(/\s+/).slice(0,-1).map(Number));
  assert.equal(source.length,17);assert.deepEqual(base.records.filter(x=>x.kind==='SOURCE').map(x=>x.c),source);
  const perms=[];for(let a=1;a<=3;a++)for(let b=1;b<=3;b++)for(let c=1;c<=3;c++){
   if(new Set([a,b,c]).size!==3)continue;const v=[0,a,b,c];
   const p=edges.map(([u,w])=>indices.get([v[u],v[w]].sort((x,y)=>x-y).join(',')));
   assert.equal(new Set(p).size,6);perms.push({v,p});
  }assert.equal(perms.length,6);
  const decode=i=>{const c=[];for(let v=1;v<=7;v++){const s=Math.floor(i/3**(v-1))%3;if(s)c.push(s===1?v:-v)}return c};
  const encode=c=>c.reduce((x,l)=>x+(l>0?1:2)*3**(Math.abs(l)-1),0);
  const sort=c=>[...c].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);
  const moveLit=(l,p)=>Math.sign(l)*(Math.abs(l)<=6?p[Math.abs(l)-1]:Math.abs(l));
  const move=(c,p)=>sort(c.map(l=>moveLit(l,p)));
  const U=Array.from({length:3**7},(_,i)=>decode(i));assert.equal(h.length,U.length);
  const T=perms.map(({p})=>U.map(c=>encode(move(c,p))));
  const canonical=U.map((_,i)=>Math.min(...T.map(t=>t[i]))),reps=[...new Set(canonical)].sort((a,b)=>a-b);
  assert.equal(reps.length,495);assert.equal(canonical[0],0);
  const values=new Map(reps.map(i=>[i,h[i]]));
  for(let i=0;i<U.length;i++)assert.equal(h[i],values.get(canonical[i]),`potential not equivariant at ${i}`);
  for(const c of source)assert.equal(values.get(canonical[encode(c)]),0);
  assert.equal(values.get(0),28);
  let inequalities=0,fail29=0;const transitionOrbits=new Set();
  const live=U.map((_,i)=>i).filter(i=>h[i]<28);
  for(const i of live)for(const j of live){const a=U[i],b=U[j];
   for(const pivot of a){if(!b.includes(-pivot))continue;
    const derived=new Set([...a.filter(x=>x!==pivot),...b.filter(x=>x!==-pivot)]);
    if([...derived].some(x=>derived.has(-x)))continue;
    const k=encode([...derived]);inequalities++;
    assert(values.get(canonical[k])<=h[i]+h[j]+1,`invalid potential inequality ${i} ${j} ${pivot}`);
    if(k===0 && h[i]+h[j]+1<29)fail29++;
    let best=null;
    for(let t=0;t<6;t++){
      const x=[T[t][i],T[t][j],moveLit(pivot,perms[t].p)];
      if(best===null||x[0]<best[0]||(x[0]===best[0]&&(x[1]<best[1]||(x[1]===best[1]&&x[2]<best[2]))))best=x;
    }
    transitionOrbits.add(best.join(','));
   }
  }
  assert.equal(inequalities,711298);assert.equal(transitionOrbits.size,120402);assert.equal(fail29,2);
  function transport(v,p){const d=structuredClone(base);
   for(const g of d.gate_defs)for(let k=1;k<=3;k++)g[k]=moveLit(g[k],p);
   for(const r of d.records){r.c=move(r.c,p);if(r.kind==='SOURCE'&&r.source>=0)r.source=v[r.source];if(r.kind==='RES')r.pivot=moveLit(r.pivot,p)}
   return d;
  }
  const cases=[];function checkCase(name,d,expected){const data=Buffer.from(JSON.stringify(d)+'\n');
   const dest=path.join(out,`${name}.json`);fs.writeFileSync(dest,data);
   const r=cp.spawnSync(process.execPath,[checker,dest],{encoding:'utf8',timeout:20000});
   assert.equal(r.status===0,expected,`${name}: ${r.stderr}`);
   const v={name,accepted:expected,bytes:data.length,sha256:sum(data)};
   if(expected){const x=JSON.parse(r.stdout);assert.equal(x.paid,29);v.assertions=x.assertions;v.work=x.paid;}
   cases.push(v);
  }
  for(let i=0;i<6;i++){const {v,p}=perms[i];checkCase(`S3_ACCEPTED_${i}`,transport(v,p),true)}
  const x=transport(perms[1].v,perms[1].p);
  const mutants={bad_source:d=>d.records[0].source=3,bad_pivot:d=>d.records.at(-1).pivot=6,underpay:d=>d.summary.paid_total=28,unknown_AND3:d=>d.records.at(-1).kind='AND3',gate_collision:d=>d.gate_defs[0][1]=7};
  for(const [name,mut] of Object.entries(mutants)){const d=structuredClone(x);mut(d);checkCase(`REJECT_${name}`,d,false)}
  const compact={scope:'tree-like strict Resolution only; original restricted /386, not R_mix341',source_sha256:sum(F),witness_sha256:sum(P),checker_git_blob:gitblob(fs.readFileSync(checker)),signed_clause_states:2187,orbits:495,group:'S3 on vertices 1,2,3, vertex 0 fixed',edge_maps:perms.map(z=>z.p),values:reps.map(i=>[i,values.get(i)])};
  const cb=Buffer.from(JSON.stringify(compact)+'\n');fs.writeFileSync(path.join(out,'S3_POTENTIAL_495.json'),cb);
  const result={status:'PROVED/EXACT restricted orbit quotient + COMPUTATIONAL original /386 OS checker; P versus NP OPEN',clause_states:2187,quotient_orbits:495,legal_resolution_inequalities:inequalities,oriented_inference_orbits:transitionOrbits.size,wrong29_inequalities:fail29,accepted:6,rejected:5,original_checker_assertions:cases.filter(x=>x.accepted).reduce((s,x)=>s+x.assertions,0),logical_work:29,tree_RES_work:28,quotient_file_sha256:sum(cb),cases};
  fs.writeFileSync(path.join(out,'S3_RAW.json'),JSON.stringify(result,null,2)+'\n');
  console.log(JSON.stringify({...result,cases:undefined}));
})();
