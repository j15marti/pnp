function run(){
const R={seed:20261124, assertions:0, low_fibers:0, reference_terminal_words:0, closure_scans:0, parity_merges:0, lifts:0, edge_checks:0, cases:[]};
function ok(v){R.assertions++;if(!v)throw Error("assertion "+R.assertions)}
function star(a,b,c,s=[0,0,0],eta=0){return {a,b,c,s,eta}}
function forbidden(e,x){let {a,b,c,s,eta}=e;return [x[a]^s[0],x[a]^s[0]^2,x[b]^s[1]^1,x[c]^s[2]^3^(eta*2)]}
function active(e,l){let {a,b,c,s}=e;return (l[a]^s[0])===(l[b]^s[1])&&(l[a]^s[0])===(l[c]^s[2])}
function closure(n,E,l){ // guard fixes every low bit; necessary high equations only
 let h=Array(n).fill(-1);
 const A=E.filter(e=>active(e,l));
 // propagation from fixed arbitrary component gauge, not unconditional pins
 while(true){
  let change=true;
  while(change){change=false;R.closure_scans++;
   for(let e of A){let p=e.eta^1,b=e.b,c=e.c;
    if(h[b]>=0&&h[c]>=0){if((h[b]^h[c])!==p)return null}
    else if(h[b]>=0){h[c]=h[b]^p;R.parity_merges++;change=true}
    else if(h[c]>=0){h[b]=h[c]^p;R.parity_merges++;change=true}
   }
  }
  let i=h.indexOf(-1);if(i<0)break;h[i]=0;
 }
 let x=l.map((v,i)=>v+2*h[i]);
 for(let e of E){let f=forbidden(e,x);let y=[0,1,2,3].find(t=>!f.includes(t));ok(y!==undefined);for(let t of f){R.edge_checks++;ok(t!==y)}}
 R.lifts++;return x;
}
function reference(n,E,l){let count=0;for(let h=0;h<2**n;h++){let x=l.map((b,i)=>b+2*((h>>i)&1));R.reference_terminal_words++;if(E.every(e=>new Set(forbidden(e,x)).size<4))count++}return count}
function degree(n,E){let d=Array(n).fill(0);for(let e of E){d[e.a]+=2;d[e.b]++;d[e.c]++}return Math.max(...d)}
function evaluate(name,n,E,expect=null,ref=true){let sat=0,counts=0;for(let i=0;i<2**n;i++){let l=Array.from({length:n},(_,j)=>(i>>j)&1);R.low_fibers++;let x=closure(n,E,l);if(x)sat++;if(ref){let c=reference(n,E,l);counts+=c;ok(!!x===(c>0))}if(expect)ok(!!x===expect(l))}
 R.cases.push({name,n,stars:E.length,max_terminal_degree:degree(n,E),low_support:sat,terminal_color_words:ref?counts:null});return sat}
let f=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
let used=Array(7).fill(-1);
function aug(i,seen){for(let v of f[i])if(!seen[v]){seen[v]=true;if(used[v]<0||aug(used[v],seen)){used[v]=i;return true}}return false}
for(let i=0;i<7;i++)ok(aug(i,Array(7).fill(false)));
let piv=Array(7);used.forEach((i,v)=>piv[i]=v);
function compile(triples,signs,dup){return triples.flatMap((t,i)=>{let a=piv[i],b=t.filter(v=>v!==a);let s=[a,...b].map(v=>signs[i][t.indexOf(v)]);return dup?[star(a,...b,s,0),star(a,...b,s,1)]:[star(a,...b,s,0)]})}
function nae(triples,signs,l){return triples.every((t,i)=>{let w=t.map((v,j)=>l[v]^signs[i][j]);return w.some(x=>x!==w[0])})}
let zero=f.map(()=>[0,0,0]);
ok(evaluate("Fano one-star physical",7,compile(f,zero,false))>0);
ok(evaluate("Fano exact doubled",7,compile(f,zero,true),l=>nae(f,zero,l))===0);
for(let i=0;i<7;i++)for(let j=0;j<3;j++){let s=zero.map(x=>x.slice());s[i][j]=1;ok(evaluate("Fano sign "+i+":"+j,7,compile(f,s,true),l=>nae(f,s,l))===10)}
for(let k=2;k<=5;k++){let E=Array.from({length:k},(_,i)=>star(k+i,i,(i+1)%k,[0,0,0],i===0?(k%2):0)); // XOR eta^1 = 0 currently; toggle first to make odd
 E[0].eta^=1;
 ok(evaluate("unbalanced rim "+k,2*k,E,l=>l.some(x=>x!==l[0]),k<=4)===2**(2*k)-2);
 E[0].eta^=1;ok(evaluate("balanced rim "+k,2*k,E,()=>true,k<=4)===2**(2*k));
}
let seed=R.seed;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}
for(let z=0;z<20;z++){let n=5,E=[];for(let i=0;i<6;i++){let a=rnd(n),b=rnd(n),c=rnd(n);while(b===a)b=rnd(n);while(c===a||c===b)c=rnd(n);E.push(star(a,b,c,[rnd(2),rnd(2),rnd(2)],rnd(2)))}evaluate("random "+z,n,E)}
// root local full affine hull: all 3 terminal colors support except 4-color coverage; verify rank 6
function rank(rows){let b=Array(6).fill(0),r=0;for(let x of rows){for(let j=5;j>=0;j--)if((x>>j)&1){if(b[j])x^=b[j];else{b[j]=x;r++;break}}}return r}
for(let eta=0;eta<2;eta++)for(let s=0;s<8;s++){let E=star(0,1,2,[s&1,(s>>1)&1,(s>>2)&1],eta);let v=[];for(let w=0;w<64;w++){let x=[w&3,(w>>2)&3,(w>>4)&3];let expected=!(active(E,x.map(t=>t&1))&&((x[1]>>1)^(x[2]>>1))===eta);let actual=new Set(forbidden(E,x)).size<4;ok(expected===actual);if(actual)v.push(w)}ok(rank(v.map(x=>x^v[0]))===6)}
return R
}
console.log(JSON.stringify(run(),null,2));
