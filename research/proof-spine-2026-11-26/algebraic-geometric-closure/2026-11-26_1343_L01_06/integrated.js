const audit = function(){
const out={cap:"r=n",cases:[],matchingCuts:0,matchingIdentityPairs:0,equalityChecks:0,failures:0};
const seq=n=>Array.from({length:n},(_,i)=>i);
const ck=(a,msg)=>{if(!a)throw Error(msg)};
const key=a=>a.join(",");
const cycle=w=>{if(new Set(w).size!==w.length)return false;let i=0,s=new Set();while(!s.has(i)){s.add(i);i=w[i]}return i===0&&s.size===w.length};
function* combinations(n,k){let a=seq(k);while(true){yield a.slice();let i=k-1;while(i>=0&&a[i]===n-k+i)i--;if(i<0)return;a[i]++;for(let j=i+1;j<k;j++)a[j]=a[j-1]+1}}
function make(n,S,T){let A=S.filter(x=>!T.includes(x)),B=T.filter(x=>!S.includes(x)),I=S.filter(x=>T.includes(x)),J=seq(n).filter(x=>!S.includes(x)&&!T.includes(x)),path=[];for(let i=0;i<A.length;i++){path.push(A[i]);if(i===0)path.push(...I);path.push(B[i]);if(i===0)path.push(...J)}let w=Array(n);path.forEach((x,i)=>w[x]=path[(i+1)%n]);return w}
for(let n of [4,8,16,32,64,128,256]){
 let S=seq(Math.floor(n/2)),Tset=new Set(),witnesses=[];
 for(let T of combinations(n,S.length)){if(key(T)===key(S))continue;let w=make(n,S,T);witnesses.push({T,w});if(witnesses.length===n+1)break}
 for(let {T,w} of witnesses){ck(cycle(w),"cycle");let img=key(S.map(i=>w[i]).sort((a,b)=>a-b));ck(img===key(T)&&!Tset.has(img),"unique image");Tset.add(img)}
 ck(witnesses.length===n+1,"overflow");out.cases.push({n,rankCap:n,certifiedRankAtLeast:witnesses.length,storedSuccessorEntries:n*witnesses.length,explicitPairsNeeded:0})
}
for(let n=2;n<=7;n++)for(let k=1;k<n;k++){let targets=[...combinations(n,k)];out.matchingCuts++;let perms=targets.map(T=>[...T,...seq(n).filter(x=>!T.includes(x))]);for(let i=0;i<targets.length;i++)for(let j=0;j<targets.length;j++){let w=[...perms[i].slice(0,k),...perms[j].slice(k)];ck((new Set(w).size===n)===(i===j),"PM identity");out.matchingIdentityPairs++}}
for(let n=1;n<=8;n++)for(let a=0;a<2**n;a++)for(let b=0;b<2**n;b++){let prod=1;for(let i=0;i<n;i++)prod*=1-(((a>>i)^(b>>i))&1);ck(prod===+(a===b),"equality product");out.equalityChecks++}
return out};
console.log(JSON.stringify(audit(),null,2));
