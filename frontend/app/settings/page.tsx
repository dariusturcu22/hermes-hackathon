"use client";

import { useState, useEffect } from "react";
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

export default function SettingsPage() {
  const [user, setUser] = useState<User | null>(null);

  // local form state
  const [field1, setField1] = useState("");
  const [field2, setField2] = useState("");

  useEffect(() => {
    // MOCK USER — schimbă tipul ca să testezi ambele roluri
    const mockUser: User = {
      type: "company", // schimbă în "volunteer" ca să testezi
      name: "Green Future Organization",
      description: "We organize environmental volunteering events.",
      eventsHosted: 12,
    };

    // const mockUser: User = {
    //   type: "volunteer",
    //   username: "alexvolunteer",
    //   points: 340,
    // };
// eslint-disable-next-line react-hooks/set-state-in-effect
    setUser(mockUser);
  }, []);

  useEffect(() => {
    if (!user) return;

    if (user.type === "volunteer") {
        // eslint-disable-next-line react-hooks/set-state-in-effect
      setField1(user.username);
    } else {
      setField1(user.name);
      setField2(user.description);
    }
  }, [user]);

  if (!user)
    return <div className="text-center pt-40 dark:text-white">Loading...</div>;

  const isVolunteer = user.type === "volunteer";

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    console.log("Updated settings:");

    if (isVolunteer) {
      console.log("New username:", field1);
    } else {
      console.log("New company name:", field1);
      console.log("New description:", field2);
    }
  }

  return (
    <main className="min-h-[calc(100vh-80px)] flex items-center justify-center px-6 py-10">
      <div
        className="
          w-full max-w-2xl
          bg-white dark:bg-gray-900
          p-10 rounded-2xl
          border border-black/10 dark:border-white/10
          shadow-xl
        "
      >
        <h1 className="text-3xl font-bold mb-8 text-center dark:text-white">
          Settings
        </h1>

        <form onSubmit={handleSubmit} className="space-y-8">

          {/* VOLUNTEER SETTINGS */}
          {isVolunteer && (
            <>

              <div>
                <label className="text-sm font-medium dark:text-gray-200">
                  Change Username
                </label>
                <input
                  value={field1}
                  onChange={(e) => setField1(e.target.value)}
                  className="
                    w-full p-3 rounded-xl
                    border border-black/10 dark:border-white/20
                    dark:bg-gray-800 dark:text-white mt-1
                  "
                />
              </div>
            </>
          )}

          {/* COMPANY SETTINGS */}
          {!isVolunteer && (
            <>
              {/* COMPANY NAME */}
              <div>
                <label className="text-sm font-medium dark:text-gray-200">
                  Company Name
                </label>
                <input
                  value={field1}
                  onChange={(e) => setField1(e.target.value)}
                  className="
                    w-full p-3 rounded-xl
                    border border-black/10 dark:border-white/20
                    dark:bg-gray-800 dark:text-white mt-1
                  "
                />
              </div>

              {/* DESCRIPTION */}
              <div>
                <label className="text-sm font-medium dark:text-gray-200">
                  Description
                </label>
                <textarea
                  value={field2}
                  onChange={(e) => setField2(e.target.value)}
                  className="
                    w-full min-h-[120px] p-3 rounded-xl
                    border border-black/10 dark:border-white/20
                    dark:bg-gray-800 dark:text-white mt-1
                  "
                />
              </div>
            </>
          )}


          <div>
            <label className="text-sm font-medium dark:text-gray-200">
              Change Password
            </label>
            <Link
              href="/password-reset"
              className="block mt-2 text-blue-600 hover:underline"
            >
              Reset via Auth0
            </Link>
          </div>


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
            Save Changes
          </button>
        </form>

        {/* GO TO DASHBOARD */}
                {/* GO TO DASHBOARD */}
        <div className="mt-10 text-center">
          <Link
            href="/dashboard"
            className="
              px-6 py-3 rounded-xl bg-gray-200 dark:bg-gray-700
              text-black dark:text-white
              font-semibold hover:bg-gray-300 dark:hover:bg-gray-600
              transition active:scale-95
            "
          >
            Back to Dashboard
          </Link>
        </div>

        {/* LOG OUT BUTTON */}
        <div className="mt-6 text-center">
          <button
            onClick={() => {
              console.log("User logged out");
              // viitor: auth0.logout()
              window.location.href = "/";
            }}
            className="
              px-6 py-3
              rounded-xl
              bg-red-600 text-white
              font-semibold
              shadow
              hover:bg-red-700
              transition
              active:scale-95
            "
          >
            Log Out
          </button>
        </div>

      </div>
    </main>
  );
}
