'use strict';
// TMR-1/082 standalone reproducible finite certificate (not a proof).
const S=[1,3], mod=x=>((x%5)+5)%5, R=(a,b)=>S.includes(mod(b-a));
let checks=0,source=0,witness=0,failures=0;
function ok(v,label){checks++;if(!v){failures++;throw Error(label);}}
function build(n,H,kind){let N=n, E=[];for(const [u,v] of H){if(kind===4){const w=N++,z=N++;E.push([u,w],[w,z],[u,z],[w,v]);}else{const a=N++,b=N++,c=N++;E.push([u,a],[a,b],[b,c],[u,c],[c,v]);}}return {N,E};}
function motifCount(N,E,k){const a=Array.from({length:N},()=>Array(N).fill(false));for(const [x,y] of E)a[x][y]=true;let z=0;
if(k===2){for(let x=0;x<N;x++)for(let y=0;y<N;y++)if(a[x][y])for(let v=0;v<N;v++)if(a[y][v]&&a[x][v])z++;}
else {for(let x=0;x<N;x++)for(let y=0;y<N;y++)if(a[x][y])for(let v=0;v<N;v++)if(a[y][v])for(let w=0;w<N;w++)if(a[v][w]&&a[x][w])z++;}
return z;}
function test(){
const shortcut=[];for(let l=1;l<=8;l++){let c=0;for(let x=0;x<(1<<l);x++){let d=0;for(let j=0;j<l;j++)d+=((x>>j)&1)?3:1;if(S.includes(mod(d)))c++;}shortcut.push(c);}ok(shortcut[1]===1&&shortcut[2]===1&&shortcut[3]===10,'shortcut multiplicities');
for(let kind of [4,5])for(let delta=0;delta<5;delta++){
let c=0;for(let a=0;a<5;a++)for(let b=0;b<5;b++)for(let d=0;d<5;d++){
if(kind===4){if(d!==0)continue;if(R(0,a)&&R(a,b)&&R(0,b)&&R(a,delta))c++;}
else if(R(0,a)&&R(a,b)&&R(b,d)&&R(0,d)&&R(d,delta))c++;
}ok(c===([0,1,0,0,1][delta]),'endpoint kind '+kind+' delta '+delta);
}
for(let n=0;n<=5;n++){const pairs=[];for(let u=0;u<n;u++)for(let v=u+1;v<n;v++)pairs.push([u,v]);
for(let mask=0;mask<2**pairs.length;mask++){const H=pairs.filter((_,j)=>(mask>>j)&1);source++;
for(let kind of [4,5]){const {N,E}=build(n,H,kind);ok(N===n+(kind===4?2:3)*H.length,'vertices');ok(E.length===(kind===4?4:5)*H.length,'arcs');ok(motifCount(N,E,kind===4?2:3)===H.length,'motif count');ok(motifCount(N,E,kind===4?3:2)===0,'no wrong shortcut');}
for(let t=0;t<5**n;t++){let a=Array(n),z=t;for(let i=0;i<n;i++){a[i]=z%5;z=Math.floor(z/5);}let legal=H.every(([u,v])=>[1,4].includes(mod(a[v]-a[u])));
for(let kind of [4,5]){const {N,E}=build(n,H,kind),c=a.slice();for(const [u,v] of H){if(kind===4){c.push(mod(a[u]+3),mod(a[u]+1));}else{c.push(mod(a[u]+1),mod(a[u]+2),mod(a[u]+3));}}
ok(E.every(([u,v])=>R(c[u],c[v]))===legal,'explicit extension');witness++;}
}
}}
const out={id:'TMR1-T5-SHORTCUT082-PUBLIC',shortcuts:shortcut,sourceGraphs:source,explicitExtensions:witness,assertions:checks,failures};console.log(JSON.stringify(out,null,2));}
test();
