import { defineConfig } from 'vite';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const root = path.dirname(fileURLToPath(import.meta.url));

/**
 * Bundle vanilla app.js (expects marked, hljs from CDN in index.html).
 * Output: static/dist/oculo-app.iife.js — optional minified deploy artifact.
 */
export default defineConfig({
  build: {
    lib: {
      entry: path.resolve(root, 'static/app.js'),
      name: 'OculoApp',
      formats: ['iife'],
      fileName: () => 'oculo-app.iife.js',
    },
    outDir: path.resolve(root, 'static/dist'),
    emptyOutDir: true,
    minify: 'esbuild',
    sourcemap: true,
    rollupOptions: {
      external: [],
      output: {
        inlineDynamicImports: true,
      },
    },
  },
});
