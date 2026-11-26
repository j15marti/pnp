/* ES02 strong tournament structural normal form audit, Node 18+ */
function run(){
 const out={seed:0x5e520027,strong_tournaments:0,nonzero_demands_checked:0,structural_unsat:0,structural_sat:0,rank2_certificates:0,largest_n:0,assertions:0};
 let seed=out.seed;function rand(){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return seed>>>0}
 const B=i=>1<<i,wt=x=>{let n=0;while(x){x&=x-1;n++}return n},parity=x=>wt(x)&1;
 const ids=(s,n)=>Array.from({length:n},(_,i)=>i).filter(i=>s&B(i));
 function ok(b,msg){out.assertions++;if(!b)throw Error(msg)}
 function T(n,t=null){let M=Array.from({length:n},(_,i)=>B(i)),k=0;for(let i=0;i<n;i++)for(let j=i+1;j<n;j++){if(t===null?(rand()&1):((t>>>k)&1))M[i]|=B(j);else M[j]|=B(i);k++}return M}
 function strong(M){let n=M.length;for(let i=0;i<n;i++){let x=B(i);while(true){let y=x;for(let j of ids(x,n))y|=M[j];if(y===x)break;x=y}if(x!==(1<<n)-1)return false}return true}
 function rank(rows){let H=new Map();for(let x of rows){while(x){let j=31-Math.clz32(x);if(H.has(j))x^=H.get(j);else{H.set(j,x);break}}}return H.size}
 function feasible(M,p){for(let i=0;i<M.length;i++)if((p&B(i))&&parity(M[i]&p))return false;return true}
 function orderTrans(M,S){let v=ids(S,M.length).sort((i,j)=>wt(M[j]&S)-wt(M[i]&S));for(let i=0;i<v.length;i++)for(let j=i+1;j<v.length;j++)if(!(M[v[i]]&B(v[j])))return null;return v}
 function structural(M,b){
  let n=M.length,W=((1<<n)-1)^b,X=orderTrans(M,b),Y=orderTrans(M,W);if(X===null||Y===null)return null;
  let c=[];for(let i of X){let k=0;while(k<Y.length&&(M[Y[k]]&B(i)))k++;for(let j=k;j<Y.length;j++)if(M[Y[j]]&B(i))return null;c.push(k)}
  let v=0;while(v+1<c.length&&c[v]>=c[v+1])v++;for(let i=v+1;i<c.length;i++)if(c[i-1]>c[i])return null;
  let records=X.map((x,i)=>({x,key:c[i]+.5,type:i<=v?0:1,tie:i<=v?i:-i})).concat(Y.map((x,j)=>({x,key:j+1,type:2,tie:j})));
  records.sort((a,b)=>b.key-a.key||a.type-b.type||a.tie-b.tie);
  return records;
 }
 function check(M){
  if(!strong(M))return;let n=M.length;out.strong_tournaments++;out.largest_n=Math.max(n,out.largest_n);
  const actual=[];for(let p=0;p<1<<n;p++)if(feasible(M,p))actual.push(p);
  // At most n independent actual witnesses are needed for single-demand truth.
  const basis=[];for(let p of actual)if(rank([...basis,p])>basis.length)basis.push(p);
  for(let b=1;b<1<<n;b++){
   let predicted=structural(M,b),no=basis.every(p=>!parity(p&b));out.nonzero_demands_checked++;
   ok(Boolean(predicted)===no,"structural iff");
   if(!predicted){out.structural_sat++;continue}
   out.structural_unsat++;
   const C=[[0,1,1],[0,1,1],[1,1,1]],completed=predicted.map(a=>predicted.reduce((r,z,j)=>r|(C[a.type][z.type]?B(j):0),0));
   for(let i=0;i<n;i++)for(let j=0;j<i;j++)ok(Boolean(completed[i]&B(j))===Boolean(M[predicted[i].x]&B(predicted[j].x)),"prescribed lower completion");
   ok(rank(completed)<=2,"rank two certificate");out.rank2_certificates++;
  }
 }
 for(let n=1;n<=6;n++)for(let t=0;t<2**(n*(n-1)/2);t++)check(T(n,t));
 for(let n=7;n<=10;n++)for(let i=0;i<60;i++)check(T(n));
 return out;
}
console.log(JSON.stringify(run(),null,2));
