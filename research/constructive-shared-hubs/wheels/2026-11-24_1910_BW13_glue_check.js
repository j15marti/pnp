function run(){
let assertions=0, rawFalse=0, repairedFalse=0, referenceChecks=0;
function assert(x){assertions++;if(!x)throw Error("assertion")}
function allowed(a,b,c,eta){return new Set([a,a^2,b^1,c^3^(eta*2)]).size<4}
function region(a,d,b,c,e){return allowed(a,b,c,e)&&allowed(d,b,c,e^1)}
for(let z=0;z<64;z++){
 let l=Array.from({length:6},(_,i)=>(z>>i)&1); // b,c,a,d,p,q
 let [b,c,a,d,p,q]=l;
 let expected=!(b===c&&c===a&&a===d)&&!(b===c&&c===p&&p===q);
 let direct=false;
 for(let h=0;h<64;h++){let x=l.map((v,i)=>v+2*((h>>i)&1));referenceChecks++;if(region(x[2],x[3],x[0],x[1],0)&&region(x[4],x[5],x[0],x[1],1))direct=true}
 if(expected&&!direct)rawFalse++;
 assert(!direct||expected);
 // Each private rim is connected by two physical exclusions of low difference 1.
 // Verify all 64 external high words, independently enumerate four private rim highs.
 for(let h=0;h<64;h++){let x=l.map((v,i)=>v+2*((h>>i)&1)), good=true;
 for(let [u,v,eta] of [[2,3,0],[4,5,1]]){let exists=false;for(let w=0;w<4;w++){
  let B=b+2*(w&1), C=c+2*((w>>1)&1);
  referenceChecks++;
  if([x[0]^B,x[1]^C].every(t=>t!==1&&t!==3)&&region(x[u],x[v],B,C,eta))exists=true
 }good=good&&exists}
 if(good!==expected)repairedFalse++;
 assert(good===expected);
 }
}
assert(rawFalse>0);return {assertions,raw_false_negative_low_fibers:rawFalse,repaired_discrepancies:repairedFalse,referenceChecks}
}
console.log(JSON.stringify(run(),null,2));
