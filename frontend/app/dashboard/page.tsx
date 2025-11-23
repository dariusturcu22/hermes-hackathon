"use client";

import {useState, useEffect} from "react";
import EventCard from "../components/EventCard";
import type {User, EventItem} from "../mockData/types/index";
import Link from "next/link";


export default function DashboardPage() {
    const [user, setUser] = useState<User | null>(null);

    const volunteerEvents: EventItem[] = [
        {
            title: "Beach Cleanup",
            organizer: "Ocean Lovers",
            image: "/event3.jpg",
            location: "Sunny Beach",
            time: "08:00 - 09:00",
            date: "2025-01-22",
        },
    ];

    const companyEvents: EventItem[] = [
        {
            title: "Food Drive",
            organizer: "Helping Hands",
            image: "/event2.jpg",
            location: "City Center",
            time: "14:00 - 16:00",
            date: "2025-01-20",
        },
    ];

    useEffect(() => {
        const mockUser: User = {
            type: "volunteer",
            name: "Alex",
        };
        const mockCompany: User = {
            type: "company",
            name: "ONG",
        };


        // eslint-disable-next-line react-hooks/set-state-in-effect
        setUser(mockUser);
    }, []);

    if (!user) return <div className="text-center pt-40">Loading...</div>;

    const isVolunteer = user.type === "volunteer";
    const events = isVolunteer ? volunteerEvents : companyEvents;

    return (
        <main className="px-6 py-10 max-w-5xl mx-auto">
            <h1 className="text-3xl font-bold mb-8">
                Dashboard – Welcome, {user.name}
            </h1>

            {events.length === 0 ? (
                <EmptyState isVolunteer={isVolunteer}/>
            ) : (
                <EventsGrid events={events}/>
            )}

            {!isVolunteer && (
                <div className="mt-10">
                    <Link
                        href="/event/create"
                        className=" px-6 py-3 rounded-xl font-semibold shadow hover:bg-gray-800 transition"
                    >
                        Add New Event
                    </Link>
                </div>
            )}
        </main>
    );
}

function EventsGrid({events}: { events: EventItem[] }) {
    return (
        <div className=" grid grid-cols-1 sm:grid-cols-2 gap-8">
            {events.map((event, index) => (
                <EventCard id={0} description={""} date_start={""} date_end={""} difficulty={""} duration_minutes={0}
                           proposed_points={0} max_participants={0} organization_id={0} status={""} created_at={""}
                           updated_at={""} key={index} {...event} />
            ))}
        </div>
    );
}

function EmptyState({isVolunteer}: { isVolunteer: boolean }) {
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
