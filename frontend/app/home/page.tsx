"use client";

import {useEffect, useState} from "react";
import EventCard from "../components/EventCard";
import {useEventStore} from "@/store/eventStore";

export default function HomePage() {
    const events = useEventStore((state) => state.events);
    const loading = useEventStore((state) => state.loading);
    const fetchEvents = useEventStore((state) => state.fetchEvents);
    const searchEventsByName = useEventStore((state) => state.searchEventsByName);

    const [search, setSearch] = useState("");
    const [eventImages, setEventImages] = useState<{ [id: number]: string }>({});

    const IMAGES = [
        "/image1.jpg",
        "/image2.jpg",
        "/image3.jpg",
        "/image4.jpg",
        "/image5.jpg",
    ];

    useEffect(() => {
        fetchEvents();
    }, [fetchEvents]);

    useEffect(() => {
        if (!events.length) return;

        const assigned: { [id: number]: string } = {};
        events.forEach((ev) => {
            assigned[ev.id] = IMAGES[Math.floor(Math.random() * IMAGES.length)];
        });

        setEventImages(assigned);
    }, [events]);

    const filtered = search ? searchEventsByName(search) : events;

    return (
        <main className="px-6 py-10 max-w-[1500px] mx-auto">
            <h1 className="text-3xl font-bold mb-8 pl-8">
                Upcoming Volunteering Events
            </h1>

            <div className="w-full flex justify-start mb-10 pl-8">
                <input
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                    className="w-full max-w-md p-3 rounded-xl border border-black/10 dark:border-white/20 dark:bg-gray-900"
                    placeholder="Search events..."
                />
            </div>

            {loading && <p>Loading...</p>}

            <div className="grid place-items-center grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-10">
                {filtered.map((event) => (
                    <EventCard
                        key={event.id}
                        {...event}
                        image={eventImages[event.id]}
                    />
                ))}
            </div>
        </main>
    );
}
