import { getInsights } from "../lib/sheets";

export default async function Home() {
  const insights = await getInsights();

  return (
    <main className="min-h-screen bg-black text-white p-10">
      <h1 className="text-6xl font-bold mb-10">
        AI Insights
      </h1>

      <div className="space-y-8">
        {insights.map((item, index) => (
          <div
            key={index}
            className="border border-zinc-800 rounded-2xl p-6"
          >
            <p className="text-zinc-500">
              {item.category}
            </p>

            <h2 className="text-3xl font-bold mt-2">
              {item.title}
            </h2>

            <p className="text-zinc-400 mt-4">
              {item.content?.slice(0, 250)}...
            </p>
          </div>
        ))}
      </div>
    </main>
  );
}