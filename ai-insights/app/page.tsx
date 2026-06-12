
import Link from "next/link";
import { getInsights } from "../lib/sheets";

export default async function Home() {
  const insights = await getInsights();

  const featured = insights[0];

  return (
    <main className="min-h-screen bg-white">

      <section className="max-w-7xl mx-auto px-6 py-12">

        {/* HERO SECTION */}

        <div className="rounded-3xl bg-gradient-to-r from-blue-50 via-violet-50 to-cyan-50 p-12 mb-16">

          <h1 className="text-8xl font-bold text-zinc-900">
            AI Intelligence
          </h1>

          <p className="text-zinc-600 text-xl mt-4">
            Daily executive insights on autonomous systems,
            enterprise transformation and intelligence infrastructure.
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

              <p className="text-blue-600 font-semibold">
                TODAY'S INSIGHT
              </p>

              <h2 className="text-5xl font-bold text-zinc-900 mt-4">
                {featured.title}
              </h2>

              <p className="text-zinc-600 mt-6 text-lg">
                {featured.content?.slice(0, 300)}...
              </p>

              <Link
                href={`/blog/${featured.id}`}
                className="inline-block mt-8 px-6 py-3 rounded-xl bg-zinc-900 text-white font-semibold"
              >
                Read Article →
              </Link>

            </div>

          </div>
        )}

        {/* ARTICLES GRID */}

        <div className="grid md:grid-cols-2 gap-8">

          {insights.slice(1).map((item) => (

            <div
              key={item.id}
              className="bg-white border border-zinc-200 rounded-3xl overflow-hidden shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300"
            >

              {item.imageUrl && (
                <img
                  src={item.imageUrl}
                  alt={item.title}
                  className="w-full h-64 object-cover"
                />
              )}

              <div className="p-6">

                <p className="text-blue-600 font-medium">
                  {item.category}
                </p>

                <h2 className="text-3xl font-bold text-zinc-900 mt-3">
                  {item.title}
                </h2>

                <p className="text-zinc-600 mt-4">
                  {item.content?.slice(0, 180)}...
                </p>

                <p className="text-zinc-400 mt-4">
                  {item.date}
                </p>

                <Link
                  href={`/blog/${item.id}`}
                  className="inline-block mt-6 text-blue-600 font-semibold"
                >
                  Read More →
                </Link>

              </div>

            </div>

          ))}

        </div>

      </section>

      {/* FOOTER */}

      <footer className="mt-24 py-12 text-center text-zinc-500 border-t border-zinc-200">

        <p className="text-lg font-medium">
          AI Insights
        </p>

        <p className="mt-2">
          Daily Intelligence for Modern Organizations
        </p>

      </footer>

    </main>
  );
}



