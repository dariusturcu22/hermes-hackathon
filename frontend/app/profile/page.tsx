"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

type UserVolunteer = {
  type: "volunteer";
  username: string;
  points: number;
};

type UserCompany = {
  type: "company";
  name: string;
  description: string;
  eventsHosted: number;
};

type User = UserVolunteer | UserCompany;

export default function ProfilePage() {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    // 💡 MOCK USER — schimbă aici ca să testezi ambele variante

    const mockUser: User = {
      type: "company", // schimbă în "volunteer"
      name: "Green Future Organization",
      description: "We organize environmental volunteering events.",
      eventsHosted: 12,
    };
    const mockUser2: User = {
      type: "volunteer",
        username: "alex_volunteer",
        points: 340,
    };

    // const mockUser: User = {
    //   type: "volunteer",
    //   username: "alexvolunteer",
    //   points: 340,
    // };
        // eslint-disable-next-line react-hooks/set-state-in-effect
    setUser(mockUser2);
  }, []);

  if (!user)
    return <div className="text-center pt-40 dark:text-white">Loading...</div>;

  const isVolunteer = user.type === "volunteer";

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
        {/* TITLE */}
        <h1 className="text-3xl font-bold mb-6 text-center dark:text-white">
          Profile
        </h1>

        {/* USER INFO */}
        <div className="space-y-6">

          {/* VOLUNTEER VARIANT */}
          {isVolunteer && (
            <>
              <div>
                <p className="text-sm text-gray-500 dark:text-gray-300">
                  Username
                </p>
                <p className="text-xl font-semibold dark:text-white">
                  {user.username}
                </p>
              </div>

              <div>
                <p className="text-sm text-gray-500 dark:text-gray-300">
                  Points
                </p>
                <p className="text-xl font-semibold dark:text-white">
                  {user.points}
                </p>
              </div>
            </>
          )}

          {/* COMPANY VARIANT */}
          {!isVolunteer && (
            <>
              <div>
                <p className="text-sm text-gray-500 dark:text-gray-300">
                  Company Name
                </p>
                <p className="text-xl font-semibold dark:text-white">
                  {user.name}
                </p>
              </div>

              <div>
                <p className="text-sm text-gray-500 dark:text-gray-300">
                  Description
                </p>
                <p className="text-md dark:text-gray-300">
                  {user.description}
                </p>
              </div>

              <div>
                <p className="text-sm text-gray-500 dark:text-gray-300">
                  Events Hosted
                </p>
                <p className="text-xl font-semibold dark:text-white">
                  {user.eventsHosted}
                </p>
              </div>
            </>
          )}
        </div>

        {/* BUTTON → DASHBOARD */}
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
