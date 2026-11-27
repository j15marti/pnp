/* T3 replay experiment. Pinned inputs and helper paths in report. */
function runTables(fs,gauge,cap=2500000){
 let stats={partial:0,support:0,clauses:0,visits:0,verifyVisits:0,probes:0,nodes:0,learned:0,peakDepth:0},base=[],seen=new Set();
 function add(C){let k=C.join(",");if(!seen.has(k)){seen.add(k);base.push(C)}}
 for(const f of fs){let w=f.vs.length;if(w>7)throw Error("width");let forbidden=new Set();for(let q=0;q<3**w;q++){stats.partial++;let n=q,pins=[],mask=0,val=0;for(let i=0;i<w;i++){let t=n%3;n=Math.floor(n/3);if(t){mask|=1<<i;val|=(t-1)<<i;pins.push([i,t])}}let ok=false;for(let a of f.ok){stats.support++;if((a&mask)===val){ok=true;break}}if(!ok){forbidden.add(q);if(pins.every(([i,t])=>!forbidden.has(q-t*3**i)))add(pins.map(([i,t])=>f.vs[i]*(t===1?1:-1)))}}}
 if(gauge!==undefined)add([-gauge]);stats.clauses=base.length;
 let db=base.slice(),proof=[];
 function close(pins,C,mode){let a=new Map();for(let l of pins){let v=Math.abs(l),z=l>0?1:0;if(a.has(v)&&a.get(v)!==z)return null;a.set(v,z)}
 for(;;){let ch=false;for(let j=0;j<C.length;j++){let c=C[mode==="verify"?C.length-1-j:j];let key=mode==="verify"?"verifyVisits":"visits";if(++stats[key]>cap)throw Error(mode+" cap");let n=0,u=0,sat=false;for(let l of c){let v=Math.abs(l);if(!a.has(v)){n++;u=l}else if(a.get(v)===(l>0?1:0)){sat=true;break}}if(sat)continue;if(n===0)return null;if(n===1){a.set(Math.abs(u),u>0?1:0);ch=true}}if(!ch)return a}}
 function learn(pins){let g=pins.slice();if(close(g,db,"discover")!==null)throw Error("non-RUP");for(let i=g.length-1;i>=0;i--){let t=g.filter((_,j)=>i!==j);stats.probes++;if(close(t,db,"discover")===null)g=t}let c=g.map(l=>-l);db.push(c);proof.push(c);stats.learned++}
 function go(pins){stats.nodes++;stats.peakDepth=Math.max(stats.peakDepth,pins.length);let a=close(pins,db,"discover");if(a===null){learn(pins);return}
 let freq=new Map();for(let c of db){if(c.some(l=>a.has(Math.abs(l))&&a.get(Math.abs(l))===(l>0?1:0)))continue;for(let l of c)if(!a.has(Math.abs(l)))freq.set(Math.abs(l),(freq.get(Math.abs(l))||0)+1)}if(!freq.size)throw Error("SAT witness");let v=[...freq].sort((a,b)=>b[1]-a[1]||a[0]-b[0])[0][0];go([...pins,-v]);go([...pins,v]);learn(pins)}
 try{go([])}catch(e){return{status:"UNKNOWN",reason:String(e),stats,proof}}
 let check=base.slice();for(let c of proof){if(close(c.map(l=>-l),check,"verify")!==null)throw Error("RUP rejected");check.push(c)}if(proof.at(-1).length!==0)throw Error("no root");
 // Negative checker control: replace first proof clause by empty. Reject unless initial closure itself contradicts.
 let corruptedRejected=close([],base,"verify")!==null;
 return{status:"UNSAT",stats,proof,base,corruptedRejected}
}
