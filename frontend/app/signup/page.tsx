"use client";

import {FormEvent, useEffect, useState} from "react";
import {useRouter} from "next/navigation";
import {useAuthStore} from "@/store/authStore";

export default function SignupPage() {
    const router = useRouter();
    const {signup, loading, user} = useAuthStore();
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    // redirect if already logged in
    useEffect(() => {
        if (user) router.push("/home");
    }, [user, router]);

    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault();
        await signup({email, password});
        const currentUser = useAuthStore.getState().user;
        if (currentUser) router.push("/home");
    };

    return (
        <main className="min-h-[calc(100vh-80px)] flex items-center justify-center">
            <div
                className="w-full max-w-md bg-white dark:bg-gray-900 p-8 rounded-2xl border border-black/10 dark:border-white/10 shadow-xl">
                <h1 className="text-3xl font-bold mb-6 text-center dark:text-white">Sign Up</h1>
                <form className="space-y-5" onSubmit={handleSubmit}>
                    <div>
                        <label className="text-sm font-medium dark:text-gray-200">Email</label>
                        <input
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            placeholder="Choose an email..."
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
                            placeholder="Choose a password..."
                            className="w-full p-3 rounded-xl border border-black/10 dark:border-white/20 dark:bg-gray-800 dark:text-white mt-1"
                            required
                        />
                    </div>
                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full px-6 py-3 rounded-xl font-semibold text-white bg-black hover:bg-gray-800 transition shadow active:scale-95"
                    >
                        {loading ? "Signing up..." : "Create Account"}
                    </button>
                </form>
            </div>
        </main>
    );
}
