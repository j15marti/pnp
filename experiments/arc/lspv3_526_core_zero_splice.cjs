/* LSPV-3/526: Original unpadded 21-source CORE to zero+arbitrary-input ER2 packet.
 * Uses pinned /524 and /523 project generators; NOT historical R_mix341.
 * node experiments/arc/lspv3_526_core_zero_splice.cjs
 */
"use strict";
const fs=require("fs"), vm=require("vm"), crypto=require("crypto"), path=require("path");
const norm=a=>{const b=[...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);if(b.some(x=>b.includes(-x)))throw Error("tautology");return b};
const equal=(a,b)=>JSON.stringify(norm(a))===JSON.stringify(norm(b));
const gitsha=s=>crypto.createHash("sha1").update("blob "+Buffer.byteLength(s)+"\0"+s).digest("hex");
function build(){
 const root=path.resolve(__dirname,"../..");
 const f524=fs.readFileSync(path.join(root,"experiments/arc/lspv1_524_strict3_inverse_cancellation.js"),"utf8");
 const f523=fs.readFileSync(path.join(root,"experiments/arc/lspv3_523_core_inverse_lift.cjs"),"utf8");
 if(gitsha(f524)!=="3fa42e25e02d05b9a915458a7f780e59fd828c12" ||
    gitsha(f523)!=="c8c62a5eb9a64a6c6949217473ba5075558500c8")throw Error("upstream Git blob changed");
 const old=vm.runInNewContext(f524+";main()"),lift=vm.runInNewContext(f523+";lift");
 const core=lift(old),m=v=>Math.abs(v)<=9?v:Math.sign(v)*(Math.abs(v)+3);
 const L=core.lines.map(v=>({...v,clause:v.clause.map(m),...(v.kind==="RES"?{pivot:m(v.pivot)}:{})}));
 const G=core.owners.map(g=>({...g,id:m(g.id),a:m(g.a),b:m(g.b)}));
 const U=core.targets.slice(-3).map(t=>t.id), Z=[-27,-29,-31], A=[10,11,12];
 if(JSON.stringify(U.map(i=>L[i].clause))!==JSON.stringify([[-27],[29],[31]]))throw Error("source zero premises");
 let next=32,nres=87;
 const line=(kind,cl,extra={})=>{const id=L.length;L.push({id,kind,clause:norm(cl),...extra});return id};
 const def=(a,b,label)=>{if(Math.abs(a)===Math.abs(b)||Math.abs(a)>=next||Math.abs(b)>=next)throw Error("DEF ports");
   const g={id:next++,owner:G.length,a,b,label,facets:[]};
   g.facets=[line("FACET",[-g.id,a],{owner:g.owner,tag:"L"}),
             line("FACET",[-g.id,b],{owner:g.owner,tag:"R"}),
             line("FACET",[g.id,-a,-b],{owner:g.owner,tag:"B"})];
   G.push(g);return g};
 const res=(a,b,p,expected)=>{let x=L[a].clause,y=L[b].clause;if(!x.includes(p)){[a,b]=[b,a];[x,y]=[y,x]}
   if(p<=0||!x.includes(p)||!y.includes(-p))throw Error("RES pivot");
   const cl=norm([...x.filter(v=>v!==p),...y.filter(v=>v!==-p)]);
   if(expected&&!equal(cl,expected))throw Error("RES conclusion");
   nres++;return line("RES",cl,{left:a,right:b,pivot:p})};
 const T=[[],[],[]],off=[[],[],[]];
 for(let i=0;i<3;i++)for(let j=0;j<3;j++){
   T[i][j]=def(Z[i],A[j],"term_"+i+"_"+j);
   if(i)off[i][j]=res(T[i][j].facets[0],U[i],Math.abs(Z[i]),[-T[i][j].id]);
 }
 const outputs=[];
 for(let k=0;k<3;k++){
   const t0=T[0][k],t1=T[1][(k+2)%3],t2=T[2][(k+1)%3];
   const mid=def(-t0.id,-t1.id,"nor1_"+k),out=def(mid.id,-t2.id,"nor2_"+k);
   const positiveTerm=res(t0.facets[2],U[0],Math.abs(Z[0]),[t0.id,-A[k]]);
   let x=res(mid.facets[2],off[1][(k+2)%3],t1.id,[mid.id,t0.id]);
   x=res(x,t0.facets[1],t0.id,[mid.id,A[k]]);
   const y=res(out.facets[2],off[2][(k+1)%3],t2.id,[out.id,-mid.id]);
   const positive=res(x,y,mid.id,[out.id,A[k]]);
   const z=res(out.facets[0],mid.facets[0],mid.id,[-out.id,-t0.id]);
   const negative=res(z,positiveTerm,t0.id,[-out.id,-A[k]]);
   outputs.push({k,bit:-out.id,input:A[k],positive,negative});
 }
 if(L.length!==237||G.length!==34||nres!==114)throw Error("incorrect node count");
 return {model:"ER2-OWNER RESTRICTED, not historical R_mix341",source_count:21,
         original_variable_bound:12,zero_units:U,targets:outputs,
         proof:{lines:L,defs:G,paid_defs:34,paid_res:114,paid_work:148}};
}
function check(q){
 const L=q.proof.lines,G=q.proof.defs;
 const source=[],cnt={RES:0,FACET:0,SOURCE:0};
 for(let j=0;j<G.length;j++){
   const g=G[j];
   if(g.id!==13+j||g.owner!==j||Math.abs(g.a)>=g.id||Math.abs(g.b)>=g.id||Math.abs(g.a)===Math.abs(g.b))throw Error("bad DEF owner");
 }
 for(let i=0;i<L.length;i++){
   const n=L[i];if(n.id!==i||JSON.stringify(n.clause)!==JSON.stringify(norm(n.clause)))throw Error("noncanonical record");
   if(!(n.kind in cnt))throw Error("rule");
   cnt[n.kind]++;
   if(n.kind==="SOURCE"){if(i>=21)throw Error("source position");source.push(n.clause)}
   else if(n.kind==="FACET"){
     const g=G[n.owner],sel=g.facets.indexOf(i),cl=[[-g.id,g.a],[-g.id,g.b],[g.id,-g.a,-g.b]][sel];
     if(sel<0||!equal(n.clause,cl))throw Error("unowned facet");
   }else{
     if(n.left>=i||n.right>=i||!L[n.left].clause.includes(n.pivot)||!L[n.right].clause.includes(-n.pivot))throw Error("bad RES ancestry");
     const c=[...L[n.left].clause.filter(v=>v!==n.pivot),...L[n.right].clause.filter(v=>v!==-n.pivot)];
     if(!equal(c,n.clause))throw Error("bad RES");
   }
 }
 const orig=[];for(let i=0;i<3;i++)for(let j=0;j<3;j++)for(let k=0;k<3;k++)
   if((i+j+k)%3!==0)orig.push(norm([-(i+1),-(j+4),-(k+7)]));
 orig.push([1,2,3],[4,5,6],[7,8,9]);
 if(source.length!==21||new Set(source.map(x=>JSON.stringify(x))).size!==21||
   source.some(c=>!orig.some(t=>equal(c,t))))throw Error("foreign original source");
 if(cnt.RES!==114||cnt.FACET!==102||cnt.SOURCE!==21)throw Error("counts");
 for(let k=0;k<3;k++){
   const t=q.targets[k];
   if(t.input!==10+k||!equal(L[t.positive].clause,[-t.bit,t.input])||
      !equal(L[t.negative].clause,[t.bit,-t.input]))throw Error("identity goals");
 }
 return {PASS:true,counts:cnt,paid_inferences:148,records:L.length};
}
if(require.main===module){const p=build();console.log(JSON.stringify(check(p),null,2));}
module.exports={build,check};
