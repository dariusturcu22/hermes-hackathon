export default function GenericEventPage() {
    return (
        <main className="max-w-3xl mx-auto px-6 py-20">
            <h1 className="text-4xl font-bold mb-6 dark:text-white">
                Event Details
            </h1>

            <p className="text-lg dark:text-gray-300">
                This is a generic event page that all events lead to.
            </p>

            <p className="mt-4 text-gray-500 dark:text-gray-400">
                Later you can add dynamic data or different content here.
            </p>

            <button
                className="mt-10 px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-xl shadow-md transition">
                Join Event
            </button>
        </main>
    );
}
