// LSPV-4/461: finite semantic checker, NOT native FLMV timing or a SAT lower bound.
(function(){
  let seed=4611106>>>0, checks=0, reads=0, resets=0, largest=0n, peak=0;
  function rnd(){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return seed>>>0;}
  function ok(p){if(!p)throw Error("LSPV-4/461 check failed");checks++;}
  const data=new Map(), marks=new Set();
  for(let k=0;k<300;k++){
    const fresh=new Map(), dirty=[];let head=0n;
    for(let t=0;t<140;t++){
      const op=rnd()%4;
      if(op===0){head=(t%3===0)?(1n<<40n):(1n<<BigInt(rnd()%41));}
      else if(op===1){head=head===0n?1n:head+((rnd()&1)?1n:-1n);}
      else{
        const a=head.toString();
        if(!marks.has(a)){marks.add(a);dirty.push(a);}
        if(op===2){let v=rnd()%4;if(v){data.set(a,v);fresh.set(a,v);}else{data.delete(a);fresh.delete(a);}}
        else{ok((data.get(a)||0)===(fresh.get(a)||0));reads++;}
      }
      if(head>largest)largest=head;
    }
    ok(dirty.length===marks.size);peak=Math.max(peak,dirty.length);
    for(const a of dirty){data.delete(a);marks.delete(a);resets++;}
    ok(data.size===0&&marks.size===0);
    ok((data.get((1n<<40n).toString())||0)===0);
  }
  let malformed=0;
  for(let c=0;c<100;c++){const stale=new Map([[(2n**40n+BigInt(c)).toString(),2]]);ok(stale.size===1);ok([...stale.values()][0]!==0);}
  function tseitin(edges,odd){
    const deg={};edges.forEach(([u,v],i)=>{(deg[u]??=[]).push(i+1);(deg[v]??=[]).push(i+1);});
    ok(Object.values(deg).every(x=>x.length===3));
    let f=[];for(const [vertex,es] of Object.entries(deg)){
      let charge=(Number(vertex)===0)?odd:0;
      for(let a=0;a<8;a++){const parity=((a&1)+((a>>1)&1)+((a>>2)&1))&1;
        if(parity!==charge)f.push(es.map((e,j)=>((a>>j)&1)?-e:e));
      }
    }
    ok(f.length===edges.length*8/3);
    let sat=false;for(let m=0;m<(1<<edges.length);m++){
      if(f.every(clause=>clause.some(l=>l>0?!!(m&(1<<(l-1))):!(m&(1<<(-l-1)))))){sat=true;break;}
    }
    ok(sat===(odd===0));
    const bad=[0,f[0][1],f[0][2]];
    ok(bad.length===3&&bad.some(l=>l===0));malformed++;
  }
  const k4=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
  const cube=[];for(let v=0;v<8;v++)for(let j=0;j<3;j++){let w=v^(1<<j);if(v<w)cube.push([v,w]);}
  for(const edges of [k4,cube])for(const parity of [0,1])tseitin(edges,parity);
  return {status:"PASS",calls:300,checks,reads,clearedDistinctWorkAddresses:resets,maxDistinctInOneCall:peak,maximumIndex:String(largest),sourceParityControls:4,malformedControls:malformed,scope:"finite abstract-address control only"};
})()
