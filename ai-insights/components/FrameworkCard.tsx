export default function FrameworkCard({
    title,
    items,
}: {
    title: string;
    items: string[];
}) {
    return (
        <div className="my-12 rounded-3xl bg-zinc-900 p-8 text-white">

            <h3 className="mb-6 text-2xl font-bold">
                {title}
            </h3>

            <div className="space-y-4">

                {items.map((item, index) => (

                    <div
                        key={index}
                        className="rounded-2xl bg-zinc-800 p-4"
                    >
                        {item}
                    </div>

                ))}

            </div>

        </div>
    );
}