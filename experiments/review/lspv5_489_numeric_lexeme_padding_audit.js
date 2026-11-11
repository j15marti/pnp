'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');
const crypto = require('crypto');
const { spawnSync } = require('child_process');

const ROOT = path.resolve(__dirname, '../..');
const CHECKER = path.join(ROOT, 'experiments/arc/lspv2_386_independent_verify.js');
const SEED = path.join(ROOT, 'results/raw/arc/2026-11-11_0336_LSPV4_540_OWNER_FACET_CROSS_CONE_ACCEPTED.json');
const RAW_OUT = path.join(ROOT, 'results/raw/arc/2026-11-11_0748_LSPV5_489_NUMERIC_LEXEME_PADDING_RAW.json');
const PACKET_OUT = path.join(ROOT, 'results/raw/arc/2026-11-11_0748_LSPV5_489_NUMERIC_LEXEME_ACCEPTED_PACKET.json');
const EXPECTED = {
  checkerBlob: '338305c0ce101704205e57543756b8127074a986',
  seedBlob: '25b5c1f95734f6eae36bdbb4a17c948c00753cff',
  checkerSha256: '22d12f665fecede1a047ea20c0c2d3f245c7195ce5df44f342891198ea04a113',
  seedSha256: 'b464205950749d02aba307a323b0d309a28dc4483a85cacb6b5a4bdb04ae1608'
};

function sha256(buf) { return crypto.createHash('sha256').update(buf).digest('hex'); }
function gitBlob(buf) {
  return crypto.createHash('sha1').update(Buffer.from(`blob ${buf.length}\0`)).update(buf).digest('hex');
}
function inject(raw, token) {
  const s = raw.toString('utf8').trimEnd();
  if (!s.endsWith('}')) throw new Error('seed is not a JSON object');
  return Buffer.from(s.slice(0, -1) + ',"pad":' + token + '}\n', 'utf8');
}
function parseOutcome(stdout) {
  const line = stdout.trim().split(/\r?\n/).filter(Boolean).at(-1);
  return line ? JSON.parse(line) : null;
}
function runPacket(packet, tempDir, label) {
  const file = path.join(tempDir, `${label}.json`);
  fs.writeFileSync(file, packet);
  const t0 = process.hrtime.bigint();
  const p = spawnSync(process.execPath, [CHECKER, file], {
    encoding: 'utf8', maxBuffer: 16 * 1024 * 1024
  });
  const elapsedMs = Number(process.hrtime.bigint() - t0) / 1e6;
  let outcome = null;
  if (p.status === 0) outcome = parseOutcome(p.stdout);
  return {
    status: p.status,
    signal: p.signal,
    accepted: p.status === 0,
    bytes: packet.length,
    sha256: sha256(packet),
    elapsedMs,
    maxRssKiB: null,
    outcome,
    stderrTail: (p.stderr || '').trim().split(/\r?\n/).slice(-3)
  };
}

const checker = fs.readFileSync(CHECKER);
const seed = fs.readFileSync(SEED);
const pins = {
  checkerBlob: gitBlob(checker), seedBlob: gitBlob(seed),
  checkerSha256: sha256(checker), seedSha256: sha256(seed)
};
for (const [k, v] of Object.entries(EXPECTED)) {
  if (pins[k] !== v) throw new Error(`pin mismatch ${k}: ${pins[k]} != ${v}`);
}

const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'lspv5-489-'));
try {
  const lengths = [1, 16, 1024, 65536, 1048576];
  const positives = lengths.map((fractionZeros) => {
    const token = '0.' + '0'.repeat(fractionZeros);
    const packet = inject(seed, token);
    const parsed = JSON.parse(packet);
    if (parsed.pad !== 0 || Object.is(parsed.pad, -0)) throw new Error('padding did not parse to +0');
    const result = runPacket(packet, tempDir, `positive-${fractionZeros}`);
    result.fractionZeros = fractionZeros;
    result.tokenBytes = Buffer.byteLength(token);
    result.parsedPad = parsed.pad;
    result.parsedTopLevelKeys = Object.keys(parsed).length;
    result.parsedRecords = parsed.records.length;
    result.canonicalBytes = Buffer.byteLength(JSON.stringify(parsed));
    return result;
  });

  const malformedTokens = ['0.', '00', '01', '0e', '0e+', '-'];
  const negatives = malformedTokens.map((token, i) => {
    const result = runPacket(inject(seed, token), tempDir, `negative-${i}`);
    result.token = token;
    return result;
  });

  const baseline = runPacket(seed, tempDir, 'baseline');
  const invariant = (r) => r.accepted && r.outcome &&
    r.outcome.paid === 31 && r.outcome.def === 1 && r.outcome.res === 30 &&
    r.outcome.records === 49 && r.outcome.sources === 17 && r.outcome.assertions === 3750;
  if (!invariant(baseline)) throw new Error('baseline did not retain expected outcome');
  if (!positives.every(invariant)) throw new Error('a valid padding member failed or changed the proof outcome');
  if (!negatives.every(r => !r.accepted)) throw new Error('a malformed near-miss was accepted');
  const shape = positives.map(r => `${r.parsedTopLevelKeys}:${r.parsedRecords}`).join('|');
  if (new Set(shape.split('|')).size !== 1) throw new Error('parsed shape changed');

  const witness = inject(seed, '0.' + '0'.repeat(64));
  fs.writeFileSync(PACKET_OUT, witness);
  const report = {
    claim: 'For every m>=1, appending an ignored top-level JSON number 0 followed by a decimal point and m zeros increases raw certificate length by m+constant while the archived checker sees the same proof structure and logical outcome.',
    status: 'COMPUTATIONAL plus symbolic JSON construction; checker acceptance sampled at five lengths',
    timestampPacific: '2026-11-11 07:48 PST',
    runtime: { node: process.version, platform: process.platform, arch: process.arch },
    pins,
    baseline,
    positives,
    malformedNearMisses: negatives,
    acceptedWitness: { path: path.relative(ROOT, PACKET_OUT), bytes: witness.length, sha256: sha256(witness), fractionZeros: 64 },
    checks: {
      allPositiveAcceptedWithSameLogicalOutcome: true,
      allMalformedNearMissesRejected: true,
      constantParsedKeyAndRecordCounts: true,
      largestRawBytes: positives.at(-1).bytes,
      largestTokenBytes: positives.at(-1).tokenBytes,
      canonicalBytesLargest: positives.at(-1).canonicalBytes
    },
    limitation: 'The checker retains the raw input Buffer while parsing and verifying. This experiment does not prove constant total process memory or parser time; it only separates raw-byte length from parsed proof-DAG shape, record count, and logical cost.'
  };
  fs.writeFileSync(RAW_OUT, JSON.stringify(report, null, 2) + '\n');
  process.stdout.write(JSON.stringify(report, null, 2) + '\n');
} finally {
  fs.rmSync(tempDir, { recursive: true, force: true });
}
