// Four-arc parsimonious T5 gadget reuses the TMR-2/068 unique-successor triangle.
// For each C5 edge u<v: u->z, u->w, w->z, w->v; z=u+1, w=u+3 unique.
const verify = function verify(){
 const R=(a,b)=>{let d=(b-a+5)%5;return d===1||d===3};
 const C=(a,b)=>{let d=(b-a+5)%5;return d===1||d===4};
 let checks=0,graphs=0,C5assignments=0,validCount=0;
 const ok=(v,msg)=>{checks++;if(!v)throw Error(msg)};
 const t=Array.from({length:5},()=>Array(5).fill(0));
 for(let a=0;a<5;a++)for(let b=0;b<5;b++){
   let count=0;
   for(let z=0;z<5;z++)for(let w=0;w<5;w++)if(R(a,z)&&R(a,w)&&R(w,z)&&R(w,b)){count++;ok(z===(a+1)%5&&w===(a+3)%5,'unique extension');}
   t[a][b]=count;ok(count===(C(a,b)?1:0),`endpoint ${a},${b}`);
 }
 for(let n=0;n<=4;n++){
  const edges=[];
  for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)edges.push([i,j]);
  for(let mask=0;mask<2**edges.length;mask++){
   const E=edges.filter((_,j)=>(mask>>j)&1);
   let colorings=0,weighted=0;
   for(let z=0;z<5**n;z++){
     let k=z,colors=[];
     for(let i=0;i<n;i++){colors.push(k%5);k=Math.floor(k/5)}
     let good=E.every(([u,v])=>C(colors[u],colors[v]));
     if(good)colorings++;
     let prod=1;
     for(const [u,v] of E)prod*=t[colors[u]][colors[v]];
     weighted+=prod;
   }
   ok(weighted===colorings,`graph n${n} mask${mask}`);
   if(n)ok(colorings%5===0,'free translation orbit');
   graphs++;C5assignments+=colorings;validCount+=weighted;
  }
 }
 // Functional 3CNF exactly-one + forbidden-pair compiler:
 const cnf=(n,E)=>{
   let c=[];
   for(let i=0;i<n;i++){
    for(let a=0;a<5;a++)for(let b=a+1;b<5;b++)c.push([-(5*i+a+1),-(5*i+b+1)]);
    let left=5*i+1;
    for(let j=1;j<=3;j++){
      const y=5*n+3*i+j;
      const x=5*i+j+1;
      c.push([-left,y],[-x,y],[left,x,-y]);left=y;
    }
    c.push([left,5*i+5]);
   }
   for(const [u,v] of E)for(let a=0;a<5;a++)for(let b=0;b<5;b++)if(!R(a,b))c.push([-(5*u+a+1),-(5*v+b+1)]);
   ok(c.length===20*n+15*E.length,'CNF clause count');
   ok(c.every(cl=>cl.length<=3),'CNF width');
   return c;
 };
 const phi=cnf(2,[[0,1]]);
 const evaluate=(bits)=>phi.every(cl=>cl.some(l=>l>0?bits[l-1]:!bits[-l-1]));
 for(let mask=0;mask<1024;mask++){
   let bits=Array(16).fill(false);
   for(let i=0;i<10;i++)bits[i]=!!(mask&(1<<i));
   for(let i=0;i<2;i++){
     let acc=bits[5*i];
     for(let j=1;j<=3;j++){acc=acc||bits[5*i+j];bits[10+3*i+j-1]=acc}
   }
   let values=[0,1].map(i=>[0,1,2,3,4].filter(a=>bits[5*i+a]));
   let should=values[0].length===1&&values[1].length===1&&R(values[0][0],values[1][0]);
   ok(evaluate(bits)===should,`CNF mask ${mask}`);
 }
 return {revision:"tmr1-t5-parsimonious072-published.v1",mode:"exhaustive finite symbolic-gadget checks, no randomness",gadgetEndpointPairs:25,undirectedGraphsEnumerated:graphs,sourceC5Colorings:C5assignments,weightedExpandedT5Colorings:validCount,oneHotBooleanPatternsChecked:1024,assertions:checks,failures:0};
};
console.log(JSON.stringify(verify(),null,2));
