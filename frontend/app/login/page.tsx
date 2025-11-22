"use client";

import {FormEvent, useState} from "react";
import {useRouter} from "next/navigation";
import {useAuthStore} from "@/store/authStore";

export default function LoginPage() {
    const router = useRouter();
    const {login, loading, user} = useAuthStore();
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    // redirect immediately if user exists
    if (user) {
        router.push("/home");
        return null; // render nothing while redirecting
    }

    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault();
        try {
            await login({username: email, password});
            router.push("/home");
        } catch {
            // errors already handled via toast in store
        }
    };

    return (
        <main className="min-h-[calc(100vh-80px)] flex items-center justify-center">
            <div
                className="w-full max-w-md bg-white dark:bg-gray-900 p-8 rounded-2xl border border-black/10 dark:border-white/10 shadow-xl">
                <h1 className="text-3xl font-bold mb-6 text-center dark:text-white">Log In</h1>
                <form className="space-y-5" onSubmit={handleSubmit}>
                    <div>
                        <label className="text-sm font-medium dark:text-gray-200">Email</label>
                        <input
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            placeholder="Enter your email..."
                            className="w-full p-3 rounded-xl border border-black/10 dark:border-white/20 dark:bg-gray-800 dark:text-white mt-1"
                            required
                        />
                    </div>
                    <div>
                        <label className="text-sm font-medium dark:text-gray-200">Password</label>
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            placeholder="Enter your password..."
                            className="w-full p-3 rounded-xl border border-black/10 dark:border-white/20 dark:bg-gray-800 dark:text-white mt-1"
                            required
                        />
                    </div>
                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full px-6 py-3 rounded-xl font-semibold text-white bg-black hover:bg-gray-800 transition shadow active:scale-95"
                    >
                        {loading ? "Logging in..." : "Log In"}
                    </button>
                </form>
                <p className="text-center text-sm mt-4 dark:text-gray-300">
                    Don’t have an account?
                    <a href="/signup" className="text-blue-600 hover:underline ml-1">Sign Up</a>
                </p>
            </div>
        </main>
    );
}
