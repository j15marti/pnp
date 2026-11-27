// Exact C6-prism local port relation with rungs forbidden in the zero matching.
// Independent enumeration of proper internal edge colors; bit i is port i.
const words=[];
let states=0;
for(let w=0;w<64;w++){
  let valid=false;
  function rec(e,c){
    states++;
    if(e===6){
      for(let i=0;i<6;i++)if(new Set([c[(i+5)%6],c[i],1+((w>>i)&1)]).size!==3)return;
      valid=true;return;
    }
    for(let v=0;v<3;v++)rec(e+1,[...c,v]);
  }
  rec(0,[]);
  if(valid)words.push(w);
}
const a=33,b=12,i=2,D=[0,2,3,5],attempted=D.filter(j=>j!==i).map(j=>a^(1<<i)^(1<<j));
if(words.length!==14||!words.includes(a)||!words.includes(b)||attempted.some(x=>words.includes(x)))throw Error("exchange falsifier failed");
console.log(JSON.stringify({words,a,b,i,D,attempted,states}));
