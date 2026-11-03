"use strict";
// Independent source, parity factor, XOR-DAG, witnesses, and hostile mutation checker.
function par(x){let p=0;while(x){p^=1;x&=x-1n;}return p;}
function must(cond,msg){if(!cond)throw Error(msg);}
function edges(k){let E=[];for(let i=0;i<k;i++)E.push([i,(i+1)%k]);for(let i=0;i<k;i++)E.push([k+i,k+(i+1)%k]);for(let i=0;i<k;i++)E.push([i,k+i]);return E;}
function evaluate(l,x){let a=Boolean(x&(1n<<BigInt(Math.abs(l)-1)));return l>0?a:!a;}
function verify(data){
 must(data&&data.schema==="MATCHING_MERGER363"&&data.calculus==="Rmix341"&&Array.isArray(data.cases),"malformed object");
 let checks=0,deleted=0,flipped=0;
 for(let z of data.cases){
  let k=z.k,h=2*k,Ed=edges(k),M=Array.from({length:k/2},(_,i)=>2*i);
  must(k>=4&&k%2===0&&z.h===h&&JSON.stringify(Ed)===JSON.stringify(z.edges),"graph");
  must(JSON.stringify(M)===JSON.stringify(z.matching),"matching");
  let n=1,cols=Ed.map((_,i)=>M.includes(i)?1:++n),rows=Array(h).fill(0n);
  must(z.n===n&&JSON.stringify(cols)===JSON.stringify(z.columns),"columns");
  for(let j=0;j<Ed.length;j++){let[u,v]=Ed[j],b=1n<<BigInt(cols[j]-1);rows[u]^=b;rows[v]^=b;}
  must(rows.every((r,i)=>z.rows[i]===r.toString(16)),"affine row masks");
  must(z.rhs.length===h&&z.rhs[0]===1&&z.rhs.slice(1).every(b=>b===0),"charge");
  must(rows.reduce((a,b)=>a^b,0n)===0n,"column parity");
  let supports=rows.map(r=>{let s=[];for(let j=1;j<=n;j++)if(r&(1n<<BigInt(j-1)))s.push(j);return s;});
  must(supports.every((s,i)=>s.length===3&&JSON.stringify(s)===JSON.stringify(z.supports[i])),"support");
  must(z.sources.length===4*h&&z.witnesses.length===4*h&&z.proof.length===4*h-1,"counts");
  let groups=Array.from({length:h},()=>[]);
  for(let j=0;j<z.sources.length;j++){let s=z.sources[j];must(Number.isInteger(s.eq)&&s.eq>=0&&s.eq<h&&Number.isInteger(s.tuple)&&s.tuple>=0&&s.tuple<8,"source header");must(par(BigInt(s.tuple))!==z.rhs[s.eq],"tuple parity");let lits=supports[s.eq].map((v,i)=>s.tuple>>i&1?-v:v);must(JSON.stringify(s.lits)===JSON.stringify(lits),"source signs");groups[s.eq].push(j);checks++;}
  must(groups.every(g=>g.length===4),"row blockers");
  function table(id,S){let m=0;for(let a=0;a<8;a++)if(z.sources[id].lits.some(l=>{let j=S.indexOf(Math.abs(l));return j>=0&&(l>0)===Boolean(a>>j&1);}))m|=1<<a;return m;}
  for(let r=0;r<h;r++){let m=255;for(let j of groups[r])m&=table(j,supports[r]);let truth=0;for(let a=0;a<8;a++)if(par(BigInt(a))===z.rhs[r])truth|=1<<a;must(m===truth,"local parity");checks+=8;}
  const derived=[];
  function lookup(ref){must(typeof ref==="string"&&/^[SD]\d+$/.test(ref),"parent syntax");let j=Number(ref.slice(1));if(ref[0]==="S"){must(j<z.sources.length,"source parent");return {type:"source",idx:j};}must(j<derived.length,"future parent");return derived[j];}
  for(let node of z.proof){
   must(node&&Array.isArray(node.parents)&&node.parents.length===2,"arity");
   let A=lookup(node.parents[0]),B=lookup(node.parents[1]);
   if(node.op==="AND3"){
    must(Array.isArray(node.support)&&node.support.length===3,"AND3 declared");
    function tm(a){if(a.type==="source")return table(a.idx,node.support);must(a.type==="factor"&&JSON.stringify(a.support)===JSON.stringify(node.support),"AND3 typed");return a.truth;}
    let truth=tm(A)&tm(B);must(node.table===truth,"factor result");derived.push({type:"factor",support:node.support,truth});checks+=8;
   }else if(node.op==="XOR"){
    function norm(a){if(a.type==="xor")return a;must(a.type==="factor","xor input");let ids=[];
     for(let r=0;r<h;r++)if(JSON.stringify(supports[r])===JSON.stringify(a.support)){let truth=0;for(let t=0;t<8;t++)if(par(BigInt(t))===z.rhs[r])truth|=1<<t;if(truth===a.truth)ids.push(r);}must(ids.length===1,"affine annotation ambiguous");return {type:"xor",mask:rows[ids[0]],rhs:z.rhs[ids[0]]};}
    let X=norm(A),Y=norm(B),mask=X.mask^Y.mask,b=X.rhs^Y.rhs;must(node.coeff===mask.toString(16)&&node.rhs===b,"xor value");derived.push({type:"xor",mask,rhs:b});checks+=2;
   }else throw Error("illegal operation");
  }
  must(derived.at(-1).type==="xor"&&derived.at(-1).mask===0n&&derived.at(-1).rhs===1,"not contradiction");
  for(let i=0;i<z.sources.length;i++){
   must(typeof z.witnesses[i]==="string"&&/^[0-9a-f]+$/.test(z.witnesses[i]),"witness syntax");
   let x=BigInt("0x"+z.witnesses[i]),fails=[];
   for(let j=0;j<z.sources.length;j++)if(!z.sources[j].lits.some(l=>evaluate(l,x)))fails.push(j);
   must(fails.length===1&&fails[0]===i,"deletion SAT witness");deleted++;
   for(let p=0;p<3;p++){let l=z.sources[i].lits.map((y,q)=>q===p?-y:y);must(l.some(t=>evaluate(t,x)),"sign repair");flipped++;}
   checks+=z.sources.length+3;
  }
  let dimacs="p cnf "+n+" "+z.sources.length+"\n"+z.sources.map(s=>s.lits.join(" ")+" 0\n").join("");
  must(z.encodedBits===8*dimacs.length,"encoded bit count");
  must(z.rhs.reduce((a,b)=>a^b,0)===1,"odd UNSAT");
  must(z.witnesses.length===4*h,"all sources used");checks+=h;
 }
 return {pass:true,checks,deleted,flipped,cases:data.cases.map(c=>({k:c.k,n:c.n,clauses:c.sources.length,logicalNodes:c.proof.length,encodedBits:c.encodedBits}))};
}
function hostile(raw){
 let bad=0;function reject(f){let q=JSON.parse(JSON.stringify(raw));f(q);try{verify(q);}catch(e){bad++;return;}throw Error("mutation accepted");}
 reject(q=>q.cases[0].sources[0].lits[0]*=-1);
 reject(q=>q.cases[0].proof[0].table^=1);
 reject(q=>q.cases[0].proof.at(-1).rhs=0);
 reject(q=>q.cases[0].witnesses[1]="0"); // source 1 excludes tuple 011, so 0 is NOT its deletion witness.
 reject(q=>q.cases[0].encodedBits+=8);
 reject(q=>q.schema="MALFORMED");
 reject(q=>q.cases=null);
 reject(q=>q.cases[0].columns=[0]);
 return bad;
}
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module){let fs=require("fs"),data=JSON.parse(fs.readFileSync(process.argv[2],"utf8"));console.log(JSON.stringify({...verify(data),hostileRejected:hostile(data)}));}