import type { APIRoute } from "astro";
import { allTexts } from "../lib/texts";

const esc = (s: string) =>
  s
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");

export const GET: APIRoute = async ({ site }) => {
  const base = site ?? new URL("https://qinxi.example/");
  const texts = await allTexts();

  const items = texts.map((t) => {
    const url = new URL(`/${t.data.slug}/`, base).href;
    const lines = [
      "    <item>",
      `      <title>${esc(t.data.title)}</title>`,
      `      <link>${url}</link>`,
      `      <guid isPermaLink="true">${url}</guid>`,
    ];
    if (t.data.date) {
      lines.push(`      <pubDate>${t.data.date.toUTCString()}</pubDate>`);
    }
    lines.push(`      <description>${esc(t.data.summary ?? "")}</description>`);
    lines.push("    </item>");
    return lines.join("\n");
  });

  const xml = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<rss version="2.0">',
    "  <channel>",
    "    <title>秦羲子</title>",
    `    <link>${base.href}</link>`,
    "    <description>小说、长文和随笔</description>",
    "    <language>zh-CN</language>",
    items.join("\n"),
    "  </channel>",
    "</rss>",
    "",
  ].join("\n");

  return new Response(xml, {
    headers: { "Content-Type": "application/rss+xml; charset=utf-8" },
  });
};
