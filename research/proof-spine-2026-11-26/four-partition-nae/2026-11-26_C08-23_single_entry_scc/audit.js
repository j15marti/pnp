function audit(){
 const C={asserts:0,wordTrials:0,transitions:0,states:0,nativeRows:0};const rng=n=>Array.from({length:n},(_,i)=>i);function ck(x,m){C.asserts++;if(!x)throw Error(m);if(C.asserts+C.wordTrials+C.transitions+C.states+C.nativeRows>2000000)throw Error("cap")}
 function nae(row,bit){return row.some(v=>bit(v)!==bit(row[0]))}
 function validate(rows,n,full=false){let seen=new Set(),mask=Array(n).fill(0);for(let {v,p} of rows){ck(v.length===3&&new Set(v).size===3,"triple");for(let x of v){ck(x>=0&&x<n&&!(mask[x]&(1<<p)),"color");mask[x]|=1<<p}for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){let k=[v[i],v[j]].sort((a,b)=>a-b).join(",");ck(!seen.has(k),"linear");seen.add(k)}}
 if(full)ck(mask.every(x=>x===15),"full partitions");return mask}
 function complete(rows,n){let mask=validate(rows,n),a=[],id=(l,j,v)=>(4*l+j)*n+v, mul=[0,2,3,1];for(let l=0;l<3;l++)for(let j=0;j<4;j++)for(let r of rows)a.push({v:r.v.map(v=>id(l,j,v)),p:r.p});
 for(let v=0;v<n;v++)for(let p=0;p<4;p++)if(!(mask[v]&(1<<p)))for(let j=0;j<4;j++)a.push({v:[id(0,j,v),id(1,j^p,v),id(2,j^mul[p],v)],p});
 validate(a,12*n,true);C.nativeRows+=a.length;
 // independent check filler mixed on both source bits, actual native IDs
 for(let r of a.slice(12*rows.length)){ck(r.v.every(v=>v%n===r.v[0]%n),"same variable filler");ck(nae(r.v,v=>+(Math.floor(v/(4*n))!==0)),"section");}
 ck(a.slice(0,rows.length).every((r,i)=>JSON.stringify(r)===JSON.stringify(rows[i])),"source projection");return a}
 function build(L){let n=0, rows=[],pins={},blocks=[],roots=[],leaves=[],sources=[],rep=new Map(),free=[];function var0(){let v=n++;free.push(v);return v}function pin(b){let v=n++;pins[v]=b;return v}function row(v,p,r=null){let i=rows.length;rows.push({v,p});if(r!==null){ck(!rep.has(r),"representative duplicate");rep.set(r,i)}return i}
 const sides=rng(2).map(k=>rng(L).map(l=>rng(2).map(j=>rng(3).map(()=>var0()))));const leaf=rng(2).map(()=>rng(2).map(()=>var0())),hub=var0();
 for(let k=0;k<2;k++){let p0=((k%2)*2), s=pin(k),first=sides[k][0].map(a=>a[0]);sources.push(row([s,...first],p0^2));
 for(let l=0;l<L;l++){let phase=k^1^(l%2),base=2*((k+l)%2),next=l+1<L?sides[k][l+1].map(a=>a[0]):leaf[k];for(let j=0;j<2;j++){
  let [x,y,z]=sides[k][l][j],p=pin(phase^1),c0=base+j,c2=base+(j^1),c1=base^2;
  let ids=[row([x,y,next[0]],c0,x),row([y,z,p],c1,y),row([z,x,next[1]],c2,z)];
  blocks.push({entry:x,internal:[y,z],exits:next,pin:p,phase,ids,k,l,j});
 }}
 let base=2*((k+L-1)%2)^2;for(let j=0;j<2;j++){let x=leaf[k][j],phase=k^1^(L%2),p=pin(phase),i=row([x,hub,p],base+j,x);leaves.push({x,phase,p,i})}}
 return {n,rows,pins,blocks,roots,leaves,sources,rep,free,hub,sides,leaf}}
 function macroTruth(a,b){let table=[];for(let w=0;w<8;w++){let vals=new Map([[b.entry,w&1],[b.exits[0],(w>>1)&1],[b.exits[1],(w>>2)&1],[b.pin,a.pins[b.pin]]]);let got=false;for(let z=0;z<4;z++){C.wordTrials++;vals.set(b.internal[0],z&1);vals.set(b.internal[1],z>>1);if(b.ids.every(i=>nae(a.rows[i].v,v=>vals.get(v))))got=true}
 let x=w&1,e0=(w>>1)&1,e1=(w>>2)&1;let expect=x!==b.phase||e0!==x||e1!==x;ck(got===expect,"exact macro");table.push(+got)}return table}
 function scc(a){let adj=new Map(a.free.map(v=>[v,[]]));for(let [v,i] of a.rep)for(let w of a.rows[i].v)if(w!==v&&adj.has(w))adj.get(v).push(w);let idx=0,ids=new Map(),low=new Map(),stack=[],on=new Set(),comps=[];function visit(v){ids.set(v,idx);low.set(v,idx++);stack.push(v);on.add(v);for(let w of adj.get(v)){if(!ids.has(w)){visit(w);low.set(v,Math.min(low.get(v),low.get(w)))}else if(on.has(w))low.set(v,Math.min(low.get(v),ids.get(w)))}if(low.get(v)===ids.get(v)){let s=[],w;do{w=stack.pop();on.delete(w);s.push(w)}while(w!==v);comps.push(s)}}for(let v of a.free)if(!ids.has(v))visit(v);let comp=new Map();comps.forEach((s,i)=>s.forEach(v=>comp.set(v,i)));let entries=comps.map(()=>new Set());for(let [v,ns] of adj)for(let w of ns)if(comp.get(v)!==comp.get(w))entries[comp.get(w)].add(w);for(let i of a.sources)for(let w of a.rows[i].v)if(comp.has(w))entries[comp.get(w)].add(w);
 ck(comps.every((s,i)=>entries[i].size<=1),"single entry");ck(comps.filter(s=>s.length===3).length===a.blocks.length,"cycle count");for(let b of a.blocks){let c=comp.get(b.entry);ck(comps[c].length===3&&entries[c].has(b.entry),"actual entry")};return comps}
 function binaryClosure(a){let cs=[];for(let {v} of a.rows){let fixed=v.filter(x=>x in a.pins).map(x=>a.pins[x]),fr=v.filter(x=>!(x in a.pins));if(fixed.length===1)cs.push([fr[0],fr[1],fixed[0]^1]);}let adj=new Map(a.free.flatMap(v=>[[2*v,[]],[2*v+1,[]]]));for(let [x,y,b] of cs){adj.get(2*x+(b^1)).push(2*y+b);adj.get(2*y+(b^1)).push(2*x+b)}
 function reach(x){let seen=new Set([x]),q=[x];for(let i=0;i<q.length;i++)for(let y of adj.get(q[i]))if(!seen.has(y)){seen.add(y);q.push(y)}return seen}
 let forced=0,contradiction=false;for(let v of a.free){let ab=reach(2*v).has(2*v+1),ba=reach(2*v+1).has(2*v);forced+=+ab+ +ba;contradiction||=ab&&ba}return {binary:cs.length,forced,contradiction}}
 function dp(a){let rules=new Map(),order=new Map(),z=0;for(let l=0;l<a.sides[0].length;l++)for(let k=0;k<2;k++)for(let b of a.blocks.filter(b=>b.l===l&&b.k===k)){order.set(b.entry,z++);rules.set(b.entry,{phase:b.phase,exits:b.exits})}for(let t of a.leaves){order.set(t.x,z++);rules.set(t.x,{phase:t.phase,exits:[a.hub]})}order.set(a.hub,z);let memo=new Map(),local=0;
 function go(d){let arr=[...d].sort((a,b)=>order.get(a[0])-order.get(b[0]));if(!arr.length)return true;let key=JSON.stringify(arr);if(memo.has(key))return memo.get(key);C.states++;local++;let [v,b]=arr[0],rest=new Map(arr.slice(1)),r=rules.get(v),ok=false;if(!r||r.phase!==b)ok=go(rest);else for(let w of r.exits){C.transitions++;let q=b^1;if(rest.has(w)&&rest.get(w)!==q)continue;let t=new Map(rest);t.set(w,q);if(go(t)){ok=true;break}}
 memo.set(key,ok);return ok}
 for(let x of a.sides[0][0].map(x=>x[0]))for(let y of a.sides[1][0].map(x=>x[0]))ck(!go(new Map([[x,1],[y,0]])),"seed must fail");return local}
 let cases=[];for(let L of [1,2,4,8,16,32,64]){
 let a=build(L),native=complete(a.rows,a.n),closure=binaryClosure(a),comps=scc(a);
 ck(!closure.contradiction&&closure.forced===0,"binary closure nontrivial");let tables=a.blocks.map(b=>macroTruth(a,b));
 // Independent global contradiction: all demanded entry phases are opposite across sides, all routes lead to same hub
 let hubPhases=[0,1].map(k=>k^1^(L%2)^1);ck(hubPhases[0]!==hubPhases[1],"hub phase contradiction");
 let states=dp(a);let count=null;if(L===1){count=0;for(let w=0;w<(1<<a.free.length);w++){C.wordTrials++;let bit=v=>v in a.pins?a.pins[v]:(w>>a.free.indexOf(v))&1;if(a.rows.every(r=>nae(r.v,bit)))count++}ck(count===0,"whole guarded core NO")}
 cases.push({L,variables:a.n,nativeVariables:12*a.n,nativeOwners:native.length,free:a.free.length,owners:a.rows.length,defect:a.rows.length-a.rep.size,cyclicSCCs:a.blocks.length,macroStates:states,closure,hubPhases,fullReferenceCount:count,rows:a.rows,pins:a.pins,representatives:[...a.rep],blocks:a.blocks,leaves:a.leaves,sources:a.sources,tableTypes:[...new Set(tables.map(JSON.stringify))],nativeFingerprintInput:JSON.stringify(native).length})
 }
 // Hostile two-entry SCC: positive 4-cycle, all exits protected. Project x2,x3.
 let rows=rng(4).map(i=>({v:[i,(i+1)%4,4+i],p:i}));let native=complete(rows,8),count=0,forbidden=[];
 for(let w=0;w<64;w++){let B=[0,1,4,5,6,7],ok=false;for(let z=0;z<4;z++){C.wordTrials++;let bit=v=>B.includes(v)?(w>>B.indexOf(v))&1:(z>>(v-2))&1;if(rows.every(r=>nae(r.v,bit)))ok=true}if(ok)count++;else forbidden.push(w)}
 ck(count===46&&forbidden.length===18,"two entry counterexample");
 return {cases,hostile:{rows,protected:[0,1,4,5,6,7],support:count,forbidden,nativeVariables:96,nativeOwners:native.length},counts:C,cap:2000000}
}
console.log(JSON.stringify(audit(),null,2));
