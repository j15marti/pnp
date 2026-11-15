const result=(function audit(){
"use strict";
let checks=0,edges=0,bruteforce=0;
const ok=(b,s)=>{checks++;if(!b)throw Error("ASSERT "+s);};
function prism(m){
 const es=[],seen=new Set(),vs=Array.from({length:2*m},()=>[]);
 function add(a,b){let x=Math.min(a,b),y=Math.max(a,b),z=x+":"+y;if(!seen.has(z)){seen.add(z);es.push([x,y]);}}
 for(let row=0;row<2;row++)for(let i=0;i<m;i++)add(row*m+i,row*m+(i+1)%m);
 for(let i=0;i<m;i++)add(i,m+i);
 es.forEach(([u,v],i)=>{vs[u].push(i+1);vs[v].push(i+1);});
 vs.forEach(v=>v.sort((a,b)=>a-b));
 ok(es.length===3*m&&vs.every(v=>v.length===3),"prism cubic");
 return {es,vs};
}
function block(ids,parity){
 let patterns=Array.from({length:8},(_,i)=>i).filter(i=>(((i>>2)&1)^((i>>1)&1)^(i&1))!==parity);
 if(parity)patterns.sort((a,b)=>(a===0?1:0)-(b===0?1:0)||a-b);
 return patterns.map(i=>ids.map((v,k)=>((i>>(2-k))&1)?-v:v));
}
function build(m){
 const {es,vs}=prism(m),f0=[];
 vs.forEach((ids,i)=>f0.push(...block(ids,i===2*m-1?1:0)));
 const f1=f0.map(row=>row.slice());f1[f1.length-1][2]*=-1;
 ok(f0.length===8*m&&f0[f0.length-1].every(v=>v>0),"last all-positive");
 return {es,vs,f0,f1};
}
function encode(cs,b){
 let s="1".repeat(b)+"0"+"1".repeat(cs.length)+"0";
 for(const row of cs)for(const lit of row){const v=Math.abs(lit);if(v<1||v>=2**b)throw Error("bad ID");s+=v.toString(2).padStart(b,"0")+(lit<0?"1":"0");}
 return s;
}
function decode(s){
 if(typeof s!=="string"||!/^[01]+$/.test(s))throw Error("not bits");
 const b=s.indexOf("0");if(b<1)throw Error("no width");
 const j=s.indexOf("0",b+1);if(j<=b+1)throw Error("no count");
 const M=j-b-1,start=j+1;if(s.length-start!==3*M*(b+1))throw Error("bad body");
 let p=start,cs=[];
 for(let q=0;q<M;q++){const row=[];for(let k=0;k<3;k++){
  let v=parseInt(s.slice(p,p+b),2),neg=s[p+b]==="1";p+=b+1;if(v===0)throw Error("zero ID");row.push(neg?-v:v);
 }if(new Set(row.map(Math.abs)).size!==3)throw Error("nonproper");cs.push(row);}
 return {b,cs};
}
function sat(cs,assign){return cs.every(row=>row.some(v=>(((assign>>(Math.abs(v)-1))&1)===(v>0?1:0))));}
function brute(cs,n){for(let i=0;i<2**n;i++)if(sat(cs,i))return i;return null;}
function auth(cs){
 if(cs.length%4)return false;
 for(let g=0;g<cs.length;g+=4){
  let base=cs[g].map(Math.abs).sort((a,b)=>a-b).join(),patterns=new Set(),charges=new Set();
  for(let q=0;q<4;q++){
   let row=cs[g+q],ids=row.map(Math.abs).sort((a,b)=>a-b);if(ids.join()!==base)return false;
   let signs=ids.map(v=>row.find(y=>Math.abs(y)===v)<0?1:0);
   patterns.add(signs.join());charges.add(signs[0]^signs[1]^signs[2]);
  }
  if(patterns.size!==4||charges.size!==1)return false;
 }
 return true;
}
function recognize(s){
 let d;try{d=decode(s);}catch(e){return null;}
 let M=d.cs.length;if(M%8||M<24)return null;let m=M/8,b=Math.ceil(Math.log2(3*m+1));
 if(d.b!==b)return null;
 let f=build(m);if(s===encode(f.f0,b))return false;if(s===encode(f.f1,b))return true;return null;
}
const samples=[];
for(let m=3;m<=14;m++){
 const {es,vs,f0,f1}=build(m),b=Math.ceil(Math.log2(3*m+1));
 const a=encode(f0,b),z=encode(f1,b),N=(24*m+1)*(b+1)+8*m+1;
 ok(a.length===N&&z.length===N,"bit length");
 ok(a.slice(0,-1)===z.slice(0,-1)&&a.at(-1)==="0"&&z.at(-1)==="1","only final bit");
 ok([...a].filter((x,i)=>x!==z[i]).length===1,"Hamming distance 1");
 const d0=decode(a),d1=decode(z);
 ok(d0.b===b&&d1.b===b&&JSON.stringify(d0.cs)===JSON.stringify(f0)&&JSON.stringify(d1.cs)===JSON.stringify(f1),"decoder");
 ok(auth(f0)&&!auth(f1),"complete-XOR check");
 ok(sat(f1,0)&&!sat(f0,0),"allzero witness");
 ok(recognize(a)===false&&recognize(z)===true,"uniform pair-recognizer");
 for(let eid=1;eid<=3*m;eid++)ok(vs.filter(row=>row.includes(eid)).length===2,"edge degree two");
 if(m<=5){bruteforce+=2;ok(brute(f0,3*m)===null&&brute(f1,3*m)===0,"exhaustive SAT controls");}
 const bads=[a.slice(0,-1),a+"0","0"+a,a.slice(0,b+1)+"0"+a.slice(b+2)];
 for(const x of bads){ok(recognize(x)===null,"malformed pair fallthrough");let caught=false;try{decode(x);}catch(e){caught=true;}ok(caught,"malformed decoder rejection");}
 const other=f1.map(row=>row.slice());other[0][0]*=-1;ok(recognize(encode(other,b))===null,"noncanonical valid source fallthrough");
 for(let r=-1;r<N;r++)for(let advance=0;advance<=1;advance++){
  const r2=(r+advance<N)?r+advance:r;
  for(let halt=0;halt<=1;halt++){
   if(halt&&r2<N-1)continue;
   const d=Math.max(0,N-1-r)-Math.max(0,N-1-r2);
   ok(d>=0&&d<=1,"local physical tariff");edges++;
  }
 }
 samples.push({m,H:2*m,E:3*m,clauses:8*m,b,encoded_bits:N,identical_prefix_bits:N-1,unsat_last_bit:0,sat_last_bit:1});
}
return {id:"LASTSAT073",status:"COMPUTATIONAL",native:"V8 JavaScript exact audit",random_seed:null,prism_m_range:[3,14],bruteforce_m_range:[3,5],assertions:checks,tariff_edge_checks:edges,bruteforce_runs:bruteforce,failures:0,samples,scope:"symbolic all-m proof distinct; finite JS is not compiled physical TM"};
})();
console.log(JSON.stringify(result,null,2));
