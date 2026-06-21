export default function RelatedArticles() {
    return (
        <section className="mt-32">

            <h2 className="text-4xl font-bold text-zinc-900">
                Related Insights
            </h2>

            <p className="mt-4 text-zinc-500">
                Explore more perspectives on AI agents,
                enterprise intelligence and the future of work.
            </p>

            <div className="mt-12 grid gap-8 md:grid-cols-3">

                <div
                    className="
          rounded-3xl
          border
          border-zinc-200
          p-8
          shadow-sm
          hover:shadow-2xl
          hover:-translate-y-2
          transition-all
          duration-300
          "
                >
                    <h3 className="text-2xl font-bold text-zinc-900 leading-tight">
                        Access Shapes Advantage
                    </h3>

                    <p className="mt-4 text-zinc-500">
                        Read Insight →
                    </p>
                </div>

                <div
                    className="
          rounded-3xl
          border
          border-zinc-200
          p-8
          shadow-sm
          hover:shadow-2xl
          hover:-translate-y-2
          transition-all
          duration-300
          "
                >
                    <h3 className="text-2xl font-bold text-zinc-900 leading-tight">
                        Trust Becomes Infrastructure
                    </h3>

                    <p className="mt-4 text-zinc-500">
                        Read Insight →
                    </p>
                </div>

                <div
                    className="
          rounded-3xl
          border
          border-zinc-200
          p-8
          shadow-sm
          hover:shadow-2xl
          hover:-translate-y-2
          transition-all
          duration-300
          "
                >
                    <h3 className="text-2xl font-bold text-zinc-900 leading-tight">
                        Systems Gain Agency
                    </h3>

                    <p className="mt-4 text-zinc-500">
                        Read Insight →
                    </p>
                </div>

            </div>

        </section>
    );
}