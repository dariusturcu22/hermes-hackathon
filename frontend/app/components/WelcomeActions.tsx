"use client";

import LoginButton from "./LoginButton";
import SignupButton from "./SignupButton";

export default function WelcomeActions() {
  return (
    <div className="flex flex-col items-center justify-center text-center">

      {/* TITLE */}
      <h1 className="text-4xl font-bold mb-10 dark:text-white">
        Welcome to VoW
      </h1>

      {/* BUTTONS */}
      <div className="flex gap-6">
        <LoginButton />
        <SignupButton />
      </div>

    </div>
  );
}
