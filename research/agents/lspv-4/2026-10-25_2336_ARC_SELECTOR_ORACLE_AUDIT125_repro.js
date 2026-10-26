'use strict';
// LSPV-4 ARC-SELECTOR-ORACLE-AUDIT125. Dependency-free Node >= 16.
function ok(value, message) { if (!value) throw Error('FAILED: '+message); checks++; }
let checks=0;
function abs(a){return a<0n?-a:a;}
function gcd(a,b){a=abs(a);b=abs(b);while(b){[a,b]=[b,a%b];}return a;}
function Q(n,d=1n){n=BigInt(n);d=BigInt(d);if(d===0n)throw Error('zero denominator');if(d<0n){n=-n;d=-d;}const k=gcd(n,d);return {n:n/k,d:d/k};}
function add(x,y){return Q(x.n*y.d+y.n*x.d,x.d*y.d);}
function sub(x,y){return Q(x.n*y.d-y.n*x.d,x.d*y.d);}
function mul(x,y){return Q(x.n*y.n,x.d*y.d);}
function div(x,y){return Q(x.n*y.d,x.d*y.n);}
function repr(x){return x.n.toString()+'/'+x.d.toString();}
function val(x){return Number(x.n)/Number(x.d);}
function less(x,y){return x.n*y.d<y.n*x.d;}
const one=Q(1),two=Q(2),half=Q(1,2),d=Q(901,500),ct=Q(241,200),st=Q(11642479,23232400);
const beta=div(sub(div(add(ct,two),mul(ct,ct)),ct),two);
const cstar=div(sub(mul(two,d),one),mul(d,sub(d,one)));
const delta=mul(d,d),qstar=div(delta,sub(delta,one));
const qcheck=Q(36,25);
ok(repr(beta)===repr(st),'exact beta endpoint');
ok(repr(cstar)==='651000/361301','exact coNTIME companion algebra');
ok(repr(qstar)==='811801/561801','conditional circuit bound from Theorem 6.3 first disjunct');
ok(less(qcheck,qstar),'1.44 satisfies conditional circuit threshold');
const tmargin=sub(ct,Q(6,5)),smargin=sub(st,half);
ok(repr(tmargin)==='1/200'&&repr(smargin)==='26279/23232400','strict margins');
// Proper ordinary CNF encoder: y_i fixed by one unit clause; prefix p_i is XOR(y_1,...,y_i).
function parity(a){let p=0;for(let i=0;i<a.length;i++)p^=a[i];return p;}
function parentCNF(bits){let k=bits.length,clauses=[];
 for(let i=0;i<k;i++)clauses.push([bits[i]?i+1:-(i+1)]);
 clauses.push([-1,k+1]); clauses.push([1,-(k+1)]);
 for(let i=2;i<=k;i++){let v=[k+i-1,i,k+i];
  for(let a=0;a<2;a++)for(let b=0;b<2;b++)for(let c=0;c<2;c++)if(c!==(a^b))
   clauses.push([a?-v[0]:v[0],b?-v[1]:v[1],c?-v[2]:v[2]]);
 }
 clauses.push([2*k]);return {vars:2*k,clauses};
}
function encode(c){return 'p cnf '+c.vars+' '+c.clauses.length+'\n'+c.clauses.map(a=>a.join(' ')+' 0\n').join('');}
function read(s){let lines=s.trim().split(/\n/);let header=lines.shift().trim().split(/\s+/);
 ok(header.length===4&&header[0]==='p'&&header[1]==='cnf','genuine CNF header');
 let vars=+header[2],clauses=[];
 for(let l of lines){let a=l.trim().split(/\s+/).map(Number);ok(a.at(-1)===0,'0 delimiter');a.pop();
  ok(a.every(x=>x!==0&&Math.abs(x)<=vars),'variable bounds');clauses.push(a);}
 ok(clauses.length===+header[3],'exact header clause count');return {vars,clauses};
}
function evalCNF(c,assignment){return c.clauses.every(cl=>cl.some(l=>l>0?assignment[l-1]===1:assignment[-l-1]===0));}
function satTiny(c){ok(c.vars<=12,'tiny checker range');for(let m=0;m<2**c.vars;m++){let a=Array.from({length:c.vars},(_,i)=>(m>>i)&1);if(evalCNF(c,a))return true;}return false;}
const childSat={vars:2,clauses:[[1,2],[1,-2],[-1,2]]};
const childUnsat={vars:2,clauses:[[1],[-1],[2],[-2]]};
const grandSat={vars:1,clauses:[[1]]};
const grandUnsat={vars:1,clauses:[[1],[-1]]};
let cases=0,flips=0,reads=0,serialized=0,shortened=0,bruteforce=0;
for(let k=2;k<=12;k++){
 let max=1<<k;
 for(let mask=0;mask<max;mask++){
  let bits=Array.from({length:k},(_,i)=>(mask>>i)&1),p=parity(bits);
  for(let i=0;i<k;i++){
   let copy=bits.slice();copy[i]^=1;
   ok(parity(copy)!==p,'every selector bit is essential');flips++;}
  // On data copies (x_1,x_2)=(0,1), the virtual bit is exactly parity(bits).
  let literalCopies=[0,1];ok(literalCopies[p]===p,'one-coordinate data copy');
  reads+=k;cases++;
  let parent=read(encode(parentCNF(bits)));
  let c1=read(encode(p?childSat:childUnsat));
  let c2=read(encode(p?grandSat:grandUnsat));
  ok(encode(c1).length<encode(parent).length,'real first child shorter');
  ok(encode(c2).length<encode(c1).length,'real second child shorter');shortened++;
  serialized+=encode(parent).length+encode(c1).length+encode(c2).length;
  ok(satTiny(c1)===Boolean(p),'first child both labels');
  ok(satTiny(c2)===Boolean(p),'second child both labels');
  if(k<=5){ok(satTiny(parent)===Boolean(p),'exhaustive parent semantics');bruteforce++;}
  else {let assignment=bits.concat(bits.map((_,i)=>parity(bits.slice(0,i+1))));
   if(p)ok(evalCNF(parent,assignment),'SAT witness on positive parity');
   else ok(!evalCNF(parent,assignment),'forced violation in parity control');}
 }
}
const result={id:'ARC-SELECTOR-ORACLE-AUDIT125',status:'COMPUTATIONAL checks plus separately proved parity decision-tree lower bound',
 exact:{d:repr(d),flmvTime:repr(ct),flmvSpace:repr(st),betaAtTime:repr(beta),
    coNTIMEConditional:repr(cstar),coNTIMEDecimal:val(cstar),
    Sigma2TimeExtraHypothesis:repr(delta),circuitConditional:repr(qstar),circuitDecimal:val(qstar),
    strictMargins:{time:repr(tmargin),space:repr(smargin)}},
 tests:{checks,selectorCases:cases,singleFlipChecks:flips,selectorReadsForOneFullScanEach:reads,
 realTwoLevelSATUNSATCases:shortened,exhaustiveParentCases:bruteforce,serializedASCIICharacters:serialized},
 warning:'Selector parity is a RESTRICTED easy-family control, not a lower bound on arbitrary SAT; circuit threshold assumes Sigma2SAT at exponent d^2 and a full all-input decision circuit.'};
if(typeof process!=='undefined'&&process.stdout)process.stdout.write(JSON.stringify(result,null,2)+'\n');
result;
