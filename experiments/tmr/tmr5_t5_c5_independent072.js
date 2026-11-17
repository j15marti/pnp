/* TMR-5 independent source-derived C5->T5 graph-gadget audit; exact symbolic theorem in accompanying report. */
function run() {
  const beat=(a,b)=>([1,3].includes((b-a+5)%5));
  const edge5=(a,b)=>((b-a+5)%5===1||(b-a+5)%5===4);
  const two=(a,b)=>{let t=0;for(let z=0;z<5;z++)if(beat(a,z)&&beat(z,b))t++;return t;};
  let pairs=0, graphs=0, baseAssignments=0, kst=0;
  let path=[0,1,1,0,2];
  for(let a=0;a<5;a++)for(let b=0;b<5;b++){
    let val=0;
    for(let z=0;z<5;z++)for(let w=0;w<5;w++)
      if(beat(a,z)&&beat(z,b)&&beat(b,w)&&beat(w,a))val++;
    if(val!==(edge5(a,b)?2:0)||val!==two(a,b)*two(b,a)) throw Error("four-arc gadget");
    pairs++;
  }
  function enumLabels(n,fn){let f=new Array(n).fill(0);function rec(i){if(i===n){fn(f);return;}for(let a=0;a<5;a++){f[i]=a;rec(i+1);}}rec(0);}
  for(let n=0;n<=4;n++){
    let poss=[];for(let u=0;u<n;u++)for(let v=u+1;v<n;v++)poss.push([u,v]);
    for(let mask=0;mask<2**poss.length;mask++){
      let edges=poss.filter((x,i)=>((mask>>>i)&1));
      let c5count=0,t5count=0;
      enumLabels(n,f=>{
        let ok=edges.every(([u,v])=>edge5(f[u],f[v]));
        if(ok)c5count++;
        let extensions=1;
        for(let [u,v] of edges) extensions*=two(f[u],f[v])*two(f[v],f[u]);
        t5count+=extensions;
        baseAssignments++;
      });
      if(t5count!==2**edges.length*c5count)throw Error("total-count mismatch");
      graphs++;
    }
  }
  let sample={};
  for(let s=1;s<=4;s++)for(let t=1;t<=4;t++){
    let count=0;
    enumLabels(s+t,f=>{
      let valid=true;
      for(let u=0;u<s&&valid;u++)for(let v=s;v<s+t;v++)if(!edge5(f[u],f[v])){valid=false;break;}
      if(valid)count++;
    });
    let closed=5*(2**s+2**t-2);
    if(count!==closed)throw Error("Kst closed form");
    let t5=2**(s*t)*count;
    if(t5!==2**(s*t)*closed)throw Error("expanded Kst count");
    sample[`${s}x${t}`]=t5;
    kst++;
  }
  return {revision:"tmr5-t5-independent-v8-072-v1",seed:null,mode:"exhaustive",
    endpointPairs:pairs,simpleGraphsNle4:graphs,sourceLabelings:baseAssignments,
    bipartiteCases:kst, expandedCounts:sample, failures:0,
    exactFormula:"#Hom(D(K_s,t),T5)=2^(s*t)*5*(2^s+2^t-2)"};
}
if (typeof console !== 'undefined') console.log(JSON.stringify(run(),null,2));
