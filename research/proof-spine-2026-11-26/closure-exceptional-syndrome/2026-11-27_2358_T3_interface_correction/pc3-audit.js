function pcAudit(){
const lines=[[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]],pop=x=>{let n=0;while(x){x&=x-1;n++}return n},xor=(a,b)=>{let c=new Set(a);for(let x of b)c.has(x)?c.delete(x):c.add(x);return c},mul=(a,b)=>{let c=new Set();for(let x of a){let y=x|b;c.has(y)?c.delete(y):c.add(y)}return c};
function clause(c){let S=new Set([0]);for(let [v,positive] of c){let T=mul(S,1<<v);S=positive?xor(S,T):T}return S}
function close(n,C,d,cap,target){
 let B=new Map(),nodes=[],ops=0,passes=0,status="UNKNOWN",peak=0;function count(k=1){ops+=k;if(ops>cap)throw Error("cap")}
 function node(poly,rule){let i=nodes.length;nodes.push({poly:[...poly].sort((a,b)=>a-b),rule});peak=Math.max(peak,poly.size);return i}
 function combine(i,j){let a=new Set(nodes[i].poly),b=new Set(nodes[j].poly);count(a.size+b.size);return node(xor(a,b),["xor",i,j])}
 function insert(i){let S=nodes[i].poly;while(S.length){let p=S[S.length-1];count();if(!B.has(p)){B.set(p,i);return true}i=combine(i,B.get(p));S=nodes[i].poly}return false}
 function reduce(S){let p=new Set(S),parents=[];while(p.size){let q=Math.max(...p);count();if(!B.has(q))return{missing:[...p],parents};let i=B.get(q);parents.push(i);p=xor(p,new Set(nodes[i].poly));count(nodes[i].poly.length)}return{missing:[],parents}}
 let targetProof=null;
 try{
 for(let j=0;j<C.length;j++){let p=C[j];if([...p].some(x=>pop(x)>d))throw Error("input degree");insert(node(p,["input",j]))}
 for(;;){passes++;let before=B.size;
 // For each multiplier, compute the full kernel of overflow on the entire current span, not only admissible individual basis rows.
 for(let v=0;v<n;v++){let overflow=new Map();for(let row of [...B.values()]){
 let m=1<<v,orig=new Set(nodes[row].poly);count(orig.size);let product=mul(orig,m),parents=new Set([row]),over=new Set([...product].filter(x=>pop(x)>d));
 while(over.size){let p=Math.max(...over);count();if(!overflow.has(p)){overflow.set(p,{over,parents});break}let q=overflow.get(p);over=xor(over,q.over);parents=xor(parents,q.parents);count(q.over.size+q.parents.size)}
 if(!over.size){let ids=[...parents];if(!ids.length)continue;let i=ids[0];for(let j=1;j<ids.length;j++)i=combine(i,ids[j]);let S=mul(new Set(nodes[i].poly),m);count(S.size);if([...S].some(x=>pop(x)>d))throw Error("overflow");insert(node(S,["mul",i,v]))}
 }}
 let r=reduce(target);if(!r.missing.length){targetProof=r.parents;status="TARGET";break}if(B.size===before){status="FIXED_POINT";break}
 }
 }catch(e){if(e.message!=="cap")throw e;status="CAP"}
 // Independent check of every derivation node, with original polynomial input and strict degree cap.
 let checked=0;for(let i=0;i<nodes.length;i++){let a=nodes[i],rule=a.rule,S;if(rule[0]==="input")S=C[rule[1]];else if(rule[0]==="xor"){if(rule[1]>=i||rule[2]>=i)throw Error("future");S=xor(new Set(nodes[rule[1]].poly),new Set(nodes[rule[2]].poly))}else{if(rule[1]>=i)throw Error("future");S=mul(new Set(nodes[rule[1]].poly),1<<rule[2])}if([...S].sort((a,b)=>a-b).join()!==a.poly.join()||a.poly.some(x=>pop(x)>d))throw Error("node check");checked+=S.size}
 if(targetProof){let S=new Set();for(let j of targetProof)S=xor(S,new Set(nodes[j].poly));if([...S].sort((a,b)=>a-b).join()!==[...target].sort((a,b)=>a-b).join())throw Error("target")}
 // For a fixed point, independent verification via complete kernel-image reduction on final basis, different order, and initial/target membership checks.
 let refusalChecks=0;
 if(status==="FIXED_POINT"){
 const final=[...B.values()].map(i=>new Set(nodes[i].poly)),reduce2=P=>{let s=new Set(P);while(s.size){let m=Math.max(...s),i=B.get(m);refusalChecks++;if(i===undefined)return false;s=xor(s,new Set(nodes[i].poly))}return true};
 for(let p of C)if(!reduce2(p))throw Error("initial missing");if(reduce2(target))throw Error("target in span");
 for(let v=n-1;v>=0;v--){let temp=new Map();for(let row of final.slice().reverse()){let product=mul(row,1<<v);while(true){let over=[...product].filter(x=>pop(x)>d);if(!over.length){if(!reduce2(product))throw Error("not closed");break}let j=Math.min(...over);refusalChecks++;if(!temp.has(j)){temp.set(j,product);break}product=xor(product,temp.get(j))}}}
 }
 // retain proof cone only if target; for refusal basis rows suffice plus checked input/closure, not need all derived history.
 let retained;
 if(targetProof){let needed=new Set(targetProof),stack=[...targetProof];while(stack.length){let i=stack.pop(),r=nodes[i].rule,par=r[0]==="xor"?r.slice(1):r[0]==="mul"?[r[1]]:[];for(let j of par)if(!needed.has(j)){needed.add(j);stack.push(j)}}retained=[...needed].sort((a,b)=>a-b).map(i=>({id:i,...nodes[i]}))}
 else if(status==="FIXED_POINT")retained=[...B.values()].map(i=>nodes[i].poly);
 return{n,d,status,rank:B.size,passes,ops,derivationNodes:nodes.length,checked,refusalChecks,peakTerms:peak,target:[...target],targetProof,certificate:retained}
}
const C=lines.flatMap(l=>[clause(l.map(v=>[v,true])),clause(l.map(v=>[v,false]))]),G=lines.map((_,i)=>xor(C[2*i],C[2*i+1])),target=new Set([1,2]);
let local=[];for(let [mode,P] of [["original clauses",C],["grouped quadratic",G]])for(let d of [2,3,4]){if(d===2&&mode==="original clauses")continue;local.push({mode,...close(7,P,d,2000000,target)})}
return{lines,local}
}
console.log(JSON.stringify(pcAudit(),null,2));
