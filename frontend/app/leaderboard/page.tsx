"use client";

import {useEffect} from "react";
import {motion} from "framer-motion";
import UserEntry from "./UserEntry";
import {useUserStore} from "@/store/userStore";

export default function LeaderboardPage() {
    const users = useUserStore((state) => state.users);
    const loading = useUserStore((state) => state.loading);
    const fetchUsers = useUserStore((state) => state.fetchUsers);
    const error = useUserStore((state) => state.error);

    useEffect(() => {
        fetchUsers();
        console.log(users)
    }, []);

    const topUsers = [...(users || [])]
        .sort((a, b) => b.total_points - a.total_points)
        .slice(0, 10);

    if (loading) return <p>Loading leaderboard...</p>;
    if (error) return <p>Error loading leaderboard: {error}</p>;

    return (
        <main className="px-6 py-10">
            <h1 className="text-4xl font-bold mb-10">Leaderboard</h1>

            <motion.div
                initial="hidden"
                animate="visible"
                variants={{
                    hidden: {},
                    visible: {transition: {staggerChildren: 0.15}},
                }}
                className="flex flex-col gap-6"
            >
                {topUsers.map((user, i) => (
                    <motion.div
                        key={user.id}
                        variants={{hidden: {opacity: 0, y: 40}, visible: {opacity: 1, y: 0}}}
                        transition={{duration: 0.5, ease: "easeOut"}}
                    >
                        <UserEntry
                            rank={i + 1}
                            username={user.name || user.auth0_id}
                            points={user.total_points}
                            avatar={user.avatar || "/default-avatar.png"}
                        />
                    </motion.div>
                ))}
            </motion.div>
        </main>
    );
}
