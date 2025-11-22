import EventCard from './EventCard';

export default function HomePage() {
    const events = [
        {
            title: "Clean the Park",
            location: "Central Park",
            time: "10:00 - 13:00 AM",
            organizer: "Green Volunteers",
            image: "/event1.jpg",
        },
        {
            title: "Food Donation",
            location: "City Shelter",
            time: "2:00 - 4:00 PM",
            organizer: "Helping Hands",
            image: "/event2.jpg",
        },
        {
            title: "Beach Cleanup",
            location: "Sunny Beach",
            time: "8:00 - 9:00 AM",
            organizer: "Ocean Lovers",
            image: "/event3.jpg",
        },
    ];

    return (
        <main className="px-6 py-10">
            <h1 className="text-3xl font-bold mb-8 pl-8">Upcoming Volunteer Events</h1>

            <div className="
                grid
                place-items-center
                grid-cols-1
                sm:grid-cols-2
                lg:grid-cols-3
                gap-10
                w-full
                max-w-[1500px]
                mx-auto
                  ">
                {events.map((e, index) => (
                    <EventCard
                        key={index}
                        title={e.title}
                        location={e.location}
                        time={e.time}
                        organizer={e.organizer}
                        image={e.image}
                    />
                ))}
            </div>
        </main>
    );
}