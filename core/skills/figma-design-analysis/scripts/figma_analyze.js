#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const https = require('https');
const crypto = require('crypto');

const FIGMA_API_BASE = 'https://api.figma.com/v1';
const CACHE_DIR = '.figma_cache';
const CACHE_TTL_SECONDS = 3600;
const MAX_RETRIES = 6;
const BASE_DELAY_SECONDS = 1;
const INTER_REQUEST_DELAY_MS = 200;
const MAX_RETRY_AFTER_SECONDS = 30;

function log(message) {
  process.stderr.write(`[figma_analyze] ${message}\n`);
}

function screenshotInputHint() {
  process.stderr.write([
    '[figma_analyze] Alternative input option:',
    '[figma_analyze] - Capture screenshots/images from Figma and place them under:',
    '[figma_analyze]   docs/figma_design_analysis/<TICKET-ID>_screenshots/',
    '[figma_analyze] - Supported formats: .png, .jpg, .jpeg, .webp',
    '[figma_analyze] - Then run the design analysis workflow in screenshot/image mode.',
    '',
  ].join('\n'));
}

function fail(message) {
  process.stderr.write(`[ERROR] ${message}\n`);
  process.exit(1);
}

function showUsage() {
  process.stdout.write(`Usage:\n  node figma_analyze.js --figma-url <url> [--output <file>] [--no-cache]\n  node figma_analyze.js --file-key <key> --node-id <id> [--output <file>] [--no-cache]\n  node figma_analyze.js --figma-url <url> --export-svg --asset-output <file.svg>\n  node figma_analyze.js --file-key <key> --node-id <id> --export-svg --asset-output <file.svg>\n\nEnvironment:\n  FIGMA_TOKEN is required for direct Figma API analysis.\n  .env.local is loaded automatically when present.\n`);
}

function loadDotEnvLocal() {
  const envPath = path.resolve(process.cwd(), '.env.local');
  if (!fs.existsSync(envPath)) {
    return;
  }

  const lines = fs.readFileSync(envPath, 'utf8').split(/\r?\n/);
  for (const rawLine of lines) {
    const line = rawLine.trim();
    if (!line || line.startsWith('#')) {
      continue;
    }

    const match = line.match(/^([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$/);
    if (!match) {
      continue;
    }

    const key = match[1];
    let value = match[2].trim();
    if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) {
      value = value.slice(1, -1);
    }
    if (!Object.prototype.hasOwnProperty.call(process.env, key)) {
      process.env[key] = value;
    }
  }
}

function parseArgs(argv) {
  const options = {
    figmaUrl: '',
    fileKey: '',
    nodeId: '',
    output: '',
    assetOutput: '',
    exportSvg: false,
    exportSvgNodeId: '',
    noCache: false,
  };

  const aliases = {
    '--figma-url': 'figmaUrl',
    '-FigmaUrl': 'figmaUrl',
    '--file-key': 'fileKey',
    '-FileKey': 'fileKey',
    '--node-id': 'nodeId',
    '-NodeId': 'nodeId',
    '--output': 'output',
    '-Output': 'output',
    '--asset-output': 'assetOutput',
    '-AssetOutput': 'assetOutput',
    '--export-svg-node-id': 'exportSvgNodeId',
    '-ExportSvgNodeId': 'exportSvgNodeId',
  };

  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === '--help' || arg === '-h' || arg === '/?') {
      showUsage();
      process.exit(0);
    }
    if (arg === '--no-cache' || arg === '-NoCache') {
      options.noCache = true;
      continue;
    }
    if (arg === '--export-svg' || arg === '-ExportSvg') {
      options.exportSvg = true;
      continue;
    }

    const key = aliases[arg];
    if (!key) {
      fail(`Unknown option: ${arg}`);
    }
    const value = argv[index + 1];
    if (!value || value.startsWith('--')) {
      fail(`Missing value for ${arg}`);
    }
    options[key] = value;
    index += 1;
  }

  return options;
}

