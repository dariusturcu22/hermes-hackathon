"use client";

import { useState } from "react";
import EventCard from "./EventCard";
import { events } from "../mockData/events";

export default function HomePage() {
  const [search, setSearch] = useState("");

  const filteredEvents = events.filter((e) =>
    (e.title + e.location + e.organizer)
      .toLowerCase()
      .includes(search.toLowerCase())
  );

  return (
    <main className="px-6 py-10 max-w-[1500px] mx-auto">

      <h1 className="text-3xl font-bold mb-6">Upcoming Volunteer Events</h1>

      <div className="w-full flex justify-end mb-10">
        <input
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full max-w-md p-3 rounded-xl border border-black/10 dark:border-white/20 dark:bg-gray-900"
          placeholder="Search events..."
        />
      </div>

      <div
        className="
          grid
          place-items-center
          grid-cols-1
          sm:grid-cols-2
          lg:grid-cols-3
          gap-10
        "
      >
        {filteredEvents.map((event) => (
          <EventCard key={event.slug} {...event} />
        ))}
      </div>
    </main>
  );
}
