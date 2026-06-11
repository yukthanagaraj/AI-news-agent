export default function Home() {
  return (
    <main className="min-h-screen bg-black text-white">
      <div className="max-w-7xl mx-auto px-8 py-20">

        <div className="mb-20">
          <p className="uppercase tracking-widest text-zinc-500 mb-4">
            AI INSIGHTS
          </p>

          <h1 className="text-7xl font-bold max-w-4xl leading-tight">
            Intelligence Is Becoming Infrastructure.
          </h1>

          <p className="text-zinc-400 text-xl mt-8 max-w-3xl">
            Executive insights on AI,
            digital workers, enterprise transformation,
            and the future of work.
          </p>
        </div>

        <div className="rounded-3xl overflow-hidden border border-zinc-800">

          <img
            src="https://images.unsplash.com/photo-1677442136019-21780ecad995"
            alt="AI"
            className="w-full h-[600px] object-cover"
          />

          <div className="p-10">

            <p className="text-zinc-500 text-sm">
              ENTERPRISE AI
            </p>

            <h2 className="text-5xl font-bold mt-4">
              AI Owns Outcomes
            </h2>

            <p className="text-zinc-400 mt-6 text-lg">
              The companies that deploy AI workers
              fastest will redefine productivity,
              operations, and competitive advantage.
            </p>

          </div>

        </div>

      </div>
    </main>
  );
}