'use strict';
// LSPV-3/489: executable declared two-input conservative DEF refactoring control.
// Not a historical R_mix341 accepted-byte certificate.
const assert=require('assert');let checks=0;
function ok(x){assert.ok(x);checks++}
const AND=8, MASK=4, XOR=6;
function circuit(g,expanded) {
  let n=2*g+2,steps=[];
  const def=(f,a,b)=>{const id=n+steps.length;steps.push({id,f,a,b});return id;};
  let terms=[];
  if(expanded) {
    for(let i=0;i<g;i++){const a=2+2*i,b=a+1;terms.push(def(XOR,def(AND,a,b),def(MASK,a,b)));}
    terms.push(def(AND,0,1));let y=terms[0];
    for(let i=1;i<terms.length;i++)y=def(XOR,y,terms[i]);
    return {n,steps,y};
  }
  let p=3;for(let i=1;i<g;i++)p=def(XOR,p,3+2*i);
  return {n,steps,y:def(XOR,p,def(AND,0,1))};
}
function valid(c){
  if(!Number.isInteger(c.n)||!Array.isArray(c.steps))throw Error('schema');
  c.steps.forEach((s,i)=>{if(s.id!==c.n+i||![4,6,8].includes(s.f)||!Number.isInteger(s.a)||!Number.isInteger(s.b)||s.a<0||s.b<0||s.a>=s.id||s.b>=s.id)throw Error('DEF provenance');});
  if(c.y<c.n||c.y>=c.n+c.steps.length)throw Error('final');
  return true;
}
function value(c,mask){
  valid(c);const v=[];
  for(let i=0;i<c.n;i++)v[i]=(mask>>>i)&1;
  for(let s of c.steps)v[s.id]=(s.f>>>(v[s.a]+2*v[s.b]))&1;
  return v[c.y];
}
function target(g,m){let y=((m>>>0)&1)&((m>>>1)&1);for(let i=0;i<g;i++)y^=(m>>>(2*i+3))&1;return y}
function rank(rows){const basis={};let n=0;for(let x of rows){while(x){let k=31-Math.clz32(x);if(basis[k])x^=basis[k];else{basis[k]=x;n++;break}}}return n}
let rows=[];
for(let g=1;g<=8;g++){
  const e=circuit(g,true),s=circuit(g,false);ok(e.steps.length===4*g+1);ok(s.steps.length===g+1);
  let cases=g<=6?(1<<(2*g+2)):4096;
  for(let i=0;i<cases;i++){
    let m=g<=6?i:(Math.imul(i+1,0x9e3779b1)^Math.imul(i+7,0x85ebca6b))>>>0;
    ok(value(e,m)===target(g,m));ok(value(s,m)===target(g,m));
  }
  let minRank=null,choices=0;
  if(g<=4)for(let bits=0;bits<1<<(2*g+1);bits++){
    let a=[];for(let i=0;i<g;i++)for(let j=0;j<2;j++)a.push(1<<(2+2*i+((bits>>>(2*i+j))&1)));
    a.push(1<<((bits>>>(2*g))&1));
    let r=rank(a);minRank=minRank===null?r:Math.min(r,minRank);choices++;ok(r>=g+1);
  }
  if(g<=4)ok(minRank===g+1);
  ok((target(g,0)^target(g,1)^target(g,2)^target(g,3))===1);
  rows.push({g,paidExpanded:e.steps.length,paidFactored:s.steps.length,anchorRankMinimum:minRank,anchorChoices:choices,assignments:cases});
}
let hostile=0,base=circuit(2,true);
for(let change of [c=>c.steps[0].id=777,c=>c.steps[0].a=c.steps[0].id,c=>c.steps[1].f=255]){
  const c=JSON.parse(JSON.stringify(base));change(c);try{valid(c)}catch{hostile++}
}
ok(hostile===3);
// Original-source odd/even K4 signed 3CNF control.
const E=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
function cnf(ch){let F=[];for(let v=0;v<4;v++){let I=E.map((e,i)=>e.includes(v)?i:-1).filter(i=>i>=0);
for(let z=0;z<8;z++)if(((z&1)^((z>>1)&1)^((z>>2)&1))!==ch[v])F.push(I.map((j,k)=>((z>>k)&1)?-(j+1):j+1));}return F;}
function models(F){let n=0;for(let a=0;a<64;a++)if(F.every(C=>C.some(l=>l>0?((a>>(l-1))&1)===1:((a>>(-l-1))&1)===0)))n++;return n}
const odd=cnf([1,0,0,0]),even=cnf([0,0,0,0]);ok(odd.length===16&&even.length===16);ok(models(odd)===0&&models(even)===8);
for(let i=0;i<odd.length;i++)ok(models(odd.filter((_,j)=>i!==j))>0);
console.log(JSON.stringify({kind:'LSPV3-489-DECLARED-DEF',rows,assertions:checks,hostileRejected:hostile,K4:{oddClauses:16,oddModels:0,evenModels:8,indispensableClauses:16},status:'restricted; historical R_mix341 OPEN',pVsNP:'OPEN'},null,2));
