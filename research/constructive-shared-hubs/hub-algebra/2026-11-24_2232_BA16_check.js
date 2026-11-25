function run(){
 const R={assertions:0,closureScans:0,fourierUpdates:0,referenceWords:0,charts:0,planarControls:0,signNeighbors:[],budgetNeighbors:[],deletedFano:[],ring:[]};const ok=(p,msg)=>{R.assertions++;if(!p)throw Error(msg)};
 const bits=(w,i)=>(w>>i)&1, parity=x=>{let a=0;while(x){a^=1;x&=x-1}return a};
 const sat=(w,e)=>{let t=e.v.map((i,j)=>bits(w,i)^bits(e.s,j));return !(t[0]===t[1]&&t[1]===t[2])};
 const owners=a=>a.map(v=>({v,s:0}));const fano=owners([[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]]);
 const plane=owners([...Array.from({length:3},(_,a)=>Array.from({length:3},(_,b)=>Array.from({length:3},(_,i)=>3*i+(a*i+b)%3))).flat(),...Array.from({length:3},(_,i)=>[3*i,3*i+1,3*i+2])]);
 function closure(n,E,pins){let p=new Map(pins),change=true;while(change){change=false;R.closureScans++;for(const e of E){let good=[];for(let w=0;w<8;w++){if(e.v.some((v,j)=>p.has(v)&&p.get(v)!==bits(w,j)))continue;if(!sat(w,{v:[0,1,2],s:e.s}))continue;good.push(w)}if(!good.length)return null;for(let j=0;j<3;j++)if(!p.has(e.v[j])&&good.every(w=>bits(w,j)===bits(good[0],j))){p.set(e.v[j],bits(good[0],j));change=true}}}return p}
 function models(n,E,pins=[]){let out=[];for(let w=0;w<1<<n;w++){R.referenceWords++;if(pins.every(([i,b])=>bits(w,i)===b)&&E.every(e=>sat(w,e)))out.push(w)}return out}
 function dual(n,E){let z=new Map([[0,1n]]);for(const e of E){let opts=[[0,3n]];for(let i=0;i<3;i++)for(let j=i+1;j<3;j++)opts.push([(1<<e.v[i])^(1<<e.v[j]),bits(e.s,i)===bits(e.s,j)?-1n:1n]);let next=new Map();for(const [a,c] of z)for(const [b,d] of opts){R.fourierUpdates++;next.set(a^b,(next.get(a^b)||0n)+c*d)}z=next}let den=4n**BigInt(E.length),num=1n<<BigInt(n);return mask=>{let t=(z.get(mask)||0n)*num;ok(t%den===0n,"integral character");return t/den}}
 function signature(M,vs){let a=Array(16).fill(0);for(const w of M){let y=vs.reduce((v,i)=>2*v+bits(w,i),0);a[y]++}return a}
 function identity(a){for(let i=0;i<16;i++)ok(a[i]===a[15-i],"complement");return a[0]*a[5]+a[3]*a[6]-a[1]*a[4]-a[2]*a[7]}
 function chart(n,E,name){R.charts++;let p=closure(n,E,[]);let M=models(n,E);ok(p!==null||!M.length,"sound closure");let D=dual(n,E);for(let q=0;q<1<<n;q++){let m=M.reduce((s,w)=>s+(parity(w&q)?-1:1),0);ok(D(q)===BigInt(m),"character "+name);if(q){for(let b=0;b<2;b++)ok((D(0)+(b?-D(q):D(q)))/2n===BigInt(M.filter(w=>parity(w&q)===b).length),"guard")}}
 for(let b=0;b<2;b++){let C=closure(n,E,[[0,b]]),M2=models(n,E,[[0,b]]);ok(C!==null||!M2.length,"pin closure");if(C)ok(M2.every(w=>[...C].every(([i,t])=>bits(w,i)===t)),"pin deductions")}
 return M}
 const F=chart(7,fano,"Fano"),P=chart(9,plane,"plane");ok(F.length===0&&P.length===0,"root");
 for(let i=0;i<7;i++)for(let j=0;j<3;j++){let E=fano.map((e,k)=>({...e,s:k===i?1<<j:0})),M=chart(7,E,"sign");ok(M.length===10,"sign neighbor");R.signNeighbors.push(M.length)}
 for(let i=0;i<7;i++){let E=fano.filter((_,j)=>i!==j),M=chart(7,E,"deleted");let e=fano[i];let counts=[0,0];for(const w of M){ok(!sat(w,e),"critical");counts[bits(w,e.v[0])]++}for(let b=0;b<2;b++){ok(counts[b]===5,"budget count");R.budgetNeighbors.push(counts[b])}R.deletedFano.push(M.length)}
 let G=plane.filter(e=>![[0,3,6],[1,4,7]].some(v=>v.every((x,j)=>x===e.v[j])));let GM=chart(9,G,"DS16 G");let a=signature(GM,[0,1,3,4]);R.ds16G={models:GM.length,signature:a,identity:identity(a)};
 for(let s=0;s<8;s++)for(let t=0;t<8;t++){let E=[{v:[0,1,4],s},{v:[2,3,4],s:t}];let M=chart(5,E,"cofacial fan");ok(identity(signature(M,[0,1,2,3]))===0,"planar identity");R.planarControls++}
 for(let A=1;A<=9;A++)for(let B=1;B<=9;B++){let a=Array(16).fill(0);a[0]=a[15]=A;a[5]=a[10]=B;ok(identity(a)===A*B&&A*B>0,"cross obstruction")}
 function ring(q){const L=12*q,n=3*L,E=[];for(let i=0;i<L;i++)for(let j=0;j<3;j++)E.push({v:[3*i+j,3*((i+1)%L)+j,3*((i+1)%L)+(j+1)%3],s:0});const ordinary=[[0,2,5],[1,3,8],[4,7,10],[6,9,11]],alt=[[0,2,5],[1,3,10],[4,7,9],[6,8,11]],special=[[0,4,8],[1,3,6],[2,9,11],[5,7,10]];for(let b=0;b<q;b++)for(let j=0;j<3;j++)for(let v of (b===0&&j===0?special:j===2?alt:ordinary))E.push({v:v.map(i=>3*(12*b+i)+j),s:0});let p=closure(n,E,[]);ok(p&&p.size===0,"ring root closure");let z=Array.from({length:n},(_,v)=>(Math.floor(v/3)%2)^Number(v%3===Math.floor(v/3)%3));let deg=Array(n).fill(0),edges=new Set();for(let e of E){ok(new Set(e.v.map(i=>z[i])).size===2,"ring witness");for(let u of e.v)deg[u]++;for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){let s=[e.v[i],e.v[j]].sort((a,b)=>a-b).join(",");ok(!edges.has(s),"linear");edges.add(s)}}ok(deg.every(d=>d===4)&&edges.size===4*n,"primal density");for(let b=0;b<2;b++){let w=z.map(x=>x^z[0]^b);ok(w[0]===b&&E.every(e=>new Set(e.v.map(i=>w[i])).size===2),"pin witness")}R.ring.push({q,n,edges:edges.size,minDeleted:n+6,minRank:Math.ceil((n+6)/8)})}
 for(let q of [1,2,4,8])ring(q);
 return R;
}
console.log(JSON.stringify(run(),null,2));