function normalizeNodeId(raw) {
  return decodeURIComponent(String(raw)).replace(/-/g, ':');
}

function parseFigmaUrl(url) {
  let parsed;
  try {
    parsed = new URL(url);
  } catch {
    fail(`Invalid Figma URL: ${url}`);
  }

  const segments = parsed.pathname.split('/').filter(Boolean);
  const fileMarkerIndex = segments.findIndex((segment) => ['design', 'file', 'proto'].includes(segment));
  if (fileMarkerIndex < 0 || !segments[fileMarkerIndex + 1]) {
    fail(`Could not extract FILE_KEY from URL: ${url}`);
  }

  return {
    fileKey: segments[fileMarkerIndex + 1],
    nodeId: parsed.searchParams.get('node-id') ? normalizeNodeId(parsed.searchParams.get('node-id')) : '0',
  };
}

function cacheKey(input) {
  return crypto.createHash('sha256').update(input).digest('hex').slice(0, 16);
}

function cachePath(key) {
  return path.join(CACHE_DIR, `${key}.json`);
}

function cacheGet(key, noCache) {
  const targetPath = cachePath(key);
  if (noCache || !fs.existsSync(targetPath)) {
    return null;
  }

  const stat = fs.statSync(targetPath);
  const ageSeconds = (Date.now() - stat.mtimeMs) / 1000;
  if (ageSeconds > CACHE_TTL_SECONDS) {
    return null;
  }

  log(`Cache hit: ${key}`);
  return fs.readFileSync(targetPath, 'utf8');
}

