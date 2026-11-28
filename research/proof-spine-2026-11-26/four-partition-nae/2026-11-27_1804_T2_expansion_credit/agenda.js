function canonical(c){return [...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b)}

function key(c){return c.join(",")}

function up(C,guard=[],meter=null){
 const a=new Map();for(let l of guard){let v=Math.abs(l),b=+(l>0);if(a.has(v)&&a.get(v)!==b)return {no:true,a};a.set(v,b)}
 let ch=true;while(ch){ch=false;for(let c of C){let open=[],sat=false;for(let l of c){if(meter)meter("up");let v=Math.abs(l);if(!a.has(v))open.push(l);else if(a.get(v)===+(l>0)){sat=true;break}}if(sat)continue;if(!open.length)return {no:true,a};if(open.length===1){a.set(Math.abs(open[0]),+(open[0]>0));ch=true}}}
 return {no:false,a};
}

function agenda(base,W,mode,cap=1000000,subsumption=true){
 let clauses=[], seen=new Map(), pending=Array.from({length:W+1},()=>[]),cursor=new Array(W+1).fill(0),byLit=new Map(),trace=[],counts={pairs:0,lits:0,subsets:0,queue:0,up:0},events=0,done=false,status="UNKNOWN",why="saturated",maxWidth=0,small=0,wide=0,peak=0,attemptsAtSmall=[];
 function tick(k,n=1){counts[k]+=n;events+=n;if(events>cap)throw Error("cap")}
 function add(c,parents=null){let k=key(c);if(seen.has(k))return false;
   if(parents&&subsumption&&c.length<=W){for(let m=0;m<(1<<c.length)-1;m++){tick("subsets");let s=c.filter((_,i)=>m>>i&1);if(seen.has(key(s)))return false}}
   let i=clauses.length;clauses.push(c);seen.set(k,i);if(parents){trace.push({c,p:parents});if(c.length<=2){small++;attemptsAtSmall.push(counts.pairs)}else if(c.length>3)wide++;maxWidth=Math.max(maxWidth,c.length)}
   if(c.length<=W)pending[c.length].push(i);if(!c.length){done=true;status="UNSAT";why="empty clause"}peak=Math.max(peak,clauses.length);return true;
 }
 for(let c of base){c=canonical(c);if(!c.some(l=>c.includes(-l)))add(c)}
 const initial=clauses.length;
 try{
  let root=up(clauses,[],tick);if(root.no){status="UNSAT";why="root UP";done=true}
  while(!done){
   let bucket=-1;if(mode==="fifo"){let best=Infinity;for(let w=0;w<=W;w++){let x=pending[w][cursor[w]];if(x!==undefined&&x<best){best=x;bucket=w}}}else for(let w=0;w<=W;w++)if(cursor[w]<pending[w].length){bucket=w;break}
   if(bucket<0)break;
   let i=pending[bucket][cursor[bucket]++],c=clauses[i];tick("queue");
   for(let l of c){
    let list=byLit.get(-l)||[];
    for(let j of list){tick("pairs");let d=clauses[j];if(mode==="same"&&!(c.length===d.length&&c.every(x=>d.some(y=>Math.abs(x)===Math.abs(y)))))continue;
     tick("lits",c.length+d.length);
     let q=canonical([...c.filter(x=>x!==l),...d.filter(x=>x!==-l)]);if(q.length>W||q.some(x=>q.includes(-x)))continue;
     add(q,[i,j,l]);if(done)break
    }if(done)break
   }
   for(let l of c){if(!byLit.has(l))byLit.set(l,[]);byLit.get(l).push(i)}
  }
 }catch(e){if(e.message!=="cap")throw e;why="event cap"}
 return {status,why,mode,W,initial,clauses,trace,counts,events,small,wide,maxWidth,peak,attemptsAtSmall};
}

function replayAgenda(base,out){
 let clauses=[], seen=new Set(),checks=0,rows=0;
 for(let c of base){c=canonical(c);let k=key(c);if(!c.some(l=>c.includes(-l))&&!seen.has(k)){seen.add(k);clauses.push(c)}}
 if(clauses.length!==out.initial)throw Error("initial");
 for(let {c,p} of out.trace){let [i,j,l]=p,a=clauses[i],b=clauses[j];if(!a||!b||!a.includes(l)||!b.includes(-l))throw Error("parent/pivot");let s=canonical([...a.filter(x=>x!==l),...b.filter(x=>x!==-l)]);if(key(s)!==key(c)||c.length>out.W||c.some(x=>c.includes(-x))||seen.has(key(c)))throw Error("invalid resolvent");
  const vs=[...new Set([...a,...b].map(Math.abs))];
  if(vs.length<=10)for(let w=0;w<2**vs.length;w++){rows++;const sat=q=>q.some(z=>((w>>vs.indexOf(Math.abs(z)))&1)===+(z>0));if(sat(a)&&sat(b)&&!sat(c))throw Error("truth replay")}
  clauses.push(c);seen.add(key(c));checks++;
 }
 if(JSON.stringify(clauses)!==JSON.stringify(out.clauses))throw Error("clauses");
 if(out.status==="UNSAT"&&!clauses.some(c=>!c.length)&&!up(clauses).no)throw Error("terminal");
 return {checks,rows,verified:true};
}

