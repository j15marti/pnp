'use strict';
// Independent no-producer-import certificate/signed-marker auditor.
// Usage: node experiments/arc/lspv1_357_independent_verify.js /path/to/raw.json
// This does not verify a theorem of arithmetic, nor SAT-in-P.
const fs=require('fs'),crypto=require('crypto'),assert=require('assert');
const file=process.argv[2]||'LSPV1_GODEL_REFLECTION_B3_FIREWALL357_raw.json';
const dat=JSON.parse(fs.readFileSync(file,'utf8'));
let count=0;
function eq(a,b){count++;assert.deepStrictEqual(a,b);}
function sha(s){return crypto.createHash('sha256').update(s).digest('hex');}
function enc(p){let s='p cnf '+(p.length+1)+' '+(p.length+1)+'\n1 0\n';
for(let i=0;i<p.length;i++)s+=(p[i]==='1'?i+2:-(i+2))+' 0\n';
return s;}
function parse(s){
 if(typeof s!=='string'||!s.endsWith('\n'))return null;
 const lines=s.split('\n').slice(0,-1),header=lines.shift();
 if(!header)return null;
 const h=header.split(' ');
 if(h.length!==4||h[0]!=='p'||h[1]!=='cnf'||!/^(0|[1-9][0-9]*)$/.test(h[2])||!/^(0|[1-9][0-9]*)$/.test(h[3]))return null;
 const n=+h[2],m=+h[3];if(n>20||m>100||lines.length!==m)return null;
 let rows=[];
 for(const line of lines){
  if(!/^-?(0|[1-9][0-9]*)( -?(0|[1-9][0-9]*))*$/.test(line))return null;
  const v=line.split(' ').map(Number);
  if(v.at(-1)!==0||v.slice(0,-1).some(x=>x===0||Math.abs(x)>n))return null;
  rows.push(v.slice(0,-1));
 }
 return {n,rows};
}
function decode(s){
 const p=parse(s);
 if(!p||p.n<1||p.rows.length!==p.n||p.rows[0].length!==1||p.rows[0][0]!==1)return null;
 let bits='';
 for(let i=1;i<p.n;i++){
  if(p.rows[i].length!==1||Math.abs(p.rows[i][0])!==i+1)return null;
  bits+=p.rows[i][0]>0?'1':'0';
 }
 return enc(bits)===s?bits:null;
}
function label(s){
 const p=parse(s);
 if(!p)return 'MALFORMED';
 for(let mask=0;mask<2**p.n;mask++){
  if(p.rows.every(row=>row.some(l=>Boolean(mask & (2**(Math.abs(l)-1)))===(l>0))))return 'SAT';
 }
 return 'UNSAT';
}
function wrap(s,check){const p=decode(s);return p!==null&&check(p)?'UNSAT':label(s);}
const seen=new Set();
for(const row of dat.markers){
 const s=enc(row.p);eq(s.length*8,row.N_bits);eq(sha(s),row.sha256);
 eq(decode(s),row.p);eq(label(s),'SAT');eq(wrap(s,()=>false),'SAT');
 eq(wrap(s,p=>p==='101'),row.hostile_label);seen.add(row.p);
}
eq(seen.size,127);eq(dat.marker_count,127);eq(dat.hostile_error_p,['101']);
for(const c of dat.controls){
 eq(sha(c.text),c.sha256);eq(label(c.text),c.expected);
 eq(decode(c.text)!==null,c.recognized);eq(wrap(c.text,()=>false),c.expected);
}
const target=enc('101'),altered=target.replace('2 0','2 3 0');
eq(decode(altered),null);eq(label(altered),'SAT');eq(wrap(altered,p=>p==='101'),'SAT');
eq(wrap(target,p=>p==='101'),'UNSAT');eq(label(target),'SAT');
console.log(JSON.stringify({independent_assertions:count,marker_cases:dat.markers.length,
  additional_fixtures:dat.controls.length,status:'PASS'}));
