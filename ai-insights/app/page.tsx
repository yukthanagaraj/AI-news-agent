export const dynamic = "force-dynamic";

import Link from "next/link";
import { getInsights } from "../lib/sheets";

export default async function Home() {

  const insights = await getInsights();

  const featured = insights[0];

  const featuredWords =
    featured?.content?.split(/\s+/).length || 0;

  const featuredReadTime = Math.max(
    1,
    Math.ceil(featuredWords / 130)
  );

  return (
    <main className="min-h-screen bg-white">

      <section className="max-w-7xl mx-auto px-6 py-12">

        {/* HERO */}

        <div className="rounded-3xl bg-gradient-to-r from-blue-50 via-violet-50 to-cyan-50 p-12 mb-16">

          <h1 className="text-8xl font-bold text-zinc-900">
            AI Insights
          </h1>

          <p className="text-zinc-600 text-xl mt-4 leading-9">
            Daily insights on AI agents, AI employees,
            enterprise intelligence and the future of work.
          </p>

        </div>

        {/* FEATURED ARTICLE */}

        {featured && (
          <div className="mb-20 rounded-3xl overflow-hidden shadow-lg hover:shadow-2xl transition-all duration-300">

            {featured.imageUrl && (
              <img
                src={featured.imageUrl}
                alt={featured.title}
                className="w-full h-[500px] object-cover"
              />
            )}

            <div className="p-8">

              <p className="text-orange-600 font-semibold">
                TODAY'S INSIGHT
              </p>

              <h2 className="text-5xl font-bold text-zinc-900 mt-4 leading-tight">
                {featured.title}
              </h2>

              <p className="text-zinc-400 mt-4 text-sm">
                {featured.date} • {featuredReadTime} min read
              </p>

              <p className="text-zinc-600 mt-6 text-lg leading-8">
                {featured.content?.slice(0, 300)}...
              </p>

              <Link
                href={`/blog/${featured.id}`}
                className="inline-block mt-8 px-6 py-3 rounded-xl bg-zinc-900 text-white font-semibold hover:bg-black transition"
              >
                Read Article →
              </Link>

            </div>

          </div>
        )}

        {/* ARTICLES GRID */}

        <div className="grid md:grid-cols-2 gap-8">

          {insights.slice(1).map((item) => {

            const words =
              item.content?.split(/\s+/).length || 0;

            const readTime = Math.max(
              1,
              Math.ceil(words / 130)
            );

            return (

              <div
                key={item.id}
                className="
                bg-white
                border
                border-zinc-200
                rounded-3xl
                overflow-hidden
                shadow-sm
                hover:shadow-2xl
                hover:-translate-y-2
                transition-all
                duration-300
                "
              >

                {item.imageUrl && (
                  <img
                    src={item.imageUrl}
                    alt={item.title}
                    className="w-full h-64 object-cover"
                  />
                )}

                <div className="p-6">

                  <h2 className="text-3xl font-bold text-zinc-900 leading-tight">
                    {item.title}
                  </h2>

                  <p className="text-zinc-400 mt-4 text-sm">
                    {item.date} • {readTime} min read
                  </p>

                  <p className="text-zinc-600 mt-4 leading-8">
                    {item.content?.slice(0, 180)}...
                  </p>

                  <Link
                    href={`/blog/${item.id}`}
                    className="
                    inline-block
                    mt-6
                    text-orange-600
                    font-semibold
                    hover:text-orange-700
                    "
                  >
                    Read Insight →
                  </Link>

                </div>

              </div>

            );
          })}

        </div>

      </section>

      <footer className="mt-24 py-12 text-center text-zinc-500 border-t border-zinc-200">

        <p className="text-lg font-medium">
          AI Insights
        </p>

        <p className="mt-2">
          Research and analysis on AI agents,
          digital labor and enterprise transformation.
        </p>

      </footer>

    </main>
  );
}


