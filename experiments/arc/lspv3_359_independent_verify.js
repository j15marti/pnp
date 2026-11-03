"use strict";
// LSPV-3 359 independently written no-import raw proof-DAG referee.
// Usage: node lspv3_359_independent_verify.js raw.json
const fs=require("fs");
function independentVerify(raw){
 let checks=0;
 function check(flag,msg){checks++;if(!flag)throw Error(msg)}
 const bit=(mask,j)=>Number((BigInt(mask)>>BigInt(j-1))&1n);
 function clauseTrue(c,x){let truth=false;for(const lit of c)truth=truth||(bit(x,Math.abs(lit))===(lit>0?1:0));return truth}
 function localTable(c,scope){let out=0;for(let t=0;t<8;t++){let a=0n;for(let j=0;j<3;j++)if(t>>j&1)a|=1n<<BigInt(scope[j]-1);if(clauseTrue(c,a))out+=2**t}return out}
 function xor3(x){let z=0;for(;x;x>>=1)z^=x&1;return z}
 function checkOne(p){
  let {h,n,m,scopes,rows,sigma,clauses,steps,witnesses,root}=p;
  check(h>=6&&h%2===0&&n===h+2&&m===4*h,"shape");
  check(clauses.length===m&&steps.length===m-1&&witnesses.length===m,"array count");
  const matrix=[];
  for(let v=0;v<h;v++){
   let cycL=(v+h-1)%h+1,cycR=v+1,extra=(v===0||v===h/2)?h+1:h+2;
   let support=[cycL,cycR,extra].sort((a,b)=>a-b);
   check(JSON.stringify(support)===JSON.stringify(scopes[v]),"row support");
   let row=0n;for(let x of support)row|=1n<<BigInt(x-1);
   check(rows[v]===row.toString()&&sigma[v]===(v===0?1:0),"row signature");
   matrix.push(row);
   for(let k=0;k<4;k++){
    let c=clauses[4*v+k];
    check(c.length===3&&c.every((z,j)=>Math.abs(z)===support[j]),"source signature");
    let wrong=0;for(let j=0;j<3;j++)if(c[j]<0)wrong|=1<<j;
    check(xor3(wrong)!==sigma[v],"source wrong parity");
    for(let a=0;a<8;a++){
      let x=0n;for(let j=0;j<3;j++)if(a>>j&1)x|=1n<<BigInt(support[j]-1);
      check(clauseTrue(c,x)===(a!==wrong),"local canonical clause")
    }
   }
  }
  for(let j=1;j<=n;j++){let freq=0;for(const row of matrix)freq+=bit(row,j);check(freq%2===0,"even incidence")}
  const bank=new Map();
  for(let k=0;k<m;k++)bank.set(k+1,{kind:"clause",cl:clauses[k]});
  for(let k=0;k<steps.length;k++){
    let s=steps[k];
    check(s.id===m+k+1&&s.parents.length===2&&s.parents.every(t=>t<s.id&&bank.has(t)),"indexed proof");
    let [p1,p2]=s.parents.map(t=>bank.get(t));
    if(s.rule==="AND3"){
      check(s.scope.length===3&&new Set(s.scope).size===3,"conjunction support");
      function tab(x){
        if(x.kind==="clause")return localTable(x.cl,s.scope);
        if(x.kind==="factor"&&JSON.stringify(x.vars)===JSON.stringify(s.scope))return x.truth;
        return null;
      }
      let x=tab(p1),y=tab(p2);check(x!==null&&y!==null&&s.truth===(x&y),"checked conjunction");
      if(s.row){
        let mask=0n;for(let v of s.scope)mask|=1n<<BigInt(v-1);
        check(s.row[0]===mask.toString(),"affine row mask");
        for(let a=0;a<8;a++)check(((s.truth>>a)&1)===(xor3(a)===s.row[1]?1:0),"affine row exact");
        bank.set(s.id,{kind:"row",mask,charge:s.row[1]});
      }else bank.set(s.id,{kind:"factor",vars:s.scope,truth:s.truth});
    }else if(s.rule==="XOR"){
      check(p1.kind==="row"&&p2.kind==="row","valid row parents");
      check(s.row[0]===(p1.mask^p2.mask).toString()&&s.row[1]===(p1.charge^p2.charge),"affine addition");
      bank.set(s.id,{kind:"row",mask:BigInt(s.row[0]),charge:s.row[1]});
    }else throw Error("unauthorized rule");
  }
  const last=bank.get(root);check(last?.kind==="row"&&last.mask===0n&&last.charge===1,"contradiction");
  for(let k=0;k<m;k++){
    let witness=BigInt(witnesses[k]);
    for(let j=0;j<m;j++)check(clauseTrue(clauses[j],witness)===(j!==k),"one deleted clause");
    for(let r=0;r<3;r++){
      let changed=clauses[k].slice();changed[r]*=-1;
      check(clauseTrue(changed,witness),"all sign flips repaired");
    }
  }
  const zero=0n;check(matrix.every(r=>Number([...Array(n).keys()].reduce((acc,j)=>acc^bit(r,j+1)*0,0))===0),"zero-charge SAT witness");
  if(n<=14){let odd=0,even=0;for(let a=0;a<2**n;a++){
   let x=BigInt(a);if(clauses.every(c=>clauseTrue(c,x)))odd++;
   let valid=true;for(let v=0;v<h;v++){
    let p=0;for(let j=1;j<=n;j++)if(bit(matrix[v],j))p^=bit(x,j);
    if(p!==0){valid=false;break}
   }if(valid)even++
   }check(odd===0&&even===8,"both-label brute");
  }
 }
 check(raw.id==="LSPV3-EVEN-COLUMN-HYPEREDGE359"&&raw.cases.length===7,"raw fixture");
 for(const c of raw.cases)checkOne(c);
 return {checks,caseCount:raw.cases.length,accepted:true};
}
if(require.main===module){const raw=JSON.parse(fs.readFileSync(process.argv[2],"utf8"));console.log(JSON.stringify(independentVerify(raw),null,2))}
module.exports={independentVerify};
