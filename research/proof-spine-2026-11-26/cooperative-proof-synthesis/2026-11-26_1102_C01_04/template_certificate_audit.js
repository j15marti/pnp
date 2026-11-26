const templates=[
  {
    "type": "L-adj",
    "n": [
      3,
      2,
      2
    ],
    "T": [
      [
        1,
        0,
        1
      ],
      [
        2,
        1,
        0
      ],
      [
        2,
        1,
        1
      ],
      [
        0,
        1,
        1
      ],
      [
        2,
        0,
        0
      ]
    ],
    "order": [
      "a0",
      "a1",
      "b0",
      "c0"
    ],
    "R": {
      "0": [
        2
      ],
      "13": [
        3,
        4
      ],
      "14": [
        0,
        1
      ]
    },
    "rot": {
      "a1": "t0 a0 h b0",
      "a2": "t2 t4 t1",
      "c1": "t0 t2 t3",
      "a0": "t3 c0 h a1",
      "b0": "c0 t4 t0 a1 h",
      "b1": "t1 t3 t2",
      "c0": "a0 t1 t4 b0 h",
      "t0": "a1 b0 c1",
      "t1": "a2 c0 b1",
      "t2": "c1 a2 b1",
      "t3": "b1 a0 c1",
      "t4": "b0 c0 a2",
      "h": "b0 a1 a0 c0"
    }
  },
  {
    "type": "L-alt",
    "n": [
      3,
      2,
      2
    ],
    "T": [
      [
        0,
        0,
        1
      ],
      [
        2,
        1,
        1
      ],
      [
        1,
        0,
        1
      ],
      [
        2,
        1,
        0
      ]
    ],
    "order": [
      "a0",
      "b0",
      "a1",
      "c0"
    ],
    "R": {
      "0": [
        1
      ],
      "13": [
        0,
        3
      ],
      "14": [
        2,
        3
      ]
    },
    "rot": {
      "a1": "t2 b0 h c0",
      "a2": "t3 t1",
      "c1": "t2 t1 t0",
      "a0": "t0 c0 h b0",
      "b0": "a0 h a1 t2 t0",
      "b1": "t1 t3",
      "c0": "h a0 t3 a1",
      "t0": "c1 a0 b0",
      "t1": "a2 c1 b1",
      "t2": "a1 c1 b0",
      "t3": "c0 a2 b1",
      "h": "b0 a0 c0 a1"
    }
  },
  {
    "type": "U-adj",
    "n": [
      3,
      3,
      3
    ],
    "T": [
      [
        1,
        1,
        2
      ],
      [
        2,
        0,
        0
      ],
      [
        2,
        2,
        1
      ],
      [
        2,
        1,
        2
      ],
      [
        0,
        2,
        1
      ]
    ],
    "order": [
      "a0",
      "a1",
      "b0",
      "c0"
    ],
    "R": {
      "1": [
        3,
        4
      ],
      "2": [
        0,
        2
      ],
      "15": [
        0,
        1,
        4
      ]
    },
    "rot": {
      "a1": "t0 a0 h b0",
      "b2": "t4 t2",
      "c1": "t2 t4",
      "a0": "c0 h a1 t4",
      "b1": "t0 t3",
      "c0": "t1 b0 h a0",
      "a2": "t3 t1 t2",
      "c2": "t3 t0",
      "b0": "h c0 t1 a1",
      "t0": "a1 b1 c2",
      "t1": "a2 b0 c0",
      "t2": "b2 a2 c1",
      "t3": "b1 a2 c2",
      "t4": "a0 b2 c1",
      "h": "a0 c0 b0 a1"
    }
  },
  {
    "type": "U-alt",
    "n": [
      2,
      2,
      2
    ],
    "T": [
      [
        0,
        1,
        1
      ],
      [
        0,
        1,
        0
      ],
      [
        1,
        1,
        1
      ],
      [
        1,
        0,
        1
      ]
    ],
    "order": [
      "a0",
      "b0",
      "a1",
      "c0"
    ],
    "R": {
      "1": [
        0
      ],
      "2": [
        2
      ],
      "15": [
        1,
        3
      ]
    },
    "rot": {
      "a1": "t2 c0 h b0 t3",
      "c1": "t2 t3 t0",
      "a0": "t0 b0 h c0 t1",
      "b0": "h a0 t3 a1",
      "b1": "t1 t2 t0",
      "c0": "t1 a0 h a1",
      "t0": "c1 a0 b1",
      "t1": "a0 c0 b1",
      "t2": "a1 c1 b1",
      "t3": "b0 c1 a1",
      "h": "c0 a0 b0 a1"
    }
  }
];
function audit(ts){
 const B=["a0","a1","b0","c0"],A=(v,msg)=>{if(!v)throw new Error(msg)},col="abc";
 const names=t=>t.map((v,i)=>col[i]+v);
 function support(T,n){
  let privateV=[];n.forEach((k,c)=>{for(let i=0;i<k;i++){const v=col[c]+i;if(!B.includes(v))privateV.push(v)}});
  let R=new Set;
  for(let s=0;s<(1<<T.length);s++){
   let arr=T.flatMap((t,j)=>s>>j&1?names(t):[]);
   if(arr.length!==new Set(arr).size||privateV.some(v=>!arr.includes(v)))continue;
   R.add(B.reduce((m,v,i)=>m+(arr.includes(v)?1<<i:0),0));
  }
  return [...R].sort((a,b)=>a-b).join(",");
 }
 let rows=[];
 for(const d of ts){
  const wanted=Object.keys(d.R).map(Number).sort((a,b)=>a-b);
  A(support(d.T,d.n)===wanted.join(","),"full support");
  for(let m=1;m<1<<wanted.length;m++){
   let M=wanted.filter((x,i)=>m>>i&1),J=new Set(M.flatMap(x=>d.R[x]));A(support(d.T.filter((_,j)=>J.has(j)),d.n)===M.join(","),"subset support");
  }
  let ed=new Set, edge=(v,w)=>[v,w].sort().join(" ");
  d.T.forEach((t,j)=>names(t).forEach(v=>ed.add(edge("t"+j,v))));
  for(let i=0;i<4;i++){ed.add(edge(d.order[i],d.order[(i+1)%4]));ed.add(edge(d.order[i],"h"))}
  let R=Object.fromEntries(Object.entries(d.rot).map(([v,s])=>[v,s.split(" ")])), seen=new Set;
  for(let [v,ns] of Object.entries(R))for(let w of ns){A(ed.has(edge(v,w))&&R[w].includes(v),"rotation edge");seen.add(v+" "+w)}
  A(seen.size===2*ed.size,"edge completeness");
  let used=new Set,F=0;
  for(let s of seen){if(used.has(s))continue;F++;let cur=s;do{A(!used.has(cur),"face overlap");used.add(cur);let[v,w]=cur.split(" "),ns=R[w];cur=w+" "+ns[(ns.indexOf(v)+ns.length-1)%ns.length]}while(cur!==s)}
  let V=Object.keys(R).length,E=ed.size;A(V-E+F===2,"sphere Euler");
  let reach=new Set(["t0"]);for(let again=true;again;){again=false;for(let v of [...reach])for(let w of R[v])if(!B.includes(w)&&w!=="h"&&!reach.has(w)){reach.add(w);again=true}}
  A(reach.size===V-5&&B.every(b=>R[b].some(v=>reach.has(v))),"interior connected and touches four");
  rows.push({type:d.type,V,E,F,support:wanted,nonemptySubsets:7})
 }
 let sig=new Set;
 for(let a=0;a<4;a++)for(let b=0;b<4;b++)for(let c=0;c<4;c++){
  let M=[];for(let m=0;m<16;m++)if(a+(m&1)+(m>>1&1)===b+(m>>2&1)&&b+(m>>2&1)===c+(m>>3&1))M.push(m);
  for(let s=1;s<1<<M.length;s++)sig.add(M.filter((_,i)=>s>>i&1).join(","))
 }
 A(sig.size===26,"signature count");return {rotations:rows,signatures:sig.size}
}
console.log(JSON.stringify(audit(templates),null,2));
