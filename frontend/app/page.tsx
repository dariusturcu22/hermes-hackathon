"use client";

import Image from "next/image";
import LoginButton from "./components/LoginButton";
import SignupButton from "./components/SignupButton";

export default function LandingPage() {
  return (
    <main className="min-h-screen flex flex-col lg:flex-row items-center justify-center px-8 gap-16 pt-20">

      {/* LEFT SIDE - IMAGE */}
      <div className="w-full lg:w-1/2 flex justify-center">
        <div className="relative w-[300px] h-[300px] sm:w-[400px] sm:h-[400px] lg:w-[500px] lg:h-[500px]">
          <Image
            src="/landing-illustration2.png"
            alt="Volunteering Illustration"
            fill
            className="object-contain"
          />
        </div>
      </div>

      {/* RIGHT SIDE - TEXT + BUTTONS */}
      <div className="w-full lg:w-1/2 flex flex-col items-center lg:items-start text-center lg:text-left">

        <h1 className="text-5xl sm:text-6xl font-extrabold mb-4 dark:text-white">
          VoW
        </h1>

        <p className="text-lg text-gray-600 dark:text-gray-300 max-w-md mb-8">
          Volunteering made simple. Discover, join, and track meaningful events
          that make a real difference.
        </p>

        {/* BUTTONS USING YOUR COMPONENTS */}
        <div className="flex gap-4">
          <LoginButton />
          <SignupButton />
        </div>

      </div>
    </main>
  );
}
