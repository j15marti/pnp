function experiment(F,gauge,mode,cap=10000000,certificate=null,imports=[]){
 const vs=[...new Set(F.flatMap(f=>f.vs))].sort((a,b)=>a-b),ix=new Map(vs.map((v,i)=>[v,i])),n=vs.length;let work=0,probes=0,batches=[],terminal="UNKNOWN",db=F.map(f=>({v:f.vs.map(x=>ix.get(x)),ok:f.ok})),keys=new Set(),clauses=[],epoch=0;
 const tick=()=>{if(++work>cap)throw Error("CAP")};
 function add(c){c=[...new Set(c)].sort((a,b)=>a-b);if(c.some(x=>c.includes(-x)))return false;let key=c.join(",");if(keys.has(key))return false;keys.add(key);clauses.push(c);let v=[...new Set(c.map(x=>ix.get(Math.abs(x))))].sort((a,b)=>a-b);if(v.some(x=>x===undefined))throw Error("id");let ok=[];for(let w=0;w<2**v.length;w++)if(c.some(x=>((w>>v.indexOf(ix.get(Math.abs(x))))&1)===Number(x>0)))ok.push(w);db.push({v,ok});return true}
 function closure(extra){
  const a=new Int8Array(n).fill(-1);
  for(const [v,b] of [...(gauge===null?[]:[[gauge,0]]),...extra]){let i=ix.get(v);if(i===undefined)throw Error("pin");if(a[i]>=0&&a[i]!==b)return null;a[i]=b}
  let ch=true;while(ch){ch=false;for(const f of db){let all=-1,any=0,found=false;for(let w of f.ok){tick();if(!f.v.every((v,j)=>a[v]<0||a[v]===(w>>j&1)))continue;found=true;all&=w;any|=w}if(!found)return null;for(let j=0;j<f.v.length;j++){let v=f.v[j],b=all>>j&1;if(a[v]<0&&b===(any>>j&1)){a[v]=b;ch=true}}}}return a
 }
 function directCheck(pivot,C){let a=[0,1].map(b=>{probes++;return closure([[pivot,b]])});for(const c of C){for(let b=0;b<2;b++){if(!a[b])continue;if(!c.some(l=>a[b][ix.get(Math.abs(l))]===Number(l>0)))throw Error("bad learned clause")}}}
 try{
 for(const c of imports)add(c);
 while(true){epoch++;let root=closure([]);if(!root){terminal="UNSAT";break}
 if(certificate){if(batches.length>=certificate.length)break;let {pivot,C}=certificate[batches.length];directCheck(pivot,C);for(let c of C)if(!add(c))throw Error("duplicate");batches.push({pivot,C});continue}
 let change=false;
 for(const pivot of vs){if(root[ix.get(pivot)]>=0)continue;let a=[0,1].map(b=>{probes++;return closure([[pivot,b]])}),C=[];
 if(!a[0]&&!a[1])C.push([]);
 else if(!a[0])C.push([pivot]);else if(!a[1])C.push([-pivot]);else if(mode!=="local"){
 for(let j=0;j<n;j++){let v=vs[j];if(v===pivot||root[j]>=0)continue;let x=a[0][j],y=a[1][j];
 if(x>=0&&x===y)C.push([x?v:-v]);
 else if(x>=0&&y>=0){C.push([pivot,x?v:-v],[-pivot,y?v:-v])}
 else if(mode==="hybrid"){if(x>=0)C.push([pivot,x?v:-v]);if(y>=0)C.push([-pivot,y?v:-v])}
 }}
 let D=[];for(let c of C)if(add(c))D.push(c);if(D.length){batches.push({pivot,C:D});change=true;break}
 }if(!change)break
 }
 }catch(e){if(e.message==="CAP")terminal="UNKNOWN_CAP";else throw e}
 return{terminal,mode,work,probes,epoch,learned:clauses.length,batches}
}
function independent(F,gauge,batches,cap=10000000,imports=[]){
 let fs=F.map(f=>({vs:f.vs,ok:f.ok})),work=0;let clauses=[...imports];
 function close(pivot,bit){let p=new Map(gauge===null?[]:[[gauge,0]]);if(pivot!==null){if(p.has(pivot)&&p.get(pivot)!==bit)return null;p.set(pivot,bit)}for(;;){let old=p.size;for(let c of clauses){work++;if(work>cap)throw Error("CAP");if(c.some(l=>p.get(Math.abs(l))===Number(l>0)))continue;let u=c.filter(l=>!p.has(Math.abs(l)));if(!u.length)return null;if(u.length===1)p.set(Math.abs(u[0]),Number(u[0]>0))}
 for(let f of fs){let rows=[];for(let w of f.ok){if(++work>cap)throw Error("CAP");if(f.vs.every((v,i)=>!p.has(v)||p.get(v)===(w>>i&1)))rows.push(w)}if(!rows.length)return null;for(let i=0;i<f.vs.length;i++)if(rows.every(w=>(w>>i&1)===(rows[0]>>i&1)))p.set(f.vs[i],rows[0]>>i&1)}if(p.size===old)return p}}
 try{for(let {pivot,C} of batches){let a=close(pivot,0),b=close(pivot,1);for(let c of C)for(let p of [a,b])if(p&&!c.some(l=>p.get(Math.abs(l))===Number(l>0)))throw Error("bad certificate");clauses.push(...C)}return{verified:close(null,0)===null,work}}catch(e){return{verified:false,work,error:String(e)}}
}
module.exports={experiment,independent};
