function audit(){
 let checks=0, probes=0, scans=0, pairs=0; const ok=(v)=>{checks++;if(!v)throw Error("assertion "+checks)};
 const rows=Array.from({length:16},(_,i)=>Array.from({length:4},(_,j)=>(i>>j)&1)).filter(a=>a.reduce((s,x)=>s+x,0)===2);
 const mask=(a)=>a.reduce((s,x,i)=>s+(x<<i),0);
 const guardPatterns=Array.from({length:243},(_,i)=>{let a=[];for(let j=0;j<5;j++){a.push(i%3-1);i=Math.floor(i/3)}return a});
 // All possible pins on x,y,a,b,c, compare exact relay relation to occupancy formula.
 for(const g of guardPatterns){
   let actual=[],pred=[];
   for(let i=0;i<32;i++){let w=Array.from({length:5},(_,j)=>(i>>j)&1);if(g.some((v,j)=>v>=0&&v!==w[j]))continue;if(w[0]+w[2]+w[3]+w[4]===2&&w[1]+w[2]+w[3]+w[4]===2)actual.push(i)}
   for(let q=0;q<2;q++)for(let j=0;j<8;j++){let a=[q,q,j&1,(j>>1)&1,(j>>2)&1];if(a[2]+a[3]+a[4]===2-q&&!g.some((v,k)=>v>=0&&v!==a[k]))pred.push(mask(a))}
   ok(actual.sort((a,b)=>a-b).join()===pred.sort((a,b)=>a-b).join())
 }
 function source(k,sat){
   let n=0, C=[], witness=[], previous=-1, lines=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
   for(let b=0;b<k;b++){
     let ids=[previous<0?n++:previous,...Array.from({length:6},()=>n++)];previous=ids[3];
     let color=[1,1,1,0,0,0,0];if(b&&witness[ids[0]]!==color[0])color=color.map(x=>1-x);
     ids.forEach((v,i)=>witness[v]=color[i]);
     for(let j=sat?1:0;j<7;j++){let c=lines[j].map(i=>ids[i]);let d=n++;if(sat)witness[d]=2-c.reduce((s,v)=>s+witness[v],0);C.push([...c,d])}
   }
   return {n,C,witness}
 }
 function compile(F){
   let n=F.n,A=[],B=[],ports=[];
   for(let c=0;c<F.C.length;c++){
     let clone=[];for(let i=0;i<4;i++){
       let v=F.C[c][i],y=n++,p=[n++,n++,n++];clone.push(y);
       A.push([y,...p]);B.push([v,...p]);ports.push({c,v,y,p})
     } A.push(clone)
   }
   return {n,A,B,C:[...A,...B],ports}
 }
 function verify(F,w){return F.C.every(c=>c.reduce((s,v)=>s+w[v],0)===2)}
 function forest(C,n){
   let parent=Array.from({length:n+C.length},(_,i)=>i);let root=x=>{while(parent[x]!==x){parent[x]=parent[parent[x]];x=parent[x]}return x};
   for(let i=0;i<C.length;i++)for(const v of C[i]){let x=root(v),y=root(n+i);if(x===y)return false;parent[x]=y}return true
 }
 function close(F,pin){
   let a=Array(F.n).fill(-1);if(pin)a[pin[0]]=pin[1];let change=true;
   while(change){change=false;for(const c of F.C){scans++;let t=0,u=[];for(const v of c){if(a[v]===1)t++;else if(a[v]<0)u.push(v)}
     if(t>2||t+u.length<2)return null;
     if(t===2||t+u.length===2){let b=t===2?0:1;for(const v of u){a[v]=b;change=true}}
   }}return a
 }
 function closure(F,all){let a=close(F,null);ok(a!==null);ok(a.every(x=>x<0));if(all){for(let v=0;v<F.n;v++){probes+=2;let p=close(F,[v,0]),q=close(F,[v,1]);ok(p!==null&&q!==null)}}}
 // Arc consistency on exact projected quotient, each variable node is all-equal.
 function seams(F){let counts=Array(F.n).fill(0);for(const c of F.C){ok(c.length===4&&new Set(c).size===4);for(let j=0;j<4;j++){let v=c[j];counts[v]++;for(const r of rows){pairs++;ok(r[j]===0||r[j]===1);}}}return counts}
 let results=[];
 for(const k of [1,2,4,8,16,32,64])for(const sat of [false,true]){
   let F=source(k,sat),G=compile(F), counts=seams(F);
   ok(forest(G.A,G.n));ok(forest(G.B,G.n));ok(G.C.length===9*F.C.length);
   ok(G.n===F.n+16*F.C.length);ok(new Set(G.C.map(c=>c.slice().sort((a,b)=>a-b).join())).size===G.C.length);
   closure(F,k<=8);closure(G,k<=4);
   if(sat){ok(verify(F,F.witness));let w=F.witness.slice();for(const {v,y,p} of G.ports){let q=w[v];w[y]=q;for(let i=0;i<3;i++)w[p[i]]=+(i<2-q)}ok(verify(G,w));ok(verify(F,w))}
   if(k===1){let num=0;for(let i=0;i<2**F.n;i++){let w=Array.from({length:F.n},(_,j)=>(i>>j)&1);if(verify(F,w))num++}ok((num>0)===sat);results.push({k,sat,sourceVariables:F.n,sourceClauses:F.C.length,liftVariables:G.n,liftClauses:G.C.length,maxDegree:Math.max(...counts),cycleRank:4*F.C.length-F.C.length-F.n+1,exhaustiveSourceModels:num})}
   else results.push({k,sat,sourceVariables:F.n,sourceClauses:F.C.length,liftVariables:G.n,liftClauses:G.C.length,maxDegree:Math.max(...counts),cycleRank:3*F.C.length-F.n+1})
 }
 return {checks,probes,scans,pairs,relayGuardCases:guardPatterns.length,results}
}
console.log(JSON.stringify(audit(),null,2));