function cachePut(key, content) {
  fs.mkdirSync(CACHE_DIR, { recursive: true });
  fs.writeFileSync(cachePath(key), content, 'utf8');
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function requestText(url, token) {
  return new Promise((resolve, reject) => {
    const headers = {
      'Accept': 'application/json',
    };
    if (token) {
      headers['X-FIGMA-TOKEN'] = token;
    }

    const request = https.request(url, {
      method: 'GET',
      headers,
    }, (response) => {
      const chunks = [];
      response.on('data', (chunk) => chunks.push(chunk));
      response.on('end', () => {
        resolve({
          statusCode: response.statusCode || 0,
          headers: response.headers,
          body: Buffer.concat(chunks).toString('utf8'),
        });
      });
    });

    request.on('error', reject);
    request.end();
  });
}

function requestBuffer(url) {
  return new Promise((resolve, reject) => {
    https.get(url, (response) => {
      const chunks = [];
      response.on('data', (chunk) => chunks.push(chunk));
      response.on('end', () => {
        resolve({
          statusCode: response.statusCode || 0,
          headers: response.headers,
          body: Buffer.concat(chunks),
        });
      });
    }).on('error', reject);
  });
}

async function apiGetJson(url, key, token, noCache) {
  const cached = cacheGet(key, noCache);
  if (cached) {
    return JSON.parse(cached);
  }

  for (let attempt = 1; attempt <= MAX_RETRIES; attempt += 1) {
    const response = await requestText(url, token);
    if (response.statusCode >= 200 && response.statusCode < 300) {
      cachePut(key, response.body);
      await sleep(INTER_REQUEST_DELAY_MS);
      return JSON.parse(response.body);
    }

    if (response.statusCode === 429) {
      const retryAfter = Number(response.headers['retry-after']);
      const exponentialDelay = Math.min(BASE_DELAY_SECONDS * (2 ** (attempt - 1)), MAX_RETRY_AFTER_SECONDS);
      const delaySeconds = Number.isFinite(retryAfter) && retryAfter <= MAX_RETRY_AFTER_SECONDS
        ? retryAfter
        : exponentialDelay + Math.random() * 0.5;
      log(`Rate limited (429). Backoff ${delaySeconds.toFixed(2)}s (attempt ${attempt}/${MAX_RETRIES})`);
      await sleep(delaySeconds * 1000);
      continue;
    }

    fail(`Figma API request failed (HTTP ${response.statusCode}): ${response.body}`);
  }

  screenshotInputHint();
  fail('Figma API exhausted retries after 429 responses.');
}

function fetchFileMetadata(fileKey, token, noCache) {
  log(`Fetching file metadata for: ${fileKey}`);
  return apiGetJson(`${FIGMA_API_BASE}/files/${encodeURIComponent(fileKey)}`, cacheKey(`file:${fileKey}`), token, noCache);
}

function fetchNodeDetails(fileKey, nodeIds, token, noCache) {
  const normalized = nodeIds.split(',').map((nodeId) => normalizeNodeId(nodeId.trim())).join(',');
  const encoded = normalized.split(',').map((nodeId) => encodeURIComponent(nodeId)).join(',');
  log(`Fetching node details: ${normalized}`);
  return apiGetJson(`${FIGMA_API_BASE}/files/${encodeURIComponent(fileKey)}/nodes?ids=${encoded}`, cacheKey(`nodes:${fileKey}:${normalized}`), token, noCache);
}

function fetchImageExport(fileKey, nodeId, format, token, noCache) {
  const normalized = normalizeNodeId(nodeId);
  const encoded = encodeURIComponent(normalized);
  log(`Requesting ${format.toUpperCase()} export URL for node: ${normalized}`);
  return apiGetJson(`${FIGMA_API_BASE}/images/${encodeURIComponent(fileKey)}?ids=${encoded}&format=${format}`, cacheKey(`images:${fileKey}:${normalized}:${format}`), token, noCache);
}

async function exportSvgNode({ fileKey, nodeId, assetOutput, token, noCache }) {
  const normalizedNodeId = normalizeNodeId(nodeId);
  const exportResponse = await fetchImageExport(fileKey, normalizedNodeId, 'svg', token, noCache);
  const exportUrl = exportResponse.images ? exportResponse.images[normalizedNodeId] : '';
  if (!exportUrl) {
    fail(`Figma did not return an SVG export URL for file_key=${fileKey} node_id=${normalizedNodeId}.`);
  }

  const output = assetOutput || `figma-${fileKey}-${normalizedNodeId.replace(/:/g, '-')}.svg`;
  const svgResponse = await requestBuffer(exportUrl);
  if (svgResponse.statusCode < 200 || svgResponse.statusCode >= 300) {
    fail(`Failed to download SVG export (HTTP ${svgResponse.statusCode}).`);
  }

  const outputDirectory = path.dirname(output);
  if (outputDirectory && outputDirectory !== '.') {
    fs.mkdirSync(outputDirectory, { recursive: true });
  }
  fs.writeFileSync(output, svgResponse.body);
  log(`SVG export saved to: ${output}`);
  process.stdout.write(`${output}\n`);
}

function markdown(value) {
  return String(value ?? '').replace(/\|/g, '\\|').replace(/[\r\n]+/g, ' ');
}

function nodeSize(node) {
  const box = node.absoluteBoundingBox || node.size || {};
  const width = box.width ?? box.x ?? '?';
  const height = box.height ?? box.y ?? '?';
  return `${width} x ${height}`;
}

function selectedDocuments(nodeDetails) {
  return Object.values(nodeDetails.nodes || {}).map((entry) => entry.document).filter(Boolean);
}

function flattenNodes(root) {
  if (!root || typeof root !== 'object') {
    return [];
  }
  const nodes = [root];
  for (const child of root.children || []) {
    nodes.push(...flattenNodes(child));
  }
  return nodes;
}

function allSelectedNodes(nodeDetails) {
  return selectedDocuments(nodeDetails).flatMap(flattenNodes);
}

function toByte(value) {
  return Math.max(0, Math.min(255, Math.round((value ?? 0) * 255)));
}

function colorHex(color) {
  if (!color) {
    return 'n/a';
  }
  const hex = `#${[color.r, color.g, color.b].map((part) => toByte(part).toString(16).padStart(2, '0').toUpperCase()).join('')}`;
  return (color.a ?? 1) < 1 ? `${hex} @ ${color.a}` : hex;
}

function paintName(paint) {
  if (paint?.type === 'SOLID' && paint.color) {
    return colorHex(paint.color);
  }
  return paint?.type || 'Unknown paint';
}

function uniqueSorted(values) {
  return Array.from(new Set(values.filter(Boolean))).sort((left, right) => left.localeCompare(right));
}

function limit(values, count) {
  return values.slice(0, count);
}

function section(title, lines) {
  return [`## ${title}`, '', ...lines].join('\n');
}

function extractOverview(fileMetadata, nodeDetails) {
  const documents = selectedDocuments(nodeDetails);
  const pages = (fileMetadata.document?.children || []).map((page) => page.name).join(', ');
  const rootRows = documents.length === 0
    ? ['| Not found | - | - | - | - |']
    : documents.map((document) => `| ${markdown(document.name || 'Unnamed')} | ${markdown(document.type || 'Unknown')} | ${markdown(document.id || '-')} | ${nodeSize(document)} | ${(document.children || []).length} |`);

  return section('Overview', [
    '- **Input source:** Direct Figma API',
    `- **File name:** ${markdown(fileMetadata.name || 'Unknown')}`,
    `- **Last modified:** ${markdown(fileMetadata.lastModified || 'Unknown')}`,
    `- **Version:** ${markdown(fileMetadata.version || 'Unknown')}`,
    `- **Selected node count:** ${documents.length}`,
    `- **Top-level pages in file:** ${markdown(pages)}`,
    '',
    '### Selected Root Nodes',
    '',
    '| Node | Type | Figma Node ID | Size | Children |',
    '|------|------|---------------|------|----------|',
    ...rootRows,
  ]);
}

function extractDesignTokens(fileMetadata, nodeDetails) {
  log('Extracting design tokens from Figma JSON...');
  const nodes = allSelectedNodes(nodeDetails);
  const colors = uniqueSorted(nodes.flatMap((node) => [...(node.fills || []), ...(node.strokes || [])]
    .filter((paint) => paint.visible !== false)
    .map(paintName)));
  const typography = uniqueSorted(nodes
    .filter((node) => node.type === 'TEXT' && node.style)
    .map((node) => {
      const style = node.style;
      return [
        style.fontFamily || 'Unknown',
        style.fontPostScriptName || '',
        `${style.fontSize ?? '?'}px`,
        `weight ${style.fontWeight ?? '?'}`,
        `lineHeight ${style.lineHeightPx ?? style.lineHeightPercentFontSize ?? '?'}`,
        `letterSpacing ${style.letterSpacing ?? '?'}`,
      ].join(' | ');
    }));
  const spacing = limit(uniqueSorted(nodes
    .filter((node) => node.layoutMode && node.layoutMode !== 'NONE')
    .map((node) => `- **${markdown(node.name || 'Unnamed')}** (id=${node.id || '-'}): layout=${node.layoutMode}, gap=${node.itemSpacing ?? 'n/a'}, padding=${node.paddingTop ?? 0}/${node.paddingRight ?? 0}/${node.paddingBottom ?? 0}/${node.paddingLeft ?? 0}, sizing=${node.layoutSizingHorizontal ?? 'n/a'}/${node.layoutSizingVertical ?? 'n/a'}`)), 40);
  const radii = limit(uniqueSorted(nodes
    .filter((node) => node.cornerRadius !== undefined || node.rectangleCornerRadii !== undefined || node.strokeWeight !== undefined)
    .map((node) => `- **${markdown(node.name || 'Unnamed')}** (id=${node.id || '-'}): radius=${node.cornerRadius ?? JSON.stringify(node.rectangleCornerRadii ?? 'n/a')}, strokeWeight=${node.strokeWeight ?? 'n/a'}`)), 40);
  const effects = limit(uniqueSorted(nodes.flatMap((node) => node.effects || [])
    .filter((effect) => effect.visible !== false)
    .map((effect) => `- ${effect.type || 'Unknown'}: radius=${effect.radius ?? 'n/a'}, offset=${effect.offset?.x ?? 0},${effect.offset?.y ?? 0}, spread=${effect.spread ?? 'n/a'}, color=${colorHex(effect.color)}`)), 40);
  const styles = limit(Object.entries(fileMetadata.styles || {})
    .map(([id, style]) => `- **${markdown(style.name || id)}**: type=${style.styleType || 'unknown'}, id=${id}`), 60);

  return section('Design Tokens', [
    '### Colors',
    '',
    ...(colors.length ? colors.map((color) => `- ${color}`) : ['- Not found in selected node JSON.']),
    '',
    '### Typography',
    '',
    ...(typography.length ? typography.map((item) => `- ${item}`) : ['- Not found in selected node JSON.']),
    '',
    '### Spacing & Auto Layout',
    '',
    ...(spacing.length ? spacing : ['- No auto-layout spacing found in selected node JSON.']),
    '',
    '### Borders & Radius',
    '',
    ...(radii.length ? radii : ['- No border/radius values found in selected node JSON.']),
    '',
    '### Effects',
    '',
    ...(effects.length ? effects : ['- No effects found in selected node JSON.']),
    '',
    '### Published Styles',
    '',
    ...(styles.length ? styles : ['- No published styles returned by Figma API.']),
  ]);
}

function treeLines(node, depth = 0) {
  if (!node || depth > 5) {
    return [];
  }
  const indent = '  '.repeat(depth);
  return [
    `${indent}- ${markdown(node.name || 'Unnamed')} (type=${node.type || 'Unknown'}, id=${node.id || '-'}, size=${nodeSize(node)})`,
    ...(node.children || []).flatMap((child) => treeLines(child, depth + 1)),
  ];
}

function propertyLines(nodes) {
  return limit(uniqueSorted(nodes
    .filter((node) => node.componentProperties || node.componentPropertyDefinitions)
    .map((node) => {
      const source = node.componentProperties || node.componentPropertyDefinitions || {};
      const properties = Object.entries(source).map(([key, value]) => `${markdown(key)}=${value.value ?? value.defaultValue ?? value.type ?? ''}`);
      return `- **${markdown(node.name || 'Unnamed')}** (id=${node.id || '-'}): ${properties.join(', ')}`;
    })), 80);
}

function extractComponents(nodeDetails) {
  log('Extracting component hierarchy from Figma JSON...');
  const documents = selectedDocuments(nodeDetails);
  const nodes = allSelectedNodes(nodeDetails);
  const rootLines = documents.length
    ? documents.map((document) => `- **${markdown(document.name || 'Unnamed')}** (id=${document.id || '-'}, type=${document.type || 'Unknown'}): size=${nodeSize(document)}, visible=${document.visible ?? true}, clips=${document.clipsContent ?? false}`)
    : ['- Selected node was not returned by Figma API.'];
  const hierarchy = limit(documents.flatMap((document) => treeLines(document)), 160);
  const properties = propertyLines(nodes);
  const text = limit(nodes
    .filter((node) => node.type === 'TEXT')
    .map((node) => `- **${markdown(node.name || 'Text')}** (id=${node.id || '-'}): ${markdown(node.characters || '')}`), 80);
  const constraints = limit(uniqueSorted(nodes
    .filter((node) => node.constraints)
    .map((node) => `- **${markdown(node.name || 'Unnamed')}** (id=${node.id || '-'}): horizontal=${node.constraints?.horizontal ?? 'n/a'}, vertical=${node.constraints?.vertical ?? 'n/a'}, layoutAlign=${node.layoutAlign ?? 'n/a'}, grow=${node.layoutGrow ?? 'n/a'}`)), 80);
  const assetTypes = new Set(['VECTOR', 'BOOLEAN_OPERATION', 'STAR', 'LINE', 'ELLIPSE', 'POLYGON']);
  const assets = limit(uniqueSorted(nodes
    .filter((node) => assetTypes.has(node.type) || (node.fills || []).some((fill) => fill.type === 'IMAGE'))
    .map((node) => `- **${markdown(node.name || 'Asset')}** (id=${node.id || '-'}, type=${node.type || 'Unknown'}): export candidate for image/icon asset.`)), 80);

  return section('Component Specifications', [
    ...rootLines,
    '',
    '### Layer Hierarchy',
    '',
    ...(hierarchy.length ? hierarchy : ['- No layer hierarchy returned.']),
    '',
    '### Variants, Component Properties & States',
    '',
    ...(properties.length ? properties : ['- No explicit component properties or variants found in selected node JSON.']),
    '',
    '### Text Content',
    '',
    ...(text.length ? text : ['- No text layers found.']),
    '',
    '### Layout Constraints',
    '',
    ...(constraints.length ? constraints : ['- No explicit constraints found.']),
    '',
    '### Asset Candidates',
    '',
    ...(assets.length ? assets : ['- No vector/image asset candidates found in selected node JSON.']),
  ]);
}

function extractAccessibility(nodeDetails) {
  const smallTargets = limit(allSelectedNodes(nodeDetails)
    .filter((node) => {
      const box = node.absoluteBoundingBox;
      if (!box) {
        return false;
      }
      const name = node.name || '';
      return (box.width < 44 || box.height < 44) && (/button|btn|icon|close|back|next|tap|link/i.test(name) || node.type === 'INSTANCE');
    })
    .map((node) => `- **${markdown(node.name || 'Unnamed')}** (id=${node.id || '-'}): ${node.absoluteBoundingBox.width} x ${node.absoluteBoundingBox.height}`), 60);

  return section('Accessibility & UX Notes', [
    '- Verify contrast in implementation because Figma API colors can be nested in overlays, effects, and opacity inheritance.',
    '- Preserve reading order according to the layer hierarchy unless product requirements specify a different order.',
    '- Validate touch targets for all tappable layers; flag any controls below 44 x 44 pt during implementation review.',
    '- Map disabled/error/loading states from component properties when present; otherwise confirm missing states with design/product.',
    '',
    '### Small Touch Target Candidates',
    '',
    ...(smallTargets.length ? smallTargets : ['- No obvious small touch-target candidates detected by name/type heuristic.']),
  ]);
}

function extractImplementation(fileKey, nodeId) {
  return section('Implementation Recommendations', [
    `- Treat this report as the implementation source of truth only for nodes returned by the selected Figma node ID: ${nodeId}.`,
    '- Map extracted colors, typography, spacing, radius, and effects to existing project design constants before adding new constants.',
    '- Implement Figma component properties as explicit UI states where applicable: default, selected, disabled, loading, error, expanded/collapsed.',
    '- Export each asset candidate through this Node.js analyzer before coding the final screen.',
    '- Keep raw Figma node IDs in implementation notes or test fixtures when useful for design QA traceability.',
    '',
    '### Useful Follow-up Commands',
    '',
    `node ./.github/skills/figma-design-analysis/scripts/figma_analyze.js --file-key ${fileKey} --node-id ${nodeId}`,
    `node ./.github/skills/figma-design-analysis/scripts/figma_analyze.js --file-key ${fileKey} --node-id <NODE_ID> --export-svg --asset-output docs/assets/figma-<NODE_ID>.svg`,
    '',
    '## AC-to-Design Traceability',
    '',
    '| JIRA AC | Design Component | Figma Node | Notes |',
    '|---------|------------------|-----------|-------|',
    '| (Merge with JIRA analysis) | | | |',
    '',
    '---',
    '',
    '**Next Steps:**',
    '1. Cross-reference design components with JIRA acceptance criteria.',
    '2. Confirm missing states and ambiguous interactions with design/product.',
    '3. Export required image/vector assets.',
    '4. Implement UI using project components and design constants.',
    '5. Validate against screenshots or exported frame images on target devices.',
  ]);
}

function generateReport({ figmaUrl, fileKey, nodeId, fileMetadata, nodeDetails }) {
  const fileName = fileMetadata.name || 'Figma Design';
  const generatedAt = new Date().toISOString().replace('T', ' ').replace(/\.\d{3}Z$/, ' UTC');
  return [
    '# Figma Design Analysis',
    '',
    `**File:** [${markdown(fileName)}](${figmaUrl || `https://www.figma.com/file/${fileKey}`})  `,
    `**File Key:** ${fileKey}  `,
    `**Node ID:** ${nodeId}  `,
    `**Generated:** ${generatedAt}`,
    '',
    extractOverview(fileMetadata, nodeDetails),
    '',
    extractDesignTokens(fileMetadata, nodeDetails),
    '',
    extractComponents(nodeDetails),
    '',
    extractAccessibility(nodeDetails),
    '',
    extractImplementation(fileKey, nodeId),
    '',
  ].join('\n');
}

function defaultOutputPath() {
  const timestamp = new Date().toISOString().replace(/[-:T]/g, '').slice(0, 12);
  return path.join('docs', 'design', `figma_analysis_${timestamp}.md`);
}

async function main() {
  loadDotEnvLocal();
  const options = parseArgs(process.argv.slice(2));

  if (options.figmaUrl) {
    const parsed = parseFigmaUrl(options.figmaUrl);
    options.fileKey = options.fileKey || parsed.fileKey;
    options.nodeId = options.nodeId || parsed.nodeId;
    log(`Parsed Figma URL: FILE_KEY=${options.fileKey} NODE_ID=${options.nodeId}`);
  }

  if (!options.fileKey || !options.nodeId) {
    fail('Either --figma-url or both --file-key and --node-id must be provided.');
  }

  options.nodeId = normalizeNodeId(options.nodeId);
  if (options.exportSvgNodeId) {
    options.exportSvgNodeId = normalizeNodeId(options.exportSvgNodeId);
  }
  const token = process.env.FIGMA_TOKEN;
  if (!token) {
    screenshotInputHint();
    fail('FIGMA_TOKEN environment variable is not set. Direct Figma API analysis requires a token.');
  }

  const output = options.output || defaultOutputPath();
  log('Starting Figma design analysis');
  log(`FILE_KEY: ${options.fileKey}`);
  log(`NODE_ID: ${options.nodeId}`);
  log(`OUTPUT: ${options.exportSvg ? (options.assetOutput || '(default SVG output)') : output}`);

  if (options.exportSvg) {
    await exportSvgNode({
      fileKey: options.fileKey,
      nodeId: options.exportSvgNodeId || options.nodeId,
      assetOutput: options.assetOutput,
      token,
      noCache: options.noCache,
    });
    return;
  }

  const fileMetadata = await fetchFileMetadata(options.fileKey, token, options.noCache);
  const nodeDetails = await fetchNodeDetails(options.fileKey, options.nodeId, token, options.noCache);
  const report = generateReport({
    figmaUrl: options.figmaUrl,
    fileKey: options.fileKey,
    nodeId: options.nodeId,
    fileMetadata,
    nodeDetails,
  });

  fs.mkdirSync(path.dirname(output), { recursive: true });
  fs.writeFileSync(output, report, 'utf8');
  log(`Design analysis saved to: ${output}`);
  process.stdout.write(`${output}\n`);
}

if (require.main === module) {
  main().catch((error) => {
    fail(error && error.stack ? error.stack : String(error));
  });
}

module.exports = {
  parseFigmaUrl,
  normalizeNodeId,
  generateReport,
};