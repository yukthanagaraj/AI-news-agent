export default function NewsletterBox() {
    return (
        <section className="mt-32 rounded-[2rem] bg-orange-50 p-12">

            <h2 className="text-5xl font-bold text-zinc-900">
                Stay Ahead of AI
            </h2>

            <p className="mt-6 text-xl text-zinc-600">
                Enterprise intelligence powered by live news.
            </p>

            <button
                className="
                mt-10
                rounded-full
                bg-orange-600
                px-8
                py-4
                font-semibold
                text-white
                "
            >
                Subscribe →
            </button>

        </section>
    );
}