"use client";

import { useState } from "react";
import { EventItem } from "../../mockData/types/index";
import { useRouter } from "next/navigation";
import { slugify } from "../../utils/slugify";

export default function CreateEventPage() {
  const router = useRouter();

  // form state
  const [title, setTitle] = useState("");
  const [organizer, setOrganizer] = useState("Your Company");
  const [location, setLocation] = useState("");
  const [time, setTime] = useState("");
  const [date, setDate] = useState("");
  const [description, setDescription] = useState("");
  const [image, setImage] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    const slug = slugify(`${title}-${organizer}`);

    const newEvent: EventItem = {

      title,
      organizer,
      location,
      time,
      date,
      image: image || "/placeholder.jpg",
    };

    console.log("New Event:", newEvent, "\nDescription:", description);

    // redirect to dashboard after creation
    router.push("/dashboard");
  };

  return (
    <main className="min-h-[calc(100vh-80px)] flex items-center justify-center px-6 py-10">
      <div className="
        w-full max-w-2xl
        bg-white dark:bg-gray-900
        p-10 rounded-2xl
        border border-black/10 dark:border-white/10
        shadow-xl
      ">

        <h1 className="text-3xl font-bold mb-8 text-center dark:text-white">
          Create a New Event
        </h1>

        <form onSubmit={handleSubmit} className="space-y-6">

          {/* TITLE */}
          <div>
            <label className="text-sm font-medium dark:text-gray-200">Event Title</label>
            <input
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
              className="
                w-full p-3 rounded-xl
                border border-black/10 dark:border-white/20
                dark:bg-gray-800 dark:text-white mt-1
              "
              placeholder="Ex: Beach Cleanup"
            />
          </div>

          {/* ORGANIZER */}
          <div>
            <label className="text-sm font-medium dark:text-gray-200">Organizer</label>
            <input
              value={organizer}
              onChange={(e) => setOrganizer(e.target.value)}
              required
              className="
                w-full p-3 rounded-xl
                border border-black/10 dark:border-white/20
                dark:bg-gray-800 dark:text-white mt-1
              "
              placeholder="Your Organization"
            />
          </div>

          {/* LOCATION */}
          <div>
            <label className="text-sm font-medium dark:text-gray-200">Location</label>
            <input
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              required
              className="
                w-full p-3 rounded-xl
                border border-black/10 dark:border-white/20
                dark:bg-gray-800 dark:text-white mt-1
              "
              placeholder="Ex: Central Park"
            />
          </div>

          {/* TIME */}
          <div>
            <label className="text-sm font-medium dark:text-gray-200">Time</label>
            <input
              value={time}
              onChange={(e) => setTime(e.target.value)}
              required
              className="
                w-full p-3 rounded-xl
                border border-black/10 dark:border-white/20
                dark:bg-gray-800 dark:text-white mt-1
              "
              placeholder="Ex: 10:00 - 13:00"
            />
          </div>

          {/* DATE */}
          <div>
            <label className="text-sm font-medium dark:text-gray-200">Date</label>
            <input
              type="date"
              value={date}
              onChange={(e) => setDate(e.target.value)}
              required
              className="
                w-full p-3 rounded-xl
                border border-black/10 dark:border-white/20
                dark:bg-gray-800 dark:text-white mt-1
              "
            />
          </div>

          {/* IMAGE */}
          <div>
            <label className="text-sm font-medium dark:text-gray-200">Image URL</label>
            <input
              value={image}
              onChange={(e) => setImage(e.target.value)}
              className="
                w-full p-3 rounded-xl
                border border-black/10 dark:border-white/20
                dark:bg-gray-800 dark:text-white mt-1
              "
              placeholder="https://example.com/image.jpg"
            />
          </div>

          {/* DESCRIPTION */}
          <div>
            <label className="text-sm font-medium dark:text-gray-200">Description</label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              required
              className="
                w-full min-h-[140px] p-3 rounded-xl
                border border-black/10 dark:border-white/20
                dark:bg-gray-800 dark:text-white mt-1
              "
              placeholder="Describe your event..."
            />
          </div>

          {/* BUTTON */}
          <button
            type="submit"
            className="
              w-full px-6 py-3
              rounded-xl font-semibold
              bg-black text-white
              hover:bg-gray-800
              transition shadow active:scale-95
            "
          >
            Create Event
          </button>
        </form>
      </div>
    </main>
  );
}
