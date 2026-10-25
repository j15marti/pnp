// ARC-GRID-LOCAL-ACCESS117 deterministic finite both-label nested-source reproducer.
// Run: node <this_file> [results.json]. No dependencies beyond Node.js.
// Counter fields are abstract bit events, not FLMV TM steps/hardware flips.
function runExperiment(){
  const assert=(x,msg)=>{if(!x)throw new Error(msg||"assertion failure");};
  let assertions=0;
  const check=(x,msg)=>{assert(x,msg);assertions++;};
  const W=v=>Math.ceil(Math.log2(v+1));
  const num=z=>{let b=z.toString(2);return "1".repeat(b.length)+"0"+b;};
  const header=(v,n)=>"10011010"+num(v)+num(n);
  const encode=(v,cs)=>{let w=W(v);return header(v,cs.length)+cs.map(c=>c.map(l=>(l<0?"1":"0")+Math.abs(l).toString(2).padStart(w,"0")).join("")).join("");};
  function decode(bits){
    assert(bits.slice(0,8)==="10011010");let at=8;
    const integer=()=>{let k=0;while(bits[at+k]==="1")k++;assert(bits[at+k]==="0");let value=parseInt(bits.slice(at+k+1,at+2*k+1),2);at+=2*k+1;return value;};
    const v=integer(),n=integer(),w=W(v);
    assert(bits.length===at+3*n*(w+1));
    const clauses=[];for(let i=0;i<n;i++){let c=[];for(let j=0;j<3;j++){let sign=bits[at++],id=parseInt(bits.slice(at,at+w),2);at+=w;assert(id>=1&&id<=v);c.push(sign==="1"?-id:id);}assert(new Set(c.map(Math.abs)).size===3);clauses.push(c);}
    return clauses;
  }
  function satisfiable(cs){
    function recur(asgn){
      while(true){
        let fresh=false,pivot=0;
        for(const clause of cs){let accept=false,unassigned=[];
          for(const lit of clause){const got=asgn.get(Math.abs(lit));if(got===undefined)unassigned.push(lit);else if(got===(lit>0)){accept=true;break;}}
          if(accept)continue;if(!unassigned.length)return false;
          if(unassigned.length===1){let lit=unassigned[0],id=Math.abs(lit),bit=lit>0;if(asgn.has(id)&&asgn.get(id)!==bit)return false;if(!asgn.has(id)){asgn.set(id,bit);fresh=true;}}
          else if(!pivot)pivot=Math.abs(unassigned[0]);
        }
        if(fresh)continue;if(!pivot)return true;
        let yes=new Map(asgn);yes.set(pivot,true);if(recur(yes))return true;
        let no=new Map(asgn);no.set(pivot,false);return recur(no);
      }
    }
    return recur(new Map());
  }
  function componentSAT(cs){
    let parent=new Map();
    function root(x){if(!parent.has(x))parent.set(x,x);if(parent.get(x)!==x)parent.set(x,root(parent.get(x)));return parent.get(x);}
    function join(x,y){x=root(x);y=root(y);if(x!==y)parent.set(x,y);}
    for(const c of cs){join(Math.abs(c[0]),Math.abs(c[1]));join(Math.abs(c[1]),Math.abs(c[2]));}
    let groups=new Map();for(const c of cs){let k=root(Math.abs(c[0]));if(!groups.has(k))groups.set(k,[]);groups.get(k).push(c);}
    return [...groups.values()].every(satisfiable);
  }
  function packet(p,kind){
    const all=[];for(let a=0;a<8;a++)all.push([(a&1)?-1:1,(a&2)?-2:2,(a&4)?-3:3]);
    const table={yes:[[1,2,3]],horn:[[-1,-2,3]],two:[[1,2,3],[1,2,-3]],xor:[[1,2,-3],[1,-2,3],[-1,2,3],[-1,-2,-3]],no:all};
    let s=table[kind];assert(p>=s.length);return Array.from({length:p},(_,k)=>s[k%s.length].slice());
  }
  function make(m,pattern){
    let p=m*m,q=m,v=3*p,V=q*q*v,all=[],grid=[];
    for(let i=0;i<q;i++){let row=[];for(let j=0;j<q;j++){let k=i*q+j,type="yes";
      if((pattern==="firstNo"&&k===0)||(pattern==="lastNo"&&k===q*q-1)||(pattern==="manyNo"&&k%3===0))type="no";
      if(pattern==="mix")type=["yes","horn","xor","two"][k%4];
      let cs=packet(p,type);row.push(cs);for(const c of cs)all.push(c.map(z=>Math.sign(z)*(Math.abs(z)+k*v)));
    }grid.push(row);}
    return {m,p,q,v,V,grid,all,bits:encode(V,all),pattern};
  }
  function oracle(F){
    const w0=W(F.V),h0=header(F.V,F.all.length).length,w1=W(F.q*F.v),h1=header(F.q*F.v,F.q*F.p).length,w2=W(F.v);
    let sourceReads=0,workspaceReads=0,workspaceWrites=0,unchangedWrites=0,realFlips=0,logicalBitOps=0,peakScratch=0;
    let tape=new Array(128).fill(0);
    const source=i=>{assert(i>=0&&i<F.bits.length);sourceReads++;return F.bits[i];};
    function scratch(id,value){const w=Math.max(1,2*w0);for(let z=0;z<w;z++){let at=(id*w+z)%128,b=Math.floor(value/2**z)%2;workspaceReads++;workspaceWrites++;if(tape[at]===b)unchangedWrites++;else realFlips++;tape[at]=b;peakScratch=Math.max(peakScratch,at+1);}logicalBitOps+=w*w;}
    function literal(c,k){let base=h0+(c*3+k)*(1+w0),sign=source(base)==="1",id=0;for(let z=0;z<w0;z++)id=id*2+Number(source(base+1+z));scratch(0,id);return sign?-id:id;}
    function bit(i,j,k){let row=j===null,v=row?F.q*F.v:F.v,n=row?F.q*F.p:F.p,w=row?w1:w2,h=header(v,n);
      assert(k>=0&&k<h.length+3*n*(w+1));if(k<h.length){scratch(1,k);return h[k];}
      let off=k-h.length,which=Math.floor(off/(w+1)),place=off%(w+1),clause=Math.floor(which/3),col=which%3;
      const block=row?i*F.q: i*F.q+j,sourceClause=row?i*F.q*F.p+clause:block*F.p+clause;
      let lit=literal(sourceClause,col);if(place===0)return lit<0?"1":"0";
      let value=Math.abs(lit)-block*F.v;scratch(2,value);assert(value>=1&&value<=v);return value.toString(2).padStart(w,"0")[place-1];
    }
    function nested(i,j,k){let h=header(F.v,F.p),w=w2;if(k<h.length){scratch(3,k);return h[k];}
      let off=k-h.length,which=Math.floor(off/(w+1)),place=off%(w+1),clause=Math.floor(which/3),col=which%3;
      let base=h1+((j*F.p+clause)*3+col)*(w1+1);if(!place)return bit(i,null,base);
      let rowid=0;for(let z=0;z<w1;z++)rowid=rowid*2+Number(bit(i,null,base+1+z));
      let local=rowid-j*F.v;scratch(3,local);assert(local>=1&&local<=F.v);
      return local.toString(2).padStart(w,"0")[place-1];
    }
    function scan(){for(let i=0;i<F.bits.length;i++)source(i);}
    function counts(){return {sourceReads,workspaceReads,workspaceWrites,unchangedWrites,realFlips,logicalBitOps,peakScratch};}
    return {bit,nested,scan,counts};
  }
  let results=[];
  for(const m of [3,4,5])for(const pattern of ["allYes","firstNo","lastNo","manyNo","mix"]){
    const F=make(m,pattern),A=oracle(F);check(JSON.stringify(decode(F.bits))===JSON.stringify(F.all),"root serialization");A.scan();
    let labels=[],leafProbes=0,rowProbes=0,L1=0,L2=0;
    for(let i=0;i<F.q;i++){
      let clauses=[];for(let j=0;j<F.q;j++)for(const c of F.grid[i][j])clauses.push(c.map(z=>Math.sign(z)*(Math.abs(z)+j*F.v)));
      let row=encode(F.q*F.v,clauses);L1=row.length;check(JSON.stringify(decode(row))===JSON.stringify(clauses),"row serialization");
      for(let k=0;k<row.length;k++){check(A.bit(i,null,k)===row[k],`row ${m}/${pattern}/${i}/${k}`);rowProbes++;}
      let rowLabel=true;
      for(let j=0;j<F.q;j++){
        let leaf=encode(F.v,F.grid[i][j]);L2=leaf.length;check(JSON.stringify(decode(leaf))===JSON.stringify(F.grid[i][j]),"leaf serialization");
        for(let k=0;k<leaf.length;k++){check(A.bit(i,j,k)===leaf[k],`direct ${i}/${j}/${k}`);check(A.nested(i,j,k)===leaf[k],`nested ${i}/${j}/${k}`);leafProbes+=2;}
        let label=satisfiable(F.grid[i][j]);rowLabel=rowLabel&&label;check(label===satisfiable(decode(leaf)),"leaf truth");
      }
      check(rowLabel===componentSAT(clauses),"row truth");labels.push(rowLabel);
    }
    let rootLabel=componentSAT(F.all);check(rootLabel===labels.every(Boolean),"root truth");
    results.push({m,p:F.p,q:F.q,pattern,N:F.bits.length,L1,L2,SAT:rootLabel,rowSAT:labels,rowProbes,leafProbes,counts:A.counts()});
  }
  let totals={sourceReads:0,workspaceWrites:0,unchangedWrites:0,realFlips:0,rowProbes:0,leafProbes:0};
  for(const r of results)for(const k of Object.keys(totals))totals[k]+=r.counts[k]??r[k];
  return {run:"ARC-GRID-LOCAL-ACCESS117",generatedAt:"2026-10-25T11:36:00Z",experimentScope:"15 deterministic finite proper 3CNF grid sources; every row and leaf bit; direct and nested byte-oracles; all SAT/UNSAT outcomes",modelCaution:"instrumented abstract bit events; neither an FLMV tape trace nor a proof for all SAT",seed:null,exhaustiveWithinDeclaredCases:true,assertions,failures:0,totals,maxPeakScratch:Math.max(...results.map(r=>r.counts.peakScratch)),results};
}
const result=runExperiment();
const fs=require('fs');
const out=process.argv[2]||'ARC_GRID_LOCAL_ACCESS117_results.json';
fs.writeFileSync(out,JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({assertions:result.assertions,cases:result.results.length,totals:result.totals,raw:out},null,2));
