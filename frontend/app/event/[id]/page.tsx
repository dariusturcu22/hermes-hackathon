"use client";

import {useEffect} from "react";
import {useParams} from "next/navigation";
import {useEventStore} from "@/store/eventStore";

export default function EventDetailPage() {
    const params = useParams<{ id: string }>();
    const id = Number(params.id);

    const {events, fetchEvents, getEventById, loading, error} = useEventStore();

    const event = Number.isFinite(id) ? getEventById(id) : undefined;

    useEffect(() => {
        if (!events || events.length === 0) {
            fetchEvents();
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    if (!Number.isFinite(id)) {
        return <p className="px-6 py-10">Invalid event id.</p>;
    }

    if (loading && !event) {
        return <p className="px-6 py-10">Loading event...</p>;
    }

    if (error && !event) {
        return <p className="px-6 py-10 text-red-500">Error: {error}</p>;
    }

    if (!event) {
        return <p className="px-6 py-10">Event not found.</p>;
    }

    return (
        <main className="max-w-3xl mx-auto px-6 py-20">
            <h1 className="text-4xl font-bold mb-4 dark:text-white">{event.title}</h1>
            <p className="text-gray-500 dark:text-gray-400 mb-2">
                {event.location} • {new Date(event.date_start).toLocaleString()} – {" "}
                {new Date(event.date_end).toLocaleString()}
            </p>
            <p className="mb-4 text-sm text-gray-400 dark:text-gray-500">
                Difficulty: {event.difficulty} • Duration: {event.duration_minutes} min •
                Points: {event.proposed_points}
            </p>
            <p className="text-lg dark:text-gray-300 mb-8">{event.description}</p>

            <button className="mt-4 px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-xl shadow-md transition">
                Join Event
            </button>
        </main>
    );
}

