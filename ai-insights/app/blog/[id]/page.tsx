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
        return <div>Article not found</div>;
    }

    return (
        <main className="min-h-screen bg-black text-white">

            <article className="max-w-4xl mx-auto px-8 py-16">

                <img
                    src={article.imageUrl}
                    alt={article.title}
                    className="w-full rounded-3xl mb-10"
                />

                <p className="text-zinc-500">
                    {article.category}
                </p>

                <h1 className="text-6xl font-bold mt-4">
                    {article.title}
                </h1>

                <p className="text-zinc-600 mt-4">
                    {article.date}
                </p>

                <div className="mt-10 text-xl leading-9 whitespace-pre-wrap">
                    {article.content}
                </div>

                <a
                    href={article.sourceUrl}
                    target="_blank"
                    className="inline-block mt-10 text-lg font-semibold"
                >
                    View Original Source →
                </a>

            </article>

        </main>
    );
}