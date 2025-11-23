"use client";

import {useState} from "react";
import {Home, Trophy, Menu} from "lucide-react";
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger
} from "@/components/ui/dropdown-menu";
import Link from "next/link";
import {useTheme} from "../ThemeProvider";
import {useAuthStore} from "@/store/authStore";

export default function Navbar() {
    const {dark, toggleDark} = useTheme();
    const user = useAuthStore((state) => state.user);

    const logout = useAuthStore((state) => state.logout);


    const [mobileOpen, setMobileOpen] = useState(false);

    return (
        <div>
            <nav
                className={`fixed top-0 left-0 z-50
    h-16 w-full
    flex justify-between items-center
    px-6 py-0
    backdrop-blur-xl
    border-b border-[var(--color-secondary)]/20
    transition-all

    bg-[var(--color-navbar)] bg-opacity-80
    text-[var(--color-text)]`}
            >
                {/* LEFT SIDE */}
                <div className="flex items-center gap-6">

                    {/* LOGO - always visible */}
                    <div className="font-bold text-xl tracking-tight lg:mr-10">VoW</div>

                    <Link
                        href="/home"
                        className="flex items-center gap-2 transition lg:px-5 lg:py-3 lg:rounded-xl lg:border
              lg:border-white/20 lg:bg-white/8 lg:backdrop-blur-xl hover:lg:bg-white/20"
                    >
                        <Home className="w-8 h-8 lg:w-6 lg:h-6"/>
                        <span className="text-sm font-medium hidden lg:block">Home</span>
                    </Link>


                    <Link
                        href="/leaderboard"
                        className="flex items-center gap-2 transition lg:px-5 lg:py-3 lg:rounded-xl lg:border
              lg:border-white/20 lg:bg-gray/8 lg:backdrop-blur-xl hover:lg:bg-white/20"
                    >
                        <Trophy className="w-8 h-8 lg:w-6 lg:h-6"/>
                        <span className="text-sm font-medium hidden lg:block">Leaderboard</span>
                    </Link>


                </div>

                {/* RIGHT SIDE */}
                <div className="flex items-center gap-4">
                    {/* User info */}
                    <div className="text-sm font-medium">Hello, {user?.name || "Guest"}</div>
                    <div
                        className="text-sm font-medium px-3 py-1 rounded-xl backdrop-blur-xl bg-white/10 border border-white/20">
                        {user?.total_points ?? 0} points
                    </div>

                    {/* Desktop dropdown */}
                    <div className="hidden lg:flex items-center gap-4">

                        {/* PROFILE DROPDOWN */}
                        <DropdownMenu>
                            <DropdownMenuTrigger className="cursor-pointer select-none">
                                <span className="text-sm font-medium underline">Menu</span>
                            </DropdownMenuTrigger>

                            <DropdownMenuContent
                                className=" bg-[var(--color-navbar)]
                                            text-[var(--color-text)]
                                            border border-[var(--color-secondary)]/20
                                            backdrop-blur-xl
                                            rounded-xl
                                            shadow-lg">
                                <DropdownMenuItem asChild>
                                    <Link href="/profile">Profile</Link>
                                </DropdownMenuItem>
                                <DropdownMenuItem asChild>
                                    <Link href="/dashboard">Dashboard</Link>
                                </DropdownMenuItem>
                                <DropdownMenuItem asChild>
                                    <Link href="/settings">Settings</Link>
                                </DropdownMenuItem>
                                <DropdownMenuItem onClick={logout}>
                                    Logout
                                </DropdownMenuItem>
                            </DropdownMenuContent>
                        </DropdownMenu>
                    </div>

                    {/* Mobile menu button */}
                    <button
                        className="lg:hidden p-2 rounded-lg bg-white/10 border border-white/20"
                        onClick={() => setMobileOpen(!mobileOpen)}
                    >
                        <Menu className="w-6 h-6"/>
                    </button>

                    {/* Dark mode toggle */}
                    <button
                        onClick={toggleDark}
                        className="text-xl px-4 py-2 rounded-xl backdrop-blur-xl bg-white/10 border border-white/20 hover:bg-white/20 transition hidden lg:block"
                    >
                        {dark ? "☀️" : "🌙"}
                    </button>

                </div>
            </nav>

            {/* MOBILE MENU */}
            {mobileOpen && (
                <div className="lg:hidden bg-gray-950 border-b border-white/10 text-white px-6 py-4 space-y-4">
                    <Link href="/profile" className="block py-2 hover:opacity-80">
                        Profile
                    </Link>
                    <Link href="/dashboard" className="block py-2 hover:opacity-80">
                        Dashboard
                    </Link>
                    <Link href="/settings" className="block py-2 hover:opacity-80">
                        Settings
                    </Link>

                    <button
                        onClick={toggleDark}
                        className="w-full text-left py-2 hover:opacity-80"
                    >
                        Toggle: {dark ? "Light Mode" : "Dark Mode"}
                    </button>
                </div>
            )}
        </div>
    );
}
