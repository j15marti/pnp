// Standalone independent native reference; node reference.js
const guards=[[7,13,15,18,21,23,26,27,31,33,36,41,44,50,53,57,65,78,81,87,90,94,95,97,98,104,106,111,116,119,124],[9,10,16,17,23,25,27,28,29,32,42,44,52,65,69,71,72,74,75,76,82,83,87,95,103,104,105,109,111,115,125,126],[1,4,11,19,23,24,28,30,33,36,39,40,41,59,65,67,70,82,87,91,92,109,110,112,120],[1,2,5,7,21,23,26,28,37,39,40,41,44,45,47,52,58,60,61,64,69,77,79,92,97,100,110,117,118,121],[0,7,9,16,17,20,24,25,27,30,33,35,49,50,52,54,68,69,75,76,80,85,91,101,103,110,114,115,124],[0,7,10,15,26,27,33,35,36,39,49,52,58,61,64,70,82,83,87,94,95,103,106,110,112,115,117,119,121,126],[0,4,8,12,13,20,22,27,28,31,40,42,46,55,57,62,63,67,68,69,71,73,76,80,88,95,101,103,111,126],[5,7,9,20,21,22,30,31,50,55,56,64,65,67,69,70,83,85,90,92,96,98,99,104,105,107,116,119,121,126]];
function reference(guards) {
 const k=4, cmp=(a,b)=>{for(let i=0;i<a.length;i++)if(a[i]!==b[i])return a[i]-b[i];return 0}, F=new Map();
 const face=(vs)=>{vs.sort(cmp);F.set(JSON.stringify(vs),vs)};
 for(const s of [-1,1])for(const t of [-1,1])for(const u of [-1,1]){
 const v=(a,b)=>[s*a||0,t*b||0,u*(k-a-b)||0];
 for(let a=0;a<k;a++)for(let b=0;b<k-a;b++){face([v(a,b),v(a+1,b),v(a,b+1)]);if(a+b+2<=k)face([v(a+1,b),v(a,b+1),v(a+1,b+1)]);}}
 const fs=[...F.values()].sort((a,b)=>cmp(a.flat(),b.flat()));const color=v=>(Math.abs(v[1])+2*Math.abs(v[2]))%3;
 const V=[0,1,2].map(c=>[...new Map(fs.flat().filter(v=>color(v)===c).map(v=>[v.join(","),v])).values()].sort(cmp));
 const T=fs.map(f=>V.map((W,c)=>W.findIndex(v=>v.join(",")===f.find(x=>color(x)===c).join(","))));const q=V[0].length;
 if(T.length!==128||q!==22||V.some(W=>W.length!==q)||new Set(T.map(t=>t.join(","))).size!==128)throw Error("source mismatch");
 const masks=T.map(t=>t.reduce((a,v,c)=>a|(1n<<BigInt(c*q+v)),0n));
 return guards.map((g,job)=>{const bad=new Set(g);let nodes=0;const memo=new Set();const adj=Array.from({length:3*q},(_,v)=>masks.map((m,i)=>[m,i]).filter(([m,i])=>!bad.has(i)&&((m>>BigInt(v))&1n)).map(([m,i])=>i));
 function search(left){if(++nodes>65536)throw Error("reference cap");if(!left)return true;if(memo.has(left))return false;let best=null;for(let v=0;v<3*q;v++)if((left>>BigInt(v))&1n){const z=adj[v].filter(i=>(masks[i]&left)===masks[i]);if(best===null||z.length<best.length)best=z;if(!best.length)break;}for(const i of best)if(search(left^masks[i]))return true;memo.add(left);return false;}
 const sat=search((1n<<BigInt(3*q))-1n);if(sat)throw Error("mislabelled NO");return {job,triples:T.length,owners_per_color:q,deleted:g.length,reference:"NO",nodes};});
}
console.log(JSON.stringify(reference(guards),null,2));
