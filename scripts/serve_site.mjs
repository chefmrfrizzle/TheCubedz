#!/usr/bin/env node
import { createReadStream } from 'node:fs';
import { access, readFile, stat } from 'node:fs/promises';
import http from 'node:http';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const projectRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const root = path.join(projectRoot, process.env.SITE_DIR || 'dist');
const port = Number(process.env.PORT || process.argv[2] || 4173);
const host = process.env.HOST || '127.0.0.1';

const types = new Map([
  ['.html', 'text/html; charset=utf-8'], ['.css', 'text/css; charset=utf-8'], ['.js', 'text/javascript; charset=utf-8'], ['.mjs', 'text/javascript; charset=utf-8'],
  ['.json', 'application/json; charset=utf-8'], ['.jsonl', 'application/x-ndjson; charset=utf-8'], ['.md', 'text/markdown; charset=utf-8'], ['.txt', 'text/plain; charset=utf-8'],
  ['.svg', 'image/svg+xml'], ['.png', 'image/png'], ['.xml', 'application/xml; charset=utf-8'], ['.webmanifest', 'application/manifest+json'], ['.cff', 'text/plain; charset=utf-8'],
]);

async function exists(filePath) { try { await access(filePath); return true; } catch { return false; } }

async function resolveRequest(url) {
  const pathname = decodeURIComponent(new URL(url, `http://${host}:${port}`).pathname);
  const candidate = path.resolve(root, `.${pathname}`);
  if (!candidate.startsWith(root)) return null;
  if (await exists(candidate)) {
    const details = await stat(candidate);
    if (details.isDirectory() && await exists(path.join(candidate, 'index.html'))) return path.join(candidate, 'index.html');
    if (details.isFile()) return candidate;
  }
  const htmlCandidate = path.join(candidate, 'index.html');
  if (await exists(htmlCandidate)) return htmlCandidate;
  return path.join(root, '404.html');
}

const server = http.createServer(async (request, response) => {
  try {
    const filePath = await resolveRequest(request.url || '/');
    if (!filePath) {
      response.writeHead(400, { 'content-type': 'text/plain; charset=utf-8' });
      response.end('Bad request');
      return;
    }
    const isNotFound = filePath.endsWith(`${path.sep}404.html`) && !String(request.url).endsWith('/404.html');
    response.writeHead(isNotFound ? 404 : 200, {
      'content-type': types.get(path.extname(filePath).toLowerCase()) || 'application/octet-stream',
      'cache-control': path.extname(filePath) === '.html' ? 'no-cache' : 'public, max-age=3600',
      'x-content-type-options': 'nosniff',
    });
    if (request.method === 'HEAD') response.end();
    else createReadStream(filePath).pipe(response);
  } catch (error) {
    response.writeHead(500, { 'content-type': 'text/plain; charset=utf-8' });
    response.end(`Internal server error\n${error.message}`);
  }
});

server.listen(port, host, () => console.log(`Static research site: http://${host}:${port}`));
