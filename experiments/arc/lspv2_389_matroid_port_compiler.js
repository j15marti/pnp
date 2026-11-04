/* LSPV-2/389. Exact mixed proof compiler on GF(2) matroid circuits (row width 2/3).
 * Fixed R_mix341: original source clauses free; AND3 and XOR cost one per binary inference.
 * node lspv2_389_matroid_port_compiler.js > cases.json */
"use strict";
function rowClauses(vs,b) {
  const out=[];
  for(let mask=0;mask<(1<<vs.length);mask++) {
    let parity=0;for(let k=0;k<vs.length;k++)parity^=(mask>>k)&1;
    if(parity!==b)out.push(vs.map((v,k)=>mask&(1<<k)?-v:v));
  }
  return out;
}
function bits(vs){return vs.reduce((acc,v)=>acc|(1<<(v-1)),0);}
function rank(ms){
  const p={};let count=0;
  for(let x of ms){while(x){const k=31-Math.clz32(x);if(p[k]===undefined){p[k]=x;count++;break;}x^=p[k];}}
  return count;
}
function models(source,n){
  const out=[];
  for(let a=0;a<(1<<n);a++){
    if(source.every(c=>c.some(l=>!!(a&(1<<(Math.abs(l)-1)))===(l>0))))out.push(a);
  }
  return out;
}
function compile(name,n,rows) {
  const ms=rows.map(r=>bits(r.vars));
  const source=[],parts=[];
  for(const r of rows) {
    const start=source.length,cl=rowClauses(r.vars,r.b);
    parts.push(cl.map((_,j)=>start+j));source.push(...cl);
  }
  const rank_other=[],projection_dim=[];
  for(let i=0;i<rows.length;i++){
    const other=ms.filter((_,j)=>j!==i),nullspace=[];
    rank_other.push(rank(other));
    for(let a=0;a<(1<<n);a++)if(other.every(row=>!(popcount(a&row)&1)))nullspace.push(a);
    const proj=nullspace.map(a=>rows[i].vars.reduce((z,v,k)=>z|(((a>>(v-1))&1)<<k),0));
    projection_dim.push(rank(proj));
  }
  const xor=ms.reduce((a,b)=>a^b,0),rhs=rows.reduce((a,r)=>a^r.b,0);
  const circuit=xor===0&&rhs===1&&rank_other.every(k=>k===rows.length-1);
  const fullproj=projection_dim.every((k,i)=>k===rows[i].vars.length-1);
  const actual=models(source,n),deletions=[],flips=[];
  for(let j=0;j<source.length;j++){
    const remove=models(source.filter((_,k)=>j!==k),n);
    deletions.push(remove.length?remove[0]:null);
    const modified=source.map(c=>c.slice());modified[j][0]*=-1;
    const flip=models(modified,n);flips.push(flip.length?flip[0]:null);
  }
  const r={name,n,rows,sources:source,parts,rank_other,projection_dim,circuit,fullproj,models:actual,delete:deletions,flip:flips,compiled:false};
  if(!(circuit&&fullproj&&actual.length===0))return r;
  const proof=[],outputs=[];
  for(let i=0;i<rows.length;i++){
    const scope=rows[i].vars,cs=parts[i],num=1<<scope.length;
    if(cs.length<2)throw Error("width-one outside theorem");
    let previous="s"+cs[0];
    for(let k=1;k<cs.length;k++){
      let truth=0;
      for(let assignment=0;assignment<num;assignment++){
        const env=scope.reduce((z,v,j)=>z|(((assignment>>j)&1)<<(v-1)),0);
        if(cs.slice(0,k+1).every(id=>source[id].some(l=>!!(env&(1<<(Math.abs(l)-1)))===(l>0))))
          truth|=1<<assignment;
      }
      const id="d"+proof.length;
      proof.push({id,rule:"AND3",parents:[previous,"s"+cs[k]],scope,truth,
        equation:k===cs.length-1?{vars:scope,b:rows[i].b}:null});
      previous=id;
    }
    outputs.push(previous);
  }
  let current=outputs[0],curmask=ms[0],currhs=rows[0].b;
  for(let i=1;i<rows.length;i++){
    curmask^=ms[i];currhs^=rows[i].b;
    const vs=Array.from({length:n},(_,k)=>k+1).filter(x=>curmask&(1<<(x-1)));
    const id="d"+proof.length;proof.push({id,rule:"XOR",parents:[current,outputs[i]],equation:{vars:vs,b:currhs}});
    current=id;
  }
  if(curmask!==0||currhs!==1||proof.length!==source.length-1)throw Error("construction failed");
  r.compiled=true;r.proof=proof;r.paid=proof.length;return r;
}
function popcount(x){let n=0;while(x){x&=x-1;n++;}return n;}
function run(){
  const cases=[
    compile("odd_triangle_no_even",3,[{vars:[1,2],b:1},{vars:[2,3],b:1},{vars:[1,3],b:1}]),
    compile("four_var_mixed_affine",4,[{vars:[1,2,3],b:1},{vars:[1,4],b:1},{vars:[2,3,4],b:1}]),
    compile("five_var_hypergraph_circuit",5,[{vars:[1,2,3],b:1},{vars:[3,4,5],b:1},{vars:[1,4],b:1},{vars:[2,5],b:0}]),
    compile("charge_flipped_SAT",5,[{vars:[1,2,3],b:1},{vars:[3,4,5],b:1},{vars:[1,4],b:1},{vars:[2,5],b:1}]),
    compile("rank_projection_failure_width23",4,[{vars:[1,2,3],b:1},{vars:[1,3,4],b:1},{vars:[1,2],b:1},{vars:[1,4],b:0}])
  ];
  return {schema:"LSPV2-389-matroid-circuit-projection-v1",model:"fixed R_mix341; source clauses free, AND3/XOR paid 1 with binary premises",cases};
}
if(typeof module!=="undefined" && require.main===module)process.stdout.write(JSON.stringify(run(),null,2)+"\n");
