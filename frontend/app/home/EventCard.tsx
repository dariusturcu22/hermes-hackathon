"use client";

import Image from "next/image";

export default function EventCard(
    { title, location, time, organizer, image }: {
  title: string;
  location: string;
  time: string;
  organizer: string;
  image: string;
}) {
  return (
    <div className="
       w-full
        max-w-[380px]
        lg:max-w-[420px]
        mx-auto
        rounded-2xl
        overflow-hidden
        bg-white dark:bg-gray-900
        border border-black/10 dark:border-white/10
        shadow-lg hover:shadow-xl
        transition
    ">
      {/* IMAGE */}
      <div className="relative w-full h-72">
        <Image
          src={image}
          alt={title}
          fill
          className="object-cover"
        />
      </div>

      {/* TEXT */}
      <div className="p-6">
        <h2 className="text-2xl font-bold mb-3">{title}</h2>
        <p className="text-base text-gray-600 dark:text-gray-300">{location}</p>
        <p className="text-base text-gray-600 dark:text-gray-300">{time}</p>
        <p className="text-sm text-gray-500 dark:text-gray-400 mt-3">
          Organized by <span className="font-semibold">{organizer}</span>
        </p>
      </div>
    </div>
  );
}
