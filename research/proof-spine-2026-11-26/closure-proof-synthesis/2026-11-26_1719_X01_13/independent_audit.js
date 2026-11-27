// Independent exhaustive 3-dimensional adaptive fiber certificate audit.
// node audit.js
const span = xs => { const s=new Set([0]); for(const x of xs) for(const y of [...s]) s.add(x^y); return s; };
const diff = xs => new Set(xs.flatMap(x=>xs.map(y=>x^y)).filter(x=>x));
const intersect = ss => new Set([...ss[0]].filter(x=>ss.every(s=>s.has(x))));
const sum = (A,B) => new Set([...A].flatMap(x=>[...B].map(y=>x^y)));
let assertions=0;
function check(x){assertions++;if(!x)throw Error("assertion "+assertions);}
const F=[];
for(let p=1;p<=7;p++){
 let found;
 for(let a=1;a<=7&&!found;a++)for(let b=1;b<=7&&!found;b++)for(let c=1;c<=7;c++)
 if((a^b^c)===p && span([a,b,c]).size===8){found=[0,a,b,c];break;}
 F.push(found);
 check(!!found); check(diff(found).size===6);check(!diff(found).has(p));
 check(span([...diff(found)]).size===8);
 check(Array.from({length:7},(_,j)=>j+1).every(d=>found.some(x=>!found.includes(x^d))));
}
check(intersect(F.map(diff)).size===0);
check(intersect(F.map(s=>span([...diff(s)]))).size===8);
let triples=0, combinations=0, lifts=0;
for(const a of F)for(const b of F)for(const c of F){
 triples++;
 let basis;
 for(const x of diff(a))for(const y of diff(b))for(const z of diff(c))
 if(!basis&&span([x,y,z]).size===8)basis=[x,y,z];
 check(!!basis);check(sum(sum(a,b),c).size===8);
 const pairs=[a,b,c].map((f,i)=>{for(const x of f)if(f.includes(x^basis[i]))return [x,x^basis[i]];});
 for(let target=0;target<8;target++){
 let found=false;
 for(let m=0;m<8;m++){combinations++;const actual=pairs.map((p,i)=>p[(m>>i)&1]);if((actual[0]^actual[1]^actual[2])===target){check(actual.every((x,i)=>[a,b,c][i].includes(x)));found=true;lifts++;break;}}
 check(found);
 }
}
check(F.every(f=>f.length===4 && span(f).size===8));
const result={assertions,triples,combinations,lifts,fibers:F,commonActualNonzero:intersect(F.map(diff)).size,commonSpanSize:intersect(F.map(s=>span([...diff(s)]))).size};
console.log(JSON.stringify(result,null,2));
