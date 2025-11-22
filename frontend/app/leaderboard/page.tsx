"use client";

import { motion } from "framer-motion";
import UserEntry from "./UserEntry";

export default function LeaderboardPage() {
  const topUsers = [
    { rank: 1, username: "Alice", points: 3200, avatar: "/p1.png" },
    { rank: 2, username: "Bob", points: 2975, avatar: "/p2.png" },
    { rank: 3, username: "Chris", points: 2500, avatar: "/p3.png" },
    { rank: 4, username: "Diana", points: 2200, avatar: "/p4.png" },
    { rank: 5, username: "Evan", points: 1800, avatar: "/p5.png" },
  ];

  return (
    <main className="px-6 py-10">
      <h1 className="text-4xl font-bold mb-10">Leaderboard</h1>

      <motion.div
        initial="hidden"
        animate="visible"
        variants={{
          hidden: {},
          visible: {
            transition: {
              staggerChildren: 0.15, // întârziere între carduri
            },
          },
        }}
        className="flex flex-col gap-6"
      >
        {topUsers.map((user) => (
          <motion.div
            key={user.rank}
            variants={{
              hidden: { opacity: 0, y: 40 },
              visible: { opacity: 1, y: 0 },
            }}
            transition={{ duration: 0.5, ease: "easeOut" }}
          >
            <UserEntry {...user} />
          </motion.div>
        ))}
      </motion.div>
    </main>
  );
}
