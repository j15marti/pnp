'use strict';
// TMR-1/057. Offline forensic validator for an authentic upstream GitHub Actions job log.
// Usage: node experiments/tmr/tmr1_pinned_ci_audit057.js <downloaded-upstream-log.txt>
// Source of data: Anthropic formal-math commit 16a5ce41304fcdaea4e0be7c132e1c361dc26da5,
// Actions job 121985557508, run 40442388505 (October 27, 2026).
// This validates public evidence, NOT a local Lean kernel execution or mathematical correctness.
const fs=require('fs');
const filename=process.argv[2];
if (!filename) { console.error('Usage: node tmr1_pinned_ci_audit057.js <job-log.txt>'); process.exit(2); }
const s=fs.readFileSync(filename,'utf8');
const lines=s.split(/\r?\n/);
const checks={
  source_commit_visible:s.includes('16a5ce41304fcdaea4e0be7c132e1c361dc26da5'),
  toolchain_lean_4_33_1:s.includes('Lean (version 4.33.1'),
  mainresults_built:/Built MainResults\b/.test(s),
  solution_built:/Built Solution\b/.test(s),
  comparator_two_declarations:s.includes('MainResults.ethIsFalse') && s.includes('MainResults.mainTheorem'),
  comparator_pass:s.includes('PASS comparator.json') && s.includes('All 1 comparator configuration(s) accepted.'),
  nanoda_accept:s.includes('nanoda kernel accepts the solution'),
  lean_default_accept:s.includes('Lean default kernel accepts the solution'),
  comparator_source_pin:s.includes('575674928e239f5bc452aab72d1dd7b0f1326494'),
  nanoda_source_pin:s.includes('68d5ca9db226849b41a6fff59d796ff19d0a8840')
};
const warnings=[...new Set(lines.filter(x=>/warning: .*declaration uses [`']sorry[`']/.test(x))
  .map(x=>x.replace(/^.*?warning: /,'').replace(/\x1b\[[0-9;]*m/g,'')))].sort();
const expected=['Challenge.lean:12:8: declaration uses `sorry`','Challenge.lean:16:8: declaration uses `sorry`'];
const warnings_approved=warnings.length===2&&expected.every(x=>warnings.includes(x));
const output={
  revision:'tmr1-pinned-ci057.offline-v1',
  upstream_run:40442388505,upstream_job:121985557508,
  source_commit:'16a5ce41304fcdaea4e0be7c132e1c361dc26da5',
  line_count:lines.length,characters:s.length,checks,warnings,warnings_approved,
  upstream_evidence_pass:Object.values(checks).every(Boolean)&&warnings_approved,
  local_kernel_replay_performed:false,
  interpretation:'Upstream CI log only; independent kernel rebuild, proof mathematics, semantics and physical model translation require separate audits.'
};
process.stdout.write(JSON.stringify(output,null,2)+'\n');
if(!output.upstream_evidence_pass)process.exit(1);
