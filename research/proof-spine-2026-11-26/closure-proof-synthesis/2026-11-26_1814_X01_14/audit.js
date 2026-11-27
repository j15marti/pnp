function audit(){
let checks=0,matchCalls=0,seed=26112614;const ok=(x,m)=>{checks++;if(!x)throw Error(m||"check "+checks)};function rnd(n){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return(seed>>>0)%n}
const unit=i=>1n<<BigInt(i),wt=x=>{let n=0;while(x){x&=x-1n;n++}return n},all=d=>unit(d)-1n;
function matching(I){matchCalls++;const {d,edges,f,target,pins}=I,owner=Array(d).fill(-1),adj=edges.map((e,i)=>(pins[i]<0?e:[e[pins[i]]]).filter(v=>target&unit(v)));
function aug(i,seen){for(const v of adj[i])if(!seen[v]){seen[v]=1;if(owner[v]<0||aug(owner[v],seen)){owner[v]=i;return true}}return false}
for(let i=0;i<edges.length;i++)aug(i,Array(d).fill(0));let m=owner.filter(i=>i>=0).length;if(wt(target)-m>f)return {yes:false,m};
let choices=edges.map((e,i)=>2*(pins[i]<0?0:pins[i])),used=0n;owner.forEach((i,v)=>{if(i>=0){choices[i]=2*edges[i].indexOf(v)+1;used|=unit(v)}});for(let j=0;j<d;j++)if((target^used)&unit(j))choices.push(j+1);while(choices.length<edges.length+f)choices.push(0);
return {yes:true,m,choices}}
function tables(I){return [...I.edges.map((e,i)=>[0,1].filter(p=>I.pins[i]<0||I.pins[i]===p).flatMap(p=>[{row:2*p,x:0n},{row:2*p+1,x:unit(e[p])}])),...Array.from({length:I.f},()=>Array.from({length:I.d+1},(_,j)=>({row:j,x:j===0?0n:unit(j-1)})))]}
function dp(I,cap){let S=new Set([0n]),peak=1,work=0;for(const R of tables(I)){let T=new Set();for(const x of S)for(const y of R){work++;T.add(x^y.x);if(T.size>cap)return {status:"UNKNOWN",peak:T.size,work}}S=T;peak=Math.max(peak,S.size)}return {status:S.has(I.target)?"YES":"NO",peak,work,S}}
function labels(I,fn){let p=[];function go(i){if(i===I.edges.length){fn(p);return}for(let j=0;j<2;j++)if(I.pins[i]<0||I.pins[i]===j){p.push(j);go(i+1);p.pop()}}go(0)}
function fixed(I,p){return {...I,pins:p.slice()}}
function cover(I){for(let k=0;k<=I.d;k++)for(let x=0n;x<=all(I.d);x++)if(wt(x)===k&&I.edges.every(e=>e.some(v=>x&unit(v))))return k;throw Error("cover")}
const atom=[[0,2,4],[0,2,5],[0,3,5],[1,2,4],[1,3,4],[1,3,5]],covers=[[0,5],[1,4],[2,3]];
let exact=[];for(let x=0;x<64;x++){let deg=Array(6).fill(0);for(let j=0;j<6;j++)if(x>>j&1)for(let v of atom[j])deg[v]++;if(deg.every(y=>y===1))exact.push(Array.from({length:6},(_,i)=>i).filter(i=>x>>i&1))}
ok(JSON.stringify(exact.slice().sort())===JSON.stringify(covers.slice().sort()));
function native(I){let T=[],G=[],Q=[],feature=Array.from({length:I.d},()=>[]);let R=tables({...I,pins:I.edges.map(()=>-1)});
for(let i=0;i<R.length;i++){let q=R[i].length,start=T.length;Q.push({start,q});for(let j=0;j<q;j++){let b=T.length;for(const t of atom)T.push(t.map(v=>v+b));if(j===0)G.push({ids:[b],b:0});if(j===q-1)G.push({ids:[b+2],b:0});if(j>0)G.push({ids:[b,b-4],b:1});for(let v=0;v<I.d;v++)if(R[i][j].x&unit(v))feature[v].push(b+1)}
if(i<I.edges.length&&I.pins[i]>=0)G.push({ids:[start+13,start+19],b:I.pins[i]})}
for(let v=0;v<I.d;v++)G.push({ids:feature[v],b:Number((I.target>>BigInt(v))&1n)});
return {T,G,Q}}
function lift(I,result,F){let X=Array(F.T.length).fill(0);result.choices.forEach((choice,i)=>{let {start,q}=F.Q[i];ok(choice>=0&&choice<q);for(let j=0;j<q;j++){let state=j>choice?0:j===choice?1:2;for(let k of covers[state])X[start+6*j+k]=1}});
let D=Array(F.T.length).fill(0);for(let i=0;i<F.T.length;i++)if(X[i])for(const v of F.T[i])D[v]++;ok(D.every(x=>x===1),"integer native cover");for(const g of F.G)ok(g.ids.reduce((x,j)=>x^X[j],0)===g.b,"native guard");let bytes=JSON.stringify({triples:F.T,guards:F.G}).length;return bytes*8}
let graphs=0,universal=0,labelsChecked=0,decisions=0,lifts=0,yes=0,no=0;for(let z=0;z<220;z++){let d=2+rnd(4),edges=[];for(let u=0;u<d;u++)for(let v=u+1;v<d;v++)if(rnd(2))edges.push([u,v]);let f=rnd(d+1),target=BigInt(rnd(1<<d)),I={d,edges,f,target,pins:edges.map(()=>-1)};graphs++;let min=d,univ=true;labels(I,p=>{let distinct=new Set(p.map((j,i)=>edges[i][j]));min=Math.min(min,distinct.size);let J={...fixed(I,p),target:all(d)};let D=dp(J,1<<d),formula=distinct.size+f>=d;ok((D.S.size===1<<d)===formula);ok((D.status==="YES")===formula);univ&&=formula;labelsChecked++});ok(min===cover(I));ok(univ===(cover(I)+f>=d));universal++;
for(let t=0;t<4;t++){let J={...I,target:BigInt(rnd(1<<d)),pins:edges.map(()=>rnd(3)-1)},a=matching(J),b=dp(J,1<<d);ok(a.yes===(b.status==="YES"));decisions++;if(a.yes){yes++;lift(J,a,native(J));lifts++}else no++}
}
let scales=[];for(let d of [8,16,32,64,128]){let edges=[];for(let v=0;v<d-1;v++)if(v!==d/2-1)edges.push([v,v+1]);let I={d,edges,f:1,target:all(d),pins:edges.map(()=>-1)},Y={...I,target:I.target^unit(0)},N=I;let a=matching(Y),b=matching(N),r=dp(Y,256),s=dp(N,256);ok(a.yes&&!b.yes);let FY=native(Y),FN=native(N);ok(JSON.stringify(FY.T)===JSON.stringify(FN.T));ok(FY.G.filter((g,i)=>JSON.stringify(g)!==JSON.stringify(FN.G[i])).length===1);let bits=lift(Y,a,FY);let supportQueries=0,forced=0;for(let i=0;i<edges.length;i++){let count=0;for(let p=0;p<2;p++){let pins=Y.pins.slice();pins[i]=p;let x=matching({...Y,pins});supportQueries++;if(x.yes)count++}ok(count>0);if(count===1)forced++}scales.push({d,edges:edges.length,triples:FY.T.length,bits,matchingYes:a.m,matchingNo:b.m,rawYes:r.status,rawNo:s.status,rawPeak:r.peak,rawTransitions:r.work,supportQueries,forcedLabels:forced})}
return{seed:26112614,checks,graphs,universal,labelsChecked,decisions,yes,no,lifts,matchCalls,scales}
}
console.log(JSON.stringify(audit(),null,2));
