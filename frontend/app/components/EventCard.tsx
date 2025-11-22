"use client";

import Image from "next/image";
import Link from "next/link";

export default function EventCard({
  id,
  title,
  location,
  time,
    date,
  organizer,
  image,

}: {
  id: number|string;
  title: string;
  location: string;
  time: string;
  date:string;
  organizer: string;
  image: string;

}) {
  return (
    <Link href={`/event`}
      className="
        block
        w-full
        max-w-[450px]
        lg:max-w-[480px]
        mx-auto
        rounded-2xl
        overflow-hidden
        bg-white dark:bg-gray-900
        border border-black/10 dark:border-white/10
        shadow-lg hover:shadow-xl
        transition
      "
    >
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
      <div className="px-6 pt-5 pb-6">
        <h2 className="text-xl font-bold mb-2">{title}</h2>
        <p className="text-sm text-gray-600 dark:text-gray-300">{location}</p>
        <p className="text-sm text-gray-600 dark:text-gray-300">{time}, {date}</p>
        <p className="text-xs text-gray-500 dark:text-gray-400 mt-2"></p>
          Organized by <span className="font-semibold">{organizer}</span>
          <p className="text-xs text-gray-500 dark:text-gray-400 mt-2">
          </p>
      </div>
    </Link>
);
}