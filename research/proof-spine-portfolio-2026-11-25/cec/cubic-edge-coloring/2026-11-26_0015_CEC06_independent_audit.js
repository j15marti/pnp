function audit(){
 const assert=(v,m)=>{if(!v)throw Error(m)};
 const edge=(u,v)=>u<v?`${u},${v}`:`${v},${u}`;
 const pair=e=>e.split(",").map(Number);
 const comp=(V,E)=>{let adj=new Map(V.map(v=>[v,[]]));for(const e of E){const [u,v]=pair(e);adj.get(u).push(v);adj.get(v).push(u)}let seen=new Set(),out=[];for(const v of V)if(!seen.has(v)){let q=[v];seen.add(v);for(let i=0;i<q.length;i++)for(const w of adj.get(q[i]))if(!seen.has(w)){seen.add(w);q.push(w)}out.push(q)}return out};
 const sub=(A,B)=>new Set([...A].filter(e=>!B.has(e)));
 const xor=(A,B)=>new Set([...sub(A,B),...sub(B,A)]);
 const deg=(E,v)=>[...E].filter(e=>pair(e).includes(v)).length;
 const matching=(V,E,all=false)=>{let out=[];function rec(V,M){if(!V.length){out.push(new Set(M));return true}let u=V[0];for(let v of V.slice(1)){let e=edge(u,v);if(E.has(e)){if(rec(V.filter(x=>x!==u&&x!==v),[...M,e])&&!all)return true}}return false}rec(V,[]);return out};
 const even=(V,E)=>V.every(v=>deg(E,v)===2)&&comp(V,E).every(c=>c.length%2===0);
 function solve(V,E,A,z){
   let base=sub(sub(E,A),new Set([z])), groups=[],choices=[];
   let [u,v]=pair(z);
   for(const C of comp(V,A)){
     if(C.length===1){if(deg(base,C[0])!==2)return null;continue}
     let cycle=[C[0]],prev=-1;
     while(cycle.length<C.length){let w=cycle.at(-1),j=[...A].map(pair).filter(e=>e.includes(w)).map(e=>e.find(x=>x!==w)).find(x=>x!==prev&&!cycle.includes(x));assert(j!==undefined,"cycle walk");prev=w;cycle.push(j)}
     let ce=cycle.map((x,i)=>edge(x,cycle[(i+1)%cycle.length])),P=[];
     for(let first of [0,1]){let vals=[first];for(let i=1;i<cycle.length;i++)vals.push(2-deg(base,cycle[i])-vals.at(-1));if(vals.every(x=>x===0||x===1)&&vals.at(-1)+vals[0]===2-deg(base,cycle[0]))P.push(new Set(ce.filter((_,i)=>vals[i])))}
     if(!P.length)return null;
     if(P.length===1){for(const e of P[0])base.add(e)}else{groups.push(C);choices.push(P)}
   }
   let ends=new Map([[u,[]],[v,[]]]),n=V.length,FE=new Set();
   for(const e of base){let p=pair(e).map(x=>{if(!ends.has(x))return x;ends.get(x).push(n);return n++});FE.add(edge(...p))}
   let FV=[...new Set([...FE].flatMap(pair))],W=new Set();for(const c of comp(FV,FE)){let p=c.filter(x=>deg(FE,x)===1);assert(p.length===0||p.length===2,"wire");if(p.length)W.add(edge(...p))}
   let R=choices.map(P=>P.map(q=>new Set(q))),reductions=0;
   function splice(M,e){let [x,y]=pair(e);if(M.has(e))return sub(M,new Set([e]));let a=[...M].find(f=>pair(f).includes(x)),b=[...M].find(f=>pair(f).includes(y));assert(a&&b&&a!==b,"splice");return new Set([...sub(M,new Set([a,b])),edge(pair(a).find(w=>w!==x),pair(b).find(w=>w!==y))])}
   for(;;){let changed=false;for(let i=0;i<R.length;i++){let [P,Q]=R[i],common=[...P].find(e=>Q.has(e));if(common){R[i]=[sub(P,new Set([common])),sub(Q,new Set([common]))];W=splice(W,common)}else{let pp=new Set([...P].flatMap(pair)),wire=[...W].find(e=>pair(e).every(x=>pp.has(x)));if(!wire)continue;R[i]=[splice(P,wire),splice(Q,wire)];W.delete(wire)}changed=true;reductions++;break}if(!changed)break}
   let ports=[...new Set([...W].flatMap(pair))],long=R.map((P,i)=>P[0].size>2?i:-1).filter(i=>i>=0),branches=0;
   for(let bits=0;bits<2**long.length;bits++){branches++;let f=new Map(long.map((i,j)=>[i,(bits>>j)&1]));let H=new Set(W);for(let i=0;i<R.length;i++)for(const e of f.has(i)?R[i][f.get(i)]:new Set([...R[i][0],...R[i][1]]))H.add(e);
     for(const x of ends.get(u))for(const y of ends.get(v)){
       let M=matching(ports.filter(w=>w!==x&&w!==y),H)[0];if(!M)continue;
       let D=xor(W,M),pathComp=comp(ports,D).find(C=>C.includes(x));assert(pathComp.includes(y),"alternating endpoints");
       let used=new Set([...sub(D,W)].filter(e=>pair(e).every(w=>pathComp.includes(w))));
       for(let i=0;i<R.length;i++)if(!f.has(i)){let needed=[...used].filter(e=>R[i].some(P=>P.has(e))),j=R[i].findIndex(P=>needed.every(e=>P.has(e)));assert(j>=0,"joint short phases");f.set(i,j)}
       let B=new Set(base);for(let i=0;i<choices.length;i++)for(const e of choices[i][f.get(i)])B.add(e);assert(even(V,B),"source even factor");assert(sub(sub(E,A),new Set([z])).size==[...B].filter(e=>!A.has(e)).length&&[...B].filter(e=>!A.has(e)).every(e=>e!==z),"exact membership");return {B:[...B].sort(),long:long.length,branches,reductions}
     }
   }
   return {B:null,long:long.length,branches,reductions};
 }
 const p=[[0,1],[0,4],[0,5],[1,2],[1,6],[2,3],[2,7],[3,4],[3,8],[4,9],[5,7],[5,8],[6,8],[6,9],[7,9]];
 const sat=p.filter(e=>!["0,4","1,2"].includes(edge(...e))).concat([[0,2],[1,4]]);
 const trap=[[0,1],[0,4],[0,5],[1,2],[1,7],[2,3],[2,6],[3,6],[3,7],[4,5],[4,7],[5,6]];
 const fp=[[0,2],[0,6],[0,9],[2,10],[2,11],[6,5],[6,7],[9,4],[9,8],[1,3],[1,7],[1,10],[3,8],[3,11],[7,8],[10,5],[11,4],[4,5]];
 const baseA=[[2,3],[2,7],[3,4],[4,9],[5,7],[5,8],[6,8],[6,9]];
 const tests=[["Petersen",p,baseA,[0,1]],["SAT neighbor",sat,baseA,[0,1]],["SAT trap",trap,[[0,1],[0,4],[1,2],[2,3],[3,7],[4,7]],[5,6]],["FP12",fp,fp.filter((_,i)=>(48501>>i)&1),[4,5]]];
 let results=[];
 for(const [name,ee,aa,zz] of tests){let V=Array.from({length:Math.max(...ee.flat())+1},(_,i)=>i),E=new Set(ee.map(e=>edge(...e))),A=new Set(aa.map(e=>edge(...e))),z=edge(...zz),Fs=matching(V,E,true).map(M=>sub(E,M)).filter(F=>even(V,F));let check=0,yes=0;
   for(let mask=0;mask<2**ee.length;mask++){let C=new Set(ee.filter((_,i)=>(mask>>i)&1).map(e=>edge(...e)));if(V.some(v=>deg(C,v)%2))continue;let odd=comp(V,C).filter(c=>c.length%2);if(odd.length!==2)continue;for(const d of sub(E,C)){if(!odd.every(c=>pair(d).some(v=>c.includes(v))))continue;let ex=Fs.some(F=>[...sub(E,C)].every(e=>F.has(e)===(e!==d))),r=solve(V,E,C,d);assert(!!r?.B===ex,`${name} mismatch`);check++;yes+=+ex}}
   let r=solve(V,E,A,z);results.push({name,sourceSAT:Fs.length>0,evenFactors:Fs.length,charts:check,positive:yes,fixture:r});
 }
 return results;
}
console.log(JSON.stringify(audit(),null,2));
