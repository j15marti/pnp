function experiment(){
 const out={seed:2081425,cases:0,labels:{SAT:0,UNSAT:0},assertions:0,closureScans:0,pins:0,branchLeaves:0,maxDefect:0,fano:[],scaling:[],random:{SAT:0,UNSAT:0}};
 let seed=out.seed;const rand=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};
 const check=x=>{out.assertions++;if(!x)throw Error("assertion "+out.assertions)};
 const bit=i=>1n<<BigInt(i);
 function parity(x){let r=0;while(x){r^=1;x&=x-1n}return r}
 function reduce(rows,n){let a=rows.map(([v,b])=>[v,b]);let p=0;for(let i=0;i<n;i++){let j=p;while(j<a.length&&!(a[j][0]&bit(i)))j++;if(j===a.length)continue;[a[p],a[j]]=[a[j],a[p]];for(let k=0;k<a.length;k++)if(k!==p&&(a[k][0]&bit(i))){a[k][0]^=a[p][0];a[k][1]^=a[p][1]}p++}if(a.some(([v,b])=>!v&&b))return null;return a.slice(0,p)}
 function first(v){let i=0;while(!(v&bit(i)))i++;return i}
 function solution(R){let x=0n;for(const[v,b]of R)if(b)x|=bit(first(v));return x}
 const word=(x,i)=>Number((x>>BigInt(2*i))&3n);
 const put=(i,v)=>[[bit(2*i),v&1],[bit(2*i+1),v>>1]];
 function local(R,n,i){return [0,1,2,3].filter(v=>reduce([...R,...put(i,v)],n)!==null)}
 function close(rows,holes){const n=2*holes.length;let R=reduce(rows,n);if(!R)return null;for(;;){out.closureScans++;let changed=false;for(let i=0;i<holes.length;i++){let L=local(R,n,i).filter(v=>v!==holes[i]);if(!L.length)return null;for(let a=1;a<=3;a++){let vals=new Set(L.map(v=>parity(BigInt(v&a))));if(vals.size!==1)continue;let row=[BigInt(a)<<BigInt(2*i),[...vals][0]];let r=reduce([...R,row],n);if(r===null)throw Error("closure invalid");if(r.length>R.length){R=r;changed=true;out.pins++;break}}if(changed)break}if(!changed)return R}}
 function defect(R,holes){let k=[];for(let i=0;i<holes.length;i++){const proj=new Set(R.map(([v])=>word(v,i)).filter(Boolean));if(proj.size>=2&&local(R,holes.length*2,i).length>1)k.push(i)}return k}
 function valid(x,rows,holes){return rows.every(([v,b])=>parity(v&x)===b)&&holes.every((h,i)=>word(x,i)!==h)}
 function solve(rows,holes){const n=2*holes.length;let R=close(rows,holes);if(!R)return {x:null,k:0};const D=defect(R,holes);out.maxDefect=Math.max(out.maxDefect,D.length);
 function visit(j,A){if(j<D.length){let i=D[j];for(let v=0;v<4;v++)if(v!==holes[i]){let B=close([...A,...put(i,v)],holes);if(B){let x=visit(j+1,B);if(x!==null)return x}}return null}
 out.branchLeaves++;check(defect(A,holes).length===0);let x=solution(A);for(let i=0;i<holes.length;i++)if(word(x,i)===holes[i]){let delta=[1,2,3].find(d=>A.every(([v])=>parity(BigInt(d&word(v,i)))===0));check(delta!==undefined);x^=BigInt(delta)<<BigInt(2*i)}check(valid(x,rows,holes));return x}
 return {x:visit(0,R),k:D.length}}
 function ref(rows,holes){let count=0,anchor=null,basis=[];let n=holes.length*2;for(let z=0;z<2**n;z++){let x=BigInt(z);if(valid(x,rows,holes)){count++;if(anchor===null)anchor=x;else basis.push([x^anchor,0])}}return {count,rank:reduce(basis,n).length}}
 function test(rows,holes,tag){let r=solve(rows,holes),b=ref(rows,holes);check((r.x!==null)===(b.count>0));let label=b.count?"SAT":"UNSAT";out.cases++;out.labels[label]++;if(tag==="random")out.random[label]++;if(r.k===0&&b.count){let R=close(rows,holes);check(R!==null&&b.rank===2*holes.length-R.length)}return {label,count:b.count,defect:r.k}}
 // Construct a parity-check system on observation-copy coordinates by eliminating the source x.
 function compile(n,edges){let piv=new Map(),deps=[];for(let i=0;i<edges.length;i++){let [a,b,c]=edges[i];for(let j=0;j<2;j++){let v=bit(a)^bit(j===0?b:c),w=bit(2*i+j);while(v){let p=first(v);if(!piv.has(p)){piv.set(p,[v,w]);break}let [u,t]=piv.get(p);v^=u;w^=t}if(!v)deps.push([w,0])}}return deps}
 const F=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]],H=compile(7,F),zero=F.map(()=>0);
 out.fano.push(test(H,zero,"fano"));for(let i=0;i<7;i++)for(let h=1;h<4;h++){let holes=zero.slice();holes[i]=h;out.fano.push(test(H,holes,"fano"))}
 // Rank-two nonlocal deduction: two equal blocks with different holes force their shared second bit.
 let sync=[[bit(0)^bit(2),0],[bit(1)^bit(3),0]],holes=[0,1];let C=close(sync,holes);check(C.length===2);out.sync=test(sync,holes,"sync");check(out.sync.count===2);check(out.sync.defect===2);
 // Single-row arbitrary dense guards; exhaustive rank-one projection hull checks.
 for(let m=1;m<=5;m++){for(let t=0;t<30;t++){let row=BigInt(rand(2**(2*m)-1)+1);let hs=Array.from({length:m},()=>rand(4));test([[row,rand(2)]],hs,"random")}}
 for(let t=0;t<100;t++){let m=2+rand(3),hs=Array.from({length:m},()=>rand(4)),rows=Array.from({length:1+rand(2*m)},()=>[BigInt(rand(2**(2*m))),rand(2)]);test(rows,hs,"random")}
 // Arbitrary high-rank guard on a single channel: equality chain plus contradictory endpoint pins.
 for(let m of [8,32,64]){let rows=[];for(let i=1;i<m;i++)rows.push([bit(2*(i-1))^bit(2*i),0]);let hs=Array(m).fill(0);for(let bad of [false,true]){let q=[...rows,[bit(0),0],...(bad?[[bit(2*(m-1)),1]]:[])];let r=solve(q,hs);check((r.x!==null)===!bad);out.scaling.push({m,rank:bad?null:reduce(q,2*m).length,label:bad?"UNSAT":"SAT",defect:r.k})}}
 return out
}
console.log(JSON.stringify(experiment(),null,2));
