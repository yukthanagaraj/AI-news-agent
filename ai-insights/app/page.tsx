import Link from "next/link";
import { getInsights } from "../lib/sheets";

export default async function Home() {
  const insights = await getInsights();

  const featured = insights[0];

  return (
    <main className="min-h-screen bg-black text-white">

      {/* HERO */}

      <section className="max-w-7xl mx-auto px-8 py-16">

        <h1 className="text-7xl font-bold mb-12">
          AI Insights
        </h1>

        {featured && (
          <div className="mb-20">

            <img
              src={featured.imageUrl}
              alt={featured.title}
              className="w-full h-[500px] object-cover rounded-3xl"
            />

            <p className="text-zinc-500 mt-6">
              FEATURED INSIGHT
            </p>

            <h2 className="text-5xl font-bold mt-4">
              {featured.title}
            </h2>

            <p className="text-zinc-400 mt-6 text-xl">
              {featured.content?.slice(0, 300)}...
            </p>

            <Link
              href={`/blog/${featured.id}`}
              className="inline-block mt-8 text-lg font-semibold"
            >
              Read Article →
            </Link>

          </div>
        )}

        {/* GRID */}

        <div className="grid md:grid-cols-2 gap-10">

          {insights.map((item) => (

            <div
              key={item.id}
              className="border border-zinc-800 rounded-3xl overflow-hidden"
            >

              <img
                src={item.imageUrl}
                alt={item.title}
                className="w-full h-64 object-cover"
              />

              <div className="p-6">

                <p className="text-zinc-500">
                  {item.category}
                </p>

                <h2 className="text-3xl font-bold mt-2">
                  {item.title}
                </h2>

                <p className="text-zinc-400 mt-4">
                  {item.content?.slice(0, 180)}...
                </p>

                <p className="text-zinc-600 mt-4">
                  {item.date}
                </p>

                <Link
                  href={`/blog/${item.id}`}
                  className="inline-block mt-6 font-semibold"
                >
                  Read More →
                </Link>

              </div>

            </div>

          ))}

        </div>

      </section>

    </main>
  );
}