// @ts-check
import { defineConfig } from "astro/config";

// 本地开发 / 以后上 GitHub Pages / 自有服务器都用这一份
export default defineConfig({
  site: "https://qinxi.example",
  trailingSlash: "always",
  build: {
    format: "directory",
  },
  markdown: {
    shikiConfig: { theme: "github-light" },
  },
});
