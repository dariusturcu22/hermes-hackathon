import Image from "next/image";
import {notFound} from "next/navigation";
import {events} from "../mockData/events";

export default function EventPage({ params,
                                  }: {
    params: { slug: string };
}) {


    const event = events.find(e => e.slug === params.slug);
    if (!event) {
        return notFound();
    }

    return (
        <div className="max-w-4xl mx-auto px-6 py-10">

            {/* IMAGE */}
            <div className="relative w-full h-72 sm:h-96 rounded-2xl overflow-hidden shadow-lg">
                <Image
                    src={event.image}
                    alt={event.title}
                    fill
                    className="object-cover"
                />
            </div>

            {/* TITLE */}
            <h1 className="text-4xl font-bold mt-8">{event.title}</h1>

            {/* ORGANIZER */}
            <p className="text-gray-600 dark:text-gray-300 text-lg mt-2">
                Organized by <span className="font-semibold">{event.organizer}</span>
            </p>

            {/* DETAILS ROW */}
            <div className="flex flex-col sm:flex-row gap-6 mt-6 text-gray-700 dark:text-gray-300">

                <div>
                    <p className="font-semibold">📍 Location</p>
                    <p>{event.location}</p>
                </div>

                <div>
                    <p className="font-semibold">🕒 Time</p>
                    <p>{event.time}</p>
                </div>

                {"date" in event && (
                    <div>
                        <p className="font-semibold">📅 Date</p>
                        <p>{event.date}</p>
                    </div>
                )}
            </div>

            {/* DESCRIPTION */}
            <div className="mt-10">
                <h2 className="text-2xl font-semibold mb-3">About this event</h2>
                <p className="text-gray-700 dark:text-gray-300 leading-relaxed whitespace-pre-line">
                    {event.description}
                </p>
            </div>

            {/* ACTION BUTTON */}
            <button
                className="mt-10 px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-xl shadow-md transition">
                Join Event
            </button>
        </div>
    );
}
