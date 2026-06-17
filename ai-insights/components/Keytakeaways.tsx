export default function KeyTakeaways({
    items,
}: {
    items: string[];
}) {
    return (
        <div className="my-12 rounded-3xl border border-orange-200 bg-orange-50 p-8">

            <h3 className="mb-6 text-2xl font-bold text-orange-700">
                Key Takeaways
            </h3>

            <ul className="space-y-4">

                {items.map((item, index) => (

                    <li
                        key={index}
                        className="text-lg text-zinc-700"
                    >
                        • {item}
                    </li>

                ))}

            </ul>

        </div>
    );
}