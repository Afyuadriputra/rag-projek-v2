# React + TypeScript + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) (or [oxc](https://oxc.rs) when used in [rolldown-vite](https://vite.dev/guide/rolldown)) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend updating the configuration to enable type-aware lint rules:

```js
export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...

      // Remove tseslint.configs.recommended and replace with this
      tseslint.configs.recommendedTypeChecked,
      // Alternatively, use this for stricter rules
      tseslint.configs.strictTypeChecked,
      // Optionally, add this for stylistic rules
      tseslint.configs.stylisticTypeChecked,

      // Other configs...
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
```

You can also install [eslint-plugin-react-x](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-x) and [eslint-plugin-react-dom](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-dom) for React-specific lint rules:

```js
// eslint.config.js
import reactX from 'eslint-plugin-react-x'
import reactDom from 'eslint-plugin-react-dom'

export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...
      // Enable lint rules for React
      reactX.configs['recommended-typescript'],
      // Enable lint rules for React DOM
      reactDom.configs.recommended,
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
```

## LocatorJS (Alt+Click to Component)

LocatorJS now works in this project because we use the Babel plugin during `vite serve`, and initialize the runtime only in dev.

### What was changed

1. Vite Babel plugin (dev only, JSX/TSX only, path mode)

File: `vite.config.ts`

- Enable LocatorJS only for `command === "serve"`.
- Apply the plugin only to `*.jsx` and `*.tsx`.
- Use `dataAttribute: "path"` so it does not depend on `window.__LOCATOR_DATA__`.

Key snippet:

```ts
import locatorJsx from "@locator/babel-jsx";

export default defineConfig(({ command }) => {
  const isServe = command === "serve";

  return {
    plugins: [
      react({
        babel: isServe
          ? {
              overrides: [
                {
                  test: /\.[jt]sx$/,
                  plugins: [[locatorJsx, { dataAttribute: "path" }]],
                },
              ],
            }
          : undefined,
      }),
    ],
  };
});
```

2. Runtime init (Vite style)

File: `src/main.tsx`

- Use `import.meta.env.DEV` (not `process.env.NODE_ENV`).
- Initialize LocatorJS runtime in dev:

```ts
import setupLocatorUI from "@locator/runtime";

if (import.meta.env.DEV) {
  setupLocatorUI();
}
```

3. Remove conflicting tool

- `click-to-react-component` was removed from `src/main.tsx` because it conflicted with LocatorJS.

### Why it was failing before

- The LocatorJS Babel plugin was applied to `.ts` files, causing Babel parse errors.
- The default `data-locatorjs-id` mode can fail when `__LOCATOR_DATA__` is not populated as expected.
- `click-to-react-component` and LocatorJS were both intercepting clicks.
- `require.resolve(...)` was used in an ESM Vite config.

### How to reuse this in a new Vite + React project

1. Install:

```bash
npm i -D @locator/runtime @locator/babel-jsx
```

2. Add the Babel plugin in `vite.config.ts` (dev-only, JSX/TSX-only, path mode).

3. Initialize runtime in `src/main.tsx`:

```ts
import setupLocatorUI from "@locator/runtime";
if (import.meta.env.DEV) setupLocatorUI();
```

4. Restart dev server and hard-reload the browser.

### Notes for Django + InertiaJS

- Django/InertiaJS is not the root cause; the important part is that React runs in dev mode and Vite Babel transforms JSX/TSX.
