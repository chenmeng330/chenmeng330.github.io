import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

const texts = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/texts" }),
  schema: z.object({
    title: z.string(),
    slug: z.string(),
    kind: z.enum(["fiction", "longform", "essay"]),
    category: z.string().optional(),
    date: z.coerce.date().optional(),
    summary: z.string().optional(),
    order: z.number().optional(),
    draft: z.boolean().default(false),
  }),
});

export const collections = { texts };
