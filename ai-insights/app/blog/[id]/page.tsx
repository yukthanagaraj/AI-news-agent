import { getInsights } from "../../../lib/sheets";

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

            <article className="max-w-5xl mx-auto px-6 py-16">

                {article.imageUrl && (
                    <img
                        src={article.imageUrl}
                        alt={article.title}
                        className="w-full h-[500px] object-cover rounded-3xl"
                    />
                )}

                <p className="text-blue-600 font-semibold mt-8">
                    {article.category}
                </p>

                <p className="text-zinc-500 mt-2">
                    {article.date}
                </p>

                <h1 className="text-6xl font-bold text-zinc-900 mt-4">
                    {article.title}
                </h1>

                <div className="mt-10 text-xl leading-9 text-zinc-700 whitespace-pre-wrap">
                    {article.content}
                </div>

                <a
                    href={article.sourceUrl}
                    target="_blank"
                    className="inline-block mt-10 px-6 py-3 rounded-xl bg-blue-600 text-white font-semibold"
                >
                    View Original Source →
                </a>

            </article>

        </main>
    );
}