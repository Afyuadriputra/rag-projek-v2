import { defineConfig, type UserConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";
import path from "path";
import locatorJsx from "@locator/babel-jsx";

export default defineConfig(({ command }): UserConfig => {
  const isServe = command === "serve";

  return {
    // =====================================
    // PLUGINS
    // =====================================
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
      tailwindcss(),
    ],

    // =====================================
    // DJANGO STATIC CONFIG
    // =====================================
    base: "/static/",

    server: {
      host: "localhost",
      port: 5173,
      open: false,
      origin: "http://localhost:5173",
      watch: {
        usePolling: true,
      },
    },

    // =====================================
    // PATH ALIAS
    // =====================================
    resolve: {
      alias: {
        "@": path.resolve(__dirname, "./src"),
      },
    },

    // =====================================
    // BUILD OUTPUT KE DJANGO
    // =====================================
    build: {
      outDir: "../core/static/dist",
      assetsDir: "",
      manifest: true,
      emptyOutDir: true,
      rollupOptions: {
        input: {
          main: path.resolve(__dirname, "./src/main.tsx"),
        },
      },
    },
  };
});
