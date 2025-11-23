"use client";

import {Avatar, AvatarFallback, AvatarImage} from "@/components/ui/avatar";

export default function UserEntry({
                                      rank,
                                      username,
                                      points,
                                      avatar,
                                  }: {
    rank: number;
    username: string;
    points: number;
    avatar: string;
}) {
    // FULL card color per rank
    const cardColors: Record<number, string> = {
        1: "bg-yellow-200/40 border-yellow-400/60",   // gold
        2: "bg-blue-200/40 border-gray-400/60",       // silver
        3: "bg-gray-700/20 border-amber-800/40",     // bronze
    };


    const glow =
        rank === 1
            ? "shadow-[0_0_25px_rgba(255,215,0,0.75)] ring-2 ring-yellow-400"
            : "";

    return (
        <div className="relative w-full flex justify-center">


            {/* CARD */}
            <div
                className={`
          w-full max-w-xl 
          flex items-center justify-between
          rounded-2xl p-4
          transition shadow-md hover:shadow-xl
          border
          ${cardColors[rank] ?? "bg-white dark:bg-gray-900 border-black/10 dark:border-white/10"}
          ${glow}
        `}
            >
                {/* LEFT SIDE */}
                <div className="flex items-center gap-4">
                    {/* Rank Badge */}
                    <div
                        className="
              w-10 h-10 flex items-center justify-center
              rounded-full font-bold bg-black/20 text-white
            "
                    >
                        {rank}
                    </div>

                    {/* Avatar */}
                    <Avatar className="w-12 h-12">
                        <AvatarImage src={avatar}/>
                        <AvatarFallback>{username[0]}</AvatarFallback>
                    </Avatar>

                    {/* Username */}
                    <span className="text-lg font-semibold">{username}</span>
                </div>

                {/* Points */}
                <span className="text-lg font-bold opacity-80">{points} pts</span>
            </div>
        </div>
    );
}
