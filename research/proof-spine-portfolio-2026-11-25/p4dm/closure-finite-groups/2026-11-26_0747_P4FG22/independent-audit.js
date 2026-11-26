function independent(){
 let seed=2611262202; const rand=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed};const pc=x=>{let n=0;while(x){n++;x&=x-1}return n};
 let checks=0,penaltyChecks=0; const cases=[];
 for(let u=0;u<2;u++)for(let v=0;v<2;v++)for(let y=0;y<2;y++){let p=u*v-2*u*y-2*v*y+3*y;if(p<0||((p===0)!==(y===u*v)))throw Error("AND");penaltyChecks++}
 for(const k of [5,6,7]){
  let d=k-1, s=(1<<Math.floor(d/2))-1, all=(1<<d)-1;
  let masks=[];for(let m=1;m<=all;m++)if(pc(m)>1&&((m&s)===m||(m&(all^s))===m))masks.push(m);
  let total=0,n=k===7?4:24;
  for(let t=0;t<n;t++){
   let f=Array.from({length:1<<d},()=>BigInt(rand()%101)-50n), c=f.slice();
   for(let j=0;j<d;j++)for(let m=0;m<=all;m++)if(m&(1<<j))c[m]-=c[m^(1<<j)];
   let M=1n+c.reduce((a,x)=>a+(x<0n?-x:x),0n);
   for(let x=0;x<=all;x++){
    let best=null;
    for(let y=0;y<1<<masks.length;y++){
     function bit(m){if(!m)return 1n;if(pc(m)===1)return (x&m)?1n:0n;return BigInt((y>>masks.indexOf(m))&1)}
     let val=0n;
     for(let m=0;m<=all;m++)val+=c[m]*bit(m&s)*bit(m&(all^s));
     for(const m of masks){let a=bit(m&-m),b=bit(m^(m&-m)),z=bit(m);val-=M*(a*b-2n*a*z-2n*b*z+3n*z)}
     if(best===null||val>best)best=val;
    }
    if(best!==f[x])throw Error("wrong value");checks++;total++;
   }
  }
  cases.push({k,tables:n,aux:masks.length,checks:total});
 }
 return {seed:2611262202,checks,penaltyChecks,cases}
}
console.log(JSON.stringify(independent(),null,2));
