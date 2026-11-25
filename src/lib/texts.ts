import { getCollection, type CollectionEntry } from "astro:content";

export type Text = CollectionEntry<"texts">;
export type Kind = Text["data"]["kind"];

/** 全部已发布文本 */
export async function allTexts(): Promise<Text[]> {
  const entries = await getCollection("texts", ({ data }) => !data.draft);
  return entries.sort(byNewest);
}

/** 某一栏目的文本 */
export async function textsOf(kind: Kind): Promise<Text[]> {
  return (await allTexts()).filter((t) => t.data.kind === kind);
}

function byNewest(a: Text, b: Text): number {
  const ao = a.data.order;
  const bo = b.data.order;
  if (ao !== undefined || bo !== undefined) {
    return (ao ?? 9999) - (bo ?? 9999);
  }
  const at = a.data.date?.getTime() ?? 0;
  const bt = b.data.date?.getTime() ?? 0;
  return bt - at;
}

/** 2026.11.24 */
export function fmtDate(date?: Date): string {
  if (!date) return "未系年";
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, "0");
  const d = String(date.getDate()).padStart(2, "0");
  return `${y}.${m}.${d}`;
}

/** 2026 年 11 月 24 日 */
export function fmtDateLong(date?: Date): string {
  if (!date) return "未系年";
  return `${date.getFullYear()} 年 ${date.getMonth() + 1} 月 ${date.getDate()} 日`;
}

/** 栏目标题 */
export const kindMeta: Record<
  Kind,
  { label: string; href: string; english: string }
> = {
  work: { label: "作品", href: "/works/", english: "Works" },
  gallery: { label: "图画", href: "/gallery/", english: "Gallery" },
  misc: { label: "杂项", href: "/misc/", english: "Miscellany" },
  essay: { label: "随笔", href: "/essays/", english: "Essays" },
};

/** 随笔的两个区 */
export const channels = ["秦羲", "羲子"] as const;

export type Channel = (typeof channels)[number];

/** 某一区里的随笔 */
export async function essaysOfChannel(channel: Channel): Promise<Text[]> {
  return (await textsOf("essay")).filter((t) => t.data.channel === channel);
}

/** 按分类分组，保持给定顺序 */
export function groupByCategory(
  texts: Text[],
  order: string[] = [],
): { category: string; items: Text[] }[] {
  const map = new Map<string, Text[]>();
  for (const t of texts) {
    const c = t.data.category ?? "其他";
    if (!map.has(c)) map.set(c, []);
    map.get(c)!.push(t);
  }
  const keys = [...map.keys()].sort((a, b) => {
    const ia = order.indexOf(a);
    const ib = order.indexOf(b);
    return (ia === -1 ? 99 : ia) - (ib === -1 ? 99 : ib);
  });
  return keys.map((category) => ({ category, items: map.get(category)! }));
}
