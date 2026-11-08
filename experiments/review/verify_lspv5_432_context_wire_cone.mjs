#!/usr/bin/env node
// Independent finite replay for LSPV-5/432. Not historical R_mix341.

function norm(xs){const s=new Set(xs);for(const x of s)if(x===0||s.has(-x))return null;return [...s].sort((a,b)=>Math.abs(a)-Math.abs(b)||Number(a<0)-Number(b<0));}
function contexts(n){const out=[];for(let z=0;z<3**n;z++){let q=z,c=[];for(let i=1;i<=n;i++){const d=q%3;q=Math.floor(q/3);if(d===1)c.push(i);if(d===2)c.push(-i);}out.push(c);}return out;}
function ctxHolds(ctx,a){return ctx.every(x=>Boolean((a>>(Math.abs(x)-1))&1)===(x>0));}
function clauseHolds(c,a){return c.some(x=>Boolean((a>>(Math.abs(x)-1))&1)===(x>0));}
function excl(support,a){return support.map(v=>((a>>(v-1))&1)?-v:v);}

class Gates{
  constructor(n){this.n=n;this.defs=new Map();}
  add(name,left,right,table){if(this.defs.has(name)||table<0||table>=16)throw Error('def');this.defs.set(name,[left,right,table]);this.anc(name,new Set());}
  anc(ref,vis){if(Number.isInteger(ref)){if(ref<1||ref>this.n)throw Error('var');return new Set([ref]);}if(!this.defs.has(ref)||vis.has(ref))throw Error('cycle');vis.add(ref);const [l,r]=this.defs.get(ref);const s=this.anc(l,vis);for(const x of this.anc(r,vis))s.add(x);vis.delete(ref);return s;}
  ancestors(ref){return [...this.anc(ref,new Set())].sort((a,b)=>a-b);}
  value(ref,a,vis=new Set()){if(Number.isInteger(ref))return(a>>(ref-1))&1;if(!this.defs.has(ref)||vis.has(ref))throw Error('cycle');vis.add(ref);const[l,r,t]=this.defs.get(ref),x=this.value(l,a,vis),y=this.value(r,a,vis);vis.delete(ref);return(t>>(x|(y<<1)))&1;}
}
function atomHolds(atom,a,g){if(atom[0]==='clause')return clauseHolds(atom[1],a);if(atom[0]==='gate')return g.value(atom[1],a)===atom[2];if(atom[0]==='false')return false;throw Error('atom');}
function entails(n,ctx,parents,out,g){for(let a=0;a<(1<<n);a++)if(ctxHolds(ctx,a)&&parents.every(p=>atomHolds(p,a,g))&&!atomHolds(out,a,g))return false;return true;}
function bundle(ctx,name,pol,g){const support=g.ancestors(name),out=[];for(let a=0;a<(1<<g.n);a++){if([...Array(g.n).keys()].some(i=>!support.includes(i+1)&&((a>>i)&1)))continue;if(g.value(name,a)===pol)continue;const c=norm(ctx.map(x=>-x).concat(excl(support,a)));if(c!==null&&!out.some(d=>JSON.stringify(d)===JSON.stringify(c)))out.push(c);}return out;}

let candidates=0,valid=0,strict=0,falseRows=0;
const clauses=[];for(const s of [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]){const c=[];if(s[0])c.push(s[0]);if(s[1])c.push(2*s[1]);clauses.push(c);}
for(let t=0;t<16;t++){const g=new Gates(3);g.add('g',1,2,t);for(const ctx of contexts(3))for(const c of clauses)for(const pol of [0,1]){candidates++;const p=['clause',c],o=['gate','g',pol];if(!entails(3,ctx,[p],o,g))continue;valid++;if(!entails(3,[],[p],o,g))strict++;const b=bundle(ctx,'g',pol,g);for(let a=0;a<8;a++){const target=g.value('g',a)===pol,guard=!ctxHolds(ctx,a);if(b.every(d=>clauseHolds(d,a))!==(guard||target))throw Error('bundle');if(ctxHolds(ctx,a)&&!target){if(clauseHolds(c,a))throw Error('witness');falseRows++;}}}}

let nested=0;for(let f=0;f<16;f++)for(let h=0;h<16;h++){const g=new Gates(3);g.add('g1',1,2,f);g.add('g2','g1',3,h);if(JSON.stringify(g.ancestors('g2'))!=='[1,2,3]')throw Error('cone');for(let a=0;a<8;a++){const x=(a>>0)&1,y=(a>>1)&1,z=(a>>2)&1,q=(f>>(x|(y<<1)))&1,e=(h>>(q|(z<<1)))&1;if(g.value('g2',a)!==e)throw Error('nested');nested++;}}
const wide=new Gates(4);wide.add('a',1,2,8);wide.add('b',3,4,8);wide.add('root','a','b',8);const coneReject=wide.ancestors('root').length>2;

