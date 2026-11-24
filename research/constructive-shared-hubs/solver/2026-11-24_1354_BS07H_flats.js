function flatcheck(){
const L={match:0,rank:0,candidates:0,flats:0,gauss:0,comparisons:0,assertions:0},range=n=>Array.from({length:n},(_,i)=>i),bit=i=>1n<<BigInt(i);let seed=70331;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};function ck(b){L.assertions++;if(!b)throw Error("assertion")}
function parity(x){let p=0;while(x){x&=x-1n;p^=1}return p}
const sat=(E,x)=>E.every(([a,b])=>parity(a&x)===b);
function rank(R,S){L.match++;let w=Array(R.rows.length).fill(-1);function aug(v,seen){for(let i=0;i<R.rows.length;i++)if(R.rows[i].includes(v)&&!seen.has(i)){seen.add(i);if(w[i]<0||aug(w[i],seen)){w[i]=v;return true}}return false}let k=0;for(const v of S)if(aug(v,new Set()))k++;return k}
function gauss(n,rows){L.gauss++;let M=new Map();for(let [a,b] of rows){while(a){let p=a.toString(2).length-1;if(!M.has(p)){M.set(p,[a,b]);break}let [q,c]=M.get(p);a^=q;b^=c}if(!a&&b)return 0n}return 1n<<BigInt(n-M.size)}
function* choose(m,k,j=0,S=[]){if(!k){yield S;return}for(let v=j;v<=m-k;v++)yield*choose(m,k-1,v+1,[...S,v])}
function compile(R){let E=range(R.m),r=rank(R,E),d=R.m-r;if(d>3)return null;function dual(S){L.rank++;return S.length-r+rank(R,E.filter(v=>!S.includes(v)))}let F=new Map();for(let k=0;k<d;k++)for(const S of choose(R.m,k)){L.candidates++;if(dual(S)!==k)continue;let A=E.filter(v=>S.includes(v)||dual([...S,v])===k),mask=A.reduce((m,v)=>m|bit(v),0n);F.set(mask,{mask,k,eq:E.filter(v=>!(mask&bit(v))).flatMap(v=>R.ext[v].map(([a,b])=>[a,b^1])),c:0n})}
const full=(1n<<BigInt(R.m))-1n;F.set(full,{mask:full,k:d,eq:[],c:1n});let a=[...F.values()].sort((x,y)=>y.k-x.k);for(let i=1;i<a.length;i++){let c=0n;for(let j=0;j<i;j++){L.comparisons++;if((a[i].mask&a[j].mask)===a[i].mask)c-=a[j].c}a[i].c=c}L.flats+=a.length;return {d,terms:a}}
function value(P,x){return P.terms.reduce((s,t)=>s+(sat(t.eq,x)?t.c:0n),0n)}
function count(P,n,G){return P.terms.reduce((s,t)=>s+t.c*gauss(n,[...G,...t.eq]),0n)}
function direct(R,x){let U=range(R.m).filter(v=>!R.ext[v].some(e=>sat([e],x)));return rank(R,U)===U.length}
const out={random:{tested:0,skipped:0,sat:0,unsat:0,words:0},uniform:[]};for(let t=0;t<160;t++){let m=2+rnd(5),R={m,rows:range(rnd(6)).map(()=>range(m).filter(()=>rnd(7)<3)),ext:range(m).map(()=>range(rnd(3)).map(()=>[BigInt(1+rnd(15)),rnd(2)]))},P=compile(R);if(!P){out.random.skipped++;continue}let G=t%2?[[3n,t%3===0?1:0]]:[],z=0n;for(let x=0n;x<16n;x++){let b=direct(R,x);ck(value(P,x)===(b?1n:0n));out.random.words++;if(b&&sat(G,x))z++}ck(count(P,4,G)===z);out.random.tested++;out.random[z?"sat":"unsat"]++}
for(const [m,d] of [[16,1],[16,2],[16,3],[32,2]]){let R={m,rows:range(m-d).map(()=>range(m)),ext:range(m).map(i=>[[bit(i),1]])},P=compile(R),chooseN=(n,k)=>{let a=1n;for(let i=1;i<=k;i++)a=a*BigInt(n-i+1)/BigInt(i);return a};let z=(1n<<BigInt(m))-range(d).reduce((s,k)=>s+chooseN(m,k),0n);ck(count(P,m,[])===z);ck(count(P,m,range(m).map(i=>[bit(i),0]))===0n);ck(value(P,(1n<<BigInt(d))-1n)===1n);out.uniform.push({m,d,terms:P.terms.length,count:String(z)})}
return {seed:70331,out,ledger:L}
}
console.log(JSON.stringify(flatcheck(),null,2));
