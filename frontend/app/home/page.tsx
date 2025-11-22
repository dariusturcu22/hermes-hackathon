"use client";

import { useState } from "react";
import EventCard from "./EventCard";

export default function HomePage() {
  const [search, setSearch] = useState("");

  const events = [
    {
      title: "Clean the Park",
      location: "Central Park",
      time: "10:00 - 13:00",
      organizer: "Green Volunteers",
      image: "/event1.jpg",
    },
    {
      title: "Food Donation",
      location: "City Shelter",
      time: "14:00 - 16:00",
      organizer: "Helping Hands",
      image: "/event2.jpg",
    },
    {
      title: "Beach Cleanup",
      location: "Sunny Beach",
      time: "08:00 - 09:00",
      organizer: "Ocean Lovers",
      image: "/event3.jpg",
    },
  ];

  const filteredEvents = events.filter((e) =>
    (e.title + e.location + e.organizer)
      .toLowerCase()
      .includes(search.toLowerCase())
  );

  return (
    <main className="px-6 py-10 max-w-[1500px] mx-auto">

      {/* TITLE */}
      <h1 className="text-3xl font-bold mb-6">Upcoming Volunteer Events</h1>

      {/* SEARCH BAR */}
      <div className="w-full flex justify-end mb-10">
        <input
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full max-w-md p-3 rounded-xl border border-black/10 dark:border-white/20 dark:bg-gray-900"
            placeholder="Search events..."
        />
      </div>

      {/* GRID OF EVENTS */}
      <div className="
        grid 
        place-items-center
        grid-cols-1 
        sm:grid-cols-2 
        lg:grid-cols-3 
        gap-10
      ">
        {filteredEvents.map((e, index) => (
            <EventCard key={index} {...e} />
        ))}
      </div>
    </main>
  );
}
