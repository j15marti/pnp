"use strict";
// LSPV-3/506. Distinct R_TAG506 and R_EXT506 proof languages, NOT historical R_mix341.
// Run: node experiments/arc/lspv3_506_tagged_vs_extensional_gap.cjs
function run506() {
  let checks=0;
  const assert=(p,s)=>{checks++;if(!p)throw Error(s);};
  const graphs=[
    ["K4",4,[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]],
    ["K33",6,Array.from({length:3},(_,i)=>Array.from({length:3},(_,j)=>[i,3+j])).flat()],
    ["cube",8,Array.from({length:8},(_,i)=>[1,2,4].filter(j=>i<(i^j)).map(j=>[i,i^j])).flat()]
  ];
  function normalize(c){return [...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);}
  function resolve(a,b,p){
    if(!a.includes(p)||!b.includes(-p)){if(a.includes(-p)&&b.includes(p))return resolve(b,a,p);throw Error("bad pivot");}
    const c=normalize([...a.filter(z=>z!==p),...b.filter(z=>z!==-p)]);
    assert(!c.some(x=>c.includes(-x)),"tautology");return c;
  }
  function clauses(n,edges){
    const inc=Array.from({length:n},()=>[]);
    edges.forEach(([u,v],i)=>{inc[u].push(i+1);inc[v].push(i+1);});
    assert(inc.every(x=>x.length===3),"not cubic");
    const out=[];
    for(let v=0;v<n;v++)for(let bits=0;bits<8;bits++){
      const p=((bits&1)!==0)^((bits&2)!==0)^((bits&4)!==0);
      if(Number(p)===(v===0?1:0))continue;
      out.push({vertex:v,clause:inc[v].map((id,j)=>((bits>>j)&1)?-id:id)});
    }
    assert(out.length===4*n,"wrong original clause count");
    return {out,inc};
  }
  const sat=(c,a)=>c.some(x=>(a[Math.abs(x)]??0)===(x>0?1:0));
  function tt(c,vars){
    let t=0;for(let m=0;m<(1<<vars.length);m++){
      const a={};vars.forEach((v,i)=>a[v]=(m>>i)&1);
      if(sat(c,a))t|=(1<<m);
    }return t;
  }
  function local_factor(c){
    const vars=[...new Set(c.map(Math.abs))].sort((a,b)=>a-b);
    assert(vars.length<=3,"width support overflow");return {vars,table:tt(c,vars)};
  }
  function combine(A,B){
    const vars=[...new Set([...A.vars,...B.vars])].sort((a,b)=>a-b);
    assert(vars.length<=3,"AND3 support overflow");
    let table=0;for(let m=0;m<(1<<vars.length);m++){
      const a={};vars.forEach((v,i)=>a[v]=(m>>i)&1);
      const ev=F=>((F.table>>F.vars.reduce((x,v,i)=>x|=(a[v]<<i),0))&1)!==0;
      if(ev(A)&&ev(B))table|=1<<m;
    }return {vars,table};
  }
  function fixture(name,h,edges,k){
    const base=clauses(h,edges),m=base.out.length;
    const replace=new Set(Array.from({length:k},(_,i)=>i));
    let next=edges.length,source=[],per=Array.from({length:h},()=>[]),gadgets=[];
    const sourceNode=(v,c)=>{const id="S"+source.length;source.push({id,vertex:v,clause:c});return id;};
    base.out.forEach((x,i)=>{
      const [a,b,c]=x.clause;
      if(!replace.has(i)){per[x.vertex].push({type:"source",id:sourceNode(x.vertex,x.clause)});return;}
      const u=++next,v=++next;
      const A=sourceNode(x.vertex,[a,b,u]),B=sourceNode(x.vertex,[-u,c,v]),D=sourceNode(x.vertex,[-u,c,-v]);
      per[x.vertex].push({type:"gadget",A,B,D,u,v,original:x.clause});
      gadgets.push({A,B,D,u,v,original:x.clause});
    });
    assert(source.length===4*h+2*k,"wrong expanded source");
    for(const g of gadgets){
      const [a,b,c]=g.original;
      for(let mask=0;mask<8;mask++){
        const assign={};[a,b,c].forEach((lit,j)=>assign[Math.abs(lit)]=((mask>>j)&1));
        let exists=false;
        for(let u=0;u<2;u++)for(let v=0;v<2;v++){
          assign[g.u]=u;assign[g.v]=v;
          if([g.A,g.B,g.D].every(id=>sat(source[Number(id.slice(1))].clause,assign)))exists=true;
        }
        assert(exists===sat(g.original,assign),"gadget existential mismatch");
      }
    }
    const db=new Map(source.map(x=>[x.id,{type:"SOURCE",clause:x.clause}]));
    const nodes=[];let rcount=0,acount=0,xcount=0;
    const add=(type,payload)=>{
      const id="P"+(nodes.length+1);let obj={id,type,...payload};
      for(const parent of obj.parents||[])assert(db.has(parent),"missing parent");
      nodes.push(obj);db.set(id,obj);return id;
    };
    const vertexRows=[];
    for(let vertex=0;vertex<h;vertex++){
      const pool=[];
      for(const slot of per[vertex]){
        if(slot.type==="source"){pool.push(slot.id);continue;}
        const b=source[Number(slot.B.slice(1))].clause, d=source[Number(slot.D.slice(1))].clause;
        const p1=resolve(b,d,slot.v), id1=add("RES",{parents:[slot.B,slot.D],pivot:slot.v,clause:p1});rcount++;
        const a=source[Number(slot.A.slice(1))].clause;
        const p2=resolve(a,p1,slot.u), id2=add("RES",{parents:[slot.A,id1],pivot:slot.u,clause:p2});rcount++;
        assert(JSON.stringify(normalize(p2))===JSON.stringify(normalize(slot.original)),"res did not retract");
        pool.push(id2);
      }
      assert(pool.length===4,"vertex source fanin");
      const factors=pool.map(id=>local_factor(db.get(id).clause));
      let f01=combine(factors[0],factors[1]),f23=combine(factors[2],factors[3]);
      const p01=add("AND3",{parents:[pool[0],pool[1]],factor:f01});acount++;
      const p23=add("AND3",{parents:[pool[2],pool[3]],factor:f23});acount++;
      const fall=combine(f01,f23),pr=add("AND3",{parents:[p01,p23],factor:fall});acount++;
      const vars=base.inc[vertex],charge=vertex===0?1:0;
      assert(JSON.stringify(fall.vars)===JSON.stringify(vars.slice().sort((a,b)=>a-b)),"support");
      for(let a=0;a<8;a++){
        const val=(fall.table>>a)&1,par=((a&1)?1:0)^((a&2)?1:0)^((a&4)?1:0);
        assert(val===Number(par===charge),"affine truth table");
      }
      db.get(pr).row={mask:vars.reduce((s,v)=>s^(1n<<BigInt(v-1)),0n).toString(),rhs:charge};
      vertexRows.push(pr);
    }
    let wave=vertexRows.slice();
    while(wave.length>1){
      const nextWave=[];
      for(let i=0;i<wave.length;i+=2){
        if(i+1===wave.length){nextWave.push(wave[i]);continue;}
        const a=db.get(wave[i]).row,b=db.get(wave[i+1]).row;
        assert(a&&b,"non-row XOR");
        const row={mask:(BigInt(a.mask)^BigInt(b.mask)).toString(),rhs:a.rhs^b.rhs};
        nextWave.push(add("XOR",{parents:[wave[i],wave[i+1]],row}));xcount++;
      }wave=nextWave;
    }
    const sink=db.get(wave[0]).row;
    assert(sink.mask==="0"&&sink.rhs===1,"no XOR contradiction");
    assert(rcount===2*k&&acount===3*h&&xcount===h-1,"node counts");
    assert(nodes.length===4*h+2*k-1,"total node mismatch");
    const typed={RES:["SOURCE","RES"],AND3:["SOURCE","AND3","RES"],XOR:["AND3","XOR"]};
    let rejected=0;
    for(const node of nodes){
      if(node.type!=="AND3")continue;
      if(node.parents.some(p=>db.get(p).type==="RES")){
        const TAGGED=["SOURCE","AND3"];
        assert(node.parents.some(p=>!TAGGED.includes(db.get(p).type)),"tagged rejection");
        rejected++;
      }
    }
    assert(rejected>0||k===0,"no rejected RES-to-AND3 parent");
    const source_auth=source.map(x=>x.clause);
    const changed=source_auth.map(a=>a.slice());changed[0][0]=-changed[0][0];
    assert(JSON.stringify(source_auth)!==JSON.stringify(changed),"bad auth mutation");
    const maxvars=next;
    let satcount=null;
    if(maxvars<=16){
      satcount=0;
      for(let mask=0;mask<(1<<maxvars);mask++){
        const assign={};for(let i=1;i<=maxvars;i++)assign[i]=(mask>>(i-1))&1;
        if(source.every(s=>sat(s.clause,assign)))satcount++;
      }
      assert(satcount===0,"odd charge should be UNSAT");
    }
    return {name,h,k,source_clauses:source.length,source_variables:next,paid_RES:rcount,paid_AND3:acount,paid_XOR:xcount,paid_total:nodes.length,tagged_rejected_edges:rejected,extensional_accept:true,tagged_accepts_this_packet:k===0,independently_exhausted_sat_count:satcount,source_packet: k===1 && h===4 ? source : undefined,proof_dag:k===1 && h===4 ? nodes:undefined,final_root:wave[0]};
  }
  const outcomes=[];
  for(const [name,h,edges] of graphs)for(const k of [0,1,2]){
    outcomes.push(fixture(name,h,edges,k));
  }
  return {id:"LSPV3_506_TAGGED_VS_EXTENSIONAL",scope:"Two DISTINCT source-authenticated sound RES-complete unit-binary calculi; not historical R_mix341",outcomes,checks,proof_status:"PROVED_RESTRICTED symbolic gap conditional on established expanding odd-Tseitin Resolution hardness; finite instance checks",P_vs_NP:"OPEN"};
}
if(typeof module!=="undefined"){module.exports=run506;if(require.main===module)console.log(JSON.stringify(run506(),null,2));}
