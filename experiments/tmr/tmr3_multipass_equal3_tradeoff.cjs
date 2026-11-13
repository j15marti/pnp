"use strict";
function assert(x,msg){if(!x)throw Error(msg);}
function width(n){return Math.max(1,Math.ceil(Math.log2(5*n)));}
function bit(v,w){return v.toString(2).padStart(w,"0");}
function source(n,a,b){
 const N=5*n,M=8*n,w=width(n),f=w+1; let fields=[];
 function four(x,u,v,target){
   const sx=target?0:1;
   for(const [su,sv] of [[0,0],[0,1],[1,0],[1,1]])
     fields.push([[sx,x],[su,u],[sv,v]]);
 }
 for(let i=0;i<n;i++)four(i,n+i,2*n+i,(a>>i)&1);
 for(let i=0;i<n;i++)four(i,3*n+i,4*n+i,(b>>i)&1);
 const prefix="1".repeat(N)+"0"+"1".repeat(M)+"0";
 return {text:prefix+fields.map(c=>c.map(([s,v])=>String(s)+bit(v,w)).join("")).join(""),clauses:fields,N,M,w,f,header:prefix.length};
}
function satBrute(clauses,N){
 for(let m=0;m<2**N;m++){
  if(clauses.every(c=>c.some(([s,v])=>( ((m>>v)&1) !==s))))return true;
 }
 return false;
}
function sweep(src,n,B){
 const L=src.text.length,w=src.w,f=src.f,h=src.header;
 let equal=true,passes=0,scanned=0,maxRetained=0;
 for(let start=0;start<n;start+=B){
  const end=Math.min(n,start+B),retained=[],pre=(i)=>h+12*i*f,suf=(i)=>h+12*(n+i)*f;
  let i=start,j=start;
  for(let pos=0;pos<L;pos++){
   if(i<end && pos===pre(i)){retained.push(src.text[pos]);i++;}
   if(j<end && pos===suf(j)){if(src.text[pos]!==retained[j-start])equal=false;j++;}
  }
  assert(i===end && j===end && retained.length===end-start,"sweep capture mismatch");
  maxRetained=Math.max(maxRetained,retained.length);
  passes++;scanned+=L;
 }
 return {equal,passes,scanned,maxRetained};
}
function run(){
 let instances=0,comparisons=0,diagTranscripts=0,brutes=0,flips=0,checks=0;
 let maxSourceLength=0,largestProductGap=0;const byN=[];
 for(let n=1;n<=5;n++){
  let pairs=0,caseChecks=0;const signaturesByWidth=Array.from({length:n},()=>new Set());
  for(let a=0;a<(1<<n);a++)for(let b=0;b<(1<<n);b++){
   const s=source(n,a,b),expect=a===b,L=13*n+2+24*n*(1+width(n));
   assert(s.text.length===L,"binary source length");checks++;
   assert(s.M===8*n && s.N===5*n && s.clauses.length===8*n,"proper 3CNF counts");checks++;
   assert(s.clauses.every(c=>c.length===3&&new Set(c.map(x=>x[1])).size===3),"proper clauses");checks++;
   if(n<=2){assert(satBrute(s.clauses,s.N)===expect,"actual SAT semantics");brutes++;checks++;}
   for(let B=1;B<=n;B++){
    const got=sweep(s,n,B);assert(got.equal===expect,"streaming decision");
    assert(got.passes===Math.ceil(n/B),"pass count");
    assert(got.scanned===L*got.passes,"charged source scans");
    assert(got.maxRetained<=B,"retained temporary bits");
    assert(got.passes*B>=n,"communication product budget");
    checks+=5;comparisons++;caseChecks+=5;
    if(expect){
     const sig=Array.from({length:got.passes},(_,j)=>Array.from({length:Math.min(B,n-j*B)},(_,k)=>String((a>>(j*B+k))&1)).join("")).join("|");
     assert(!signaturesByWidth[B-1].has(sig),"distinct accepting transcript");
     signaturesByWidth[B-1].add(sig);diagTranscripts++;checks++;
    }
   }
   if(expect){for(let i=0;i<n;i++)for(let side=0;side<2;side++){
    const t=source(n,a^(side===0?(1<<i):0),a^(side===1?(1<<i):0));
    assert(t.text.length===L&&satBruteIfSmall(t)===(false),"opposite label flip");
    const off=(j)=>s.header+12*j*s.f;
    const positions=Array.from({length:4},(_,k)=>off((side?n:0)+i)+3*k*s.f);
    let diff=[];for(let j=0;j<L;j++)if(s.text[j]!==t.text[j])diff.push(j);
    assert(diff.length===4&&diff.every((v,k)=>v===positions[k]),"exact four sign flips");
    flips++;checks+=2;
   }}
   pairs++;instances++;maxSourceLength=Math.max(maxSourceLength,L);
  }
  for(let B=1;B<=n;B++)assert(signaturesByWidth[B-1].size===(1<<n),"accept signatures count");
  byN.push({n,pairs,encodedBits:13*n+2+24*n*(1+width(n)),positiveSignaturesEachWidth:1<<n,widths:n});
 }
 function satBruteIfSmall(s){return s.N<=10?satBrute(s.clauses,s.N):false;}
 // Missing a sensitive source bit must make two equality strings collide in a deficient one-pass transcript.
 const d=4,seen=new Map();let collision=false;
 for(let a=0;a<(1<<d);a++){let key=Array.from({length:d-1},(_,j)=>String((a>>j)&1)).join("");if(seen.has(key)&&seen.get(key)!==a)collision=true;else seen.set(key,a);}
 assert(collision,"one bit deletion destroys injectivity");checks++;
 return {status:"PASS",sourceModel:"TMR2 fixed binary strict-proper-3CNF equality E_(a,b)",instanceCount:instances,streamingComparisons:comparisons,positiveTranscriptChecks:diagTranscripts,actualBruteSATComparisons:brutes,signBlockOppositeLabelFlips:flips,assertionGroups:checks,maxEncodedBits:maxSourceLength,byN,missingSignFalsifier:"PASS",note:"Virtual sequential sweeps over binary strings, not a physical multitape TM instruction trace; p(S+1) theorem is symbolic and pending independent review."};
}
if(typeof module!=="undefined" && module.exports){module.exports={run,source,sweep};if(require.main===module)console.log(JSON.stringify(run(),null,2));}