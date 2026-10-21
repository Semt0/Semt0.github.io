import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';
import vm from 'node:vm';
import { createHash } from 'node:crypto';

const source = readFileSync(new URL('../docs/javascripts/waline-init.js', import.meta.url), 'utf8');
const head = readFileSync(new URL('../overrides/partials/extrahead.html', import.meta.url), 'utf8');
const config = readFileSync(new URL('../zensical.toml', import.meta.url), 'utf8');
const template = readFileSync(new URL('../overrides/partials/comments.html', import.meta.url), 'utf8');
const flush = () => new Promise(resolve => setImmediate(resolve));

async function harness() {
  let run, element = null, resolveDownload, rejectDownload;
  const calls = [], errors = [], imports = [];
  const download = new Promise((resolve, reject) => {
    resolveDownload = resolve;
    rejectDownload = reject;
  });
  const context = vm.createContext({
    URL,
    document: { getElementById: () => element },
    document$: { subscribe: callback => { run = callback; } },
    window: { location: { pathname: '/', href: 'https://example.com/' } },
    console: { error: (...args) => errors.push(args) },
  });
  const module = new vm.SyntheticModule(['init'], function () {
    this.setExport('init', options => {
      const call = { options, destroyed: false };
      calls.push(call);
      return { destroy: () => { call.destroyed = true; } };
    });
  }, { context });
  await module.link(() => {});
  await module.evaluate();
  new vm.Script(source, {
    importModuleDynamically: async url => {
      imports.push(url);
      await download;
      return module;
    },
  }).runInContext(context);
  return {
    calls, errors, imports,
    resolve: resolveDownload, reject: rejectDownload,
    navigate(path, enabled = true, commentPath = "") {
      element = enabled ? { dataset: { clientUrl: '/vendor/waline/waline.js', commentPath }, classList: { add() {} }, innerHTML: '', textContent: '' } : null;
      context.window.location.pathname = path;
      context.window.location.href = `https://example.com${path}`;
      run();
      return element;
    },
  };
}

test('Waline assets are hosted locally and match their recorded upstream hashes', () => {
  assert.ok(config.includes('vendor/waline/waline.css'));
  assert.ok(template.includes("'vendor/waline/waline.js' | url"));
  assert.doesNotMatch(head, /<script[^>]+waline\.js/);
  assert.doesNotMatch(head + source, /https:\/\/unpkg.com/);
  const provenance = readFileSync(new URL('../docs/vendor/waline/PROVENANCE.txt', import.meta.url), 'utf8');
  for (const extension of ['js', 'css']) {
    const bytes = readFileSync(new URL(`../docs/vendor/waline/waline.${extension}`, import.meta.url));
    assert.ok(provenance.includes(createHash('sha256').update(bytes).digest('hex')));
  }
});

test('initial page mounts once and retains the existing pathname key', async () => {
  const h = await harness();
  const el = h.navigate('/note/%E6%B5%8B%E8%AF%95/');
  h.resolve();
  await flush();
  assert.equal(h.calls.length, 1);
  assert.equal(h.calls[0].options.el, el);
  assert.equal(h.calls[0].options.path, '/note/%E6%B5%8B%E8%AF%95/');
});

test('rapid navigation during download only mounts the latest page', async () => {
  const h = await harness();
  h.navigate('/first/');
  const el = h.navigate('/second/');
  h.resolve();
  await flush();
  assert.equal(h.imports.length, 1);
  assert.equal(h.calls.length, 1);
  assert.equal(h.calls[0].options.el, el);
  assert.equal(h.calls[0].options.path, '/second/');
});

test('navigation to comments:false prevents a stale mount', async () => {
  const h = await harness();
  h.navigate('/first/');
  h.navigate('/friends/', false);
  h.resolve();
  await flush();
  assert.equal(h.calls.length, 0);
});

test('navigation destroys the previous instance and reuses the module', async () => {
  const h = await harness();
  h.resolve();
  h.navigate('/first/');
  await flush();
  h.navigate('/second/');
  await flush();
  assert.equal(h.calls[0].destroyed, true);
  assert.equal(h.calls.length, 2);
  assert.equal(h.imports.length, 1);
  h.navigate('/', false);
  assert.equal(h.calls[1].destroyed, true);
});

test('download failure is visible and a later navigation retries', async () => {
  const h = await harness();
  const el = h.navigate('/first/');
  h.reject(new Error('offline'));
  await flush();
  assert.match(el.textContent, /加载失败/);
  assert.equal(h.calls.length, 0);
  h.navigate('/second/');
  await flush();
  assert.equal(h.imports.length, 2);
});

test('friends page preserves the original homepage thread without affecting article keys', async () => {
  const h = await harness();
  h.resolve();
  h.navigate('/', false);
  await flush();
  assert.equal(h.imports.length, 0);
  h.navigate('/friends/', true, '/');
  await flush();
  assert.equal(h.calls[0].options.path, '/');
  h.navigate('/blog/article/');
  await flush();
  assert.equal(h.calls[1].options.path, '/blog/article/');
  assert.equal(h.calls[0].destroyed, true);
});
