#!/usr/bin/env node
'use strict';
/* LSPV-2/540: native /341 JSON lexical aliasing. NOT full R_mix341. Run:
   node experiments/arc/lspv2_540_json_shadow_native.cjs [output.json]
   The separate duplicate-key scanner is NOT the original parser. */
const fs=require('fs'), crypto=require('crypto');
const pins={producer:'4081022e8a3841d79f751a3d3a7a10decbb026da',checker:'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0'};
const paths={producer:'experiments/arc/lspv2_341_mixed_tseitin_min_dag.js',checker:'experiments/arc/lspv2_341_independent_verify.js'};
function need(v,m){if(!v)throw Error('540: '+m)}
function digest(x,alg='sha256'){return crypto.createHash(alg).update(x,'utf8').digest('hex')}
function blob(s){return digest('blob '+Buffer.byteLength(s)+'\0'+s,'sha1')}
/* Complete JSON token walk for detecting lexically repeated decoded object keys.
   Uses JSON.parse for exact string escape validation; arbitrary nesting limited
   by JS call stack. A rejected native packet is not excluded from full calculus. */
function scanJSON(s){
 let i=0,duplicates=[],keyCount=0;
 function ws(){while(/[ \r\n\t]/.test(s[i]||'\0'))i++}
 function take(c){need(s[i]===c,'expected '+c+' at '+i);i++}
 function str(){
   ws();need(s[i]==='"','expected string');let j=i++;
   while(i<s.length){let c=s[i++];
     if(c==='"')return JSON.parse(s.slice(j,i));
     if(c==='\\'){need(i<s.length,'truncated escape');let e=s[i++];if(e==='u')i+=4;}
   }
   throw Error('unterminated string');
 }
 function val(){
   ws();
   if(s[i]==='{'){
     i++;ws();let seen=new Set();
     if(s[i]==='}')i++;
     else while(true){
       let j=i,k=str();keyCount++;
       if(seen.has(k))duplicates.push({decodedKey:k,offset:j});
       seen.add(k);ws();take(':');val();ws();
       if(s[i]==='}'){i++;break;}take(',');
     }
   }else if(s[i]==='['){
     i++;ws();if(s[i]===']')i++;
     else while(true){val();ws();if(s[i]===']'){i++;break;}take(',');}
   }else if(s[i]==='"')str();
   else{
     let m=/^(?:true|false|null|-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?)/.exec(s.slice(i));
     need(m,'invalid scalar at '+i);i+=m[0].length;
   }
 }
 val();ws();need(i===s.length,'trailing text');JSON.parse(s);
 return {duplicates,keyCount};
}
function historical(checker,packet){
 let logs=[];try{
  new Function('require','process','console',checker)(
   ()=>({readFileSync:()=>packet}),{argv:['node','341','candidate.json']},{log:x=>logs.push(x)});
  return {accepted:true,checks:JSON.parse(logs[0]).checks};
 }catch(e){return {accepted:false,diagnostic:String(e).slice(0,130)};}
}
function cases(f){
 let good=JSON.stringify([f]),bad='[{"graph":{},"clauses":[],"proof":[]}]';
 let b=JSON.stringify({fixtures:[f],summary:[null]});
 let repl=(rx,cb)=>{need(rx.test(b),'missing mutation anchor');return b.replace(rx,cb)};
 return [
  ['BASE',b,true,false],
  ['ROOT_DUP_BAD_GOOD','{"fixtures":'+bad+',"fixtures":'+good+',"summary":[null]}',true,true],
  ['ROOT_DUP_GOOD_BAD','{"fixtures":'+good+',"fixtures":'+bad+',"summary":[null]}',false,true],
  ['ROOT_ESCAPED_KEY',b.replace('"fixtures"','"fixt\\u0075res"'),true,false],
  ['SOURCE_ESCAPED_KEY',b.replace('"literals"','"literal\\u0073"'),true,false],
  ['SOURCE_ESCAPED_ID',b.replace('"id":"s0"','"id":"s\\u0030"'),true,false],
  ['EXPONENT_LITERAL',repl(/"literals":\[(-?\d+)/,(x,n)=>'"literals":['+n+'e0'),true,false],
  ['PARENT_DUP_BAD_GOOD',repl(/"parents":(\[[^\]]*\])/,(x,g)=>'"parents":["bad","bad"],"parents":'+g),true,true],
  ['PARENT_DUP_GOOD_BAD',repl(/"parents":(\[[^\]]*\])/,(x,g)=>'"parents":'+g+',"parents":["bad","bad"]'),false,true],
  ['SOURCE_DUP_BAD_GOOD',repl(/"literals":(\[[^\]]*\])/,(x,g)=>'"literals":[1000,1001,1002],"literals":'+g),true,true],
  ['ROOT_DUP_ESCAPED_BAD_GOOD','{"fixt\\u0075res":'+bad+',"fixtures":'+good+',"summary":[null]}',true,true],
  ['WHITESPACE',b+' \r\n\t',true,false],
  ['INVALID_TRAILING',b+' true',false,null],
  ['INVALID_TRUNCATION',b.slice(0,-1),false,null]
 ];
}
function audit(producer,checker){
 need(blob(producer)===pins.producer,'producer changed');
 need(blob(checker)===pins.checker,'checker changed');
 let out=[];new Function('console',producer)({log:s=>out.push(s)});
 let original=JSON.parse(out[0]),all=historical(checker,JSON.stringify(original));
 need(all.accepted&&all.checks===30714,'seven-fixture control');
 let f=original.fixtures[0],controls=cases(f),canon=JSON.stringify(JSON.parse(controls[0][1]));
 let rows=[];
 for(let [name,bytes,want,dup] of controls){
   let v=historical(checker,bytes);
   need(v.accepted===want,'native mismatch '+name+': '+JSON.stringify(v));
   let lex=null,semantic=null;
   try{lex=scanJSON(bytes);semantic=JSON.stringify(JSON.parse(bytes));}
   catch(e){need(dup===null,'unexpected JSON lexing error '+name+': '+e);}
   if(dup===null)need(lex===null,'malformed accepted by scanner '+name);
   else{
     need((lex.duplicates.length>0)===dup,'duplicate-key mismatch '+name);
     if(want)need(semantic===canon,'accepted alias changed parsed object '+name);
   }
   rows.push({id:name,accepted:v.accepted,checks:v.checks||null,diagnostic:v.diagnostic||null,
     duplicateKeys:lex?lex.duplicates:null,rawBytes:Buffer.byteLength(bytes),rawSHA256:digest(bytes),
     parsedSHA256:semantic?digest(semantic):null});
 }
 let source='p cnf '+f.graph.edges.length+' '+f.clauses.length+'\n'+
            f.clauses.map(c=>c.literals.join(' ')+' 0').join('\n')+'\n';
 return {id:'LSPV2-540-NATIVE-JSON-SHADOW',status:'COMPUTATIONAL; recovered fixture checker only',
   pinnedGitBlobs:pins,originalSourceSHA256:digest(source),
   originalSeven:all,K4:{sourceClauses:f.clauses.length,paidNodes:f.proof.length},
   totals:{cases:rows.length,accepted:rows.filter(x=>x.accepted).length,
           rejected:rows.filter(x=>!x.accepted).length,
           acceptedDuplicate:rows.filter(x=>x.accepted&&x.duplicateKeys&&x.duplicateKeys.length).length},
   cases:rows,conclusion:'JSON.parse last-key wins and decodes escaped names/IDs; first-key source scans do not authenticate parsed source. New duplicate-key filter rejects some ACTUALLY accepted bytes and cannot be used to prove native lower bounds.',
   limits:'No RES, DEF, LOCAL-CONVERT, context, branch or discharge authentication. Zero source-only cost assumed nowhere. No proof of P != NP.'};
}
module.exports={scanJSON,cases,historical,audit};
if(require.main===module){
 let prod=fs.readFileSync(paths.producer,'utf8'),ver=fs.readFileSync(paths.checker,'utf8');
 let out=JSON.stringify(audit(prod,ver),null,2)+'\n';
 if(process.argv[2])fs.writeFileSync(process.argv[2],out);else process.stdout.write(out);
}
