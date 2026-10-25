#!/usr/bin/env node
/* ARC-PAIRED-HARD-GUARD122, deterministic two-level SAT/UNSAT and bit-index test. */
'use strict';
const crypto = require('crypto');
const fs = require('fs');
let checks = 0;
let calls = 0;
let maxSatNodes = 0;
const summaries = [];
function verify(x,msg) {checks++; if(!x) throw Error(`assertion ${checks}: ${msg}`);}
function fresh(start) {let i=start;return ()=>++i;}
function pin(l,newVar) {
  const a=newVar(),b=newVar();
  return [[l,a,b],[l,a,-b],[l,-a,b],[l,-a,-b]];
}
function maxvar(cnf) {return cnf.reduce((x,c)=>Math.max(x,...c.map(z=>Math.abs(z))),0);}
function guard(F,kind,z) {
  verify(z.length>=2 && (kind==='YES'||kind==='NO'),'good inputs');
  const m=z.length,newVar=fresh(maxvar(F));
  const clauses=[],probes=[];
  function add(c) {
    verify(c.length===3 && new Set(c.map(v=>Math.abs(v))).size===3,'proper clause');
    clauses.push(c);
  }
  const selector=kind==='NO'?newVar():null;
  for(const c of F) {
    if(kind==='YES') add(c.slice());
    else {const w=newVar(); add([-selector,c[0],w]);add([-w,c[1],c[2]]);}
  }
  const detectorVars=[];
  for(let j=0;j<m;j++) {
    const x=newVar(),p=newVar();
    for(const c of pin(x,newVar)) add(c);
    if(kind==='YES') {
      const q=newVar();
      for(const c of pin(-p,newVar)) add(c);
      for(const c of pin(-q,newVar)) add(c);
      probes.push({clause:clauses.length,literal:0});
      add([z[j]===0?x:-x,p,q]);
    } else {
      for(const c of pin(-p,newVar)) add(c);
      const d=newVar(); detectorVars.push(d);
      probes.push({clause:clauses.length,literal:1});
      add([-d,z[j]===0?-x:x,p]);
    }
  }
  if(kind==='NO') {
    const lits=[selector,...detectorVars];
    if(lits.length===3) add(lits);
    else {
      let w=newVar();add([lits[0],lits[1],w]);
      for(let i=2;i<lits.length-2;i++) {
        const next=newVar();add([-w,lits[i],next]);w=next;
      }
      add([-w,lits[lits.length-2],lits[lits.length-1]]);
    }
  }
  return {kind,clauses,probes,maxVariable:maxvar(clauses)};
}
function virtualGuardBit(F,kind,z,offset,V) {
  const M=F.length,m=z.length,yes=(kind==='YES');
  const Vout=yes?V+9*m:V+1+M+7*m+Math.max(0,m-2);
  const Mout=yes?M+13*m:2*M+10*m-1;
  const width=String(Vout).length;
  const header=`p proper3 ${Vout} ${Mout} w${width}\n`;
  if(offset<header.length) return header[offset];
  const recordLength=3*(width+2)+1;
  const record=Math.floor((offset-header.length)/recordLength);
  const column=(offset-header.length)%recordLength;
  if(record>=Mout) throw Error('virtual index outside image');
  if(column===recordLength-1) return '\n';
  const litIndex=Math.floor(column/(width+2));
  const fieldIndex=column%(width+2);
  function pinClause(l,a,b,k) {
    return [[l,a,b],[l,a,-b],[l,-a,b],[l,-a,-b]][k];
  }
  function imageClauseAt(k) {
    if(yes) {
      if(k<M) return F[k];
      const i=Math.floor((k-M)/13),slot=(k-M)%13;
      const b=V+9*i,x=b+1,p=b+2,q=b+5;
      if(slot<4) return pinClause(x,b+3,b+4,slot);
      if(slot<8) return pinClause(-p,b+6,b+7,slot-4);
      if(slot<12) return pinClause(-q,b+8,b+9,slot-8);
      return [z[i]===0?x:-x,p,q];
    }
    const sel=V+1;
    if(k<2*M) {
      const j=Math.floor(k/2), w=V+2+j, c=F[j];
      return k%2===0?[-sel,c[0],w]:[-w,c[1],c[2]];
    }
    if(k<2*M+9*m) {
      const i=Math.floor((k-2*M)/9),slot=(k-2*M)%9;
      const b=V+1+M+7*i,x=b+1,p=b+2,d=b+7;
      if(slot<4) return pinClause(x,b+3,b+4,slot);
      if(slot<8) return pinClause(-p,b+5,b+6,slot-4);
      return [-d,z[i]===0?-x:x,p];
    }
    const j=k-(2*M+9*m),base=V+1+M+7*m;
    const d=i=>V+1+M+7*i+7;
    if(m===2) return [sel,d(0),d(1)];
    if(j===0) return [sel,d(0),base+1];
    if(j===m-2) return [-(base+m-2),d(m-2),d(m-1)];
    return [-(base+j),d(j),base+j+1];
  }
  const lit=imageClauseAt(record)[litIndex];
  if(fieldIndex===0) return lit<0?'1':'0';
  if(fieldIndex===width+1) return ' ';
  return String(Math.abs(lit)).padStart(width,'0')[fieldIndex-1];
}
function appendTruePadding(base,count) {
  const clauses=base.clauses.map(x=>x.slice());
  let q=maxvar(clauses);
  for(let i=0;i<count;i++) clauses.push([++q,++q,++q]);
  return {clauses,maxVariable:maxvar(clauses)};
}
function serialize(cnf,probes) {
  const width=String(maxvar(cnf)).length;
  let text=`p proper3 ${maxvar(cnf)} ${cnf.length} w${width}\n`;
  const positions=[];
  for(let i=0;i<cnf.length;i++) {
    const pos=[];
    for(const lit of cnf[i]) {
      pos.push(text.length);
      text+=(lit<0?'1':'0')+String(Math.abs(lit)).padStart(width,'0')+' ';
    }
    text+='\n';positions.push(pos);
  }
  return {text,width,positions,guardPositions:probes.map(p=>positions[p.clause][p.literal])};
}
function parse(text) {
  const lines=text.trimEnd().split('\n');
  const h=/^p proper3 ([0-9]+) ([0-9]+) w([0-9]+)$/.exec(lines.shift());
  verify(Boolean(h),'header parses');
  const V=+h[1],M=+h[2],w=+h[3];
  verify(lines.length===M && String(V).length===w,'counts and width match');
  const clauses=[];
  for(const line of lines){
    const toks=line.trim().split(' ');
    verify(toks.length===3,'exact ternary line');
    const cl=toks.map(tok=>{
      verify(new RegExp(`^[01][0-9]{${w}}$`).test(tok),'fixed slot');
      const id=+tok.slice(1);
      verify(id>=1 && id<=V,'ID range');
      return tok[0]==='1'?-id:id;
    });
    verify(new Set(cl.map(x=>Math.abs(x))).size===3,'distinct variables');
    clauses.push(cl);
  }
  return clauses;
}
function sat(clauses) {
  calls++; let nodes=0;
  function solve(asn){
    nodes++;
    while(true){
      let changed=false, allSat=true, seen=new Map();
      for(const clause of clauses){
        let satisfied=false, unassigned=0, lone=0;
        for(const l of clause){
          const v=asn.get(Math.abs(l));
          if(v===undefined){unassigned++;lone=l;}
          else if(v===(l>0)){satisfied=true;break;}
        }
        if(satisfied) continue;
        allSat=false;
        if(unassigned===0) return false;
        if(unassigned===1){
          const id=Math.abs(lone), val=lone>0;
          const old=asn.get(id);
          if(old!==undefined && old!==val) return false;
          if(old===undefined){asn.set(id,val);changed=true;}
        } else {
          for(const l of clause) if(!asn.has(Math.abs(l)))
            seen.set(Math.abs(l),(seen.get(Math.abs(l))||0)+1);
        }
      }
      if(changed) continue;
      if(allSat) return true;
      let candidate=0,best=-1;
      for(const [id,score] of seen) if(score>best){candidate=id;best=score;}
      if(!candidate){
        for(const cl of clauses) for(const l of cl) if(!asn.has(Math.abs(l))) {candidate=Math.abs(l);break;}
      }
      verify(candidate>0,'branch candidate');
      for(const v of [true,false]) {
        const branch=new Map(asn);branch.set(candidate,v);
        if(solve(branch)) return true;
      }
      return false;
    }
  }
  const result=solve(new Map());maxSatNodes=Math.max(maxSatNodes,nodes);
  return result;
}
function maskClause(mask) {return [0,1,2].map(i=>(mask&(1<<i))?-(i+1):(i+1));}
const sources=[];
for(let subset=1;subset<256;subset++){
  if(subset!==255 && (subset.toString(2).match(/1/g)||[]).length>3) continue;
  const F=[];for(let m=0;m<8;m++) if((subset>>m)&1) F.push(maskClause(m));
  sources.push({name:`subset-${subset}`,F});
}
for(let r=0;r<8;r++){
  const F=Array.from({length:8},(_,i)=>maskClause((i+r)%8));
  F.push(maskClause(r));
  sources.push({name:`unsat-shuffle-${r}`,F});
}
let satRoots=0,unsatRoots=0,guardFlips=0,ordinaryLevels=0,checksPerLabel={YES:0,NO:0};
let lengthStats=[];let completeWork=0,nonChangingWrites=0;
for(const {name,F} of sources){
  const sourceHeaderV=maxvar(F);
  const sourceSat=sat(F);
  if(sourceSat) satRoots++;else unsatRoots++;
  const m=Math.max(2,Math.min(5,F.length));
  const z=Array(m).fill(0);
  for(const kind of ['YES','NO']) {
    const base=guard(F,kind,z);
    const central=serialize(base.clauses,base.probes);
    verify(sat(parse(central.text))===sourceSat,`${name}/${kind} faithful`);checksPerLabel[kind]++;
    for(let k=0;k<central.text.length;k++) {
      verify(virtualGuardBit(F,kind,z,k,sourceHeaderV)===central.text[k],
        `${name}/${kind} locally indexed image bit ${k}`);
    }
    const levels=[appendTruePadding(base,2*m),appendTruePadding(base,m),appendTruePadding(base,0)];
    let prev=Infinity;
    for(let depth=0;depth<3;depth++) {
      const serial=serialize(levels[depth].clauses,[]);
      verify(serial.text.length<prev,`${name}/${kind} strict shorter depth ${depth}`);
      verify(sat(parse(serial.text))===sourceSat,`${name}/${kind} depth label ${depth}`);
      prev=serial.text.length;ordinaryLevels++;
    }
    for(let j=0;j<m;j++) {
      const mask=z.slice();mask[j]=1;
      const flipped=guard(F,kind,mask);
      const changed=serialize(flipped.clauses,flipped.probes);
      verify(changed.text.length===central.text.length,'one-bit same-length encoding');
      const p=central.guardPositions[j];
      let expected=central.text.slice(0,p)+(central.text[p]==='1'?'0':'1')+central.text.slice(p+1);
      verify(changed.text===expected,`${name}/${kind} exact physical sign-bit neighbor`);
      const opposite=kind==='YES'?false:true;
      verify(sat(parse(changed.text))===opposite,`${name}/${kind} guard flip formula truth`);
      if(kind==='YES' ? sourceSat : !sourceSat) {
        verify(opposite!==sourceSat,`${name}/${kind} pivotal center`);
      }
      guardFlips++;
    }
    if(lengthStats.length<16) lengthStats.push({name,kind,sourceSat,sourceClauses:F.length,baseBits:central.text.length,rootBits:serialize(levels[0].clauses,[]).text.length,childBits:serialize(levels[1].clauses,[]).text.length,grandchildBits:serialize(levels[2].clauses,[]).text.length,guardBits:m});
    for(const lvl of levels){
      const bits=serialize(lvl.clauses,[]).text.length;
      completeWork+=bits;
      nonChangingWrites+=bits;
    }
  }
}
verify(satRoots>0 && unsatRoots>0,'both source SAT labels present');
const out={id:'ARC-PAIRED-HARD-GUARD122',mode:'deterministic exhaustive subset of 3-variable proper-3CNF masks plus 8 UNSAT clause permutations',seed:null,sourceCount:sources.length,satRoots,unsatRoots,guardFlips,ordinaryLevels,guestSatCalls:calls,maxDpllNodes:maxSatNodes,logicalAssertions:checks,checksPerLabel,serializedBytesPaid:completeWork,unchangedWritesCharged:nonChangingWrites,samples:lengthStats,notFLMVBitTrace:true,notUnconditionalSATLowerBound:true,arcEdge:'OPEN',pVsNP:'OPEN'};
const body=JSON.stringify(out,null,2)+'\n';
const path=process.argv[2]||'research/agents/lspv-4/2026-10-25_0959_ARC_PAIRED_HARD_GUARD122_raw.json';
fs.writeFileSync(path,body);
console.log(JSON.stringify({raw:path,sourceCount:sources.length,satRoots,unsatRoots,logicalAssertions:checks,guestSatCalls:calls,guardFlips,ordinaryLevels,maxDpllNodes:maxSatNodes,rawSha256:crypto.createHash('sha256').update(body).digest('hex')}));
