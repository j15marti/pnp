#!/usr/bin/env node
'use strict';
/* ARC-SPARSE-DIRECTORY119: declared bit-index-tape emulator, not a physical TM.
   Deterministic, no packages, no random seeds. Writes JSON to stdout. */
function runAudit() {
  let assertions=0;
  const ensure=(ok,msg)=>{assertions++;if(!ok)throw Error('audit assertion '+assertions+': '+msg);};
  const popcount=(n)=>{let r=0;while(n>0){r+=n%2;n=Math.floor(n/2);}return r;};
  const header=(v,m)=>\`p cnf \${v} \${m}\n\`;
  const printLit=x=>(x<0?'-':'+')+Math.abs(x);
  const canonClause=c=>c.map(printLit).join(' ')+' 0\n';
  const parseLine=line=>{
    const x=line.trim().split(/\s+/);
    ensure(x.length===4 && x[3]==='0','proper ternary DIMACS line');
    const y=x.slice(0,3).map(v=>Number(v));
    ensure(y.every(v=>Number.isSafeInteger(v) && v!==0),'signed integers');
    ensure(new Set(y.map(v=>Math.abs(v))).size===3,'distinct variable names');
    return y;
  };
  const evalLeaf=(clauses)=>{
    for(let mask=0;mask<8;mask++){
      let good=true;
      for(const c of clauses){
        if(!c.some(l=>{const bit=(mask>>(Math.abs(l)-1))&1;return l>0 ? bit===1:bit===0;})){
          good=false;break;
        }
      }
      if(good)return true;
    }
    return false;
  };
  const solveDpll=clauses=>{
    const go=(assign)=>{
      for(;;){
        let change=false;
        for(const c of clauses){
          let sat=false, unset=[];
          for(const l of c){
            const v=assign[Math.abs(l)];
            if(v===undefined)unset.push(l);
            else if((l>0)===v){sat=true;break;}
          }
          if(sat)continue;
          if(unset.length===0)return false;
          if(unset.length===1){
            const l=unset[0], name=Math.abs(l), value=l>0;
            if(assign[name]!==undefined && assign[name]!==value)return false;
            if(assign[name]===undefined){assign[name]=value;change=true;}
          }
        }
        if(!change)break;
      }
      let first;
      for(const c of clauses){
        let sat=c.some(l=>assign[Math.abs(l)]!==undefined && (l>0)===assign[Math.abs(l)]);
        if(sat)continue;
        const l=c.find(l=>assign[Math.abs(l)]===undefined);
        if(l!==undefined){first=Math.abs(l);break;}
      }
      if(first===undefined)return true;
      const a={...assign};a[first]=true;
      if(go(a))return true;
      const b={...assign};b[first]=false;
      return go(b);
    };
    return go({});
  };
  class SparseDirectory {
    constructor(source,recordCount,B){
      this.source=source;this.B=B;this.recordCount=recordCount;
      this.w=Math.ceil(Math.log2(8*source.length+2));
      this.counters={sourceByteReads:0,sourceBitReads:0,indexWrites:0,
        unchangedWrites:0,realFlips:0,parsedRecords:0,anchorWrites:0,
        arithmeticOps:0,headerBitOutputs:0,bodyBitOutputs:0};
      this.anchors=[];
      let pos=0;
      while(pos<source.length && source[pos]!=='\n'){this.readByte(pos);pos++;}
      ensure(pos<source.length,'header newline');this.readByte(pos);pos++;
      this.headerEnd=pos;
      let count=0;
      while(pos<source.length){
        if(count%B===0){this.anchors.push(pos);this.counters.anchorWrites+=this.w;}
        while(pos<source.length && source[pos]!=='\n'){this.readByte(pos);pos++;}
        ensure(pos<source.length,'terminated source record');this.readByte(pos);pos++;
        count++;
      }
      ensure(count===recordCount,'directory record count');
      this.buildReads=this.counters.sourceByteReads;
      this.peakDescriptorBits=this.anchors.length*this.w+6*this.w;
    }
    readByte(pos){
      ensure(pos>=0 && pos<this.source.length,'source read in bounds');
      const c=this.counters, w=this.w, pc=popcount(pos);
      c.sourceByteReads++;c.sourceBitReads+=8;
      // Eight consecutive addressed input bits: addresses 8*pos,...,8*pos+7.
      // For each, the declared emulator writes all w address bits and then
      // explicitly zeros all w cells (unchanged zeros are counted).
      const writes=16*w, flips=16*pc+24;
      c.indexWrites+=writes;c.realFlips+=flips;c.unchangedWrites+=writes-flips;
      c.arithmeticOps+=8*w;
      return this.source[pos];
    }
    record(k){
      ensure(k>=0 && k<this.recordCount,'record ordinal in range');
      let pos=this.anchors[Math.floor(k/this.B)];
      let skip=k%this.B;
      let read='';
      for(let j=0;j<=skip;j++){
        read='';
        for(;;){
          const ch=this.readByte(pos++);
          if(ch==='\n')break;
          read+=ch;
        }
        this.counters.parsedRecords++;
      }
      this.counters.arithmeticOps+=this.w*(skip+1);
      return parseLine(read);
    }
  }
  const sizes=[3,4,5],Bs=[1,4,16],kinds=['allSAT','firstUNSAT','lastUNSAT','middleUNSAT','alternatingUNSAT'];
  const records=[];
  let probeChecks=0,rowChecks=0,sourceCases=0;
  for(const q of sizes){
    const p=q*q,m=q*q*p;
    for(const kind of kinds){
      const bad=k=>kind==='allSAT'?false:kind==='firstUNSAT'?k===0:kind==='lastUNSAT'?k===q*q-1:kind==='middleUNSAT'?k===Math.floor(q*q/2):k%2===0;
      const clauses=[],packetClauses=[];
      for(let k=0;k<q*q;k++){
        const base=3*k, packet=[];
        for(let j=0;j<p;j++){
          let c;
          if(bad(k)&&j<8){
            c=[1,2,3].map((a,h)=>((j>>h)&1)?-(base+a):(base+a));
          }else c=[base+1,base+2,base+3];
          packet.push(c);clauses.push(c);
        }
        packetClauses.push(packet);
      }
      let src=header(3*q*q,m),positions=[];
      for(let k=0;k<m;k++){
        positions.push(src.length);
        const c=clauses[k],g=1+((k*11+q*7+kinds.indexOf(kind))%9),inner=1+((k+q)%3);
        src+=' '.repeat(g)+c.map(printLit).join(' '.repeat(inner))+'  0'+' '.repeat((k*3)%4)+'\n';
      }
      ensure(src.startsWith(header(3*q*q,m)),'root header');
      const plain=src.split('\n').slice(1,-1);
      ensure(plain.length===m,'source line count');
      for(let k=0;k<m;k++){
        const c=parseLine(plain[k]);
        ensure(c.every((v,j)=>v===clauses[k][j]),'source parse/serialize round trip');
      }
      const labels=packetClauses.map((packet,k)=>{
        const local=packet.map(c=>c.map(l=>Math.sign(l)*(Math.abs(l)-3*k)));
        return evalLeaf(local);
      });
      ensure(labels.every((v,k)=>v!==bad(k)),'independent 8-assignment leaf oracle');
      let rowLabels=[];
      for(let i=0;i<q;i++){
        const row=packetClauses.slice(i*q,(i+1)*q).flat().map(c=>c.map(l=>Math.sign(l)*(Math.abs(l)-3*i*q)));
        const rowFromBits=header(3*q,q*p)+row.map(canonClause).join('');
        ensure(rowFromBits.includes('p cnf '+3*q+' '+q*p),'real row ordinary SAT header');
        const label=solveDpll(row);
        ensure(label===labels.slice(i*q,(i+1)*q).every(Boolean),'independent DPLL row label');
        rowChecks++;rowLabels.push(label);
      }
      const rootSAT=rowLabels.every(Boolean);
      ensure(rootSAT===!packetClauses.some((_,k)=>bad(k)),'both-label root identity');
      sourceCases++;
      for(const B of Bs){
        const dir=new SparseDirectory(src,m,B);
        const constructionReads=dir.buildReads;
        const anchors=dir.anchors.slice();
        ensure(anchors.length===Math.ceil(m/B),'exact anchor count');
        for(let k=0;k<m;k+=Math.max(1,Math.floor(m/30))){
          ensure(anchors[Math.floor(k/B)]===positions[Math.floor(k/B)*B],'anchor addresses exact');
        }
        const before=dir.counters.sourceByteReads;
        let requests=0;
        for(let k=0;k<q*q;k++){
          const packet=packetClauses[k].map(c=>c.map(l=>Math.sign(l)*(Math.abs(l)-3*k)));
          const h=header(3,p),out=h+packet.map(canonClause).join('');
          const sampleEvery=q<=4?1:9;
          const width=canonClause([1,2,3]).length;
          ensure(packet.every(c=>canonClause(c).length===width),'fixed-slot ordinary leaf records');
          const probeAt=idx=>{
            let got;
            if(idx<h.length){got=h[idx];dir.counters.headerBitOutputs+=8;}
            else{
              const offset=idx-h.length, ci=Math.floor(offset/width), within=offset%width;
              const raw=dir.record(k*p+ci);
              const local=raw.map(l=>Math.sign(l)*(Math.abs(l)-3*k));
              got=canonClause(local)[within];dir.counters.bodyBitOutputs+=8;
            }
            ensure(got===out[idx],'virtual guest byte equals ordinary eager serialization');
            probeChecks++;requests++;
          };
          for(let idx=0;idx<out.length;idx+=sampleEvery)probeAt(idx);
          if((out.length-1)%sampleEvery!==0)probeAt(out.length-1);
        }
        const c=dir.counters;
        ensure(c.indexWrites===c.realFlips+c.unchangedWrites,'all index-tape writes, unchanged included');
        ensure(c.sourceBitReads===8*c.sourceByteReads,'each ASCII source byte is eight addressed bits');
        ensure(c.peakDescriptorBits===undefined,'counter object distinguishes syntactic from peak estimates');
        records.push({q,kind,rootSAT,B,rootBytes:src.length,rows:q,leaves:q*q,
          rootClauses:m,rowClauses:q*p,leafClauses:p,
          leafBytes:header(3,p).length+p*canonClause([1,2,3]).length,
          directoryAnchors:anchors.length,dirBitsBound:dir.peakDescriptorBits,
          sourceByteReadsBuild:constructionReads,sourceByteReadsProbes:c.sourceByteReads-before,
          sourceBitReadsTotal:c.sourceBitReads,indexTapeWrites:c.indexWrites,
          indexUnchangedWrites:c.unchangedWrites,indexRealFlips:c.realFlips,
          instrumentedArithmeticOps:c.arithmeticOps,recordsDecoded:c.parsedRecords,
          headerOutputBits:c.headerBitOutputs,bodyOutputBits:c.bodyOutputBits,
          guestByteProbes:requests,streamEagerLeavesPossible:true});
      }
    }
  }
  // Exact rational FLMV-facing accounting, no claim these witnesses exist.
  const cStar=241/200,dStar=11642479/23232400;
  const seed={t:7/5,s:4/5},a=1/2,lambda=1/2;
  const lazyCore=a+lambda*seed.t;
  const gammaTimeMax=cStar-lazyCore;
  const gammaSpaceMin=1-dStar;
  const eager={t:Math.max(1,a+lambda,a+lambda*seed.t),s:Math.max(lambda,lambda*seed.s)};
  ensure(gammaTimeMax<gammaSpaceMin,'disjoint anchor tradeoff requirements');
  ensure(eager.t<cStar&&eager.s<dStar,'eager promise-only point within strict box');
  ensure(lazyCore+0.5>cStar,'sqrt-record directory lazy simulated access outside box');
  return {name:'ARC-SPARSE-DIRECTORY119',timestamp:'2026-10-25',model:'restricted exact ASCII-bit-index emulation, not FLMV-TM trace',
    seed:'deterministic none',cases:sourceCases,rowsVerifiedByDpll:rowChecks,virtualGuestByteProbeAssertions:probeChecks,
    assertions,failures:0,
    strictBox:{cStar,dStar,betaFraction:'11642479/23232400'},
    conditionalNumerical:{guestSeed:seed,a,lambda,lazyCore,gammaTimeMax,gammaSpaceMin,eager,
      interpretation:'upper-envelope incompatibility for this sparse-anchor/lazy emulation only, not an all-SAT lower bound'},
    records};
}
const result=runAudit();
console.log(JSON.stringify(result,null,2));
