#!/usr/bin/env node
// Independent standard-library verifier for REFEREE376 raw controls.
import fs from 'node:fs';
import crypto from 'node:crypto';

const path = process.argv[2] || 'results/raw/review/2026-11-05_1958_LSPV5_STRICT3_REFLECTION376.json';
const d = JSON.parse(fs.readFileSync(path, 'utf8'));
let checks = 0;
const ok = (b, m) => { if (!b) throw new Error(m); checks++; };
const sha = s => crypto.createHash('sha256').update(s).digest('hex');

function parse(text) {
  const ls = text.split(/\r?\n/).map(x=>x.trim()).filter(x=>x && !x.startsWith('c'));
  if (!ls.length) return null;
  const h=ls[0].split(/\s+/); if(h.length!==4||h[0]!=='p'||h[1]!=='cnf') return null;
  const nv=Number(h[2]), nc=Number(h[3]); if(!Number.isInteger(nv)||!Number.isInteger(nc)||nv<0||nc<0||ls.length!==nc+1) return null;
  const cs=[];
  for(const line of ls.slice(1)){
    const vs=line.split(/\s+/).map(Number); if(!vs.length||vs.at(-1)!==0||vs.slice(0,-1).some(x=>!Number.isInteger(x)||x===0||Math.abs(x)>nv)) return null;
    cs.push(vs.slice(0,-1));
  }
  return [nv,cs];
}

function parity(vs,rhs){
  const out=[];
  for(let mask=0;mask<8;mask++){
    const a=[(mask>>2)&1,(mask>>1)&1,mask&1];
    if(((a[0]+a[1]+a[2])&1)!==rhs) out.push(vs.map((v,i)=>a[i]?-v:v));
  }
  return out;
}
function block(off,charge=[0,0,0,0]){
  const [a,b,c,d,e,f]=[1,2,3,4,5,6].map(x=>x+off);
  return [[a,b,c],[a,d,e],[b,d,f],[c,e,f]].flatMap((row,i)=>parity(row,charge[i]));
}
function recognize(p){
  if(!p) return null; const [nv,cs]=p; if(!nv||nv%6||cs.length!==(nv/6)*16)return null;
  let bits='';
  for(let i=0;i<nv/6;i++){
    const z=block(6*i), o=z.map(x=>[...x]); [o[0],o[1]]=[o[1],o[0]];
    const got=JSON.stringify(cs.slice(16*i,16*i+16));
    if(got===JSON.stringify(z)) bits+='0'; else if(got===JSON.stringify(o)) bits+='1'; else return null;
  }
  return bits;
}
function evalCnf(cs,a){return cs.every(c=>c.some(l=>((a[Math.abs(l)-1]===1)===(l>0))))}

ok(d.artifact==='LSPV5_REFEREE376_STRICT3_REFLECTION_FIREWALL','artifact');
for(const r of d.records){
  ok(sha(r.dimacs)===r.sha256,'source hash');
  const p=parse(r.dimacs); ok(!!p,'parse');
  ok(p[0]===r.variables&&p[1].length===r.clauses,'counts');
  ok(recognize(p)===r.proof_code,'code');
  ok(p[1].every(c=>c.length===3&&new Set(c.map(Math.abs)).size===3),'strict3');
  ok(evalCnf(p[1],Array(p[0]).fill(0)),'zero witness');
  ok(r.consistent_wrapper==='SAT','consistent wrapper');
  ok(r.hostile_toy_wrapper===(r.proof_code==='101'?'UNSAT':'SAT'),'toy trigger');
}
const op=parse(d.odd_k4_control.dimacs); ok(!!op,'odd parse');
ok(sha(d.odd_k4_control.dimacs)===d.odd_k4_control.sha256,'odd hash');
ok(recognize(op)===null,'odd not special');
let models=0; for(let m=0;m<64;m++){const a=Array.from({length:6},(_,i)=>(m>>i)&1); if(evalCnf(op[1],a))models++;}
ok(models===0&&d.odd_k4_control.label==='UNSAT','odd exact unsat');
console.log(JSON.stringify({verified:path,checks,raw_sha256:sha(fs.readFileSync(path))}));
