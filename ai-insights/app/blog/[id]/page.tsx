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

    return (
        <main className="min-h-screen bg-white">

            <article className="max-w-4xl mx-auto px-8 py-20">

                {article.imageUrl && (
                    <img
                        src={article.imageUrl}
                        alt={article.title}
                        className="w-full h-[520px] object-cover rounded-[2rem] shadow-lg"
                    />
                )}

                {/* Category */}
                <div className="mt-10 flex justify-center">
                    <div
                        className="
            px-6
            py-2
            rounded-full
            border
            border-orange-200
            bg-orange-50
            text-orange-600
            text-xs
            font-semibold
            tracking-[0.2em]
            uppercase
            "
                    >
                        {article.category}
                    </div>
                </div>

                {/* Title */}
                <h1
                    className="
          mt-10
          text-center
          text-[4rem]
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
          text-zinc-400
          text-[15px]
          "
                >
                    <div className="flex items-center gap-2">
                        <Calendar size={13} />
                        <span>{article.date}</span>
                    </div>

                    <div className="flex items-center gap-2">
                        <Clock size={13} />
                        <span>8 min read</span>
                    </div>

                    <div>
                        By Luvana AI Journal
                    </div>
                </div>

                {/* Divider */}
                <div className="mt-14 border-t border-zinc-200"></div>

                {/* Article Body */}
                <div className="prose max-w-2xl mx-auto mt-20">

                    <ReactMarkdown remarkPlugins={[remarkGfm]}>
                        {article.content}
                    </ReactMarkdown>

                </div>

                {/* Source Button */}
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
            bg-orange-100
            text-orange-700
            font-semibold
            hover:bg-orange-200
            transition
            "
                    >
                        View Original Source →
                    </a>

                </div>

                {/* Related Articles */}
                <RelatedArticles />

                {/* Newsletter */}
                <NewsletterBox />

            </article>

        </main>
    );
}