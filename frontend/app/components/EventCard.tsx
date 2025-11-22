"use client";

import Image from "next/image";
import Link from "next/link";
import {Event} from "@/store/eventStore";

interface EventCardProps extends Event {
    image?: string;
}

export default function EventCard({
                                      id,
                                      title,
                                      location,
                                      date_start,
                                      date_end,
                                      organization_name,
                                      image,
                                  }: EventCardProps) {
    const date = new Date(date_start).toLocaleDateString();
    const time = `${new Date(date_start).toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
    })} - ${new Date(date_end).toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
    })}`;

    const displayImage = image || "/placeholder.jpg";

    return (
        <Link
            href={`/event/${id}`} // use event ID for the page
            className="
        block w-full max-w-[450px] lg:max-w-[480px] mx-auto
        rounded-2xl overflow-hidden bg-white dark:bg-gray-900
        border border-black/10 dark:border-white/10
        shadow-lg hover:shadow-xl transition
      "
        >
            <div className="relative w-full h-72 bg-[var(--color-card)] border border-[var(--color-secondary)]">
                <Image src={displayImage} alt={title} fill className="object-cover"/>
            </div>

            <div className="px-6 pt-5 pb-6 bg-[var(--color-bg-medium2)]">
                <h2 className="text-xl font-bold mb-2">{title}</h2>
                <p className="text-sm text-[var(--color-text)]">{location}</p>
                <p className="text-sm text-[var(--color-text)]">
                    {time}, {date}
                </p>
                <p className="text-xs text-[var(--color-text)] mt-2">
                    Organized by <span className="font-semibold">{organization_name}</span>
                </p>
            </div>
        </Link>
    );
}
