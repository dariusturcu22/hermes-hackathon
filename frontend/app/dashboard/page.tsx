"use client";

import { useState, useEffect } from "react";
import EventCard from "../components/EventCard";
import type { User, EventItem } from "../mockData/types/index";

export default function DashboardPage() {
  // User state NOW uses a real type, not "any"
  const [user, setUser] = useState<User | null>(null);

  // Mock events with correct type
  const volunteerEvents: EventItem[] = [
    {
      title: "Beach Cleanup",
      organizer: "Ocean Lovers",
      image: "/event3.jpg",
      location: "Sunny Beach",
      time: "08:00 - 09:00",
      date:"2025-01-22",
    },
  ];


  const companyEvents: EventItem[] = [
    {
      title: "Food Drive",
      organizer: "Helping Hands",
      image: "/event2.jpg",
      location: "City Center",
      time: "14:00 - 16:00",
      date:"2025-01-20",
    },
  ];

  useEffect(() => {
    // Simulate logged-in user
    const mockUser: User = {
      type: "volunteer", // change to "company" to test
      name: "Alex",
    };
    const mockCompany: User = {
      type: "company", // change to "company" to test
      name: "ONG",
    };


      // eslint-disable-next-line react-hooks/set-state-in-effect
    setUser(mockUser);
  }, []);

  if (!user) return <div className="text-center pt-40">Loading...</div>;

  const isVolunteer = user.type === "volunteer";
  const events = isVolunteer ? [] : companyEvents;

  return (
    <main className="px-6 py-10 max-w-5xl mx-auto">
      <h1 className="text-3xl font-bold mb-8 dark:text-white">
        Dashboard – Welcome, {user.name}
      </h1>

      {events.length === 0 ? (
        <EmptyState isVolunteer={isVolunteer} />
      ) : (
        <EventsGrid events={events} />
      )}

      {!isVolunteer && (
        <div className="mt-10">
          <a
            href="/event/create"
            className="px-6 py-3 rounded-xl bg-black text-white font-semibold shadow hover:bg-gray-800 transition"
          >
            Add New Event
          </a>
        </div>
      )}
    </main>
  );
}

function EventsGrid({ events }: { events: EventItem[] }) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 gap-8">
      {events.map((event, index) => (
        <EventCard slug={""} key={index} {...event} />
      ))}
    </div>
  );
}

function EmptyState({ isVolunteer }: { isVolunteer: boolean }) {
  return (
    <div className="text-center py-20">
      <h2 className="text-2xl font-bold mb-4 dark:text-white">
        {isVolunteer
          ? "You are not enrolled in any events yet."
          : "You haven't created any events yet."}
      </h2>

      <p className="text-gray-600 dark:text-gray-300 mb-8">
        {isVolunteer
          ? "Discover events and start volunteering today!"
          : "Start by creating an event to recruit volunteers."}
      </p>

      <a
        href={isVolunteer ? "/home" : "/event/create"}
        className="px-6 py-3 rounded-xl bg-black text-white font-semibold shadow hover:bg-gray-800 transition inline-block"
      >
        {isVolunteer ? "Browse Events" : "Create Event"}
      </a>
    </div>
  );
}
