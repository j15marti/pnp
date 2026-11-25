function runProjected(data,source){
 let checks=0;const assert=(b,m)=>{checks++;if(!b)throw Error(m)};
 function solve(n,P,G=[],cap=1024,order='input',project=true){
  let R=1<<n,M=R-1,st={add:0,rankTests:0,split:0,merges:0,dedup:0,projectionRows:0,peak:1,rawPeak:1,nodes:1,closureScans:0,deductions:0,hullScans:0,steps:0,liftTests:0};
  const pivot=x=>(x&M)&-(x&M);
  function add(A,e){st.add++;for(let a of A)if(e&pivot(a))e^=a;if(!(e&M))return e&R?null:A;let p=pivot(e);return [...A.map(a=>a&p?a^e:a),e].sort((a,b)=>pivot(a)-pivot(b));}
  function join(A,B){for(let e of B){A=add(A,e);if(!A)return null;}return A;}
  function span(P){return join([],P.flat().map(e=>e&M));}
  function subtract(A,B){let C=A,parts=[];for(let e of B){let D=add(C,e);if(D===null)return [A];if(D===C)continue;parts.push(add(C,e^R));C=D;}st.split+=parts.length;return parts;}
  function parity(x){x^=x>>>16;x^=x>>>8;x^=x>>>4;return (0x6996>>>(x&15))&1;}
  function point(A){return A.reduce((x,e)=>x|(e&R?pivot(e):0),0);}
  function nullbasis(A){let piv=A.reduce((x,e)=>x|pivot(e),0),out=[];for(let j=0;j<n;j++){let p=1<<j;if(piv&p)continue;let v=p;for(let e of A)if(e&p)v|=pivot(e);out.push(v);}return out;}
  function hull(L){let S=[],a=point(L[0].A);for(let {A} of L){st.hullScans++;S=add(S,point(A)^a);for(let v of nullbasis(A)){S=add(S,v);if(S.length===n)return [];}if(S.length===n)return [];}return join([],nullbasis(S).map(v=>v|(parity(v&a)?R:0)));}
  function close(H,rest){if(!H)return null;for(;;){let old=H.length;for(let p of rest){st.closureScans++;let C=H,last=null;for(let e of p){let D=add(C,e);if(!D){C=null;break;}if(D!==C)last=e;C=D;}if(!C)continue;if(C.length===H.length)return null;if(C.length===H.length+1){H=add(H,last^R);if(!H)return null;st.deductions++;}}if(old===H.length)return H;}}
  function projection(A,W){if(!project)return A;let Q=[],basis=new Map;for(let e of A){st.projectionRows++;let t=e&M;for(let w of W)if(t&pivot(w))t^=w;while(t&&basis.has(pivot(t))){let [v,f]=basis.get(pivot(t));t^=v;e^=f;}if(t)basis.set(pivot(t),[t,e]);else Q=add(Q,e);}return Q;}
  function compress(L){for(;;){let exact=new Map;for(let q of L){let key=q.A.join(',');if(exact.has(key))st.dedup++;else exact.set(key,q);}let group=new Map,next=[],changed=false;for(let q of exact.values()){let k=q.A.map(x=>x&M).join(','),p=group.get(k);if(!p){group.set(k,q);continue;}group.delete(k);let i=p.A.findIndex((v,j)=>v!==q.A[j]);assert(i>=0,'merge distinct');let C=[];for(let j=0;j<p.A.length;j++)if(j!==i)C=add(C,p.A[j]===q.A[j]?p.A[j]:p.A[j]^p.A[i]);next.push({A:C,kind:'merge',children:[p,q]});st.nodes++;st.merges++;changed=true;}next.push(...group.values());L=next;if(!changed)return L;}}
  let H=close(join([],G),P);if(!H)return {status:'UNSAT',st};let L=[{A:H,kind:'root'}],rest=P.map((p,i)=>({p,i})),done=[],allRank=span(P).length,chosen=[],cutRanks=[];
  while(rest.length){let k=0,best=Infinity;
    if(order==='rank')for(let i=0;i<rest.length;i++){let a=span([...done,rest[i].p]).length,b=span(rest.filter((_,j)=>i!==j).map(o=>o.p)).length,c=a+b-allRank;st.rankTests++;if(c<best){best=c;k=i;}}
    let {p,i}=rest.splice(k,1)[0];done.push(p);chosen.push(i);let W=project?span(rest.map(o=>o.p)):Array.from({length:n},(_,i)=>1<<i);cutRanks.push(span(done).length+span(rest.map(o=>o.p)).length-allRank);
    let next=[];for(let parent of L)for(let B of subtract(parent.A,p)){next.push({A:projection(B,W),B,W,parent,kind:'project'});st.nodes++;}
    st.rawPeak=Math.max(st.rawPeak,next.length);L=compress(next);st.steps++;st.peak=Math.max(st.peak,L.length);
    if(!L.length)return {status:'UNSAT',st,chosen,cutRanks};
    let before=hull(L),after=close(before,rest.map(o=>o.p));if(!after)return {status:'UNSAT',st,chosen,cutRanks};
    if(after.length>before.length){L=L.map(q=>{let A=join(q.A,after);return A?{A,kind:'restrict',parent:q}:null;}).filter(Boolean);st.nodes+=L.length;L=compress(L);}
    if(!L.length)return {status:'UNSAT',st,chosen,cutRanks};
    if(L.length>cap)return {status:'OPEN',st,chosen,cutRanks};
  }
  function contains(A,x){return A.every(e=>parity(e&x)===+(!!(e&R)));}
  let node=L[0],x=point(node.A);
  while(node.kind!=='root'){st.liftTests++;assert(contains(node.A,x),'node membership');if(node.kind==='merge'){node=node.children.find(q=>contains(q.A,x));assert(node,'merge lift');continue;}if(node.kind==='restrict'){node=node.parent;continue;}
    let B=join(node.B,node.W.map(w=>w|(parity(w&x)?R:0)));assert(B,'project lift');x=point(B);node=node.parent;}
  assert(contains(G,x)&&P.every(p=>!contains(p,x)),'source check');
  return {status:'SAT',witness:x,st,chosen,cutRanks,pieces:L.length};
 }
 function compile(C,ids){let n=ids.length,R=1<<n,index=new Map(ids.map((x,i)=>[x,i]));return C.map(c=>c.slice(1).map(l=>(1<<index.get(Math.abs(l)))^(1<<index.get(Math.abs(c[0])))^((l<0)!==(c[0]<0)?R:0)));}
 function ref(n,P,G=[]){let R=1<<n;function sat(e,x){let z=e&x,p=0;while(z){p^=1;z&=z-1;}return p===+(!!(e&R));}let c=0;for(let x=0;x<2**n;x++)if(G.every(e=>sat(e,x))&&P.every(p=>!p.every(e=>sat(e,x))))c++;return c;}
 const F=[[1,2,3],[1,4,5],[1,6,7],[2,4,6],[2,5,7],[3,4,7],[3,5,6]],ids=[1,2,3,4,5,6,7],result={fano:[],guards:[],stars:[]};
 for(let i=-1;i<21;i++){let C=F.map(a=>a.slice());if(i>=0)C[Math.floor(i/3)][i%3]*=-1;let p=compile(C,ids),r=ref(7,p),z=solve(7,p,[],1024,'rank');assert(z.status===(r?'SAT':'UNSAT'),'Fano decision');result.fano.push({r,z});if(i>=0){let G=[1|(i%2?128:0),6|128],g=ref(7,p,G),w=solve(7,p,G,1024,'rank');assert(w.status===(g?'SAT':'UNSAT'),'guard decision');result.guards.push({g,w});}}
 let s=solve(7,compile(F,ids),[1,129]);assert(s.status==='UNSAT','inconsistent guard');
 for(let k=1;k<=10;k++){let C=Array.from({length:k},(_,i)=>[1,2*i+2,2*i+3]),p=compile(C,Array.from({length:2*k+1},(_,i)=>i+1));let z=solve(2*k+1,p,[],1024,'input');assert(z.status==='SAT'&&z.st.peak===1,'star projection');result.stars.push({k,z});}
 const orig=source.O.map(o=>o.t.map(x=>x+1)),r=data.common.find(x=>x.K===16).residual,idsK=[...new Set(r.C.flat().map(Math.abs))].sort((a,b)=>a-b);
 result.common={};for(let [name,C,ids] of [['raw',orig,Array.from({length:24},(_,i)=>i+1)],['K16',r.C,idsK]])for(let order of ['input','rank']){let z=solve(ids.length,compile(C,ids),[],1024,order);if(z.status==='SAT'){let word=0;for(let i=0;i<ids.length;i++)if(z.witness&(1<<i))word|=1<<(ids[i]-1);function val(l,x){return ((x>>>(Math.abs(l)-1))&1)^+(l<0);}function ok(c,x){return c.some(l=>val(l,x)!==val(c[0],x));}if(name==='K16')for(let l of r.log.slice().reverse()){let a=word&~(1<<(l.v-1)),b=a|(1<<(l.v-1));let can=x=>l.bucket.every(t=>ok([l.v,...t],x));assert(can(a)||can(b),'reverse lift');word=can(a)?a:b;}assert(orig.every(c=>ok(c,word)),'original source');z.sourceWord=word;}result.common[name+'_'+order]=z;}
 result.checks=checks;return result;
}
const fs=require('fs'); console.log(JSON.stringify(runProjected(JSON.parse(fs.readFileSync(process.argv[2],'utf8')),JSON.parse(fs.readFileSync(process.argv[3],'utf8'))),null,2));
