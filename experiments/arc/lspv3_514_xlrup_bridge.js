/* LSPV-3/514: independent textual XLRUP-subset source and proof checker.
   NOT the CakeML cake_xlrup checker. NOT historical R_mix341.
   Reproduction: node experiments/arc/lspv3_514_xlrup_bridge.js */
"use strict";
function demand(ok,msg){ if(!ok) throw Error(msg); }
function graph(kind){
  let h,edges=[];
  if(kind==="K4"){h=4;for(let a=0;a<4;a++)for(let b=a+1;b<4;b++)edges.push([a,b]);}
  else if(kind==="K33"){h=6;for(let a=0;a<3;a++)for(let b=3;b<6;b++)edges.push([a,b]);}
  else if(kind==="CUBE"){h=8;for(let a=0;a<8;a++)for(let j=0;j<3;j++){let b=a^(1<<j);if(a<b)edges.push([a,b]);}}
  else if(kind.startsWith("PRISM")){let t=Number(kind.slice(5));h=2*t;
    for(let a=0;a<t;a++)edges.push([a,(a+1)%t]);
    for(let a=0;a<t;a++)edges.push([t+a,t+(a+1)%t]);
    for(let a=0;a<t;a++)edges.push([a,t+a]);
  }else throw Error("unknown graph");
  demand(2*edges.length===3*h,"not cubic");
  return {h,edges};
}
function source(kind,odd=true){
  let {h,edges}=graph(kind),n=edges.length,inc=Array.from({length:h},()=>[]);
  edges.forEach(([a,b],i)=>{inc[a].push(i+1);inc[b].push(i+1);});
  demand(inc.every(a=>a.length===3),"not cubic");
  let charges=Array(h).fill(0);if(odd)charges[0]=1;
  let cls=[],ids=[];
  for(let v=0;v<h;v++){
    let ix=[];
    for(let p=0;p<8;p++){
      let bits=[(p>>2)&1,(p>>1)&1,p&1];
      if((bits[0]^bits[1]^bits[2])!==charges[v]){
        cls.push(inc[v].map((e,j)=>bits[j]?-e:e));ix.push(cls.length);
      }
    }
    ids.push(ix);demand(ix.length===4,"parity encoding");
  }
  let src="p cnf "+n+" "+cls.length+"\n"+cls.map(c=>c.join(" ")+" 0\n").join("");
  return {kind,h,n,inc,charges,cls,ids,src};
}
function rowText(mask,rhs,n){
  let lits=[];for(let v=1;v<=n;v++)if((mask&(1n<<BigInt(v-1)))!==0n)lits.push(v);
  if(lits.length){if(!rhs)lits[0]=-lits[0];}
  else demand(rhs===1,"satisfiable zero row cannot be encoded as contradiction");
  return lits;
}
function unpack(lits){
  let mask=0n,neg=0,seen=new Set();
  for(let l of lits){
    demand(l!==0&&!seen.has(Math.abs(l)),"bad signed XOR literal");
    seen.add(Math.abs(l));mask^=1n<<BigInt(Math.abs(l)-1);if(l<0)neg^=1;
  }
  return [mask,1^neg];
}
function emit(d){
  let out=[],rows=new Map(),front=[],id=1;
  for(let v=0;v<d.h;v++){
    let mask=d.inc[v].reduce((a,e)=>a|(1n<<BigInt(e-1)),0n);
    let row=[mask,d.charges[v]];
    out.push("i x "+id+" "+rowText(mask,row[1],d.n).join(" ")+" 0 "+d.ids[v].join(" ")+" 0");
    rows.set(id,row);front.push(id++);
  }
  while(front.length>1){
    let next=[];
    for(let i=0;i<front.length;i+=2){
      if(i+1===front.length){next.push(front[i]);continue;}
      let a=front[i],b=front[i+1],x=rows.get(a),y=rows.get(b);
      let row=[x[0]^y[0],x[1]^y[1]];
      out.push("x "+id+" "+rowText(...row,d.n).join(" ")+" 0 "+a+" "+b+" 0");
      rows.set(id,row);next.push(id++);
    }front=next;
  }
  let f=rows.get(front[0]);
  demand(f[0]===0n&&f[1]===1,"even-charge SAT control: no refutation");
  out.push("i cx "+(d.cls.length+1)+" 0 "+front[0]+" 0");
  return out.join("\n")+"\n";
}
function stop(t,start){
  let j=t.indexOf(0,start);demand(j>=0,"missing zero terminator");
  return [t.slice(start,j),j+1];
}
function clauseCovers(row,clauses,hints){
  let [mask,rhs]=row,vs=[];
  for(let k=0;k<mask.toString(2).length;k++)if((mask&(1n<<BigInt(k)))!==0n)vs.push(k+1);
  demand(vs.length<=12,"checker scope bound: only small source XOR conversions");
  for(let p=0;p<(1<<vs.length);p++){
    let parity=0,encoded=new Set();
    vs.forEach((v,j)=>{let b=(p>>j)&1;parity^=b;encoded.add(b?-v:v);});
    if(parity===rhs)continue;
    if(!hints.some(id=>clauses[id-1].every(l=>encoded.has(l))))return false;
  }
  return true;
}
function validate(d,sourceText,proof){
  demand(sourceText===d.src,"external original source bytes mismatch");
  let tok=sourceText.trim().split(/\s+/),n=Number(tok[2]),m=Number(tok[3]);
  demand(tok[0]==="p"&&tok[1]==="cnf"&&n===d.n&&m===d.cls.length,"DIMACS header mismatch");
  let srcclauses=[],cur=[];
  for(let k=4;k<tok.length;k++){
    let v=Number(tok[k]);demand(Number.isSafeInteger(v)&&Math.abs(v)<=n,"bad DIMACS literal");
    if(v===0){srcclauses.push(cur);cur=[];}else cur.push(v);
  }
  demand(!cur.length&&srcclauses.length===m,"DIMACS record count");
  demand(JSON.stringify(srcclauses)===JSON.stringify(d.cls),"unsigned or reordered original clauses");
  let rows=new Map(),done=false,lines=proof.trim().split("\n");
  for(let line of lines){
    let t=line.trim().split(/\s+/),k=t[0];
    if(k==="i"&&t[1]==="x"){
      demand(!done,"post sink step");
      let id=Number(t[2]),a=t.slice(3).map(Number),[l,j]=stop(a,0),[hint,end]=stop(a,j);
      demand(end===a.length&&id>0&&!rows.has(id)&&hint.every(c=>c>=1&&c<=m),"bad i x syntax or hints");
      let row=unpack(l);
      demand(clauseCovers(row,srcclauses,hint),"four-source i x covering check failed");
      rows.set(id,row);
    }else if(k==="x"){
      demand(!done,"post sink step");
      let id=Number(t[1]),a=t.slice(2).map(Number),[l,j]=stop(a,0),[hint,end]=stop(a,j);
      demand(end===a.length&&id>0&&!rows.has(id)&&hint.length===2&&hint.every(c=>rows.has(c)),"bad XOR parent");
      let row=unpack(l),x=rows.get(hint[0]),y=rows.get(hint[1]);
      demand(row[0]===(x[0]^y[0])&&row[1]===(x[1]^y[1]),"GF2 sum mismatch");
      rows.set(id,row);
    }else if(k==="i"&&t[1]==="cx"){
      let cid=Number(t[2]),a=t.slice(3).map(Number),[c,j]=stop(a,0),[h,end]=stop(a,j);
      demand(!done&&end===a.length&&cid===m+1&&c.length===0&&h.length===1&&rows.has(h[0]),"bad i cx");
      let r=rows.get(h[0]);demand(r[0]===0n&&r[1]===1,"not an exact contradictory XOR");done=true;
    }else throw Error("unsupported external format tag");
  }
  demand(done,"no final contradiction");
  return {source_count:m,paid_external_format_steps:lines.length,xor_rows:rows.size};
}
function runAll(){
  let result=[];
  for(let kind of ["K4","K33","CUBE","PRISM8","PRISM16","PRISM64"]){
    let d=source(kind),proof=emit(d),verify=validate(d,d.src,proof),s=proof.trim().split("\n");
    demand(verify.paid_external_format_steps===2*d.h,"bad step formula");
    let rejects=0;
    function neg(src,p){try{validate(d,src,p);}catch(e){rejects++;return;}throw Error("negative accepted");}
    neg(d.src.replace(/ 0\n/," -1 0\n"),proof);
    neg(d.src,s[0].replace(/ \d+ 0$/, " 0")+"\n"+s.slice(1).join("\n")+"\n");
    neg(d.src,s[0].replace(/ \d+ 0$/, " 999 0")+"\n"+s.slice(1).join("\n")+"\n");
    let bad=s.slice(),i=bad[0].split(" ");i[3]=String(-Number(i[3]));bad[0]=i.join(" ");neg(d.src,bad.join("\n")+"\n");
    bad=s.slice();i=bad[d.h].split(" ");i[i.length-2]="999";bad[d.h]=i.join(" ");neg(d.src,bad.join("\n")+"\n");
    bad=s.slice();i=bad[d.h].split(" ");i[2]=String(-Number(i[2]));bad[d.h]=i.join(" ");neg(d.src,bad.join("\n")+"\n");
    bad=s.slice();bad[bad.length-1]="i cx "+(d.cls.length+1)+" 1 0 "+(2*d.h-1)+" 0";neg(d.src,bad.join("\n")+"\n");
    try{emit(source(kind,false));throw Error("even SAT yielded refutation");}catch(e){demand(!/even SAT yielded/.test(String(e)),"bad even case");rejects++;}
    demand(rejects===8,"negative control count");
    result.push({kind,h:d.h,n:d.n,m:d.cls.length,source_bytes:d.src.length,proof_bytes:proof.length,external_steps:verify.paid_external_format_steps,negative_rejections:rejects});
  }
  return {status:"Independent check of the published textual XLRUP subset, not cake_xlrup and not R_mix341",cases:result};
}
if(typeof module!=="undefined"&&typeof require!=="undefined"&&require.main===module)
  console.log(JSON.stringify(runAll(),null,2));
