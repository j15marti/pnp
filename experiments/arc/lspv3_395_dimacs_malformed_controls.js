"use strict";
// LSPV-3/395 sidecar: reject malformed DIMACS sources, same-source SAT controls.
function parse(text) {
  if(typeof text!=="string")throw Error("not text");
  let lines=text.split(/\r?\n/), head=null, lits=[];
  for(const raw of lines){
    const x=raw.trim();if(!x || x.startsWith("c "))continue;
    if(x.startsWith("p ")) {
      if(head!==null)throw Error("two headers");
      const t=x.split(/\s+/);
      if(t.length!==4||t[1]!=="cnf"||!t.slice(2).every(v=>/^\d+$/.test(v)))throw Error("header");
      head=[+t[2],+t[3]];
      if(!Number.isSafeInteger(head[0])||!Number.isSafeInteger(head[1]))throw Error("range");
    }else{
      if(head===null)throw Error("clauses before header");
      for(const w of x.split(/\s+/)){
        if(!/^-?\d+$/.test(w)||!Number.isSafeInteger(Number(w)))throw Error("literal");
        let i=Number(w);if(Math.abs(i)>head[0])throw Error("bound");
        lits.push(i);
      }
    }
  }
  if(head===null)throw Error("missing header");
  let clauses=[],cur=[];
  for(const l of lits){if(l===0){clauses.push(cur);cur=[];}else cur.push(l);}
  if(cur.length || clauses.length!==head[1])throw Error("termination or clause count");
  return {n:head[0],clauses};
}
function serial(n,clauses){return "p cnf "+n+" "+clauses.length+"\n"+clauses.map(c=>c.join(" ")+" 0").join("\n")+"\n";}
function isSat(n,clauses){for(let a=0;a<(1<<n);a++)if(clauses.every(c=>c.some(l=>Boolean(a&(1<<(Math.abs(l)-1)))===(l>0))))return true;return false;}
function run(){
 const good=serial(2,[[1],[-1,2],[-2]]);
 const p=parse(good);
 if(p.clauses.length!==3||isSat(2,p.clauses))throw Error("good UNSAT");
 let passed=1;
 const satNeighbor=serial(2,[[1],[-1,2]]);
 if(!isSat(2,parse(satNeighbor).clauses))throw Error("SAT neighbor");passed++;
 const invalid=["p cnf 2 2\n1 0\n-1 2 0\n-2 0\n", // wrong clause count
 "p cnf 2 3\n1 0\n-1 2 0\n-2\n", // missing 0
 "p cnf 2 3\n3 0\n-1 2 0\n-2 0\n", // ID out of bounds
 "p cnf 2 3\nx 0\n-1 2 0\n-2 0\n", // invalid token
 "p cnf -2 1\n1 0\n", // bad header
 "p cnf 2 3\n1 0\n-1 2 0\n-2 0\n0\n", // extra empty clause
 "1 0\np cnf 2 1\n", // no header before clause
 "", // empty input
 "p cnf 2 3\n1 0\np cnf 2 2\n1 0\n", // duplicate header
 "p cnf 2 3\n1 0\n-1 2 0\n-2 0\nbad", // trailing token
 ];
 for(const x of invalid){let bad=false;try{parse(x);}catch{bad=true;}if(!bad)throw Error("accepted invalid");passed++;}
 return {status:"COMPUTATIONAL",passed,invalid_rejected:invalid.length,sat_control:true,unsat_control:true};
}
if(typeof module!=="undefined")console.log(JSON.stringify(run(),null,2));
