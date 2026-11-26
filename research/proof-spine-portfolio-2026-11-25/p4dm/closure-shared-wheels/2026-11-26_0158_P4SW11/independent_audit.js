/* P4SW11 independent finite native C54 guard-neighbor and midpoint audit, Node.js 18+. */
function audit(C){
 const check=(v,m)=>{if(!v)throw Error(m)}, key=a=>a.slice().sort((a,b)=>a-b).join(",");
 const bit=i=>1n<<BigInt(i);let n=C.length/3,R=Array.from({length:4*n},()=>[]);C.forEach((t,j)=>t.forEach((v,c)=>R[c*n+v].push(j)));check(R.every(a=>a.length===3),"E3");
 const holes=bit(0)|bit(6),ports=[1,2,18,19,20,0],P=new Set(ports),cols=C.map(t=>t.reduce((s,v,c)=>s|bit(c*n+v),0n)&~holes),tab=new Map();
 function rec(left,W){if(!left){let k=key(W.filter(j=>P.has(j))),v=tab.get(k)||{count:0,witness:W};v.count++;tab.set(k,v);return}let a=null;for(let i=0;i<R.length;i++)if(left&bit(i)){let b=R[i].filter(j=>(cols[j]&left)===cols[j]);if(a===null||b.length<a.length)a=b;if(!a.length)break}for(let j of a)rec(left^cols[j],W.concat(j))}
 rec((bit(4*n)-1n)&~holes,[]);check(tab.size===5,"five exact masks");
 const vs=[[0,0],[0,1],[1,0],[1,1]],dirs=[[0,1],[1,0],[0,-1],[-1,0]],neighbors=v=>dirs.map(d=>[v[0]+d[0],v[1]+d[1]]).filter(w=>w.every(x=>x>=0&&x<2)),id=(v,u)=>v.join(",")+":"+u.join(",");
 let rows=[];for(let v of vs)for(let u of neighbors(v))rows.push(id(v,u));
 let fresh=[rows.length,0,0,0],T=[],macro=[];
 for(let v of vs){let ns=neighbors(v),pmap=new Map();for(let i=0;i<2;i++){let u=ns[i],prev=ns[(i+1)%2];[id(v,prev),id(u,v),id(v,u)].forEach((r,z)=>pmap.set(ports[3*i+z],rows.indexOf(r)))}
 let maps=Array.from({length:4},(_,c)=>{let M={};for(let i=0;i<n;i++)if(c!==0||i!==0&&i!==6)M[i]=fresh[c]++;return M});let start=T.length;
 C.forEach((t,j)=>T.push(t.map((v,c)=>c===0&&pmap.has(j)?pmap.get(j):maps[c][v])));macro.push([...tab].map(([k,z])=>({mask:k.split(",").map(Number).map(j=>start+j),rows:k.split(",").map(Number).map(j=>pmap.get(j)),count:z.count,witness:z.witness.map(j=>start+j)})))}
 check(fresh.every(v=>v===T.length/3)&&new Set(T.map(t=>t.join(","))).size===T.length,"actual native source");
 const srcRows=Array.from({length:4*T.length/3},()=>[]);T.forEach((t,j)=>t.forEach((v,c)=>srcRows[c*T.length/3+v].push(j)));check(srcRows.every(r=>r.length===3),"actual degree3");
 const forbid=[[2,19],[1,20],[0,18],[56,74],[109,127],[108,126],[163,182]].map(key),pos=forbid.filter(k=>k!=="56,74");let patterns=0,negative=0,positive=0,total=0n,positiveCount=0n,posWitness=null,actual=[];
 function go(i,used,W,masks,count){if(i===macro.length){check(used.size===rows.length,"occupancy");check(srcRows.every(r=>r.filter(j=>W.includes(j)).length===1),"actual original lift");patterns++;total+=count;let k=masks.map(key);if(k.every(x=>!forbid.includes(x)))negative++;if(k.every(x=>!pos.includes(x))){positive++;positiveCount+=count;posWitness=W;}actual.push({masks,local_product:count.toString()});return}for(let a of macro[i])if(new Set(a.rows).size===a.rows.length&&a.rows.every(r=>!used.has(r)))go(i+1,new Set([...used,...a.rows]),W.concat(a.witness),masks.concat([a.mask]),count*BigInt(a.count))}
 go(0,new Set(),[],[],1n);check(patterns===19&&negative===0&&positive>0,"exact conditional neighbors");
 let midpoint=0,mode=0;
 for(let a=-4;a<=4;a++)for(let b=-4;b<=4;b++)for(let c=-4;c<=4;c++){check((b-a===c-b&&(b-a===0||b-a===1))===(b-a>=0&&b-a<=1&&c-b>=0&&c-b<=1&&b<=Math.max(a,c-1)&&b>=Math.min(a+1,c)),"midpoint");midpoint++}
 for(let H=-3;H<=3;H++)for(let a=H;a<=H+1;a++)for(let b=H;b<=H+1;b++)for(let c=H;c<=H+1;c++)if(a<=c&&b<=c){
   const type=c===H?0:a>b?1:b>a?2:a===H+1?3:4;
   const constraints=[c===H+1,a<=b,b<=a,H>=Math.min(a,b),c<=Math.max(a,b)];
   for(let m=0;m<32;m++){check(Boolean(m>>type&1)===constraints.every((x,i)=>(m>>i&1)||x),"five-mode atom compiler");mode++}
 }
 return {tuple_count:T.length,local_masks:[...tab].map(([k,v])=>({mask:k,count:v.count})),actual_patterns:patterns,total_covers:total.toString(),negative_patterns:negative,positive_patterns:positive,positive_covers:positiveCount.toString(),forbidden:forbid,positive_forbidden:pos,positive_original_witness:posWitness,patterns:actual,midpoint_checks:midpoint,mode_checks:mode,limitations:"Exact local enumeration, actual original source degree/distinctness, all 19 macro patterns and integer source lifts; inherited rotation/planarity and native whole-chart computations checked separately in Python."};
}
const C=[[6,0,5,1],[0,1,0,1],[0,1,1,0],[1,0,0,1],[1,0,1,0],[1,1,0,0],[2,2,3,3],[2,3,2,3],[2,4,3,2],[3,2,2,3],[3,2,3,2],[3,3,2,13],[4,3,5,5],[4,5,4,5],[4,5,5,4],[5,4,4,5],[5,4,11,4],[5,5,4,4],[0,12,1,7],[6,7,6,7],[6,7,7,6],[7,12,6,7],[7,6,7,6],[7,7,6,6],[8,8,9,9],[8,9,8,9],[8,10,9,8],[9,8,8,9],[9,8,9,8],[9,6,8,8],[10,9,11,11],[10,11,10,11],[10,11,11,10],[11,10,10,11],[11,10,7,10],[11,11,10,10],[12,9,17,2],[12,13,12,13],[12,13,17,12],[13,12,12,13],[13,6,13,12],[13,13,12,12],[14,14,15,15],[14,15,14,15],[14,16,15,14],[15,14,14,15],[15,14,15,14],[15,15,14,14],[16,15,13,17],[16,17,16,17],[16,17,17,16],[17,16,16,17],[17,16,13,16],[17,17,16,16]];
console.log(JSON.stringify(audit(C),null,2));
