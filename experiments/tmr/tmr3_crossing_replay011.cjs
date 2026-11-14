"use strict";
function run(){
 const g=n=>{const b=n.toString(2);return "0".repeat(b.length-1)+b};
 const state={COPY:"000",REWIND:"001",COMPARE:"010",ACCEPT:"011",REJECT:"100"};
 const alph={M:"00",_:"01","0":"10","1":"11"};
 function tm(a,b){
   const src=a+"#"+b+"$", tape={0:"M"};let ip=0,wp=1,highest=1,mode="COPY",T=0;const crossings={};
   while(mode!=="ACCEPT"&&mode!=="REJECT"){
    if(T>20*src.length+20)throw Error("nontermination");
    const old=ip,ch=src[ip]??"$",w=tape[wp]??"_";
    if(mode==="COPY"){if(ch==="0"||ch==="1"){tape[wp]=ch;wp++;ip++}else if(ch==="#"){wp--;mode="REWIND"}else mode="REJECT"}
    else if(mode==="REWIND"){if(w!=="M")wp--;else{wp++;ip++;mode="COMPARE"}}
    else if(mode==="COMPARE"){if((ch==="0"||ch==="1")&&ch===w){wp++;ip++}else if(ch==="$"&&w==="_")mode="ACCEPT";else mode="REJECT"}
    T++;if(Math.abs(ip-old)>1||wp<0)throw Error("nonlocal move");
    highest=Math.max(highest,wp);
    if(old!==ip){const cut=Math.max(old,ip),cells=Array.from({length:highest+1},(_,j)=>tape[j]??"_");
     (crossings[cut]??=[]).push({mode,wp,cells,dir:ip>old?"R":"L"});}
   }
   return {accept:mode==="ACCEPT",T,S:highest+1,crossings};
 }
 function code(rs){let out=g(rs.length+1);for(const r of rs)out+=g(r.cells.length)+g(r.wp+1)+state[r.mode]+(r.dir==="R"?"1":"0")+r.cells.map(x=>alph[x]).join("");return out}
 const eq={total:0,sat:0,unsat:0,codebooks:0,codewords:0,comparisons:0,projectedCollisions:0,hybridRejects:0},cnf={diagonals:0,cuts:0,splices:0,oppositeLabel:0};
 for(let n=1;n<=6;n++){let words=[];for(let i=0;i<2**n;i++)words.push(i.toString(2).padStart(n,"0"));for(const a of words)for(const b of words){let r=tm(a,b);if(r.accept!==(a===b))throw Error("wrong equality decision");eq.total++;if(r.accept)eq.sat++;else eq.unsat++;}}
 for(let n=2;n<=7;n++)for(let q=1;q<=n;q++){
   let book=[];for(let i=0;i<2**q;i++){const a=i.toString(2).padStart(q,"0")+"0".repeat(n-q),r=tm(a,a),rs=r.crossings[q]??[];if(rs.length!==1)throw Error("wrong crossing count");book.push({a,c:code(rs),p:rs.map(x=>x.mode+":"+x.wp+":"+x.dir).join("|")});eq.codewords++;}
   eq.codebooks++;if(new Set(book.map(x=>x.c)).size!==book.length)throw Error("full code collision");
   for(let i=0;i<book.length;i++)for(let j=i+1;j<book.length;j++){let a=book[i],b=book[j];if(a.c.startsWith(b.c)||b.c.startsWith(a.c))throw Error("prefix collision");if(tm(a.a,b.a).accept)throw Error("accepted crossed hybrid");eq.comparisons++;eq.hybridRejects++;if(a.p===b.p)eq.projectedCollisions++;}
 }
 const width=n=>Math.max(1,Math.ceil(Math.log2(5*n)));
 const bits=(x,w)=>x.toString(2).padStart(w,"0");
 function block(n,i,bank,x){const w=width(n),z=(bank===0?n:3*n)+2*i,s=String(1-x);let out="";for(let u=0;u<2;u++)for(let v=0;v<2;v++)out+=s+bits(i,w)+u+bits(z,w)+v+bits(z+1,w);return out}
 function source(n,a,b,m){let out="1".repeat(5*n)+"0"+"1".repeat(8*n)+"0";for(let base=0;base<n;base+=m){const hi=Math.min(n,base+m);for(let i=base;i<hi;i++)out+=block(n,i,0,a[i]);for(let i=base;i<hi;i++)out+=block(n,i,1,b[i]);}return out}
 for(let n=2;n<=6;n++)for(let m=2;m<=n;m++){const q=Math.floor(m/2),w=width(n),G=12*(w+1),A=[];for(let u=0;u<2**q;u++){const a=u.toString(2).padStart(q,"0").split("").map(Number).concat(Array(n-q).fill(0)),s=source(n,a,a,m);if(s.length!==13*n+2+2*n*G)throw Error("source length");A.push({a,s});cnf.diagonals++}for(let t=1;t<q*G;t++){const cut=13*n+2+q*G+t;cnf.cuts++;for(let x of A)for(let y of A){if(x.s.slice(0,cut)+y.s.slice(cut)!==source(n,x.a,y.a,m))throw Error("invalid original splice");cnf.splices++;if(x.a.some((z,i)=>z!==y.a[i]))cnf.oppositeLabel++}}}
 const fallback={};for(let n=1;n<=3;n++){let a=Array(n).fill(0),b=a.slice();b[0]=1;const s=source(n,a,b,n),w=width(n),H=13*n+2,R=3*(w+1),clauses=[];for(let j=0;j<8*n;j++){let clause=[];for(let t=0;t<3;t++){let f=s.slice(H+j*R+t*(w+1),H+j*R+(t+1)*(w+1));clause.push([parseInt(f.slice(1),2),f[0]==="1"])}clauses.push(clause)}let cnt=0;for(let i=0;i<2**(5*n);i++){cnt++;if(clauses.every(cl=>cl.some(([id,neg])=>Boolean((i>>id)&1)!==neg)))throw Error("unexpected SAT")}fallback[n]=cnt}
 return {id:"TMR3-CS11",status:"COMPUTATIONAL",scope:"independently implemented finite local equality TM and strict original CNF source-splicing; not a general SAT TM",deterministic:true,seed:null,equality: eq,strictCNF: cnf,literalExhaustiveFallback:fallback,failedAssertions:0};
}
console.log(JSON.stringify(run(),null,2));
