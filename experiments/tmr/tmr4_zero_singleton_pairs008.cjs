'use strict';
/* TMR-4/008. No dependencies. Run with: node tmr4_zero_singleton_pairs008.cjs */
(function () {
 const check=(v,m)=>{if(!v)throw Error(m)};
 const pop=n=>{let c=0;for(;n;n>>=1)c+=n&1;return c};
 const enc=(n,w)=>n.toString(2).padStart(w,'0');
 const flip=(s,p)=>s.slice(0,p)+(s[p]==='0'?'1':'0')+s.slice(p+1);
 function make(r){
   const t=3*r,w=Math.ceil(Math.log2(2*t+2)),N=2**w-1;
   const core=Array.from({length:t},(_,i)=>2*(i+1)+(pop(i+1)&1));
   const cs=new Set(core), spare=Array.from({length:N},(_,i)=>i+1).filter(v=>!cs.has(v));
   const clauses=[],duplicates=[];
   for(let g=0;g<r;g++){
     for(let m=1;m<=7;m++)clauses.push(core.slice(3*g,3*g+3).map((id,j)=>({id,neg:!!(m&(1<<j))})));
     duplicates.push(clauses.length);
     clauses.push(core.slice(3*g,3*g+3).map((id,j)=>({id,neg:!!(3&(1<<j))})));
   }
   const coreClauses=clauses.length;
   for(let i=0;i<spare.length;i+=3){
     const triple=spare.slice(i,i+3);
     for(const id of spare){if(triple.length===3)break;if(!triple.includes(id))triple.push(id)}
     check(triple.length===3,'filler triples');
     clauses.push(triple.map(id=>({id,neg:false})));
   }
   const M=clauses.length,fields=[];
   let bits='1'.repeat(N)+'0'+'1'.repeat(M)+'0';
   for(let c=0;c<M;c++)for(let j=0;j<3;j++){
     const l=clauses[c][j];fields.push({c,j,at:bits.length,neg:l.neg,id:l.id});
     bits+=(l.neg?'1':'0')+enc(l.id,w);
   }
   check(bits.length===N+M+2+3*M*(w+1),'serialized length');
   return {r,w,N,M,L:bits.length,core,spare,clauses,duplicates,coreClauses,fields,bits};
 }
 function parse(s){
   let p=0;
   const unary=()=>{let z=0;while(p<s.length&&s[p]==='1'){p++;z++}if(s[p]!=='0')return null;p++;return z};
   const N=unary(),M=unary();if(N===null||M===null||N<3||M<1)return null;
   const w=Math.max(1,Math.ceil(Math.log2(N)));
   if(s.length!==N+M+2+3*M*(w+1))return null;
   const clauses=[],occ=Array(N+1).fill(0);
   for(let c=0;c<M;c++){
     const lits=[],used=new Set();
     for(let j=0;j<3;j++){
       const neg=s[p++]==='1',id=parseInt(s.slice(p,p+w),2);p+=w;
       if(id<1||id>N||used.has(id))return null;
       used.add(id);occ[id]++;lits.push({id,neg});
     }
     clauses.push(lits);
   }
   if(p!==s.length||occ.slice(1).some(n=>n===0))return null;
   return {N,M,w,clauses};
 }
 function witness(p){const a=new Uint8Array(p.N+1);for(const id of p.spare)a[id]=1;return a}
 const satisfies=(p,a)=>p.clauses.every(cl=>cl.some(l=>(a[l.id]===1)!==l.neg));
 const out={tag:'TMR4-ZS8',date_PST:'2026-11-13 19:36 PST',scope:'strict no-unused-id proper 3CNF, encoded-source finite witness test',cases:[],totals:{signSAT:0,identifierSAT:0,identifierInvalid:0,unsatPairBlocks:0},failedAssertions:0};
 for(const r of [1,2,3,4,5,6,8,10,12,16]){
   const p=make(r),f=parse(p.bits);
   check(f!==null,'base source parses');
   check(satisfies(f,witness(p)),'base SAT');
   let signSAT=0,identifierSAT=0,identifierInvalid=0;
   for(const l of p.fields){
     const si=flip(p.bits,l.at),sf=parse(si);
     check(sf!==null,'sign neighbor parse');
     const a=witness(p);
     if(l.c<p.coreClauses){
       const m=l.c%8===7?3:l.c%8+1;
       const changed=m^(1<<l.j);
       if(changed===0){
         const g=Math.floor(l.c/8);
         for(let z=0;z<3;z++)a[p.core[3*g+z]]=(m>>z)&1;
       }
     }
     check(satisfies(sf,a),'single sign flip remains SAT');
     signSAT++;
     for(let z=0;z<p.w;z++){
       const y=flip(p.bits,l.at+1+z),pf=parse(y);
       if(pf===null){identifierInvalid++;continue}
       const aa=witness(p);
       if(l.c<p.coreClauses){
         const target=l.id^(1<<(p.w-z-1));
         check(p.spare.includes(target),'even-parity core id changes to dummy');
         aa[target]=l.neg?0:1;
       }
       check(satisfies(pf,aa),'single ID bit flip remains SAT');
       identifierSAT++;
     }
   }
   const pairs=[];
   for(let g=0;g<r;g++){
     const ci=p.duplicates[g],first=p.fields[3*ci],second=p.fields[3*ci+1];
     const y=flip(flip(p.bits,first.at),second.at),pf=parse(y);
     check(pf!==null,'opposite neighbor parses');
     const bans=new Set();
     for(let c=8*g;c<8*g+8;c++){
       let m=0;for(let z=0;z<3;z++)if(pf.clauses[c][z].neg)m+=1<<z;
       bans.add(m);
     }
     check(bans.size===8,'one independent block becomes UNSAT');
     pairs.push(first.at,second.at);
   }
   check(new Set(pairs).size===2*r,'disjoint sensitive pairs');
   const Q=24*r*(p.w+1);
   const entry={r,w:p.w,N:p.N,M:p.M,L:p.L,coreClauses:p.coreClauses,filler:p.M-p.coreClauses,Q,zeroSingletonFields:p.fields.length*(p.w+1),signSAT,identifierSAT,identifierInvalid,disjointPairs:r,lowerCertificate:r,ratio:Q/p.L};
   out.cases.push(entry);
   out.totals.signSAT+=signSAT;
   out.totals.identifierSAT+=identifierSAT;
   out.totals.identifierInvalid+=identifierInvalid;
   out.totals.unsatPairBlocks+=r;
 }
 if(typeof console!=='undefined')console.log(JSON.stringify(out,null,2));
 return out;
})()