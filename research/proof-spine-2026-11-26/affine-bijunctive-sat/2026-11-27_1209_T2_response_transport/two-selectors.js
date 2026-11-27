function twoBits(a){const p=x=>{let z=0;while(x){x&=x-1;z^=1}return z},F=a.classes.flatMap(c=>c.forced.map(([s,y])=>{let v=0;for(let i=0;i<4;i++)if(c.m>>i&1)v^=(s+64)<<(7*i);return[v,y,c.m,s]}));let work=0;function solve(F){let B=Array(28).fill(null);for(let [v,y] of F){for(let j=0;j<28;j++)if(v>>j&1){if(!B[j]){B[j]=[v,y];break}v^=B[j][0];y^=B[j][1];work++}if(!v&&y)return null}let x=0;for(let i=27;i>=0;i--)if(B[i]&&(p(B[i][0]&x)!==B[i][1]))x|=1<<i;return x}
 let tried=0,success=0,first=null;for(let g=1;g<64;g++)for(let h=g+1;h<64;h++){if((g^h)<h)continue;tried++;let C=Array.from({length:4},(_,i)=>solve(F.filter(([v,y,m,s])=>(p(g&s)+2*p(h&s))===i)));if(C.some(x=>x===null))continue;success++;if(!first)first={g,h,C}}
 if(first){let {g,h,C}=first;for(let [v,y,m,s] of F)if(p(v&C[p(g&s)+2*p(h&s)])!==y)throw Error("verification")}
 return{tried,success,first,work};}
const fs=require('node:fs');console.log(JSON.stringify(twoBits(JSON.parse(fs.readFileSync(process.argv[2],'utf8'))),null,2));
