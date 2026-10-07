// Projects Massachusetts counties (us-atlas, Census cartographic boundaries) to an SVG plate
// and places every town and sample listing in the same projection.
// Run from tools/web after `npm i us-atlas@3 topojson-client d3-geo`.
import fs from 'node:fs';
import path from 'node:path';
import { feature, mesh } from 'topojson-client';
import { geoConicConformal, geoPath } from 'd3-geo';
const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '../..');
const NM = path.join(ROOT, 'tools/web/node_modules');
const topo = JSON.parse(fs.readFileSync(path.join(NM, 'us-atlas/counties-10m.json')));
const data = JSON.parse(fs.readFileSync(path.join(ROOT, 'assets/data/listings.json')));
const ma = c => String(c.id).startsWith('25');
const counties = feature(topo, topo.objects.counties).features.filter(ma);
const state = feature(topo, topo.objects.states).features.find(s => String(s.id) === '25');
const W = 1000, H = 600;
const proj = geoConicConformal().parallels([41.7, 42.7]).rotate([71.5, 0]).fitExtent([[24, 24], [W - 24, H - 24]], state);
const p = geoPath(proj);
const inner = mesh(topo, topo.objects.counties, (a, b) => a !== b && ma(a) && ma(b));
const r = n => Math.round(n * 10) / 10;
const pts = {};
for (const [t, v] of Object.entries(data.towns)) { const [x, y] = proj([v.lng, v.lat]); pts[t] = { x: r(x), y: r(y) }; }
const out = { width: W, height: H, state: p(state), counties: counties.map(c => ({ id: c.id, name: c.properties.name, d: p(c), c: p.centroid(c).map(r), b: p.bounds(c).flat().map(r) })), inner: p(inner), towns: pts,
  attribution: 'County boundaries: U.S. Census Bureau cartographic boundary files via us-atlas (ISC).' };
fs.writeFileSync(path.join(ROOT, 'assets/data/ma-map.json'), JSON.stringify(out));
console.log('counties', counties.length, 'towns', Object.keys(pts).length);
