// Independent finite arithmetic audit; no native-source solver here.
const audit=function audit(){
  const words=Array.from({length:8},(_,i)=>[i>>2,(i>>1)&1,i&1]);
  let checks=0;
  function ok(b){if(!b)throw Error("assertion failed");checks++}
  // Check all positive forbidden weights b,c,d in [1,8], unique a=b+c+d.
  for(let b=1;b<=8;b++)for(let c=1;c<=8;c++)for(let d=1;d<=8;d++){
    const P=[b+c+d,0,b,0,c,0,0,d];
    const walsh=mask=>words.reduce((s,w,i)=>s+P[i]*(-1)**w.reduce((t,x,j)=>t+x*((mask>>j)&1),0),0);
    ok(walsh(7)===0);
    ok(walsh(1)===2*b);ok(walsh(2)===2*c);ok(walsh(4)===2*(b+c));
    ok(walsh(3)===2*d);ok(walsh(5)===2*(b+d));ok(walsh(6)===2*(c+d));
    for(let i=0;i<8;i++)ok((P[i]===0)===(words[i][2]===1-words[i][0]*words[i][1]));
  }
  // Independent integer circulation witness for orientation 0->1->2->3->0 plus 0->2 and 1->3.
  const E=[[0,1],[1,2],[2,3],[3,0],[0,2],[1,3]],weights=[2,1,2,3,1,1];
  const flow=[0,0,0,0];
  E.forEach(([u,v],i)=>{flow[u]+=weights[i];flow[v]-=weights[i]});ok(flow.every(x=>x===0));
  let energyZero=[];
  for(let i=0;i<16;i++){const w=Array.from({length:4},(_,j)=>(i>>j)&1);const e=E.reduce((s,[u,v],j)=>s+weights[j]*Number(w[u]===0&&w[v]===1),0);if(e===0)energyZero.push(i)}
  ok(JSON.stringify(energyZero)==="[0,15]");
  const grids=[];
  for(const l of [2,3,4,5,8,12,32,64,128]){
    const edges=new Set(), id=(i,j)=>i*l+j;
    const add=(u,v)=>edges.add([Math.min(u,v),Math.max(u,v)].join(","));
    for(let i=0;i<l-1;i++)for(let j=0;j<l-1;j++){
      const a=id(i,j),b=id(i+1,j),c=id(i+1,j+1),d=id(i,j+1);
      for(const [u,v] of [[a,b],[b,c],[a,c],[a,d],[d,c]])add(u,v);
    }
    ok(edges.size===3*l*l-4*l+1);
    grids.push({l,variables:l*l,edges:edges.size,anchor_lower:Math.ceil((edges.size-2*l*l+6)/3)});
  }
  return {checks,nand_weight_cases:512,energyZero,grids};
};
console.log(JSON.stringify(audit(),null,2));
