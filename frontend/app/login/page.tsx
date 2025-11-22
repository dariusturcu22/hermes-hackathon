"use client";

import { useState } from "react";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  return (
    <main className="min-h-[calc(100vh-80px)] flex items-center justify-center">
      <div className="w-full max-w-md bg-white dark:bg-gray-900 p-8 rounded-2xl border border-black/10 dark:border-white/10 shadow-xl">

        <h1 className="text-3xl font-bold mb-6 text-center dark:text-white">
          Log In
        </h1>

        <form className="space-y-5">

          <div>
            <label className="text-sm font-medium dark:text-gray-200">Email</label>
            <input
              type="email"
              className="w-full p-3 rounded-xl border border-black/10 dark:border-white/20 dark:bg-gray-800 dark:text-white mt-1"
              placeholder="Enter your email..."
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>

          <div>
            <label className="text-sm font-medium dark:text-gray-200">Password</label>
            <input
              type="password"
              className="w-full p-3 rounded-xl border border-black/10 dark:border-white/20 dark:bg-gray-800 dark:text-white mt-1"
              placeholder="Enter your password..."
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <button
            type="submit"
            className="
              w-full px-6 py-3 rounded-xl
              font-semibold text-white
              bg-black hover:bg-gray-800
              transition shadow active:scale-95
            "
          >
            Log In
          </button>

        </form>

        <p className="text-center text-sm mt-4 dark:text-gray-300">
          Don’t have an account?
          <a href="/signup" className="text-blue-600 hover:underline ml-1">
            Sign Up
          </a>
        </p>

      </div>
    </main>
  );
}
