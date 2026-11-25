function supplement(){
let o={signed_neighbors:0,source_words:0,root_unsat_exhaustive:0,guarded_triple_cases:0,guarded_triple_words:0,assertions:0};
function ok(v){o.assertions++;if(!v)throw Error("assertion "+o.assertions)}
function family(k){let E=[];for(let s=0;s<2;s++){let P=[[0,s],...Array.from({length:k},(_,i)=>[1+s*k+i,1]),[0,1-s]];for(let i=0;i<=k;i++)E.push([P[i][0],P[i+1][0],P[i][1],1-P[i+1][1]])}return E}
function evalE(E,x){return E.every(([i,j,a,b])=>x[i]!==a||x[j]!==b)}
for(const k of [2,3,4,5,8,16,32,64]){
let E=family(k),n=2*k+1;if(k<=5){let c=0;for(let z=0;z<2**n;z++){let x=Array.from({length:n},(_,i)=>z>>i&1);if(evalE(E,x))c++;o.source_words++}ok(c===0);o.root_unsat_exhaustive++}
for(let j=0;j<E.length;j++){let s=Math.floor(j/(k+1)),i=j%(k+1),x=Array(n).fill(0);x[0]=s;for(let l=1;l<=i;l++)x[s*k+l]=1;ok(!evalE(E,x));ok(evalE(E.filter((_,r)=>r!==j),x));for(let f=1;f<=3;f++){let F=E.map((e,r)=>r===j?[e[0],e[1],e[2]^(f&1),e[3]^(f>>1)]:e);ok(evalE(F,x));o.signed_neighbors++}}
}
const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
let seed=154032;function rng(n){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return (seed>>>0)%n}
let instances=[fano,...fano.map((_,i)=>fano.filter((_,j)=>i!==j))];for(let t=0;t<100;t++){let T=[];for(let i=0;i<1+rng(12);i++){let p=new Set();while(p.size<3)p.add(rng(7));T.push([...p])}instances.push(T)}
for(let i=0;i<instances.length;i++){let T=instances[i],c=0;for(let x=0;x<128;x++){let a=T.every(t=>t.reduce((s,j)=>s+(x>>j&1),0)===1);let b=T.every(t=>{let [u,v,w]=t.map(j=>x>>j&1);return !(u&&v)&&!(u&&w)&&!(v&&w)&&(u^v^w)===1});ok(a===b);c+=a;o.guarded_triple_words++}if(i===0)ok(c===0);if(i>0&&i<8)ok(c>0);o.guarded_triple_cases++}
return o
}
console.log(JSON.stringify(supplement(),null,2));
