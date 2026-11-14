"use strict";
/* TMR-3/007: independently reorders original TMR-2 equality 3-CNF clause blocks.
 * Executable is a source-bit emulator, not an instruction-level Turing machine.
 * The physical linear-time/log-space bound is a separate symbolic construction.
 */
const W=n=>Math.max(1,Math.ceil(Math.log2(Math.max(2,n))));
const bits=(n,w)=>n.toString(2).padStart(w,"0");
function block(n,i,bank,value){
  const w=W(5*n),z=(bank===0?n:3*n)+2*i,sgn=1-value;
  let s="";
  for(let u=0;u<2;u++)for(let v=0;v<2;v++)
    s+=sgn+bits(i,w)+u+bits(z,w)+v+bits(z+1,w);
  return s;
}
function encode(n,a,b,interleaved){
  let s="1".repeat(5*n)+"0"+"1".repeat(8*n)+"0";
  if(interleaved){
    for(let i=0;i<n;i++)s+=block(n,i,0,a[i])+block(n,i,1,b[i]);
  }else{
    for(let i=0;i<n;i++)s+=block(n,i,0,a[i]);
    for(let i=0;i<n;i++)s+=block(n,i,1,b[i]);
  }
  return s;
}
function permuteGrouped(src,n){
  const w=W(5*n),h=13*n+2,g=12*(w+1);
  let out=src.slice(0,h);
  for(let i=0;i<n;i++)out+=src.slice(h+i*g,h+(i+1)*g)
                            +src.slice(h+(n+i)*g,h+(n+i+1)*g);
  return out;
}
function recognize(src){
  let p=0,read=0,moves=0,fieldChecks=0,compared=0;
  function next(){read++;if(p>=src.length)return "#";const x=src[p++];moves++;return x;}
  function fail(){return {member:false,read,moves,fieldChecks,compared};}
  let count=0,ch;
  while((ch=next())==="1")count++;
  if(ch!=="0"||count<5||count%5!==0)return fail();
  const n=count/5,w=W(5*n);
  for(let j=0;j<8*n;j++)if(next()!=="1")return fail();
  if(next()!=="0")return fail();
  let equal=true;
  for(let i=0;i<n;i++){
    let sgn0=null;
    for(let bank=0;bank<2;bank++){
      let sgn=null, z=(bank===0?n:3*n)+2*i;
      for(let u=0;u<2;u++)for(let v=0;v<2;v++){
        const observed=next();
        if(observed!=="0"&&observed!=="1")return fail();
        if(sgn===null){
          sgn=observed;
          if(bank===0)sgn0=sgn;
          else {equal=equal&&(sgn===sgn0);compared++;}
        }
        if(observed!==sgn)return fail();
        const expected=bits(i,w)+u+bits(z,w)+v+bits(z+1,w);
        for(let k=0;k<expected.length;k++){
          fieldChecks++;
          if(next()!==expected[k])return fail();
        }
      }
    }
  }
  if(next()!=="#"||p!==src.length)return fail();
  return {member:true,sat:equal,n,L:src.length,read,moves,fieldChecks,compared};
}
function brute(src,n){
  const w=W(5*n),h=13*n+2,rec=3*(w+1),clauses=[];
  for(let j=0;j<8*n;j++){
    const c=[];
    for(let k=0;k<3;k++){
      const f=src.slice(h+j*rec+k*(w+1),h+j*rec+(k+1)*(w+1));
      c.push([parseInt(f.slice(1),2),f[0]==="1"]);
    }
    clauses.push(c);
  }
  for(let mask=0;mask<2**(5*n);mask++){
    let all=true;
    for(const clause of clauses){
      if(!clause.some(([v,neg])=>Boolean((mask>>v)&1)!==neg)){all=false;break;}
    }
    if(all)return true;
  }
  return false;
}
function audit(){
  const out={id:"TMR3-CLAUSE-ORDER-STREAM007",status:"COMPUTATIONAL",model:"one local input head, bit-serial recognizer, fully charged TM construction symbolic",valid:0,sat:0,unsat:0,allCNFBrute:0,exactRecordPermutations:0,mutantRejections:0,totalReadEvents:0,totalInputMoves:0,totalFieldChecks:0,totalPairComparisons:0,maxL:0,failures:0,samples:[]};
  function check(cond,msg){if(!cond){out.failures++;throw Error(msg);}}
  function test(n,a,b,controls){
    const grouped=encode(n,a,b,false), src=encode(n,a,b,true);
    const r=recognize(src), expected=a.every((v,i)=>v===b[i]), w=W(5*n), h=13*n+2, g=12*(w+1);
    check(src===permuteGrouped(grouped,n),"not exact clause-block permutation");
    check(src.length===grouped.length&&src.length===h+2*n*g,"length changed");
    check(r.member&&r.sat===expected&&r.n===n,"SAT/UNSAT parsing");
    check(r.moves===src.length&&r.read===src.length+1&&r.compared===n,"one-sweep charge");
    check(r.fieldChecks===8*n*3*w+8*n*2,"identifier and sign bit charges");
    out.valid++;out[r.sat?"sat":"unsat"]++;out.exactRecordPermutations++;
    out.totalReadEvents+=r.read;out.totalInputMoves+=r.moves;out.totalFieldChecks+=r.fieldChecks;out.totalPairComparisons+=r.compared;out.maxL=Math.max(out.maxL,src.length);
    if(n<=2){check(brute(src,n)===expected&&brute(grouped,n)===expected,"independent CNF enumeration");out.allCNFBrute+=2;}
    if(out.samples.length<12&&(!out.samples.some(x=>x.n===n&&x.sat===expected)))out.samples.push({n,L:src.length,sat:expected,source_moves:r.moves,field_bits:r.fieldChecks});
    if(controls){
      const bad=[src.slice(0,-1),src+"0",src.slice(1),src.slice(0,h+g+(w+1)*3)+(src[h+g+(w+1)*3]==="0"?"1":"0")+src.slice(h+g+(w+1)*3+1)];
      // Flip a first-literal identifier bit in second record. Never a legal canonical source.
      const pos=h+(w+1)+1;
      bad.push(src.slice(0,pos)+(src[pos]==="0"?"1":"0")+src.slice(pos+1));
      for(const candidate of bad){check(!recognize(candidate).member,"structural mutation escaped recognizer");out.mutantRejections++;}
    }
  }
  for(let n=1;n<=5;n++)for(let a=0;a<2**n;a++)for(let b=0;b<2**n;b++)
    test(n,Array.from({length:n},(_,i)=>(a>>i)&1),Array.from({length:n},(_,i)=>(b>>i)&1),true);
  let seed=0x12131415;
  const rand=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed;};
  for(const n of [8,16,32,64,128,256,512])for(let k=0;k<8;k++){
    const a=Array.from({length:n},()=>rand()&1);
    const b=k===0?a.slice():Array.from({length:n},()=>rand()&1);
    test(n,a,b,true);
  }
  return out;
}
if(typeof require!=="undefined"&&require.main===module)console.log(JSON.stringify(audit(),null,2));
if(typeof module!=="undefined")module.exports={encode,permuteGrouped,recognize,brute,audit};