#!/usr/bin/env node
"use strict";
// Separate general-CNF syntax control. Parses canonical/standard DIMACS with
// comments, multi-line clauses, empty clauses, signed integer literals.
function ensure(x,s){if(!x)throw Error(s)}
function parseDIMACS(source){
  ensure(typeof source==="string"&&source.length>0,"not text");
  ensure(!/[^\x09\x0a\x0d\x20-\x7e]/.test(source),"non-ASCII");
  let header=null,clauses=[],current=[],sawContent=false;
  for(const line of source.split(/\r?\n/)){
    let s=line.trim();if(!s||/^c(\s|$)/.test(s))continue;
    if(s.startsWith("p")){ensure(!header&&!sawContent,"duplicate/late header");let mat=/^p\s+cnf\s+([0-9]+)\s+([0-9]+)$/.exec(s);ensure(mat,"header grammar");let n=Number(mat[1]),m=Number(mat[2]);ensure(Number.isSafeInteger(n)&&Number.isSafeInteger(m),"oversize header");header={n,m};continue}
    sawContent=true;ensure(header,"missing header");
    for(const tok of s.split(/\s+/)){
      ensure(/^(0|[1-9][0-9]*|-[1-9][0-9]*)$/.test(tok),"malformed signed literal");
      let v=Number(tok);ensure(Number.isSafeInteger(v)&&Math.abs(v)<=header.n,"out of range");
      if(v===0){clauses.push(current);current=[];ensure(clauses.length<=header.m,"too many clauses")}
      else current.push(v);
    }
  }
  ensure(header&&current.length===0&&clauses.length===header.m,"unterminated/incorrect count");
  return {n:header.n,clauses};
}
function run(raw){
 let accepted=0;
 for(const entry of raw.cases){
   const p=entry.proof;
   let lines=(C)=>"p cnf "+p.n+" "+C.length+"\n"+C.map(x=>x.join(" ")+" 0\n").join("");
   for(const C of [p.clauses,p.evenClauses]){
     let r=parseDIMACS(lines(C));ensure(r.n===p.n&&JSON.stringify(r.clauses)===JSON.stringify(C),"source roundtrip");accepted++;
   }
 }
 let malformed=[
  "",
  "1 0\n",
  "p cnf 1 1\n2 0\n",
  "p cnf 2 1\n1 2\n",
  "p cnf 1 1\nx 0\n",
  "p cnf 1 1\n-0\n",
  "p cnf 1 1\n1 0\np cnf 1 0\n",
  "p cnf 1 2\n1 0\n",
  "p cnf 1 0\n0\n",
  "p cnf 1 1\n1 0\n\x00"
 ];let rejected=0;
 for(const x of malformed){try{parseDIMACS(x)}catch(e){rejected++;continue}throw Error("malformed accepted: "+JSON.stringify(x))}
 const extra=["p cnf 1 1\n0\n","c comment\np cnf 2 1\n1\n-2 0\n"];
 for(const s of extra){let x=parseDIMACS(s);ensure(x.clauses.length===1,"extra valid");accepted++}
 return {accepted,malformed_rejected:rejected,malformed_tested:malformed.length,corpus_cases:raw.cases.length};
}
if(require.main===module){let r=JSON.parse(require("fs").readFileSync(process.argv[2],"utf8"));process.stdout.write(JSON.stringify(run(r))+"\n")}
module.exports={parseDIMACS,run};
