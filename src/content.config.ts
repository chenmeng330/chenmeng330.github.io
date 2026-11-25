import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

const texts = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/texts" }),
  schema: z.object({
    title: z.string(),
    slug: z.string(),
    kind: z.enum(["work", "gallery", "misc", "essay"]),
    /** 随笔分两个区，秦羲是副本的日记，羲子是本人写的 */
    channel: z.enum(["秦羲", "羲子"]).optional(),
    category: z.string().optional(),
    /** 图画栏目的缩略图 */
    cover: z.string().optional(),
    date: z.coerce.date().optional(),
    summary: z.string().optional(),
    order: z.number().optional(),
    draft: z.boolean().default(false),
  }),
});

export const collections = { texts };
