#!/usr/bin/env node
/* Independent verifier, no producer import; run: node FILE DIR */
'use strict';
const fs=require('fs'),path=require('path');
let assertions=0,rejected=0,verified=0;
function ok(c,msg){assertions++;if(!c)throw Error(msg||'assertion failed')}
function eq(a,b){return JSON.stringify(a)===JSON.stringify(b)}
function bit(k){return 1n<<BigInt(k-1)}
function par(x){let r=0;while(x){x&=x-1n;r^=1}return r}
function solve(rows,n){
 const A=rows.map(r=>({...r})),piv=[];let k=0;
 for(let c=1;c<=n;c++){
  let j=k;while(j<A.length&&(A[j].mask&bit(c))===0n)j++;
  if(j===A.length)continue;
  [A[j],A[k]]=[A[k],A[j]];
  for(let i=0;i<A.length;i++)if(i!==k&&(A[i].mask&bit(c))!==0n){A[i].mask^=A[k].mask;A[i].rhs^=A[k].rhs}
  piv.push(c);k++;
 }
 if(A.some(r=>r.mask===0n&&r.rhs))return null;
 let ans=0n;for(let i=0;i<piv.length;i++)if(A[i].rhs)ans|=bit(piv[i]);
 ok(rows.every(r=>par(ans&r.mask)===r.rhs),'GF2 incorrect witness');
 return ans;
}
function verify(x){
 const V=x.vertices,n=x.nvariables,E=x.edges;
 ok(V>=4&&V%2===0&&E.length===n&&2*n===3*V,'cubic counts');
 ok(x.charge.length===V&&x.charge.every(v=>v===0||v===1),'charge syntax');
 ok(x.charge.reduce((a,b)=>a^b,0)===1,'odd charge');
 const inc=Array.from({length:V},()=>[]);
 E.forEach((e,j)=>{
   const [a,b]=e;ok(Number.isInteger(a)&&0<=a&&a<b&&b<V,'edge syntax');
   inc[a].push(j+1);inc[b].push(j+1);
 });
 ok(inc.every(a=>a.length===3),'3 regular');
 ok(new Set(E.map(e=>e.join(','))).size===E.length,'simple graph');
 function connected(skip){
  const seen=new Set([0]),stk=[0];
  while(stk.length){const a=stk.pop();E.forEach(([u,v],j)=>{
    if(j===skip)return;const b=(u===a?v:(v===a?u:-1));
    if(b>=0&&!seen.has(b)){seen.add(b);stk.push(b)}
  })}
  return seen.size===V;
 }
 ok(connected(-1),'connected graph');
 for(let j=0;j<n;j++)ok(connected(j),'bridgeless graph');
 const m=x.sources.length,q=x.nodes.length;
 ok(m===4*V&&q===m-1,'source and derivation counts');
 const D=new Map();
 for(let i=0;i<m;i++){
  const s=x.sources[i];
  ok(s.id==='s'+i&&s.type==='SRC'&&Number.isInteger(s.v)&&s.v>=0&&s.v<V,'source ID');
  ok(eq(s.lits.map(Math.abs),inc[s.v]),'signed source support');
  const wrong=s.lits.reduce((a,l)=>a^(l<0?1:0),0);
  ok(wrong!==x.charge[s.v],'signed wrong parity');
  D.set(s.id,{...s,depth:0});
 }
 for(let v=0;v<V;v++){
  const p=x.sources.filter(s=>s.v===v).map(s=>s.lits.map(l=>Number(l<0)).join(''));
  ok(p.length===4&&new Set(p).size===4,'all 4 parity blockers');
 }
 const str='p cnf '+n+' '+m+'\n'+x.sources.map(s=>s.lits.join(' ')+' 0\n').join('');
 ok(x.dimacs===str&&x.claimed.dimacs_utf8_bits===8*Buffer.byteLength(str),'encoded source authentic');
 for(let i=0;i<q;i++){
  const z=x.nodes[i];
  ok(z.id==='d'+i&&!D.has(z.id),'unique topological ID');
  ok(z.parents.length===2&&z.parents[0]!==z.parents[1]&&z.parents.every(j=>D.has(j)),'exact two valid parents');
  const [a,b]=z.parents.map(j=>D.get(j)),depth=1+Math.max(a.depth,b.depth);
  if(z.type==='AND3'){
   ok(a.v===z.vertex||a.vertex===z.vertex,'first local factor');
   ok(b.v===z.vertex||b.vertex===z.vertex,'second local factor');
   function val(t,k){
    if(t.type==='AND3')return t.table[k];
    return Number(t.lits.some((l,j)=>((k>>j)&1)===Number(l>0)));
   }
   const table=Array.from({length:8},(_,k)=>val(a,k)&val(b,k));
   ok(eq(z.table,table),'correct AND3 table');
   if(z.alias){
    ok(eq(z.alias.mask,inc[z.vertex])&&z.alias.rhs===x.charge[z.vertex],'verified parity alias');
    for(let k=0;k<8;k++)ok(z.table[k]===Number((par(BigInt(k)))===z.alias.rhs),'truth-table equivalence');
   }
   D.set(z.id,{...z,depth});
  }else if(z.type==='XOR'){
   const ra=a.row||a.alias,rb=b.row||b.alias;
   ok(!!ra&&!!rb,'authenticated row parents');
   const mask=ra.mask.filter(k=>!rb.mask.includes(k)).concat(rb.mask.filter(k=>!ra.mask.includes(k))).sort((p,r)=>p-r);
   ok(eq(z.row.mask,mask)&&z.row.rhs===(ra.rhs^rb.rhs),'correct GF2 XOR');
   D.set(z.id,{...z,depth});
  }else throw Error('illegal derived node');
 }
 const root=D.get(x.root);
 ok(!!root&&root.type==='XOR'&&eq(root.row,{mask:[],rhs:1}),'false root');
 const lower=Math.ceil(Math.log2(m));
 ok(root.depth===lower&&x.claimed.depth===lower&&x.claimed.lower_depth===lower,'exact balanced depth');
 const ancestry=new Set(),stack=[x.root];
 while(stack.length){const a=stack.pop();if(ancestry.has(a))continue;ancestry.add(a);
  if(a[0]==='d')stack.push(...x.nodes[Number(a.slice(1))].parents);
 }
 ok(x.sources.every(s=>ancestry.has(s.id)),'complete source ancestry');
 const rows=inc.map((edgeNumbers,v)=>({mask:edgeNumbers.reduce((m,k)=>m|bit(k),0n),rhs:x.charge[v]}));
 ok(solve(rows,n)===null,'odd charge is UNSAT');
 const even=rows.map((r,j)=>({mask:r.mask,rhs:r.rhs^(j===0?1:0)}));
 ok(solve(even,n)!==null,'matched even charge SAT');
 function satClause(s,assignment){return s.lits.some(l=>l>0?((assignment&bit(l))!==0n):((assignment&bit(-l))===0n))}
 for(const C of x.sources){
  const sub=rows.filter((_,v)=>v!==C.v);
  for(const lit of C.lits)sub.push({mask:bit(Math.abs(lit)),rhs:Number(lit<0)});
  const witness=solve(sub,n);
  ok(witness!==null,'deletion witness exists');
  ok(!satClause(C,witness),'deletion witness falsifies only deleted clause');
  for(const s of x.sources)if(s.id!==C.id)ok(satClause(s,witness),'all remaining source clauses SAT');
 }
 if(n<=12){
  let odd=0,evenModels=0;
  for(let a=0;a<(1<<n);a++){
   const mask=BigInt(a);
   if(x.sources.every(s=>satClause(s,mask)))odd++;
   if(even.every(r=>par(mask&r.mask)===r.rhs))evenModels++;
  }
  ok(odd===0&&evenModels===(2**(n-V+1)),'exhaustive both-label model count');
 }
 verified++;
 return {name:x.name,m,q,depth:root.depth,dimacs_bits:x.claimed.dimacs_utf8_bits};
}
function reject(obj,mutate,name){
 const clone=JSON.parse(JSON.stringify(obj));mutate(clone);
 try{verify(clone);throw Error('accepted corrupted '+name)}
 catch(e){if(e.message.startsWith('accepted corrupted'))throw e;rejected++}
}
const dir=process.argv[2];if(!dir)throw Error('directory needed');
const rows=[];
for(const name of ['K4','K33','Cube','Prism3','Prism6','Prism16']){
 const x=JSON.parse(fs.readFileSync(path.join(dir,'certificate_'+name+'.json'),'utf8'));
 rows.push(verify(x));
 reject(x,c=>c.nodes[c.nodes.length-1].row.rhs^=1,'false root');
 reject(x,c=>c.nodes[0].table[0]^=1,'wrong factor');
 reject(x,c=>c.sources[0].lits[0]*=-1,'wrong source sign');
 reject(x,c=>c.nvariables--,'malformed header');
 reject(x,c=>c.nodes[c.nodes.length-1].parents[0]='d999999','invalid dependency');
}
const result={status:'COMPUTATIONAL',assertions,rejected,verified,rows};
fs.writeFileSync(path.join(dir,'independent_results.json'),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result,null,2));
