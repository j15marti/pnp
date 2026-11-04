// LSPV-1 376. Root-only bounded-support Boolean normalization controls.
// This checks 3-input truth-table semantics, NOT an Rmix341 proof checker.
'use strict';
function run(){
 let checks=0;function chk(v){checks++;if(!v)throw Error('assertion '+checks)}
 const bit=(a,i)=>(a>>i)&1, all=255;
 function blocks(q){let v=[];for(let a=0;a<8;a++)if(!(q&(1<<a)))v.push([0,1,2].map(i=>bit(a,i)?-(i+1):i+1));return v}
 function cl(c,a){return c.some(l=>l>0?bit(a,l-1):!bit(a,-l-1))}
 function circuit(q){let g=[['i',0],['i',1],['i',2],['c',0]];let neg=[];
  for(let i=0;i<3;i++){neg[i]=g.length;g.push(['!',i])}
  let root=3;const add=(op,u,v)=>{let i=g.length;g.push([op,u,v]);return i};
  for(let a=0;a<8;a++)if(q&(1<<a)){let l=[0,1,2].map(i=>bit(a,i)?i:neg[i]);root=add('|',root,add('&',add('&',l[0],l[1]),l[2]))}
  return {g,root}
 }
 function evalCircuit(c,a){let vals=[];for(let i=0;i<c.g.length;i++){let [op,u,v]=c.g[i];let z;
  if(op==='i'){if(u<0||u>2)throw Error('input');z=bit(a,u)}
  else if(op==='c')z=u;
  else{if(u<0||u>=i||(op!=='!'&&(v<0||v>=i)))throw Error('ref');
    if(op==='!')z=1-vals[u];else if(op==='&')z=vals[u]&vals[v];else if(op==='|')z=vals[u]|vals[v];else throw Error('op')}
  vals.push(z)}
  if(c.root<0||c.root>=vals.length)throw Error('root');return vals[c.root]}
 function table(c){let o=0;for(let a=0;a<8;a++)o|=evalCircuit(c,a)<<a;return o}
 const cs=[];for(let q=0;q<256;q++){const c=circuit(q);chk(table(c)===q);for(let a=0;a<8;a++)chk(blocks(q).every(clause=>cl(clause,a))===!!(q&(1<<a)));cs.push(c)}
 let legal=0,illegal=0,implicates=0;
 for(let s=0;s<256;s++)for(let q=0;q<256;q++){const valid=(s&(~q&all))===0;
  let implied=true;for(let a=0;a<8;a++)if(s&(1<<a))implied=implied&&!!evalCircuit(cs[q],a);
  chk(implied===valid);
  if(valid){legal++;for(let clause of blocks(q)){chk(Array.from({length:8},(_,a)=>!(s&(1<<a))||cl(clause,a)).every(Boolean));implicates++}}
  else {illegal++;chk((s&(~q&all))!==0)}
  chk(table(cs[s&q])===(s&q))
 }
 chk(legal===6561&&illegal===58975);
 function reject(f){let bad=false;try{f()}catch(e){bad=true}chk(bad)}
 reject(()=>evalCircuit({g:[['!',0]],root:0},0));
 reject(()=>evalCircuit({g:[['i',3]],root:0},0));
 reject(()=>evalCircuit({g:[['wat',0]],root:0},0));
 reject(()=>evalCircuit({g:[],root:0},0));
 let corruptions=0;for(let k of [4,16,128,512]){
  let g=[['i',0]];for(let j=0;j<k;j++)g.push(['c',1]);
  let root=0;for(let j=0;j<k;j++){let t=g.length;g.push(['&',root,j+1]);root=t}
  chk(table({g,root})===170);
  for(let j=0;j<k;j++){let g2=g.map(x=>x.slice());g2[j+1]=['c',0];chk(table({g:g2,root})===0);corruptions++}
 }
 function k4(c){let edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]], n=0;
  for(let a=0;a<64;a++)if(c.every((rhs,v)=>edges.reduce((sum,e,i)=>sum^(e.includes(v)?bit(a,i):0),0)===rhs))n++;return n}
 chk(k4([1,0,0,0])===0&&k4([0,0,0,0])===8);
 return {run_id:'LSPV1_ROOT_EXTENSIONAL_SEMANTIC_QUOTIENT376',checks,functions:256,semantic_pairs:65536,legal,illegal,implied_basis_clauses:implicates,corruptions,malformed_rejections:4,k4_odd_models:0,k4_even_models:8,scope:'semantic controls, not strict ER2 certificate replay',status:'PASS'};
}
if(typeof require==='function'&&typeof module==='object'&&require.main===module)console.log(JSON.stringify(run(),null,2));
