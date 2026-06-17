export default function QuoteBox({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <div className="my-12 rounded-3xl border-l-4 border-orange-500 bg-orange-50 p-8">

            <p className="text-2xl italic font-semibold leading-relaxed text-zinc-900">
                {children}
            </p>

        </div>
    );
}