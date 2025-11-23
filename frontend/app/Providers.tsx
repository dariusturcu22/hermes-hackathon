"use client";

import ThemeProvider from "./ThemeProvider";
import {Toaster} from "react-hot-toast";
import {QueryClient, QueryClientProvider} from "@tanstack/react-query";

const queryClient = new QueryClient();

export default function Providers({children}: { children: React.ReactNode }) {
    return (
        <ThemeProvider>
            <QueryClientProvider client={queryClient}>
                <Toaster position="bottom-center" reverseOrder={false}/>
                {children}
            </QueryClientProvider>
        </ThemeProvider>
    );
}

