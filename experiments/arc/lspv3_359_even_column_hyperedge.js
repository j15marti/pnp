"use strict";
// LSPV-3 EVEN-COLUMN HYPEREDGE359. Usage: node lspv3_359_even_column_hyperedge.js [raw.json]
const fs=require("fs");
function research(){
 let checks=0;const ck=(v,m)=>{checks++;if(!v)throw Error(m)};
 const pc=x=>{let n=0;for(x=BigInt(x);x;x&=x-1n)n++;return n},px=x=>pc(x)%2;
 const rank=aa=>{const p=new Map();for(let x of aa){x=BigInt(x);while(x){let k=x.toString(2).length-1;if(p.has(k))x^=p.get(k);else{p.set(k,x);break}}}return p.size};
 function solve(aa,bb){let p=new Map();for(let i=0;i<aa.length;i++){let x=BigInt(aa[i]),b=bb[i];while(x){let k=x.toString(2).length-1;if(p.has(k)){let z=p.get(k);x^=z[0];b^=z[1]}else{p.set(k,[x,b]);break}}if(!x&&b)return null}let x=0n;for(let k of [...p.keys()].sort((a,b)=>a-b)){let [a,b]=p.get(k);if(b^px(a&x))x|=1n<<BigInt(k)}ck(aa.every((a,i)=>px(BigInt(a)&x)===bb[i]),"linear witness");return x}
 const sat=(cl,x)=>cl.some(l=>Number(x>>BigInt(Math.abs(l)-1)&1n)===(l>0?1:0));
 const table=(cl,s)=>{let t=0;for(let a=0;a<8;a++){let x=0n;for(let j=0;j<3;j++)if(a>>j&1)x|=1n<<BigInt(s[j]-1);if(sat(cl,x))t|=1<<a}return t};
 function parse(s){const lines=s.trim().split(/\r?\n/).filter(t=>t&&!t.startsWith("c"));if(!/^p cnf \d+ \d+$/.test(lines[0]))throw Error("header");let z=lines[0].split(" "),n=+z[2],m=+z[3],c=[];for(let line of lines.slice(1)){line=line.trim();if(!/^-?\d+( -?\d+)*$/.test(line))throw Error("token");let a=line.split(/\s+/).map(Number);if(a.at(-1)!==0||a.slice(0,-1).some(x=>!x||Math.abs(x)>n))throw Error("literal");c.push(a.slice(0,-1))}if(c.length!==m)throw Error("count");return c}
 function build(h){ck(h>=6&&h%2===0,"h");const n=h+2,S=[],R=[],sigma=Array(h).fill(0);sigma[0]=1;
  for(let i=0;i<h;i++){let s=[(i+h-1)%h+1,i+1,i===0||i===h/2?h+1:h+2].sort((a,b)=>a-b);S.push(s);R.push(s.reduce((a,j)=>a|1n<<BigInt(j-1),0n))}
  ck(rank(R)===h-1,"rank");for(let i=0;i<n;i++)ck(R.reduce((a,r)=>a+((r>>BigInt(i))&1n),0n)%2n===0n,"even column");
  for(let i=0;i<h;i++)ck(rank(R.filter((_,j)=>i!==j).map(r=>r&(((1n<<BigInt(n))-1n)^R[i])))===h-2,"punctured rank");
  ck(solve(R,sigma)===null&&solve(R,Array(h).fill(0))===0n,"odd/even");
  const clauses=[],owners=[];for(let i=0;i<h;i++)for(let a=0;a<8;a++)if(pc(BigInt(a))%2!==sigma[i]){clauses.push(S[i].map((q,j)=>a>>j&1?-q:q));owners.push(i)}
  let m=clauses.length;ck(m===4*h,"clause count");const witnesses=[];
  for(let i=0;i<m;i++){let a=R.filter((_,j)=>j!==owners[i]),b=sigma.filter((_,j)=>j!==owners[i]);
   for(let l of clauses[i]){a.push(1n<<BigInt(Math.abs(l)-1));b.push(l<0?1:0)}
   let x=solve(a,b);ck(x!==null,"deletion SAT");for(let j=0;j<m;j++)ck(sat(clauses[j],x)===(j!==i),"unique bad clause");
   for(let l of clauses[i])ck(sat(clauses[i].map(z=>z===l?-z:z),x),"sign repair");witnesses.push(x.toString())}
  const steps=[],local=[];let next=m;
  for(let i=0;i<h;i++){let last=4*i+1,t=255;for(let j=1;j<4;j++){t=(j===1?table(clauses[4*i],S[i]):t)&table(clauses[4*i+j],S[i]);let st={id:++next,rule:"AND3",parents:[last,4*i+j+1],scope:S[i],truth:t};if(j===3)st.row=[R[i].toString(),sigma[i]];steps.push(st);last=st.id}local.push(last)}
  let mask=R[0],bit=sigma[0],last=local[0];for(let i=1;i<h;i++){mask^=R[i];bit^=sigma[i];let st={id:++next,rule:"XOR",parents:[last,local[i]],row:[mask.toString(),bit]};steps.push(st);last=st.id}
  ck(mask===0n&&bit===1&&steps.length===m-1,"final proof");
  let dimacs="p cnf "+n+" "+m+"\n"+clauses.map(c=>c.join(" ")+" 0\n").join("");ck(parse(dimacs).length===m,"input parsed");
  if(n<=14){let o=0,e=0;for(let a=0;a<2**n;a++){let x=BigInt(a);o+=+clauses.every(c=>sat(c,x));e+=+R.every(r=>px(r&x)===0)}ck(o===0&&e===8,"brute labels")}
  return {h,n,m,Nbits:dimacs.length*8,scopes:S,rows:R.map(String),sigma,clauses,steps,root:last,witnesses,evenModels:8}
 }
 // Independent source reconstruction and inference replay, without trusting generator's labels.
 function verify(A){try{
  let {h,n,m,scopes,rows,sigma,clauses,steps,root,witnesses}=A;if(n!==h+2||m!==4*h||clauses.length!==m||steps.length!==m-1)return false;
  for(let i=0;i<h;i++){let s=[(i+h-1)%h+1,i+1,i===0||i===h/2?h+1:h+2].sort((a,b)=>a-b),r=s.reduce((a,j)=>a|1n<<BigInt(j-1),0n);
   if(JSON.stringify(s)!==JSON.stringify(scopes[i])||rows[i]!==String(r)||sigma[i]!==+(i===0))return false;let cl=[];for(let a=0;a<8;a++)if(pc(BigInt(a))%2!==sigma[i])cl.push(s.map((q,j)=>a>>j&1?-q:q));if(JSON.stringify(cl)!==JSON.stringify(clauses.slice(4*i,4*i+4)))return false}
  let db=new Map();clauses.forEach((c,i)=>db.set(i+1,{type:"CLAUSE",c}));
  for(let i=0;i<steps.length;i++){let st=steps[i];if(st.id!==m+i+1||st.parents.length!==2||st.parents.some(p=>p>=st.id||!db.has(p)))return false;
   let [a,b]=st.parents.map(p=>db.get(p));
   if(st.rule==="AND3"){if(a.type==="ROW"||b.type==="ROW"||st.scope.length!==3)return false;let f=x=>x.type==="CLAUSE"?table(x.c,st.scope):(JSON.stringify(st.scope)===JSON.stringify(x.scope)?x.truth:null);let u=f(a),v=f(b);if(u===null||v===null||st.truth!==(u&v))return false;
    if(st.row){let mask=st.scope.reduce((z,q)=>z|1n<<BigInt(q-1),0n),bit=st.row[1];if(st.row[0]!==mask.toString())return false;for(let j=0;j<8;j++)if((st.truth>>j&1)!==+(pc(BigInt(j))%2===bit))return false;db.set(st.id,{type:"ROW",mask,bit})}
    else db.set(st.id,{type:"FACTOR",scope:st.scope,truth:st.truth});
   }else if(st.rule==="XOR"){if(a.type!=="ROW"||b.type!=="ROW"||st.row[0]!==String(a.mask^b.mask)||st.row[1]!==(a.bit^b.bit))return false;db.set(st.id,{type:"ROW",mask:BigInt(st.row[0]),bit:st.row[1]})}
   else return false}
  let last=db.get(root);if(!last||last.type!=="ROW"||last.mask!==0n||last.bit!==1||witnesses.length!==m)return false;
  for(let i=0;i<m;i++){let x=BigInt(witnesses[i]);for(let j=0;j<m;j++)if(sat(clauses[j],x)!==(i!==j))return false;for(let l of clauses[i])if(!sat(clauses[i].map(q=>q===l?-q:q),x))return false}return true;
 }catch(e){return false}}
 const cases=[];for(let h of [6,8,10,12,16,24,32]){let a=build(h);ck(verify(a),"proof replay");cases.push(a)}
 const deep=a=>JSON.parse(JSON.stringify(a));for(let f of [a=>a.steps[0].truth^=1,a=>a.steps[0].parents[0]=99999,a=>a.steps.at(-1).row[1]=0,a=>a.clauses[0][0]*=-1,a=>a.witnesses[0]="1"]){let a=deep(cases[0]);f(a);ck(!verify(a),"corruption")}
 for(let txt of ["p cnf a 1\n1 0","p cnf 2 2\n1 0","p cnf 2 1\n3 0","p cnf 2 1\n1","p cnf 2 1\n1 0\np cnf 2 1"]){let bad=false;try{parse(txt)}catch(e){bad=true}ck(bad,"malformed")}
 const summary={assertions:checks,cases:cases.map(a=>({h:a.h,variables:a.n,clauses:a.m,bits:a.Nbits,exactMinimum:a.steps.length,highDegree:a.h-2,rawCaseBytes:JSON.stringify(a).length})),
   controls:"odd UNSAT/even SAT 8 models; all deletions/sign flips; 5 corrupted; 5 malformed"};
 return {summary,raw:{id:"LSPV3-EVEN-COLUMN-HYPEREDGE359",system:"unchanged Rmix341",status:"PROVED/EXACT symbolic, COMPUTATIONAL finite verifier",summary,cases}};
}
if(require.main===module){let o=research();if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(o.raw,null,2)+"\n");console.log(JSON.stringify(o.summary,null,2))}
module.exports={research};
