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

    // Dynamic reading time
    const words =
        article.content?.split(/\s+/).length || 0;

    const readTime = Math.max(
        1,
        Math.ceil(words / 130)
    );

    return (
        <main className="min-h-screen bg-white">

            <article className="max-w-5xl mx-auto px-8 py-24">

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

                {/* Title */}
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

                {/* Metadata */}
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


                {/* Body */}
                <div className="prose max-w-4xl mx-auto mt-24">

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
                            )
                        }}
                    >
                        {article.content}
                    </ReactMarkdown>

                </div>

                {/* Source */}
                <div className="mt-16">

                    <a
                        href={article.sourceUrl}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="
            inline-flex
            items-center
            px-7
            py-4
            rounded-full
            bg-orange-50
            border
            border-orange-200
            hover:-translate-y-1
            hover:shadow-lg
            text-orange-700
            font-semibold
            hover:bg-orange-200
            transition
            "
                    >
                        View Original Source →
                    </a>

                </div>

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