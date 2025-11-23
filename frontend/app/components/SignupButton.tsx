"use client";

import Link from "next/link";

export default function SignupButton() {
    return (
        <Link
            href="/signup"
            className="
        inline-flex items-center justify-center
        px-6 py-3
        rounded-xl
        font-semibold
        text-white
        bg-green-600
        hover:bg-green-700
        shadow
        transition
        active:scale-95
      "
        >
            Sign Up
        </Link>
    );
}
