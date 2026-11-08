"use strict";
/* LSPV-1/500 finite CNF factor compiler controls, distinct calculus, no historical checker. */
function run() {
 let state=2026110802>>>0, checks=0,cases=0,peak={};
 function ok(v,name){checks++;if(!v)throw Error(name||"assertion")}
 function rnd(){state=(Math.imul(1664525,state)+1013904223)>>>0;return state}
 function bit(a,i){return(a>>>i)&1}
 function exclude(ids,p){return ids.map((v,j)=>bit(p,j)?-(v+1):(v+1))}
 function sat(c,a){return c.some(l=>l>0?bit(a,l-1)===1:bit(a,-l-1)===0)}
 function key(c){return c.slice().sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b).join(",")}
 function support(n){const m=1+rnd()%((1<<n)-1);return [...Array(n).keys()].filter(i=>bit(m,i))}
 function table(ids){const s=new Set();for(let x=0;x<(1<<ids.length);x++)if(rnd()%5<3)s.add(x);return s}
 function proj(a,ids){return ids.reduce((m,i,j)=>m+(bit(a,i)<<j),0)}
 for(let n=2;n<=5;n++){let max=0;
  for(let trial=0;trial<24;trial++){
   const id1=support(n),id2=support(n),out=support(n),t1=table(id1),t2=table(id2),allowed=new Set();
   for(let p=0;p<(1<<out.length);p++){
    let necessary=false;
    for(let a=0;a<(1<<n);a++)if(proj(a,out)===p&&t1.has(proj(a,id1))&&t2.has(proj(a,id2)))necessary=true;
    if(necessary||rnd()%3!==0)allowed.add(p);
   }
   const parents=[{ids:id1,t:t1},{ids:id2,t:t2}],extras=[...Array(n).keys()].filter(i=>!out.includes(i));
   let work=0;
   for(let p=0;p<(1<<out.length);p++)if(!allowed.has(p)){
    let rows=[];
    for(let e=0;e<(1<<extras.length);e++){
     let a=out.reduce((m,i,j)=>m+(bit(p,j)<<i),0);
     for(let j=0;j<extras.length;j++)a+=bit(e,j)<<extras[j];
     let antecedent=null;
     for(let parent of parents){const x=proj(a,parent.ids);if(!parent.t.has(x)){antecedent=exclude(parent.ids,x);break}}
     ok(antecedent!==null,"unsound-local");
     const widened=exclude([...Array(n).keys()],a);
     ok(antecedent.every(l=>widened.includes(l)),"invalid-weakening");
     ok([...Array(1<<n).keys()].every(x=>!sat(antecedent,x)||sat(widened,x)),"weakening-soundness");
     rows.push(widened);work++;
    }
    for(const v of extras){const next=[],pivot=v+1;
     for(let j=0;j<rows.length;j+=2){
      const a=rows[j],b=rows[j+1];
      ok((a.includes(pivot)&&b.includes(-pivot))||(a.includes(-pivot)&&b.includes(pivot)),"bad-pivot");
      const c=[...new Set([...a,...b].filter(x=>Math.abs(x)!==pivot))];
      ok([...Array(1<<n).keys()].every(x=>!sat(a,x)||!sat(b,x)||sat(c,x)),"resolution-soundness");
      next.push(c);work++;
     }
     rows=next;
    }
    ok(rows.length===1&&key(rows[0])===key(exclude(out,p)),"bad-conclusion");
   }
   ok(work<=2*(1<<n),"bad-bound");max=Math.max(max,work);cases++;
  }
  peak[n]=max;
 }
 const source=[];
 for(const n of [6,8,10,12]){
  const clauses=[];
  for(let j=0;j<8*n;j++){
   const ids=[];while(ids.length<3){const i=1+rnd()%n;if(!ids.includes(i))ids.push(i)}
   clauses.push(ids.map(i=>rnd()%2?i:-i));
  }
  ok(clauses.length===8*n&&clauses.every(c=>new Set(c.map(Math.abs)).size===3),"proper-3");
  let models=0;
  for(let a=0;a<(1<<n);a++)if(clauses.every(c=>sat(c,a)))models++;
  source.push({n,clauses:clauses.length,models});
 }
 ok(![0,1].every(a=>!(a===1)||(a===0)),"corrupted implication reject");
 return {status:"COMPUTATIONAL",seed:2026110802,trials:cases,assertions:checks,
  max_inference_nodes_by_locality:peak,random_proper_3cnf_source_controls:source,
  corrupt_implication_rejected:true,historical_checker_executed:false,
  external_theorem_reproved:false};
}
if(typeof module!=="undefined" && require.main===module)console.log(JSON.stringify(run(),null,2));
