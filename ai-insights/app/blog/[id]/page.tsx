import { getInsights } from "../../../lib/sheets";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Calendar, Clock } from "lucide-react";

import RelatedArticles from "../../../components/RelatedArticles";
import NewsletterBox from "../../../components/NewsletterBox";

export default async function BlogPage({
    params,
}: {
    params: Promise<{ id: string }>;
}) {
    const { id } = await params;

    const insights = await getInsights();

    const article = insights.find(
        (item) => item.id === Number(id)
    );

    if (!article) {
        return (
            <main className="min-h-screen flex items-center justify-center">
                <h1 className="text-4xl font-bold">
                    Article Not Found
                </h1>
            </main>
        );
    }

    const words =
        article.content?.split(/\s+/).length || 0;

    const readTime = Math.max(
        1,
        Math.ceil(words / 130)
    );

    return (
        <main className="min-h-screen bg-white">

            <article className="max-w-6xl mx-auto px-8 py-24">

                {article.imageUrl && (
                    <img
                        src={article.imageUrl}
                        alt={article.title}
                        className="
                            w-full
                            aspect-[16/9]
                            object-cover
                            rounded-[2rem]
                            shadow-2xl
                        "
                    />
                )}

                <h1
                    className="
                        mt-14
                        text-center
                        text-[clamp(3rem,6vw,4.8rem)]
                        leading-[1.05]
                        tracking-[-0.05em]
                        font-bold
                        text-zinc-950
                    "
                >
                    {article.title}
                </h1>

                {article.subtitle && (
                    <p
                        className="
                            mt-5
                            text-center
                            text-[clamp(1.1rem,2vw,1.4rem)]
                            leading-snug
                            text-zinc-500
                            font-normal
                            max-w-3xl
                            mx-auto
                        "
                    >
                        {article.subtitle}
                    </p>
                )}

                <div
                    className="
                        mt-7
                        flex
                        items-center
                        justify-center
                        gap-8
                        text-zinc-500
                        tracking-[0.12em]
                        uppercase
                        text-[13px]
                    "
                >
                    <div className="flex items-center gap-2">
                        <Calendar size={13} />
                        <span>{article.date}</span>
                    </div>

                    <div className="flex items-center gap-2">
                        <Clock size={13} />
                        <span>{readTime} min read</span>
                    </div>

                    <div className="metadata-author">
                        By Luvana AI Journal
                    </div>
                </div>

                <div className="prose max-w-5xl mx-auto mt-24">

                    <ReactMarkdown
                        remarkPlugins={[remarkGfm]}
                        components={{
                            h2: ({ children }) => (
                                <h2 className="font-bold text-zinc-950">
                                    {children}
                                </h2>
                            ),

                            h3: ({ children }) => (
                                <h3 className="font-bold text-zinc-950">
                                    {children}
                                </h3>
                            ),

                            ul: ({ children }) => (
                                <ul className="my-8 space-y-4">
                                    {children}
                                </ul>
                            ),

                            li: ({ children }) => (
                                <li className="leading-8">
                                    {children}
                                </li>
                            ),

                            blockquote: ({ children }) => (
                                <blockquote>
                                    {children}
                                </blockquote>
                            ),
                        }}
                    >
                        {article.content}
                    </ReactMarkdown>
                </div>

                {article.relatedSources && article.relatedSources.length > 0 && (
                    <div className="mt-16 border-t border-zinc-200 pt-10">

                        <p className="text-xs uppercase tracking-[0.12em] text-zinc-400 font-semibold mb-5">
                            Reported by
                        </p>

                        <div className="flex flex-col gap-3">
                            {article.relatedSources.map(
                                (
                                    s: {
                                        source: string;
                                        url: string;
                                        primary?: boolean;
                                    },
                                    i: number
                                ) => (
                                    <a
                                        key={i}
                                        href={s.url}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="
                                            flex items-center justify-between
                                            px-6 py-4
                                            rounded-2xl
                                            bg-orange-50
                                            border border-orange-200
                                            hover:-translate-y-0.5
                                            hover:shadow-md
                                            hover:bg-orange-100
                                            text-orange-700
                                            font-semibold
                                            transition
                                        "
                                    >
                                        <span>
                                            {s.primary ? "Original Source — " : ""}
                                            {s.source}
                                        </span>

                                        <span>→</span>
                                    </a>
                                )
                            )}
                        </div>

                    </div>
                )}

                <div className="mt-24">
                    <RelatedArticles />
                </div>

                <div className="mt-20">
                    <NewsletterBox />
                </div>

            </article>

        </main>
    );
}