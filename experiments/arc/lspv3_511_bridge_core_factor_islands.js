"use strict";
// LSPV-3/511: exact-support SOURCE/AND3/XOR local factor and graph controls.
// A separately defined, incomplete calculus; not the full historical R_mix341.
function assert(x,m){if(!x)throw Error(m);}
function pop(x){let c=0;while(x){c+=x&1;x>>=1;}return c;}
function k4(o){let a=[];for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)a.push([o+i,o+j]);return a;}
function sub(o){return k4(o).filter(([a,b])=>a!==o||b!==o+1).concat([[o,o+4],[o+1,o+4]]);}
function fixtures(){let cube=[];for(let i=0;i<8;i++)for(let b=0;b<3;b++){let j=i^(1<<b);if(i<j)cube.push([i,j]);}
let a=[["K4",4,k4(0)],["K33",6,Array.from({length:9},(_,i)=>[Math.floor(i/3),3+i%3])],["CUBE",8,cube],
["BRIDGE2",10,sub(0).concat(sub(5),[[4,9]])],["BRIDGE3",16,sub(0).concat(sub(5),sub(10),[[15,4],[15,9],[15,14]])]];
for(let h of [16,32,64,128]){let k=h/2,e=[];for(let i=0;i<k;i++)e.push([i,(i+1)%k],[k+i,k+(i+1)%k],[i,k+i]);a.push(["PRISM"+k,h,e]);}
return a;}
function parts(n,edges,omit){
const adj=Array.from({length:n},()=>[]);for(let [a,b] of edges)if(a!==omit&&b!==omit){adj[a].push(b);adj[b].push(a);}
const seen=new Set([omit]),out=[];
for(let u=0;u<n;u++)if(!seen.has(u)){let stack=[u];seen.add(u);for(let j=0;j<stack.length;j++)for(let v of adj[stack[j]])if(!seen.has(v)){seen.add(v);stack.push(v);}out.push(new Set(stack));}
return out;}
function compute(){
let checks=0,local=[];
for(let charge of [0,1]){
 let bad=Array.from({length:8},(_,i)=>i).filter(i=>pop(i)%2!==charge),rowCount=0;
 for(let subset=1;subset<16;subset++){
  let table=0;for(let z=0;z<8;z++)if(!bad.some((b,i)=>b===z&&(subset>>i&1)))table|=1<<z;
  let matches=[];for(let mask=0;mask<8;mask++)for(let rhs=0;rhs<2;rhs++){
    if(Array.from({length:8},(_,i)=>i).every(i=>!!(table>>i&1)===(pop(i&mask)%2===rhs)))matches.push([mask,rhs]);
  }
  assert(matches.length===(subset===15?1:0),"local affine alias");
  if(matches.length){assert(matches[0][0]===7&&matches[0][1]===charge,"row identity");rowCount++;}
  checks++;
 }
 assert(rowCount===1,"local closure");
 local.push({charge,reachable_nonempty_factors:15,affine_seeds:rowCount});
}
let cases=[];
for(let [name,n,edges] of fixtures()){
 let inc=Array.from({length:n},()=>[]);for(let e=0;e<edges.length;e++){let [u,v]=edges[e];assert(u!==v,"loop");inc[u].push(e);inc[v].push(e);}
 assert(inc.every(x=>x.length===3)&&edges.length*2===3*n,"cubic");
 assert(new Set(inc.map(v=>v.slice().sort((a,b)=>a-b).join(","))).size===n,"separate supports");
 const components={1:0,2:0,3:0};let essential=0;
 for(let v=0;v<n;v++){
  let cs=parts(n,edges,v),c=cs.length;assert(c>=1&&c<=3,"components");components[c]++;
  let count=0,charge=v===0?1:0;
  for(let z=0;z<8;z++)if(pop(z)%2!==charge){
    let good=cs.every(C=>{
      let required=0;for(let u of C)if(u===0)required^=1;
      let boundary=0;for(let j=0;j<3;j++){let e=inc[v][j],[a,b]=edges[e];if(C.has(a)!==C.has(b))boundary^=(z>>j)&1;}
      return required===boundary;
    });
    if(good)count++;
    checks++;
  }
  assert(count===1<<(3-c),"source-essentiality formula");
  essential+=count;checks++;
 }
 // Every proper nonempty vertex subset of a connected graph has an edge crossing.
 if(n<=16)for(let S=1;S<(1<<n)-1;S++){
   assert(edges.some(([a,b])=>((S>>a)&1)!==((S>>b)&1)),"connected incidence dependency");
   checks++;
 }
 cases.push({graph:name,h:n,m:4*n,E:edges.length,essential,nonessential:4*n-essential,
              source_floor:essential-1,core_exact_work:4*n-1,cut_components:components});
}
assert(cases.find(x=>x.graph==="BRIDGE2").essential===36,"bridge 36");
assert(cases.find(x=>x.graph==="BRIDGE3").essential===55,"bridge 55");
return {status:"PROVED/RESTRICTED symbolic proof plus finite controls",scope:"SOURCE/AND3/XOR exact positional factors only; no RES, LOCAL or DEF",checks,local,cases};
}
const result=compute();
if(typeof module!=="undefined" && require.main===module)process.stdout.write(JSON.stringify(result,null,2)+"\n");