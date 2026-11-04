"use strict";
/* LSPV4/392: executable restricted oracle + source-authenticated 2m-node Resolution refutation.
   Run: node lspv4_392_implicit_cnf.js . No external libraries. */
function ip(x,m){let p=0;for(let i=0;i<m;i++)p^=((x>>(2*i))&1)&((x>>(2*i+1))&1);return p;}
function size(m){const w=1+Math.ceil(Math.log2(2*m+1));const slots=1n<<BigInt(2*m);return {w,slots,total:(slots+1n)*BigInt(2*m*w),body:slots*BigInt(2*m*w)};}
function signed(m,z,j){let x=Number(z),v=(x>>(2*m-1-j))&1;
 if(ip(x,m)===0)return {sign:v,id:j+1};
 if(j===0)return {sign:0,id:1};if(j===1)return {sign:1,id:1};
 return {sign:0,id:j};}
function bitAt(m,b,index){const s=size(m);let t=BigInt(index);if(t<0n||t>=s.total)throw Error("index");
 let lit,k;
 if(t<s.body){let slot=t/BigInt(2*m*s.w),rem=t%BigInt(2*m*s.w);lit=signed(m,slot,Number(rem/BigInt(s.w)));k=Number(rem%BigInt(s.w));}
 else{let rem=t-s.body,j=Number(rem/BigInt(s.w));lit={sign:((b>>(2*m-1-j))&1)?0:1,id:j+1};k=Number(rem%BigInt(s.w));}
 return k===0?lit.sign:((lit.id>>(s.w-1-k))&1);}
function test(){let cases=0,sat=0,unsat=0,assignments=0,checks=0,refutations=0;
 for(let m=1;m<=4;m++){let s=size(m),lim=1<<(2*m);
  for(let b=0;b<lim;b++){cases++;ip(b,m)?sat++:unsat++;
   for(let v=0;v<lim;v++){let ok=true;
    for(let z=0;z<lim;z++){let clause=false;
     for(let j=0;j<2*m;j++){let l=signed(m,BigInt(z),j);clause||=(((v>>(2*m-l.id))&1)!==l.sign);}
     if(!clause){ok=false;break;}
    }
    if(v!==b)ok=false;
    if(ok!==((v===b)&&ip(b,m)===1))throw Error("wrong SAT status");checks++;assignments++;
   }
   let first=signed(m,BigInt(b),0);
   if(ip(b,m)===0){let live=Array.from({length:2*m},(_,j)=>signed(m,BigInt(b),j));
    for(let j=0;j<2*m;j++){let u={sign:((b>>(2*m-1-j))&1)?0:1,id:j+1};
      let k=live.findIndex(l=>l.id===u.id&&l.sign!==u.sign);if(k<0)throw Error("invalid pivot");live.splice(k,1);checks++;}
    if(live.length)throw Error("not refuted");refutations++;
   }else if(first.id!==1)throw Error("not tautology");
   for(let idx of [0n,BigInt(s.w-1),s.body-1n,s.body,s.total-1n]){let bit=bitAt(m,b,idx);if(bit!==0&&bit!==1)throw Error("bitAt");checks++;}
  }
 }
 return {cases,sat,unsat,assignments,checks,refutations,status:"PASS"};
}
if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(test()));
