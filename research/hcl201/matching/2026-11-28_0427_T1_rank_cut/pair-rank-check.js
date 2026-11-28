
function runPairControls(sha){
const enc=x=>JSON.stringify(x)+"\n",A=(b,m)=>{if(!b)throw Error(m)},bit=x=>Number(!!x);
function B(X){let b=new Map();for(let x of X)while(x){let k=x&-x;if(!b.has(k)){b.set(k,x);break}x^=b.get(k)}return b}
function mem(b,x){while(x){let k=x&-x;if(!b.has(k))return false;x^=b.get(k)}return true}
function cut(L,R){let X=L.flatMap(s=>s.map(x=>x^s[0])),Y=R.flatMap(s=>s.map(x=>x^s[0]));return B(X).size+B(Y).size-B(X.concat(Y)).size}
function matching(D){for(let a=0;a<3;a++)for(let b=0;b<3;b++)if(a!==b&&!(D>>a&1)&&!(D>>b&1))return [a,b];return null}
let results=[];
for(let m of [2,4,8,16,32,64])for(let no of [false,true]){
 let g=1n<<BigInt(3*m),S=[],target=g;
 for(let i=0;i<m;i++){let a=1n<<BigInt(3*i),b=a<<1n,c=a<<2n;S.push([0n,a,b^g,c]);target^=a^b^(no&&i===m-1?c:0n)}
 for(let i=0;i<m;i++){let a=1n<<BigInt(3*i);S.push([0n,a,a<<1n,a<<2n])}
 let source={format:"DELETION-SYNDROME-v1",q:3,adj:[[0,1,2],[0,1,2]],labels:S.map(s=>s.slice(1).map(x=>x.toString(16))),target:target.toString(16)},singleDrops=0;
 for(let i=0;i<S.length;i++){let b=B(S.filter((_,j)=>j!==i).flat());for(let s of S[i])if(!mem(b,target^s))singleDrops++}
 let own=new Map();S.forEach((s,i)=>{let x=s.reduce((a,b)=>a|b,0n);while(x){let k=x&-x;x^=k;if(!own.has(k))own.set(k,[]);own.get(k).push(i)}});
 let candidates=new Map();for(let [k,v] of own)if(v.length===2){let key=v.join(","),c=candidates.get(key)||{mask:0n,count:0};c.mask|=k;c.count++;candidates.set(key,c)}
 let pairs=[],used=new Set(),T=S.map(s=>s.slice()),checks=0;
 for(let [key,{mask}] of [...candidates].sort((a,b)=>b[1].count-a[1].count||a[0].localeCompare(b[0]))){
 let [i,j]=key.split(",").map(Number);if(used.has(i)||used.has(j))continue;used.add(i);used.add(j);let out=[];
 for(let a=0;a<4;a++)for(let b=0;b<4;b++){checks++;let x=S[i][a]^S[j][b];if(!((x^target)&mask))out.push([a,b,x.toString(16)])}
 pairs.push({i,j,mask:mask.toString(16),out});if(out.length){T[i]=[...new Set(out.map(x=>S[i][x[0]]))];T[j]=[...new Set(out.map(x=>S[j][x[1]]))]}}
 A(used.size===2*m,"coverage");let empty=pairs.some(p=>!p.out.length),states=new Map([[0,[]]]),transitions=0;
 if(!empty)for(let p of pairs){let next=new Map();for(let [s,w] of states)for(let [a,b,x] of p.out){transitions++;let t=s^bit(BigInt("0x"+x)&g);if(!next.has(t))next.set(t,w.concat([[p.i,a,p.j,b]]))}states=next}
 let witness=empty?null:states.get(1)??null,lift=null;if(witness){let t=0n;lift=[];for(let [i,a,j,b] of witness){t^=S[i][a]^S[j][b];for(let [k,v] of [[i,a],[j,b]]){let z=matching(v?1<<(v-1):0);A(z!==null,"lift");lift.push([k,z])}}A(t===target,"syndrome")}
 // Independent local brute-force matching oracle, known paired recipe only in checker.
 let oracle=new Set([0]),oracleChecks=0;for(let i=0;i<m;i++){let mask=7n<<BigInt(3*i),O=new Set();
 for(let a=0;a<8;a++)if(matching(a))for(let b=0;b<8;b++)if(matching(b)){oracleChecks++;let x=S[i][a?Math.log2(a)+1:0]^S[m+i][b?Math.log2(b)+1:0];if(!((x^target)&mask))O.add(bit(x&g))}
 oracle=new Set([...oracle].flatMap(a=>[...O].map(b=>a^b)))}
 A(oracle.has(1)===!!witness,"oracle");A(!!witness!==no,"label");
 let cert={instance_id:source.format+":sha256:"+sha(enc(source)),N:enc(source).length*8,source,guard:"EMPTY",residual:"ROOT",parents:[],original_ids:{shells:[0,2*m-1],demands:[0,4*m-1],resources:[0,6*m-1],syndrome:[0,3*m]},pairs,decision:witness?"YES":"NO",witness,lift,originalCut:cut(S.slice(0,m),S.slice(m)),filteredCut:empty?null:cut(T.slice(0,m),T.slice(m)),singleDrops,checks,transitions,oracleChecks};
 results.push({certificate_id:"CERT-v1:sha256:"+sha(enc(cert)),cert})
}return results}
