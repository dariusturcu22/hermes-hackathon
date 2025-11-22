"use client";

import {useState} from "react";
import {Home, Trophy, Menu, ChevronDown} from "lucide-react";
import {Avatar, AvatarFallback, AvatarImage} from "@/components/ui/avatar";
import {DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger} from "@/components/ui/dropdown-menu";
import Link from "next/link";

export default function Navbar() {
    const [dark, setDark] = useState(true);
    const [mobileOpen, setMobileOpen] = useState(false);

    return (
        <div className={dark ? "dark" : ""}>
            <nav
                className={`h-16 w-full flex justify-between items-center px-6 py-0 backdrop-blur-xl border-b border-white/10 transition-all ${
                    dark ? "bg-gray-950 text-white" : "bg-gray-100 text-black"
                }`}>
                {/* LEFT SIDE */}
                <div className="flex items-center gap-6">

                    {/* LOGO - always visible */}
                    <div className="font-bold text-xl tracking-tight lg:mr-10">VoW</div>

                    <Link
                        href="/home"
                        className="  flex items-center gap-2 transition lg:px-5 lg:py-3 lg:rounded-xl lg:border
                        lg:border-white/20 lg:bg-white/8 lg:backdrop-blur-xl hover:lg:bg-white/20"
                    >
                        <Home className="w-8 h-8 lg:w-6 lg:h-6"/>
                        <span className="text-sm font-medium hidden lg:block">Home</span>
                    </Link>


                    <Link
                        href="/leaderboard"
                        className=" flex items-center gap-2 transition lg:px-5 lg:py-3 lg:rounded-xl lg:border
                        lg:border-white/20 lg:bg-white/8 lg:backdrop-blur-xl hover:lg:bg-white/20    "
                    >
                        <Trophy className="w-8 h-8 lg:w-6 lg:h-6"/>
                        <span className="text-sm font-medium hidden lg:block">Leaderboard</span>
                    </Link>


                </div>

                {/* RIGHT SIDE */}
                <div className="flex items-center gap-4">
                    <div className="text-sm font-medium">Hello name</div>
                    <div
                        className="text-sm font-medium px-3 py-1 rounded-xl backdrop-blur-xl bg-white/10 border border-white/20">0
                        points
                    </div>
                    {/* ON DESKTOP show avatar + dropdown */}
                    <div className="hidden lg:flex items-center gap-4">

                        {/* PROFILE DROPDOWN */}
                        <DropdownMenu>
                            <DropdownMenuTrigger className="flex items-center gap-2 cursor-pointer select-none">
                                <Avatar className="w-8 h-8">
                                    <AvatarImage src="/placeholder.png"/>
                                    <AvatarFallback>N</AvatarFallback>
                                </Avatar>
                                <ChevronDown className="w-4 h-4 opacity-70"/>
                            </DropdownMenuTrigger>
                            <DropdownMenuContent
                                className="bg-gray-900/90 text-white border border-white/10 backdrop-blur-xl rounded-xl">
                                <DropdownMenuItem asChild>
                                    <Link href="/profile">Profile</Link>
                                </DropdownMenuItem>
                                <DropdownMenuItem asChild>
                                    <Link href="/settings">Settings</Link>
                                </DropdownMenuItem>
                            </DropdownMenuContent>
                        </DropdownMenu>
                    </div>

                    {/* MOBILE MENU BUTTON */}
                    <button
                        className="lg:hidden p-2 rounded-lg bg-white/10 border border-white/20"
                        onClick={() => setMobileOpen(!mobileOpen)}>
                        <Menu className="w-6 h-6"/>
                    </button>


                    {/* DARK MODE TOGGLE */}
                    <button
                        onClick={() => setDark(!dark)}
                        className="text-xl px-4 py-2 rounded-xl backdrop-blur-xl bg-white/10 border border-white/20 hover:bg-white/20 transition hidden lg:block">
                        {dark ? "☀️" : "🌙"}
                    </button>
                </div>
            </nav>
            {/* MOBILE MENU DROPDOWN */}
            {mobileOpen && (
                <div className="lg:hidden bg-gray-950 border-b border-white/10 text-white px-6 py-4 space-y-4">
                    <Link href="/profile" className="block py-2 hover:opacity-80">
                        Profile
                    </Link>
                    <Link href="/settings" className="block py-2 hover:opacity-80">
                        Settings
                    </Link>
                    <button
                        onClick={() => setDark(!dark)}
                        className="w-full text-left py-2 hover:opacity-80"
                    >
                        Toggle: {dark ? "Light Mode" : "Dark Mode"}
                    </button>
                </div>
            )}
        </div>
    );
}
