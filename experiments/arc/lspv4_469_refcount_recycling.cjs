/* LSPV-4/469. Reference-counted canonical address roots with physical slot recycling. Host-language finite checks only. */
function runLspv4_469(){
  "use strict";
  let checks=0,updates=0,creates=0,releases=0,lookups=0,peak=0,peakId=0;
  function ok(cond,msg){checks++;if(!cond)throw Error(msg)}
  class Intern {
    constructor(){this.nodes=new Map();this.unique=new Map();this.next=1;this.free=[];}
    z(d){return d===0?"b0":"z"+d;}
    hold(id){if(id[0]==="n")this.nodes.get(id).ref++;return id;}
    drop(id){
      if(id[0]!=="n")return;
      let n=this.nodes.get(id);ok(!!n,"dangling ref "+id);
      n.ref--;ok(n.ref>=0,"negative ref");
      if(n.ref!==0)return;
      this.nodes.delete(id);this.unique.delete(n.key);releases++;
      this.free.push(Number(id.slice(1)));
      this.drop(n.l);this.drop(n.r);
    }
    intern(d,l,r){
      if(l===this.z(d-1)&&r===this.z(d-1))return this.z(d);
      const key=d+":"+l+":"+r,old=this.unique.get(key);
      if(old){this.hold(old);return old;}
      const num=this.free.length?this.free.pop():this.next++;
      const id="n"+num;ok(!this.nodes.has(id),"reused still-live id");
      this.nodes.set(id,{d,l,r,key,ref:1});
      this.unique.set(key,id);this.hold(l);this.hold(r);creates++;
      peak=Math.max(peak,this.nodes.size);peakId=Math.max(peakId,num);
      ok(peakId<=peak,"physical highwater exceeds maximum live arena "+peakId+"/"+peak);
      return id;
    }
    children(id,d){
      if(id===this.z(d))return [this.z(d-1),this.z(d-1)];
      let n=this.nodes.get(id);ok(!!n&&n.d===d,"bad node depth");
      return [n.l,n.r];
    }
    bit(id,d,pos){
      lookups++;if(d===0)return id==="b1"?1:0;
      let [l,r]=this.children(id,d),half=2**(d-1);
      return pos<half?this.bit(l,d-1,pos):this.bit(r,d-1,pos-half);
    }
    put(id,d,pos,value){
      updates++;if(d===0)return value?"b1":"b0";
      const half=2**(d-1);
      let [l,r]=this.children(id,d);
      if(pos<half){
        let q=this.put(l,d-1,pos,value),out=this.intern(d,q,r);this.drop(q);return out;
      }
      let q=this.put(r,d-1,pos-half,value),out=this.intern(d,l,q);this.drop(q);return out;
    }
    extend(id,d){return this.intern(d+1,id,this.z(d));}
    make(value,d){
      let root=this.z(d),n=Number(value);
      for(let j=0;j<2**d;j++)if(Math.floor(n/2**j)%2===1){
        let v=this.put(root,d,j,1);this.drop(root);root=v;
      }
      return root;
    }
  }
  const gray=[];
  for(let r of [4,6,8,10,12]){
    const D=Math.ceil(Math.log2(r)),a=new Intern();let root=a.z(D),maximum=0,high=0;
    for(let i=0;i<2**r;i++){
      if(i){
        let j=Math.log2(i&-i),old=a.bit(root,D,j);
        let next=a.put(root,D,j,1-old);a.drop(root);root=next;
      }
      let expected=i^(i>>1),seen=0;
      for(let j=0;j<r;j++)seen+=a.bit(root,D,j)*2**j;
      ok(seen===expected,"Gray mismatch "+r+":"+i);
      maximum=Math.max(maximum,a.nodes.size);
      high=Math.max(high,a.next-1);
    }
    a.drop(root);ok(a.nodes.size===0,"gray leak "+r);
    ok(high<=maximum+8,"gray physical index leak "+r);
    gray.push({r,states:2**r,maximum_live_nodes:maximum,highest_node_id:high,final_nodes:a.nodes.size});
  }
  const a=new Intern();let d=6,work=new Map(),oracle=new Map(),maxWorkNodes=0,highWater=0;
  function make(v){return a.make(v,d)}
  for(let i=0;i<1100;i++){
    if(i===310||i===740){
      let replacement=new Map();
      for(let [old,val] of work){
        const fresh=a.extend(old,d);ok(!replacement.has(fresh),"expansion alias");replacement.set(fresh,val);a.drop(old);
      }
      work=replacement;d++;
    }
    const address=(i*73+i*i*17)%Math.min(2**d,256);
    let key=make(address),oldOracle=oracle.get(address)||0;
    ok((work.get(key)||0)===oldOracle,"work read alias "+i);
    if(i%7===0||i%11===0){
      let target=(i%11===0)?0:1;
      if(target){if(!work.has(key)){a.hold(key);work.set(key,1)}oracle.set(address,1);}
      else {if(work.has(key)){work.delete(key);a.drop(key)}oracle.delete(address);}
    }
    let route=make(address);ok(route===key,"independent route alias "+i);
    a.drop(route);a.drop(key);
    maxWorkNodes=Math.max(maxWorkNodes,a.nodes.size);highWater=Math.max(highWater,a.next-1);
    ok(a.nodes.size<40*(oracle.size+1),"retention bound "+i);
  }
  for(let key of work.keys())a.drop(key);
  ok(a.nodes.size===0,"work keys leak");
  const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],models=[];
  for(let odd of [false,true]){
    const chi=[odd?1:0,0,0,0],clauses=[];
    for(let v=0;v<4;v++){
      const ee=edges.map((e,k)=>e.includes(v)?k:-1).filter(x=>x>=0);
      for(let k=0;k<8;k++){
        if((Number(k.toString(2).replace(/0/g,"").length)%2)===chi[v])continue;
        clauses.push(ee.map((idx,j)=>((k>>j)&1)?-(idx+1):(idx+1)));
      }
    }
    ok(clauses.length===16,"Tseitin 3CNF clause count");
    for(let c of clauses)ok(c.length===3&&new Set(c.map(Math.abs)).size===3,"invalid source");
    let count=0;
    for(let assignment=0;assignment<64;assignment++){
      if(clauses.every(c=>c.some(l=>(((assignment>>(Math.abs(l)-1))&1)===Number(l>0)))))count++;
    }
    ok(count===(odd?0:8),"K4 charge control");
    models.push({odd_charge:odd,clauses:clauses.length,satisfying_assignments:count});
  }
  ok(new Set([1,1,2].map(Math.abs)).size!==3,"duplicate-literal malformed control");
  return {label:"COMPUTATIONAL; exact ref-count host-language checker, not native FLMV",
    gray,work:{operations:1100,capacity_final:2**d,maximum_live_nodes:maxWorkNodes,highest_node_id:highWater,final_nodes:a.nodes.size},
    tseitin:models,counters:{assertions:checks,updates,creates,releases,lookups,peak,peakId},
    caveat:"reference counting and physical slot recycling modeled abstractly; balanced unique table and machine instruction compilation unexecuted"};
}
console.log(JSON.stringify(runLspv4_469(),null,2));
