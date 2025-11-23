"use client";

import {useEffect} from "react";
import Link from "next/link";
import {useAuthStore} from "@/store/authStore";

export default function ProfilePage() {
    const user = useAuthStore((state) => state.user);
    const initialize = useAuthStore((state) => state.initialize);

    useEffect(() => {
        initialize();
    }, [initialize]);

    if (!user)
        return <div className="text-center pt-40 dark:text-white">Loading...</div>;

    const isVolunteer = user.role === "volunteer";

    return (
        <main className="min-h-[calc(100vh-80px)] flex items-center justify-center px-6 py-10">
            <div
                className="
        w-full max-w-xl
        bg-white dark:bg-gray-900
        p-10 rounded-2xl
        border border-black/10 dark:border-white/10
        shadow-xl
      "
            >
                <h1 className="text-3xl font-bold mb-6 text-center dark:text-white">
                    Profile
                </h1>

                <div className="space-y-6">

                    {isVolunteer && (
                        <>
                            <div>
                                <p className="text-sm text-gray-500 dark:text-gray-300">Name</p>
                                <p className="text-xl font-semibold dark:text-white">
                                    {user.name}
                                </p>
                            </div>

                            <div>
                                <p className="text-sm text-gray-500 dark:text-gray-300">
                                    Email
                                </p>
                                <p className="text-xl font-semibold dark:text-white">
                                    {user.email}
                                </p>
                            </div>

                            <div>
                                <p className="text-sm text-gray-500 dark:text-gray-300">
                                    Points
                                </p>
                                <p className="text-xl font-semibold dark:text-white">
                                    {user.total_points}
                                </p>
                            </div>
                        </>
                    )}

                    {!isVolunteer && (
                        <>
                            <div>
                                <p className="text-sm text-gray-500 dark:text-gray-300">
                                    Organizer Name
                                </p>
                                <p className="text-xl font-semibold dark:text-white">
                                    {user.name}
                                </p>
                            </div>

                            <div>
                                <p className="text-sm text-gray-500 dark:text-gray-300">
                                    Email
                                </p>
                                <p className="text-xl font-semibold dark:text-white">
                                    {user.email}
                                </p>
                            </div>
                        </>
                    )}
                </div>

                <div className="mt-10 flex justify-center">
                    <Link
                        href="/dashboard"
                        className="
              px-6 py-3 rounded-xl bg-black text-white
              font-semibold shadow hover:bg-gray-800
              transition active:scale-95
            "
                    >
                        Go to Dashboard
                    </Link>
                </div>
            </div>
        </main>
    );
}