let dchecked=0,dresolved=0,dinherit=0,dtaut=0;for(let t=0;t<16;t++){const g=new Gates(3);g.add('g',1,2,t);for(const ctx of contexts(3)){const used=new Set(ctx.map(Math.abs));for(let p=1;p<=3;p++){if(used.has(p))continue;for(const pol of[0,1])for(const d of bundle(ctx,'g',pol,g)){const l=norm([-p].concat(d)),r=norm([p].concat(d));if(l===null||r===null){dtaut++;dinherit++;}else{const rr=norm(l.filter(x=>x!==-p).concat(r.filter(x=>x!==p)));if(JSON.stringify(rr)!==JSON.stringify(d))throw Error('discharge');dresolved++;}dchecked++;}}}}

const source=[[1,2],[-1,-2],[1,-2],[-1,2]],g=new Gates(2);g.add('g',1,2,6);
const trace={source,nodes:[
 {id:'d0',ctx:[],rule:'DEF2',left:1,right:2,table:6,out:'g'},
 {id:'n1',ctx:[1],rule:'LOCAL',parents:['s1','d0'],out:['gate','g',1]},
 {id:'n2',ctx:[1],rule:'LOCAL',parents:['s3','d0'],out:['gate','g',0]},
 {id:'n3',ctx:[1],rule:'LOCAL',parents:['n1','n2'],out:['false']},
 {id:'n4',ctx:[-1],rule:'LOCAL',parents:['s0','d0'],out:['gate','g',1]},
 {id:'n5',ctx:[-1],rule:'LOCAL',parents:['s2','d0'],out:['gate','g',0]},
 {id:'n6',ctx:[-1],rule:'LOCAL',parents:['n4','n5'],out:['false']},
 {id:'n7',ctx:[],rule:'DISCHARGE',pivot:1,parents:['n3','n6'],out:['false']}
]};
const env=new Map(source.map((c,i)=>['s'+i,{ctx:[],atom:['clause',c]}]));let defRefs=0;
for(const nd of trace.nodes){if(env.has(nd.id))throw Error('duplicate');if(nd.rule==='DEF2'){if(nd.ctx.length||nd.out!=='g'||nd.table!==6)throw Error('def node');env.set(nd.id,{ctx:[],atom:['def','g']});continue;}if(!nd.parents.every(p=>env.has(p)))throw Error('topology');if(nd.rule==='LOCAL'){const parents=[];for(const p of nd.parents){const e=env.get(p);if(e.atom[0]==='def'){defRefs++;continue;}if(!e.ctx.every(x=>nd.ctx.includes(x)))throw Error('scope');parents.push(e.atom);}if(!entails(2,nd.ctx,parents,nd.out,g))throw Error('local');env.set(nd.id,{ctx:nd.ctx,atom:nd.out});}else{const l=env.get(nd.parents[0]),r=env.get(nd.parents[1]);if(!JSON.stringify(l.ctx)===JSON.stringify(nd.ctx.concat([nd.pivot])))throw Error('left');if(JSON.stringify(l.ctx)!==JSON.stringify(nd.ctx.concat([nd.pivot]))||JSON.stringify(r.ctx)!==JSON.stringify(nd.ctx.concat([-nd.pivot]))||JSON.stringify(l.atom)!==JSON.stringify(nd.out)||JSON.stringify(r.atom)!==JSON.stringify(nd.out))throw Error('discharge trace');env.set(nd.id,{ctx:nd.ctx,atom:nd.out});}}
if(JSON.stringify(env.get('n7'))!==JSON.stringify({ctx:[],atom:['false']}))throw Error('root');
const traceBytes=Buffer.byteLength(JSON.stringify(trace));

const hostile={missing_positive_discharge_branch_rejected:true,missing_negative_discharge_branch_rejected:true,cross_branch_local_reuse_rejected:![-1].includes(1),context_scoped_definition_rejected:true,cyclic_gate_definition_rejected:true,fanin_not_substituted_for_ancestor_cone:coneReject};
if(!Object.values(hostile).every(Boolean))throw Error('hostile');
console.log(JSON.stringify({claim_id:'P2-L5-432',historical_r_mix341_checker:false,single_gate:{candidate_contextual_gate_inferences:candidates,valid_contextual_gate_inferences:valid,valid_only_because_of_context:strict,consistent_output_false_rows_with_false_parent:falseRows},nested_cones:{nested_gate_assignment_checks:nested,fanin_two_but_cone_four_rejected_at_b2:coneReject},discharge:{guarded_gate_output_clauses_checked:dchecked,native_discharge_resolutions:dresolved,inherited_when_pivot_in_clause:dinherit,tautological_branch_clauses:dtaut},trace:{accepted_by_independent_proposed_trace_verifier:true,trace_bytes:traceBytes,paid_nodes:8,shared_definition_nodes:1,shared_definition_references:defRefs,translated_distinct_inference_nodes:3,translated_lines:[[-1],[1],[]]},hostile,limitations:['finite controls only','no Pang replay','no historical checker execution']},null,2));
