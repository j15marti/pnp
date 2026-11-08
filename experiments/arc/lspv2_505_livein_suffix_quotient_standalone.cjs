'use strict';
/* LSPV-2/505: standalone V8 verifier. NOT a native FLMV checker. */
const lspv505=(function(){
let checks=0,positive=0,negative=0,inputReject=0,forged=0;
const test=(x,m)=>{if(!x)throw Error(m);checks++};
const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
const encode=charges=>{
 let rows=[];
 for(let v=0;v<4;v++){
  let vars=edges.map((p,i)=>p.includes(v)?i+1:0).filter(Boolean);
  for(let k=0;k<8;k++){let bits=[k&1,(k>>1)&1,(k>>2)&1];
   if((bits[0]^bits[1]^bits[2])!==charges[v])
     rows.push(vars.map((e,i)=>bits[i]?-e:e));
  }
 }
 return "p cnf 6 "+rows.length+"\n"+rows.map(r=>r.join(" ")+" 0\n").join("");
};
function classify(s){
 if(!/^p cnf 6 16\n/.test(s)||!s.endsWith("\n"))return "MALFORMED";
 const lines=s.split("\n").slice(1,-1);if(lines.length!==16)return "MALFORMED";
 let c=[];for(let row of lines){if(!/^-?\d+ -?\d+ -?\d+ 0$/.test(row))return "MALFORMED";
 let a=row.split(" ").slice(0,3).map(Number);
 if(a.some(v=>v===0||Math.abs(v)>6)||new Set(a.map(Math.abs)).size!==3)return "MALFORMED";c.push(a);}
 for(let k=0;k<64;k++){if(c.every(a=>a.some(z=>Boolean(k&(1<<(Math.abs(z)-1)))===(z>0))))return "SAT";}
 return "UNSAT";
}
const bits=s=>{let b=[];for(let c of s)for(let k=7;k>=0;k--)b.push((c.charCodeAt(0)>>k)&1);return b};
const run=(raw,start)=>{
 let memory=new Map(start),written=new Set(),trace=[];
 const W=(a,v)=>{memory.set(a,v);written.add(a);trace.push(["W",a,v])};
 const R=a=>{let v=memory.get(a)||0;trace.push(["R",a,v,!written.has(a)]);return v};
 W(1,1);test(R(1)===1,"overwrite");
 if(R(8)){let v=R(17);W(64,v);test(R(64)===v,"dynamic overwrite");}
 W(1000000,0);test(R(1000000)===0,"sparse overwrite");R(19);
 let input=bits(raw);
 input.forEach((v,i)=>trace.push(["I",i,v]));
 let label=classify(raw);trace.push(["HALT",label]);return {trace,label};
};
function certify(trace,raw,work){
 let b=bits(raw),seenInput=new Set(),seenWork=new Set();
 for(let e of trace){
  if(e[0]==="I"&&!seenInput.has(e[1])){seenInput.add(e[1]);if(b[e[1]]!==e[2])return false;}
  if(e[0]==="R"&&e[3]&&!seenWork.has(e[1])){seenWork.add(e[1]);if((work.get(e[1])||0)!==e[2])return false;}
 }
 return true;
}
for(let ch=0;ch<16;ch++){
 let charges=[0,1,2,3].map(i=>(ch>>i)&1),raw=encode(charges),label=classify(raw);
 test(label===((charges.reduce((a,b)=>a^b,0))?"UNSAT":"SAT"),"tseitin parity");
 for(let u of [0,1]){
  let state=new Map([[1,0],[8,u],[17,1],[19,1],[64,1],[1000000,1],[300,1]]);
  let anchor=run(raw,state);
  for(let j=0;j<8;j++){
   let w=new Map(state);w.set(1,j%2);w.set(64,j%3);w.set(1000000,j);w.set(300,j+3);
   if(!u)w.set(17,j%2);
   test(certify(anchor.trace,raw,w),"dead cells allow reuse");
   let guest=run(raw,w);test(guest.label===anchor.label&&JSON.stringify(guest.trace)===JSON.stringify(anchor.trace),"same observed suffix");
   positive++;
  }
  for(let a of u?[8,17,19]:[8,19]){
   let w=new Map(state);w.set(a,(w.get(a)||0)^1);
   test(!certify(anchor.trace,raw,w),"live in must block");negative++;
  }
  let changed=raw.slice(0,-2)+"1\n";
  test(!certify(anchor.trace,changed,state),"changed input must block");inputReject++;
  let fake=anchor.trace.map(e=>e.slice()),k=fake.findIndex(e=>e[0]==="I");fake[k][2]^=1;
  test(JSON.stringify(fake)!==JSON.stringify(run(raw,state).trace),"forged trace replay must reject");forged++;
 }
}
for(let bad of ["","p bad 6 16\n",encode([0,0,0,0]).slice(0,-1)]){
 test(classify(bad)==="MALFORMED","malformed");let mem=new Map([[8,1],[17,0],[19,0]]);
 let a=run(bad,mem);test(a.label==="MALFORMED"&&certify(a.trace,bad,mem),"malformed replay");
}
return {checks,positive,negative,inputReject,forged,originalSources:16,malformed:3};
})();
if(typeof console!=="undefined") console.log(JSON.stringify(lspv505,null,2));
lspv505;