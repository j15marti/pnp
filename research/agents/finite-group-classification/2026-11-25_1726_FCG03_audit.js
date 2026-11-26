// FCG03 standalone independent finite audit. Run node <file>.
console.log(JSON.stringify((function audit(){
const B=[0,5,6,9,10,15], bit=(m,i)=>(m>>i)&1, P=[0,1,2,3], pc=m=>m.toString(2).replace(/0/g,"").length;
const exchange=T=>T.length>0&&T.every(a=>T.every(b=>P.every(i=>!bit(a^b,i)||P.some(j=>j!==i&&bit(a^b,j)&&T.includes(a^(1<<i)^(1<<j))))));
function graph(T){
if(!exchange(T))return null;const t=T[0],U=T.map(a=>a^t),A=P.filter(i=>bit(t,i)===(i>=2?1:0)),D=P.filter(i=>!A.includes(i)),E=U.filter(x=>pc(x)===2);let n=4,edges=[],ports=[...P];const members=x=>P.filter(i=>bit(x,i));
if(U.includes(15)){for(const a of E)edges.push(members(a^15))}
else if(E.length){n=6;for(const i of A)if(E.some(a=>bit(a,i)))edges.push([4,A.find(j=>j!==i)]);for(const i of D)if(E.some(a=>bit(a,i)))edges.push([5,D.find(j=>j!==i)]);edges.push(members(E[0]))}
else{n=8;for(const i of P)edges.push([i,i+4])}
for(const i of P)if(bit(t,i)){ports[i]=n++;edges.push([i,ports[i]])}
return {n,edges,ports}
}
function pm(g,word){let mask=(1<<g.n)-1;for(const i of P)if(bit(word,i))mask^=1<<g.ports[i];function rec(m){if(!m)return true;let i=0;while(!bit(m,i))i++;for(const [a,b] of g.edges){const j=a===i?b:b===i?a:-1;if(j>=0&&bit(m,j)&&rec(m^(1<<i)^(1<<j)))return true}return false}return rec(mask)}
let catalogue=[],checks=0;for(let m=0;m<64;m++){const T=B.filter((a,i)=>bit(m,i)),g=graph(T);if(g){for(let w=0;w<16;w++){checks++;if(pm(g,w)!==T.includes(w))throw Error("mask mismatch")}}catalogue.push({mask:m,words:T,admitted:!!g,vertices:g?.n??null})}
const H=[[0,2,1],[0,3,4],[3,5,6],[5,7,1],[8,2,9],[8,10,4],[10,11,6],[11,7,9],[0,8,2],[9,7,1],[3,10,4],[5,11,6]],C=[1,0,1,0,0,1,0,1,2,2,2,2];
const models=[];for(let w=0;w<4096;w++)if(H.every(c=>c.reduce((s,i)=>s+bit(w,i),0)===1))models.push(w);
for(let i=0;i<12;i++)if(H.map((c,j)=>c.includes(i)?C[j]:-1).filter(x=>x>=0).sort().join()!=="0,1,2")throw Error("partition");
const local=[];for(let w=0;w<32;w++){const [a,b,c,d,e]=[0,1,2,3,4].map(i=>bit(w,i));if(a+b+c===1&&d+b+e===1&&a+b+d===1)local.push(a+2*c+4*d+8*e)}
const mask=[...new Set(local)].sort((a,b)=>a-b);if(mask.join()!=="0,6,9"||exchange(mask)||!models.includes(212))throw Error("source mask");
return {catalogue,checks,admitted:catalogue.filter(x=>x.admitted).length,source:{H,C,models,mask},limitations:"Independent bounded graph and local exhaustive audit; planarity/connectivity and scalable tests in Python bundle."}
})(),null,2));
