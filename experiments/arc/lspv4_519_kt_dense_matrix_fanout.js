'use strict';
// Independent source, linear-equation and component-matrix construction control.
// Not a native FLMV machine, topological diagram checker, or R_mix341 proof checker.
const assert=require('node:assert/strict');
const crypto=require('node:crypto');
const MAGIC='10110110';
let assertions=0;
const sha=(s)=>crypto.createHash('sha256').update(s).digest('hex');
function graphs(){
  let k4=[],cube=[],prism3=[],prism5=[];
  for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)k4.push([i,j]);
  for(let i=0;i<8;i++)for(let j=i+1;j<8;j++){let t=i^j;if(t && (t&(t-1))===0)cube.push([i,j]);}
  const prism=(t)=>{let edge=new Map();for(let z=0;z<2;z++)for(let i=0;i<t;i++){const pair=[z*t+i,z*t+(i+1)%t].sort((a,b)=>a-b);edge.set(pair.join(','),pair)}for(let i=0;i<t;i++)edge.set(i+','+(t+i),[i,t+i]);return [...edge.values()].sort((a,b)=>a[0]-b[0]||a[1]-b[1])};
  prism3=prism(3);prism5=prism(5);
  return [['K4',k4,3],['prism3',prism3,4],['cube',cube,5],['prism5',prism5,6]];
}
function encode(edges,charges){
  const h=charges.length, e=edges.length, w=Math.ceil(Math.log2(e+1));
  let out=MAGIC+'1'.repeat(e)+'0', constraints=[];
  const forbidden=[[0,0,1],[0,1,0],[1,0,0],[1,1,1]];
  for(let v=0;v<h;v++){
    let around=[];edges.forEach(([a,b],idx)=>{if(v===a||v===b)around.push(idx+1)});
    assert.equal(around.length,3);assertions++;
    constraints.push({around,charge:charges[v]});
    for(const [p,s,t] of forbidden){let signs=[p^charges[v],s,t];for(let j=0;j<3;j++)out+=around[j].toString(2).padStart(w,'0')+signs[j];}
  }
  return [out+'01',constraints];
}
function isSolvableGF2(rows,variables){
  let equations=rows.map(({around,charge})=>{let a=new Uint8Array(variables+1);for(let id of around)a[id-1]^=1;a[variables]=charge;return a});
  let pivotRow=0;
  for(let col=0;col<variables;col++){
    let pr=pivotRow;while(pr<equations.length && !equations[pr][col])pr++;
    if(pr===equations.length)continue;
    [equations[pr],equations[pivotRow]]=[equations[pivotRow],equations[pr]];
    for(let i=0;i<equations.length;i++)if(i!==pivotRow && equations[i][col])for(let j=col;j<=variables;j++)equations[i][j]^=equations[pivotRow][j];
    pivotRow++;
  }
  return !equations.some(row=>row.slice(0,variables).every(x=>x===0)&&row[variables]===1);
}
function validateBinary(s){
  if(!/^[01]+$/.test(s)||!s.startsWith(MAGIC)||!s.endsWith('01'))return false;
  const i=s.indexOf('0',8);if(i<0)return false;
  const e=i-8;if(e<6||e%3)return false;
  const h=e*2/3,w=Math.ceil(Math.log2(e+1));
  if(s.length!==8+e+1+12*h*(w+1)+2)return false;
  let p=i+1;
  let seen=new Array(e+1).fill(0);
  for(let v=0;v<h;v++){
    let base=null;
    const signs=[];
    for(let f=0;f<4;f++){
      let ids=[],row=[];
      for(let j=0;j<3;j++){const id=parseInt(s.slice(p,p+w),2);p+=w;const sign=Number(s[p++]);ids.push(id);row.push(sign);if(id<1||id>e)return false;}
      if(!base){base=ids;if(new Set(base).size!==3)return false;for(let id of base)seen[id]++}else if(base.some((id,j)=>ids[j]!==id))return false;
      signs.push(row);
    }
    const forbidden=[[0,0,1],[0,1,0],[1,0,0],[1,1,1]];
    if(![0,1].some(c=>signs.every((arr,j)=>arr.join('')===[forbidden[j][0]^c,forbidden[j][1],forbidden[j][2]].join(''))))return false;
  }
  return p===s.length-2&&seen.slice(1).every(x=>x===2);
}
function matrix(e,c){const v=2*e+c;let out='',ones=0;for(let i=0;i<v;i++)for(let j=0;j<v;j++){const one=(i<e&&j===e+i)||(j<e&&i===e+j)?1:0;out+=one;ones+=one;}return {out,ones,v};}
function run(){let records=[];
  for(const [name,edges,k] of graphs()){
    const h=Math.max(...edges.flat())+1,e=edges.length,q=2**k;
    let expectedHash=null,sat=0,unsat=0,firstSource=null;
    for(let d=0;d<q;d++){
      const charges=Array.from({length:h},(_,i)=>i<k?((d>>i)&1):0);
      const [src,rows]=encode(edges,charges);
      if(d===0)firstSource=src;
      assert.equal(validateBinary(src),true);assertions++;
      const label=isSolvableGF2(rows,e);sat+=Number(label);unsat+=Number(!label);
      assert.equal(label,charges.reduce((a,b)=>a^b,0)===0);assertions++;
      const mat=matrix(e,4*h);
      assert.equal(mat.ones,2*e);assertions++;
      if(expectedHash===null)expectedHash=sha(mat.out);
      assert.equal(sha(mat.out),expectedHash);assertions++;
    }
    assert.equal(sat,unsat);assertions++;
    const invalid=[firstSource.slice(0,-1),firstSource+'1','00000000'+firstSource.slice(8),firstSource.slice(0,8)+'1'.repeat(e+1)+firstSource.slice(8+e+1)];
    for(let z of invalid){assert.equal(validateBinary(z),false);assertions++}
    const m=firstSource.length,components=2*e+4*h;
    records.push({graph:name,H:h,edge_variables:e,cnf_clauses:4*h,source_bits:m,formal_N:m*m,virtual_children:q,KT_components:components,full_dense_link_bits:components**2,nonzero_link_bits:2*e,per_child_dense_bits:q*components**2,sat,unsat,source_zero_sha256:sha(firstSource),dense_matrix_sha256:expectedHash});
  }
  return {status:'PASS',assertions,graphs:records,note:'Independent JS GF(2) satisfiability and source-checker; not diagram checker or FLMV simulator'};
}
const result=run();process.stdout.write(JSON.stringify(result,null,2)+'\n');
