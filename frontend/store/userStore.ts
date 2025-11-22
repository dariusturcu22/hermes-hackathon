// store/users.ts
import {create} from "zustand";
import axios from "axios";

export interface User {
    id: number;
    auth0_id: string;
    name: string;
    email: string;
    role: "volunteer" | "organizer";
    total_points: number;
    avatar?: string; // optional
}

interface UserStore {
    users: User[];
    loading: boolean;
    error: string | null;
    fetchUsers: () => Promise<void>;
}

export const useUserStore = create<UserStore>((set) => ({
    users: [],
    loading: false,
    error: null,
    fetchUsers: async () => {
        set({loading: true, error: null});
        try {
            const res = await axios.get("http://127.0.0.1:8000/users/"); // full URL
            set({users: res.data.data, loading: false});
        } catch (err: any) {
            set({error: err.message, loading: false});
        }
    },
}));
