// RT32 finite raw rank-two chart tests, not full cooperative solver.
function runRT32(){
const stats={assertions:0,transversalCalls:0,augmentations:0,reductions:0,exchangeScans:0,certificates:0,exhaustiveAssignments:0,signingsChecked:0,verifiedLifts:0,cases:[]};
function ok(v,m){stats.assertions++;if(!v)throw Error(m)}
function bit(i){return 1n<<BigInt(i)}
function par(x){let p=0;while(x){x&=x-1n;p^=1}return p}
function high(x){return x.toString(2).length-1}
function elim(rows){let B=new Map(),dep=[];for(let i=0;i<rows.length;i++){let x=rows[i],z=bit(i);while(x){let j=high(x),b=B.get(j);if(!b){B.set(j,[x,z]);break}x^=b[0];z^=b[1];stats.reductions++}if(!x)dep.push(z)}return {B,dep}}
function reduce(x,B){let z=0n;while(x){let b=B.get(high(x));if(!b)break;x^=b[0];z^=b[1];stats.reductions++}return [x,z]}
function rank(rows){return elim(rows).B.size}
function solve(rows,rhs,n){let B=new Map();for(let i=0;i<rows.length;i++){let x=rows[i],b=rhs[i];while(x){let j=high(x),v=B.get(j);if(!v){B.set(j,[x,b]);break}x^=v[0];b^=v[1];stats.reductions++}if(!x&&b)return null}let x=0n;for(let j=0;j<n;j++)if(B.has(j)){let [a,b]=B.get(j);if(par(a&x)^b)x|=bit(j)}return x}
function nullbasis(rows,n){let B=elim(rows).B,out=[];for(let k=0;k<n;k++)if(!B.has(k)){let x=bit(k);for(let j=0;j<n;j++)if(B.has(j)&&par(B.get(j)[0]&x))x|=bit(j);out.push(x)}return out}
function options(P){return P.flatMap(([a,b],i)=>[[a,bit(2*i),i],[b,bit(2*i+1),i],[a^b,bit(2*i)^bit(2*i+1),i]])}
function strict(P,r){if(P.length!==r+1||rank(P.flat())!==r||P.some(q=>rank(q)!==2))return false;if(P.length>12)throw Error("small strict oracle only");for(let t=1;t<(1<<P.length)-1;t++){let q=[];for(let i=0;i<P.length;i++)if(t>>i&1)q.push(...P[i]);if(rank(q)<q.length/2)return false}return true}
function transversal(P,r,delta){
stats.transversalCalls++;let opt=options(P),m=P.length,vec=opt.map(([a,c])=>a|(par(c&delta)?bit(r):0n)),S=[];
while(S.length<m){
 let used=new Set(S.map(j=>opt[j][2])),inS=new Set(S),B=elim(S.map(j=>vec[j])).B,Q=[],prev=new Map();
 for(let j=0;j<opt.length;j++)if(!inS.has(j)&&!used.has(opt[j][2])){Q.push(j);prev.set(j,-1)}
 let end=-1;for(let k=0;k<Q.length&&end<0;k++){let j=Q[k];if(!inS.has(j)){let [x,z]=reduce(vec[j],B);if(x){end=j;break}for(let l=0;l<S.length;l++)if(z&bit(l)){let h=S[l];stats.exchangeScans++;if(!prev.has(h)){prev.set(h,j);Q.push(h)}}}else{for(let h=0;h<opt.length;h++)if(!inS.has(h)&&(!used.has(opt[h][2])||opt[h][2]===opt[j][2])){stats.exchangeScans++;if(!prev.has(h)){prev.set(h,j);Q.push(h)}}}}
 if(end<0)break;
 let T=new Set(S);for(let j=end;j!==-1;j=prev.get(j)){if(T.has(j))T.delete(j);else T.add(j)}S=[...T];stats.augmentations++;ok(new Set(S.map(j=>opt[j][2])).size===S.length&&rank(S.map(j=>vec[j]))===S.length,"augment valid")
}
return S.map(j=>opt[j])
}
function gauge(P,r){return Array.from({length:r},(_,j)=>P.reduce((v,[a,b],i)=>v|((a&bit(j))?bit(2*i):0n)|((b&bit(j))?bit(2*i+1):0n),0n))}
function legal(P,s,x){return P.every(([a,b],i)=>par(a&x)!==Number((s>>BigInt(2*i))&1n)||par(b&x)!==Number((s>>BigInt(2*i+1))&1n))}
function cert(P,r,delta){let T=transversal(P,r,delta);ok(T.length===P.length,"Rado full lift");let rows=T.map(q=>q[0]),{dep}=elim(rows);ok(dep.length===1,"one dependence");let p=0n;for(let i=0;i<T.length;i++)if(dep[0]&bit(i))p^=T[i][1];ok(par(p&delta)===1,"new constraint");stats.certificates++;return {T,p,b:1^par(dep[0])}}
function candidate(P,r){let n=2*P.length,G=elim(gauge(P,r)).B,E=[];for(;;){let d=nullbasis(E.map(e=>e.p),n).find(v=>reduce(v,G)[0]);if(d===undefined)break;E.push(cert(P,r,d));ok(rank(E.map(e=>e.p))===E.length,"rank increase")}ok(E.length===n-r,"quotient dimension");let s=solve(E.map(e=>e.p),E.map(e=>e.b),n);ok(s!==null,"independent equations consistent");return {E,s,G}}
function checkSign(P,r,s,C,brute){let e=C.E.find(e=>par(e.p&s)!==e.b),w=null;if(e){w=solve(e.T.map(q=>q[0]),e.T.map(q=>1^par(q[1]&s)),r);ok(w!==null&&legal(P,s,w),"source lift");stats.verifiedLifts++}else ok(!reduce(s^C.s,C.G)[0],"candidate coset");
let models=null;if(brute){models=0;for(let x=0;x<1<<r;x++){stats.exhaustiveAssignments++;if(legal(P,s,BigInt(x)))models++}ok(!e||models>0,"no false SAT");if(!models)ok(!e,"UNSAT confined")}
stats.signingsChecked++;return {outside:!!e,models}}
let seed=20261125;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>8)%n}
let F=[];const coord=i=>i===1?0n:bit(i-2);for(let i=1;i<=7;i++)for(let j=i+1;j<=7;j++){let k=i^j;if(k>j)F.push([coord(i)^coord(j),coord(i)^coord(k)])}
function audit(P,r,label,all,known){if(P.length<=12)ok(strict(P,r),"strict core");let C=candidate(P,r),q=2*P.length-r,ss=all?Array.from({length:1<<(2*P.length)},(_,i)=>BigInt(i)):Array.from({length:120},()=>{let z=0n;for(let j=0;j<2*P.length;j++)if(rnd(2))z|=bit(j);return z}).concat([C.s,0n,...(known===undefined?[]:[known])]);let outside=0,unsat=0,inside=0;for(let s of ss){let a=checkSign(P,r,s,C,r<=10);outside+=a.outside;inside+=!a.outside;unsat+=a.models===0}let cand=checkSign(P,r,C.s,C,r<=10);if(known!==undefined)ok(!reduce(known^C.s,C.G)[0],"known UNSAT gauge");stats.cases.push({label,m:P.length,r,q,signings:ss.length,outside,inside,unsat: r<=10?unsat:null,candidateModels:cand.models,candidate:C.s.toString()});return C}
audit(F,6,"Fano",true,0n);audit([[1n,2n],[1n,2n],[1n,2n]],2,"three equal planes",true);
for(let k=0;k<18;k++){let r=3+rnd(2),P,tries=0;do{P=Array.from({length:r+1},()=>{let a=1+rnd((1<<r)-1),b=1+rnd((1<<r)-1);while(a===b)b=1+rnd((1<<r)-1);return [BigInt(a),BigInt(b)]});if(++tries>1000)throw Error("generation")}while(!strict(P,r));audit(P,r,"random "+k,true)}
function expand(P,r){let Q=[],s=0n;for(let i=0;i<P.length;i++){let [a,b]=P[i],p=bit(r+3*i),q=bit(r+3*i+1),v=bit(r+3*i+2);Q.push([a^q,b^v],[p,v],[p,q],[p^q,p^v]);s|=2n<<BigInt(2*(4*i+1));s|=3n<<BigInt(2*(4*i+2));s|=1n<<BigInt(2*(4*i+3))}return {Q,r:r+3*P.length,s}}
let ex=expand(F,6);audit(ex.Q,ex.r,"RT21 full depth-one expansion (strictness symbolic)",false,ex.s)
return stats
}
function cubeAudit(){
let seed=1234321;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>8)%n}
function p(a){let t=0;while(a){a&=a-1;t^=1}return t}
function rank(A){let b=[];for(let x of A){while(x){let k=31-Math.clz32(x);if(b[k])x^=b[k];else{b[k]=x;break}}}return b.filter(Boolean).length}
let st={cases:0,coefficients:0,signingCoefficientChecks:0,fullLiftCoefficients:0,zeroLiftCoefficients:0,verifiedWitnesses:0,assertions:0};function ok(a){st.assertions++;if(!a)throw Error("cube audit")}
for(let d=1;d<=3;d++)for(let i=0;i<24;i++){let r=3+rnd(2),m=r+d,A=[],s=rnd(1<<(2*m)),delta=Array.from({length:d},()=>rnd(1<<(2*m)));for(let j=0;j<m;j++){let a=1+rnd((1<<r)-1),b=1+rnd((1<<r)-1);while(a===b)b=1+rnd((1<<r)-1);A.push([a,b,a^b])}
let signings=Array.from({length:1<<d},(_,a)=>delta.reduce((v,w,j)=>a>>j&1?v^w:v,s));st.cases++;
for(let z=0;z<3**m;z++){let n=z,rows=[],cs=[],lift=[];for(let j=0;j<m;j++){let k=n%3;n=Math.floor(n/3);let a=A[j][k],c=(k+1)<<(2*j);rows.push(a);cs.push(c);lift.push(delta.reduce((v,w,h)=>v|(p(c&w)<<(r+h)),a))}
let full=rank(lift)===m,base=rank(rows)===r,res=0,solutions=0,last=null;for(let l=0;l<signings.length;l++){let signs=signings[l],b=rows.map((a,j)=>a|((1^p(cs[j]&signs))<<r));let consistent=base&&rank(b)===r;if(consistent){res^=1;solutions++;last=signs}st.signingCoefficientChecks++}
st.coefficients++;ok(res===Number(full));if(full){st.fullLiftCoefficients++;ok(solutions===1);let w=-1;for(let x=0;x<1<<r;x++)if(rows.every((a,j)=>p(a&x)===(1^p(cs[j]&last)))){w=x;break}ok(w>=0&&A.every(([a,b],j)=>p(a&w)!==(last>>(2*j)&1)||p(b&w)!==(last>>(2*j+1)&1)));st.verifiedWitnesses++}else st.zeroLiftCoefficients++}
}
return st
}
console.log(JSON.stringify({deficiencyOne:runRT32(),affineCubes:cubeAudit()},null,2));
