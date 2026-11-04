// LSPV-1/392 finite controls: node experiments/arc/lspv1_392_php_patch.js
"use strict";
function php(h) {
  const v=h*(h+1), m=(h+1)+h*(h+1)*h/2, lines=["p cnf "+v+" "+m], id=(p,j)=>p*h+j+1;
  for(let p=0;p<=h;p++) lines.push(Array.from({length:h},(_,j)=>id(p,j)).join(" ")+" 0");
  for(let j=0;j<h;j++) for(let p=0;p<=h;p++) for(let q=p+1;q<=h;q++)
    lines.push("-"+id(p,j)+" -"+id(q,j)+" 0");
  return lines.join("\n")+"\n";
}
function recognized(s) {
  const a=/^p cnf ([0-9]+) ([0-9]+)\n/.exec(s); if(!a) return false;
  const v=Number(a[1]),m=Number(a[2]); if(!Number.isSafeInteger(v)||!Number.isSafeInteger(m)) return false;
  for(let h=1;h<=s.length&&h*(h+1)<=v;h++)
    if(h*(h+1)===v && m===h+1+h*(h+1)*h/2) return php(h)===s;
  return false;
}
function parse(s){
  if(typeof s!=="string"||!s.endsWith("\n")) return null;
  const lines=s.slice(0,-1).split("\n");
  const a=/^p cnf ([1-9][0-9]*) ([1-9][0-9]*)$/.exec(lines[0]);
  if(!a) return null;
  const v=Number(a[1]),m=Number(a[2]);
  if(!Number.isSafeInteger(v)||!Number.isSafeInteger(m)||v>20||m!==lines.length-1) return null;
  const cls=[];
  for(const line of lines.slice(1)){
    if(!/^-?[1-9][0-9]*( -?[1-9][0-9]*)* 0$/.test(line)) return null;
    const c=line.split(" ").slice(0,-1).map(Number);
    if(c.some(x=>Math.abs(x)>v)) return null;
    cls.push(c);
  }
  return {v,cls};
}
function countModels(p){
  let found=0;
  for(let a=0;a<(1<<p.v);a++)
    if(p.cls.every(c=>c.some(l=>!!(a&(1<<(Math.abs(l)-1)))===(l>0)))) found++;
  return found;
}
function label(s){const p=parse(s);return !p?"MALFORMED":countModels(p)?"SAT":"UNSAT";}
function patch(s){return recognized(s)?"UNSAT":label(s);}
function produce(){
  let checks=0;const cases=[],lookalikes=[];
  for(const h of [1,2,3]){
    const s=php(h),p=parse(s);if(!p||!recognized(s))throw Error("canonical not parsed");checks+=2;
    if(countModels(p)!==0||patch(s)!=="UNSAT")throw Error("bad canonical label");checks+=2;
    let flips=0;
    for(let i=0;i<p.cls.length;i++)for(let j=0;j<p.cls[i].length;j++){
      const a=p.cls.map(c=>c.slice());a[i][j]*=-1;
      if(countModels({v:p.v,cls:a})===0)throw Error("SAT polarity neighbor failed");checks++;flips++;
    }
    cases.push({h,variables:p.v,clauses:p.cls.length,signs:flips,SAT_sign_flips:flips,UNSAT_models:0,input_bits:8*s.length});
    const arr=s.split("\n");[arr[1],arr[2]]=[arr[2],arr[1]];
    const changed=arr.join("\n");
    if(recognized(changed)||patch(changed)!=="UNSAT")throw Error("noncanonical UNSAT");
    checks+=2;lookalikes.push({h,canonical:false,label:"UNSAT"});
    const s2="p cnf 1 1\n1 0\n";
    if(patch(s2)!=="SAT")throw Error("SAT sentinel");checks++;
  }
  const bad=["","p cnf 1 1\n1\n","p cnf 1 1\n2 0\n",
    "p cnf 1 1\n1 0\n1 0\n","p cnf 1 1\n-1 0\nx\n",
    "p cnf 0 1\n1 0\n","p cnf 1 1\n0\n","p cnf 1 1\n1 0"];
  for(const x of bad){if(patch(x)!=="MALFORMED"||recognized(x))throw Error("malformed");
    checks+=2;}
  const neg="p cnf 1 2\n1 0\n-1 0\n";
  if(patch(neg)!=="UNSAT"||recognized(neg))throw Error("ordinary UNSAT");
  checks+=2;
  return {schema:"LSPV1-392-v1",model:"ordinary shared-DAG Resolution; logic tests, not time measurements",
    cases,lookalikes,malformed_rejections:bad.length,checks,seed:null};
}
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module)
  process.stdout.write(JSON.stringify(produce(),null,2)+"\n");
