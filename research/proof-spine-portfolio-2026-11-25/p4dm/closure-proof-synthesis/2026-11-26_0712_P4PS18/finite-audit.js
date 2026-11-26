function audit(){
 const pop=x=>{let n=0;while(x){x&=x-1;n++}return n}, bit=(x,i)=>(x>>i)&1;
 let parityTables=0,bijunctive=0,edmCount=0;
 for(let n=1;n<=4;n++)for(let p=0;p<2;p++){
 const words=Array.from({length:1<<n},(_,i)=>i).filter(x=>pop(x)%2===p);
 for(let s=1;s<(1<<words.length);s++){
 const R=words.filter((_,i)=>bit(s,i)),S=new Set(R);parityTables++;
 const maj=R.every(a=>R.every(b=>R.every(c=>S.has((a&b)|(a&c)|(b&c)))));
 if(!maj)continue;bijunctive++;
 const T=R.map(x=>x^R[0]), groups=new Map();
 for(let i=0;i<n;i++){let key=T.map(x=>bit(x,i)).join("");if(key.includes("1")){if(!groups.has(key))groups.set(key,[]);groups.get(key).push(i);}}
 const G=[...groups.values()];if(G.some(g=>g.length%2))throw Error("odd block");
 const masks=G.map(g=>g.reduce((a,i)=>a|(1<<i),0)),B=T.map(x=>G.reduce((a,g,j)=>a|(bit(x,g[0])<<j),0));
 const pairOK=(x,i,j)=>B.some(y=>bit(x,i)===bit(y,i)&&bit(x,j)===bit(y,j));
 let count=0;for(let x=0;x<1<<G.length;x++){if(!G.every((g,i)=>G.every((h,j)=>pairOK(x,i,j))))continue;count++;let y=masks.reduce((a,m,i)=>a^(bit(x,i)?m:0),R[0]);if(!S.has(y))throw Error("bad projection");}
 if(count!==R.length)throw Error("bad count");
 const edm=R.every(a=>R.every(b=>Array.from({length:n},(_,i)=>i).every(i=>!bit(a^b,i)||Array.from({length:n},(_,j)=>j).some(j=>j!==i&&bit(a^b,j)&&S.has(a^(1<<i)^(1<<j))))));
 if(edm)edmCount++;if(edm!==(G.every(g=>g.length===2)&&R.length===1<<G.length))throw Error("EDM");
 }}
 const E=Array.from({length:9},(_,i)=>[Math.floor(i/3),i%3]);
 const isMatching=x=>E.every(([a,b],i)=>!bit(x,i)||E.every(([c,d],j)=>j===i||!bit(x,j)||(a!==c&&b!==d)));
 const M=Array.from({length:512},(_,i)=>i).filter(isMatching), P=M.filter(x=>pop(x)===3);
 let seed=26112618;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};
 let fibers=0,admitted=0,clauseCases=0,empty=0;
 for(let t=0;t<1512;t++){
 const A=E.map((_,i)=>t<512?bit(t,i):rnd(1<<(2+Math.floor((t-512)/200))));
 const val=x=>A.reduce((a,c,i)=>a^(bit(x,i)?c:0),0);
 const F=M.filter(x=>val(x)===0),S=new Set(F);
 const edm=F.every(a=>F.every(b=>E.every((_,i)=>!bit(a^b,i)||S.has(a^(1<<i)))));
 const zero=A.reduce((a,c,i)=>a|(!c?1<<i:0),0);
 const criterion=isMatching(zero)&&!F.some(x=>x!==0&&(x&zero)===0);
 if(edm!==criterion)throw Error("zero fiber criterion");
 if(edm){admitted++;const span=new Set([0]);for(const a of A)for(const s of [...span])span.add(s^a);if(span.size<4)throw Error("rank bound");}fibers++;
 }
 const pairs=[];for(let i=0;i<9;i++)for(let j=i+1;j<9;j++)if(E[i][0]===E[j][0]||E[i][1]===E[j][1])pairs.push([i,j]);
 for(let t=0;t<1000;t++){
 const C=Array.from({length:rnd(10)},()=>[...pairs[rnd(pairs.length)],rnd(2),rnd(2)]);
 const valid=(x,c)=>bit(x,c[0])!==c[2]||bit(x,c[1])!==c[3];
 const expected=P.filter(x=>C.every(c=>valid(x,c)));
 let allowed=511;
 for(const c of C){const [i,j]=c,side=E[i][0]===E[j][0]?0:1;
 for(let k=0;k<9;k++)if(E[k][side]===E[i][side]&&!valid(1<<k,c))allowed&=~(1<<k);}
 const got=P.filter(x=>(x&allowed)===x);
 if(expected.join()!==got.join())throw Error("context absorption");if(!got.length)empty++;clauseCases++;
 }
 return {parityTables,bijunctive,edmCount,fibers,admitted,clauseCases,empty,seed:26112618};
}
console.log(JSON.stringify(audit(),null,2));
