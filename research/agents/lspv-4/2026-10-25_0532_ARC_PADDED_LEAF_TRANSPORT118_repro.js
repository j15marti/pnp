#!/usr/bin/env node
'use strict';
function audit(){
  "use strict";
  const summary={
    run_id:"ARC-PADDED-LEAF-TRANSPORT118",
    date:"2026-10-25",
    deterministic:true,
    samples:[],
    patterns:["yes","no","horn","two","affine"],
    sizes:[8,9,10],
    source_cases:0,sat_roots:0,unsat_roots:0,
    first_level_children:0,second_level_children:0,
    assertions:0,failures:0,
    events:{serializer_write_events:0,serializer_zero_unchanged_on_fresh_zero_cell:0,serializer_one_changed_on_fresh_zero_cell:0,serializer_strings:0,encoded_bits_read_by_validation:0,source_input_bits_parsed:0,source_literal_references_copied:0,row_serialized_bits:0,leaf_serialized_bits:0},
    status:{finite:"COMPUTATIONAL",size_tax:"PROVED/EXACT within intact-leaf hypothesis; independent review pending",unrestricted_ARC:"OPEN",P_vs_NP:"OPEN"}
  };
  function ck(ok,why){summary.assertions++;if(!ok){summary.failures++;throw Error(why)}}
  function bits(x){ck(Number.isSafeInteger(x)&&x>=0,"bad integer");return x.toString(2)}
  function unary(x){const s=bits(x);return "1".repeat(s.length)+"0"+s}
  function recordWrite(s){summary.events.serializer_strings++;summary.events.serializer_write_events+=s.length;for(let i=0;i<s.length;i++){if(s[i]==="0")summary.events.serializer_zero_unchanged_on_fresh_zero_cell++;else if(s[i]==="1")summary.events.serializer_one_changed_on_fresh_zero_cell++;else throw Error("non-bit")}}
  function enc(V,clauses){
    ck(Number.isInteger(V)&&V>=3,"declared vars");ck(Array.isArray(clauses),"clauses array");
    const w=Math.ceil(Math.log2(V+1));
    let s="10011010"+unary(V)+unary(clauses.length);
    for(const clause of clauses){
      ck(clause.length===3,"ternary"); const seen=new Set();
      for(const lit of clause){
        const a=Math.abs(lit);ck(Number.isInteger(lit)&&a>=1&&a<=V&&!seen.has(a),"illegal literal");
        seen.add(a);s+= (lit<0?"1":"0")+bits(a).padStart(w,"0");
      }
    }
    recordWrite(s);return s;
  }
  function parse(s){
    let i=0;function take(k){ck(i+k<=s.length,"truncated");const p=s.slice(i,i+k);i+=k;summary.events.encoded_bits_read_by_validation+=k;return p}
    ck(take(8)==="10011010","bad header");
    function readU(){let k=0;while(true){const b=take(1);if(b==="0")break;ck(b==="1","invalid unary");k++;ck(k<64,"too many header unary bits")}ck(k>0,"empty unary");const p=take(k);ck(p[0]==="1","noncanonical unary");return parseInt(p,2)}
    const V=readU(),M=readU();ck(Number.isInteger(V)&&V>=3&&Number.isSafeInteger(M)&&M>=0,"header fields");const w=Math.ceil(Math.log2(V+1));
    ck(i+M*3*(w+1)===s.length,"length mismatch");
    const clauses=[];
    for(let j=0;j<M;j++){const clause=[],seen=new Set();for(let k=0;k<3;k++){const sign=take(1),mag=parseInt(take(w),2);ck(mag>=1&&mag<=V&&!seen.has(mag),"bad target literal");seen.add(mag);clause.push(sign==="1"?-mag:mag)}clauses.push(clause)}
    ck(i===s.length,"trailing bits");return {V,M,clauses}
  }
  function sourceClauses(m,type){
    const Y=[1,2,3],NO=Array.from({length:8},(_,a)=>Array.from({length:3},(_,b)=>(a&(1<<b))?-(b+1):b+1));
    const XOR=[[1,2,3],[-1,-2,3],[-1,2,-3],[1,-2,-3]];
    const out=[];
    for(let i=0;i<m;i++){
      if(type==="yes")out.push(Y.slice());
      else if(type==="no")out.push(NO[i%8].slice());
      else if(type==="horn")out.push([-1,-2,3]);
      else if(type==="two")out.push(i%2?[1,2,-3]:[1,2,3]);
      else if(type==="affine")out.push(XOR[i%4].slice());
      else throw Error("unknown source type");
    }
    return out;
  }
  function solve3(clauses){
    for(let mask=0;mask<8;mask++){
      if(clauses.every(c=>c.some(lit=>{const v=(mask>>(Math.abs(lit)-1))&1;return lit>0?!!v:!v})))return true;
    }return false;
  }
  function canonPair(clauses){return clauses.map(c=>c.join(",")).join(";")}
  const expected={yes:true,no:false,horn:true,two:true,affine:true};
  for(const m of summary.sizes)for(const type of summary.patterns){
    const source=sourceClauses(m,type),nSourceVars=3*m,sourceS=enc(nSourceVars,source),parsedSource=parse(sourceS);
    summary.events.source_input_bits_parsed+=sourceS.length;
    ck(canonPair(parsedSource.clauses)===canonPair(source),"source round trip");
    const sourceSat=solve3(source);ck(sourceSat===expected[type],"source label independent");
    const leafCount=m*m*m,rowCount=m*m,rootClauses=[],rows=[];
    for(let rowId=0;rowId<rowCount;rowId++){
      const rowClauses=[],leafRecords=[];
      for(let j=0;j<m;j++){
        const leafId=rowId*m+j,body=leafId===0?source:sourceClauses(m,"yes"),packetOff=3*m*leafId,rowOff=3*m*j;
        if(leafId===0)summary.events.source_literal_references_copied+=3*m;
        for(const c of body){
          const rowC=c.map(lit=>Math.sign(lit)*(Math.abs(lit)+rowOff));
          const rootC=c.map(lit=>Math.sign(lit)*(Math.abs(lit)+packetOff));
          rowClauses.push(rowC);rootClauses.push(rootC);
        }
        leafRecords.push(body);
      }
      rows.push({rowId,rowClauses,leafRecords});
    }
    ck(rootClauses.length===m**4&&rows.length===rowCount,"sizes");
    const rootS=enc(3*m**4,rootClauses);
    const parsedRoot=parse(rootS);
    ck(parsedRoot.M===m**4&&parsedRoot.V===3*m**4,"root header");
    ck(canonPair(rootClauses)===canonPair(parsedRoot.clauses),"root serialization clause round-trip");
    let rowsSat=true,leavesSat=true;
    for(const row of rows){
      const rowS=enc(3*m*m,row.rowClauses),rp=parse(rowS);
      summary.events.row_serialized_bits+=rowS.length;
      ck(canonPair(rp.clauses)===canonPair(row.rowClauses),"row round trip");
      const expectedRow=parsedRoot.clauses.slice(row.rowId*m*m,(row.rowId+1)*m*m).map(c=>c.map(l=>Math.sign(l)*(Math.abs(l)-row.rowId*3*m*m)));
      ck(canonPair(expectedRow)===canonPair(rp.clauses),"row from actual root");
      const rowS2=enc(3*m*m,expectedRow);
      ck(rowS.length===rowS2.length,"row equality length");
      for(let z=0;z<rowS.length;z++)ck(rowS[z]===rowS2[z],"row bit mismatch");
      const rsat=[];summary.first_level_children++;
      for(let j=0;j<m;j++){
        const leafId=row.rowId*m+j,body=row.leafRecords[j];
        const leafS=enc(3*m,body),lp=parse(leafS);
        summary.events.leaf_serialized_bits+=leafS.length;
        ck(canonPair(lp.clauses)===canonPair(body),"leaf round trip");
        const copyFromRow=rp.clauses.slice(j*m,(j+1)*m).map(c=>c.map(l=>Math.sign(l)*(Math.abs(l)-j*3*m)));
        ck(canonPair(copyFromRow)===canonPair(lp.clauses),"actual row to leaf identity");
        const leafS2=enc(3*m,copyFromRow);ck(leafS.length===leafS2.length,"leaf bit length");
        for(let z=0;z<leafS.length;z++)ck(leafS[z]===leafS2[z],"leaf bit mismatch");
        const localSat=solve3(body);const extractedSat=solve3(copyFromRow);
        ck(localSat===extractedSat,"leaf independent exact decision");
        if(leafId===0)ck(leafS===sourceS&&localSat===sourceSat,"hard packet intact");
        else ck(localSat===true,"public free packet truly satisfiable");
        rsat.push(localSat);leavesSat=leavesSat&&localSat;summary.second_level_children++;
      }
      const actualRowSat=rsat.every(Boolean);
      ck(actualRowSat=== (row.rowId===0?sourceSat:true),"row OR/AND label");
      rowsSat=rowsSat&&actualRowSat;
    }
    const rootGroupsSat=Array.from({length:leafCount},(_,leafId)=>{
      const packetCl=parsedRoot.clauses.slice(leafId*m,(leafId+1)*m).map(c=>c.map(l=>Math.sign(l)*(Math.abs(l)-leafId*3*m)));
      return solve3(packetCl)
    }).every(Boolean);
    ck(rootGroupsSat===leavesSat&&rowsSat===leavesSat&&rowsSat===sourceSat,"independent root row leaf SAT equivalence");
    ck((rootS.length>sourceS.length)&&(rootS.length>0),"no root amplification");
    summary.samples.push({
      m,type,source_sat:sourceSat,source_bits:sourceS.length,
      root_bits:rootS.length,row_bits:enc(3*m*m,rows[0].rowClauses).length,leaf_bits:sourceS.length,
      rows:rowCount,leaves:leafCount,
      log_root_over_log_source:Math.log(rootS.length)/Math.log(sourceS.length)
    });
    summary.source_cases++;
    if(sourceSat)summary.sat_roots++;else summary.unsat_roots++;
  }
  let refused=false;try{parse("101010") }catch(e){refused=true}ck(refused,"malformed not rejected");
  ck(summary.source_cases===15&&summary.second_level_children===3**3*0+8**3*5+9**3*5+10**3*5,"counts");
  ck(summary.events.serializer_write_events===summary.events.serializer_zero_unchanged_on_fresh_zero_cell+summary.events.serializer_one_changed_on_fresh_zero_cell,"bit writes sum");
  ck(summary.sat_roots>0&&summary.unsat_roots>0,"both root labels");
  return summary;
}
console.log(JSON.stringify(audit(), null, 2));
