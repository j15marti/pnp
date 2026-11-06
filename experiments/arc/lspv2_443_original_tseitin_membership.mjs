#!/usr/bin/env node
// LSPV-2/443 independent original-source 3-CNF membership equality replay.
// No third-party dependencies, no SAT hardness claim and no FLMV simulation.
import crypto from 'node:crypto';
let assertions=0;
function check(x,msg){assertions++;if(!x)throw Error(msg||'failed')}
const E=[];
function edge(a,b){E.push([Math.min(a,b),Math.max(a,b)])}
for(let a=0;a<4;a++)for(let b=a+1;b<4;b++)if(a!==0||b!==1)edge(a,b);
edge(0,4);edge(1,4);
for(let a=5;a<9;a++)for(let b=a+1;b<9;b++)if(a!==5||b!==6)edge(a,b);
edge(5,9);edge(6,9);edge(4,9);
E.sort((p,q)=>p[0]-q[0]||p[1]-q[1]);
check(E.length===15);
const B=E.findIndex(e=>e[0]===4&&e[1]===9);check(B>=0);
function quartet(ids,charge){
 const result=[];
 for(let mask=0;mask<8;mask++){
  const a=(mask>>2)&1,b=(mask>>1)&1,c=mask&1;
  if((a^b^c)!==charge)result.push(ids.map((v,j)=>((mask>>(2-j))&1)?-v:v));
 }
 return result;
}
function source(m,u,v,anchor){
 const base=10**(String(100*m+100).length+1),left=[],right=[];
 for(let i=0;i<m;i++)for(let z=0;z<10;z++){
  const ids=E.map((e,j)=>({e,j})).filter(o=>o.e.includes(z)).map(o=>base+100*i+4*o.j+(o.j===B?Number(z<5?u[i]:v[i]):0)).sort((a,b)=>a-b);
  check(ids.length===3);
  (z<5?left:right).push(...quartet(ids,0));
 }
 const common=[],ke=[];
 for(let a=0;a<4;a++)for(let b=a+1;b<4;b++)ke.push([a,b]);
 for(let z=0;z<4;z++)common.push(...quartet(ke.flatMap((e,j)=>e.includes(z)?[j+1]:[]),anchor==='odd'&&z===0?1:0));
 const rows=[...common,...left,...right];
 return 'p cnf '+(2*base)+' '+rows.length+'\n'+rows.map(a=>a.join(' ')+' 0\n').join('');
}
function classify(text){
 const lines=text.trimEnd().split('\n'),h=lines.shift().split(' ');
 if(h.length!==4||h[0]!=='p'||h[1]!=='cnf')return 'MALFORMED';
 const max=Number(h[2]),cnt=Number(h[3]);
 if(!Number.isSafeInteger(max)||!Number.isSafeInteger(cnt)||lines.length!==cnt)return 'MALFORMED';
 const groups=new Map();
 for(const line of lines){
  const xs=line.split(' ').map(Number);
  if(xs.length!==4||xs[3]!==0||xs.slice(0,3).some(v=>!Number.isSafeInteger(v)||v===0||Math.abs(v)>max))return 'MALFORMED';
  const support=xs.slice(0,3).map(Math.abs).sort((a,b)=>a-b);
  if(new Set(support).size!==3)return 'OUTSIDE';
  const key=support.join(',');
  const mask=support.reduce((v,id,j)=>v+((xs.find(x=>Math.abs(x)===id)<0)?(1<<j):0),0);
  const a=groups.get(key)||[];a.push(mask);groups.set(key,a);
 }
 const own=new Map();
 for(const [key,a] of groups){
  if(a.length!==4||new Set(a).size!==4||new Set(a.map(m=>((m&1)+((m>>1)&1)+((m>>2)&1))%2)).size!==1)return 'OUTSIDE';
  for(const id of key.split(',').map(Number))own.set(id,(own.get(id)||0)+1);
 }
 if([...own.values()].some(x=>x!==2))return 'OUTSIDE';
 const grp=[...groups.keys()].map(k=>new Set(k.split(',')));
 for(let i=0;i<grp.length;i++)for(let j=i+1;j<grp.length;j++)
  if([...grp[i]].filter(x=>grp[j].has(x)).length>1)return 'OUTSIDE';
 return 'FAMILY';
}
let cases=0,recognized=0,outside=0,even=0,odd=0;
const expectedLengths=[1027,1887,2748,3608,4468];
for(let m=1;m<=5;m++){
 let prefixes=new Set(),lengths=new Set();
 for(let a=0;a<2**m;a++){
  const u=a.toString(2).padStart(m,'0');
  prefixes.add(source(m,u,'0'.repeat(m),'even').split('\n').slice(0,17+20*m).join('\n'));
  for(let b=0;b<2**m;b++){
   const v=b.toString(2).padStart(m,'0');
   for(const anchor of ['even','odd']){
    const input=source(m,u,v,anchor);
    lengths.add(Buffer.byteLength(input));
    const result=classify(input);
    check(result===(a===b?'FAMILY':'OUTSIDE'),'membership '+m+': '+u+' '+v+' '+anchor);
    if(a===b)recognized++;else outside++;
    cases++;if(anchor==='odd')odd++;else even++;
    if(m===1&&a===0&&b===0&&anchor==='even')
     check(crypto.createHash('sha256').update(input).digest('hex')==='fc7412f95f71071ff34bee79e1145c21bef3d9818c6c5ad7ce9703ff83bc59bb','independent source hash');
   }
  }
 }
 check(prefixes.size===2**m,'prefix separation');check(lengths.size===1,'constant length');
 check([...lengths][0]===expectedLengths[m-1],'length agreement');
}
const s=source(3,'011','011','even');
check(classify(s.replace(' 0\n',' 1\n'))==='MALFORMED','corrupt terminator');
const lines=s.trimEnd().split('\n'),row=lines[1].split(' ');
row[0]=String(-Number(row[0]));lines[1]=row.join(' ');
check(classify(lines.join('\n')+'\n')==='OUTSIDE','wrong source sign');
check(classify(s.replace('p cnf ','p broken '))==='MALFORMED','corrupt header');
check(cases===2728&&recognized===124&&outside===2604&&odd===1364&&even===1364,'counts');
console.log(JSON.stringify({status:'PASS',cases,recognized,outside,even,odd,assertions,lengths:expectedLengths},null,2));