function dpll(C,phase,cap=700000,depth=22){
 let events=0,nodes=0,deep=0,reason="complete",tree=null;
 function meter(k){if(++events>cap)throw Error("cap")}
 function search(guard,d){nodes++;deep=Math.max(deep,d);let u=up(C,guard,meter);if(u.no)return 0;let scores=new Map();for(let c of C){let sat=false,open=[];for(let l of c){meter("score");let v=Math.abs(l);if(!u.a.has(v))open.push(v);else if(u.a.get(v)===+(l>0)){sat=true;break}}if(!sat)for(let v of open)scores.set(v,(scores.get(v)||0)+2**(4-Math.min(4,open.length)))}
 if(!scores.size)return "SAT";if(d>=depth)return null;let v=[...scores].sort((a,b)=>b[1]-a[1]||a[0]-b[0])[0][0],p=phase?.get(v)??0,l=p?v:-v;
 let a=search([...guard,l],d+1);if(a===null||a==="SAT")return a;let b=search([...guard,-l],d+1);return b===null||b==="SAT"?b:[l,a,b]}
 try{tree=search([],0)}catch(e){if(e.message!=="cap")throw e;reason="cap"}
 if(tree===null&&reason==="complete")reason="depth";
 return {status:tree===null?"UNKNOWN":tree==="SAT"?"SAT":"UNSAT",tree,nodes,events,depth:deep,reason};
}

function replayTree(C,t){let visits=0,nodes=0;
 function walk(t,g){nodes++;if(t===0){if(!up(C,g,()=>visits++).no)throw Error("false leaf");return}if(!Array.isArray(t)||t.length!==3||g.some(l=>Math.abs(l)===Math.abs(t[0])))throw Error("split");walk(t[1],[...g,t[0]]);walk(t[2],[...g,-t[0]])}
 walk(t,[]);return{nodes,visits,verified:true};
}

function flip(C,residue,cap=1000000){
 const vars=[...new Set(C.flat().map(Math.abs))].sort((a,b)=>a-b),a=new Map(vars.map(v=>[v,1]));let visits=0,changes=0,moves=[],reason="stall",initial=null,initialFields=null,last=null;
 function evalWord(v=null){let bad=0,z=0,fields=[];for(let c of C){let k=0,sum=0;for(let l of c){if(++visits>cap)throw Error("cap");let b=a.get(Math.abs(l))^+(Math.abs(l)===v),s=b===+(l>0)?(l>0?1:-1):0;k+=s*s;sum+=s}let r=((sum%3)+3)%3;if(!k)bad++;if(k&&r===0)z++;fields.push([k,k%3,r])}return{bad,z,fields}}
 try{let cur=evalWord();initial=cur.bad;initialFields={allTrue:cur.fields,allFalse:null};let old=a;for(let v of vars)a.set(v,0);initialFields.allFalse=evalWord().fields;for(let v of vars)a.set(v,1);last=cur;for(let step=0;step<=C.length;step++){let best=null,ordinary=null;for(let v of vars){let t=evalWord(v);if(t.bad>=cur.bad)continue;if(!ordinary||t.bad<ordinary.t.bad||t.bad===ordinary.t.bad&&v<ordinary.v)ordinary={v,t};if(!best||t.bad<best.t.bad||t.bad===best.t.bad&&((residue&&t.z<best.t.z)||(!residue||t.z===best.t.z)&&v<best.v))best={v,t}}if(!best)break;if(best.v!==ordinary.v)changes++;a.set(best.v,1-a.get(best.v));cur=best.t;last=cur;moves.push({v:best.v,bad:cur.bad,z:cur.z,ordinary:ordinary.v});if(!cur.bad){reason="candidate SAT";break}}
 }catch(e){if(e.message!=="cap")throw e;reason="cap"}
 return {phase:[...a],visits,changes,moves,initial,last:last?{bad:last.bad,z:last.z,fields:last.fields}:null,initialFields,reason};
}
module.exports={canonical,key,up,agenda,replayAgenda,dpll,replayTree,flip};
