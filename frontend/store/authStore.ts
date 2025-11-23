import {create} from "zustand";
import {devtools, persist} from "zustand/middleware";
import axios, {AxiosError} from "axios";
import {toast} from "react-hot-toast";

export interface User {
    id: number;
    auth0_id: string;
    name: string;
    email: string;
    role: string;
    total_points: number;
}

export interface Auth0LoginResponse {
    access_token: string;
    expires_in: number;
    id_token: string;
    scope: string;
    token_type: string;
}

export interface SignupData {
    name?: string;
    email: string;
    password: string;
}

export interface LoginData {
    username: string;
    password: string;
}

interface SignupResponse {
    success: boolean;
    auth0: Auth0LoginResponse;
    user: User;
}

interface PasswordRuleItem {
    message: string;
    verified: boolean;
}

interface PasswordRule {
    message: string;
    verified: boolean;
    items?: PasswordRuleItem[];
}

interface Auth0Error {
    message: string;
    description?: { rules?: PasswordRule[] };
}

interface AuthState {
    user: User | null;
    token: string | null;
    loading: boolean;
    error: string | null;

    signup: (data: SignupData) => Promise<void>;
    login: (data: LoginData) => Promise<void>;
    logout: () => void;
    fetchPrivate: () => Promise<unknown>;
    initialize: () => Promise<void>;
}

const API_BASE = "http://localhost:8000";


export const useAuthStore = create<AuthState>()(
    devtools(
        persist(
            (set, get) => ({
                user: null,
                token: null,
                loading: false,
                error: null,

                signup: async (data: SignupData) => {
                    set({loading: true, error: null});
                    try {
                        const res = await axios.post<SignupResponse>(`${API_BASE}/auth/signup`, data);

                        set({user: res.data.user, token: res.data.auth0.access_token, loading: false});
                        toast.success("Account created successfully!");
                    } catch (err) {
                        set({loading: false});
                        handleAuthError(err, set);
                    }
                },

                login: async (data: LoginData) => {
                    set({loading: true, error: null});
                    try {
                        const res = await axios.post<Auth0LoginResponse>(`${API_BASE}/auth/login`, data);

                        const token = res.data.access_token;
                        set({token, loading: false});
                        localStorage.setItem("auth_token", token);
                        toast.success("Logged in successfully!");

                        // fetch user
                        const userRes = await axios.get<User>(`${API_BASE}/users/me`, {
                            headers: {Authorization: `Bearer ${token}`},
                        });
                        set({user: userRes.data});
                    } catch (err) {
                        set({loading: false});
                        handleAuthError(err, set, "Login failed");
                    }
                },

                logout: () => {
                    set({user: null, token: null});
                    localStorage.removeItem("auth_token");
                    toast.success("Logged out successfully!");
                },

                fetchPrivate: async () => {
                    const token = get().token;
                    if (!token) throw new Error("No token available");

                    const res = await axios.get(`${API_BASE}/auth/api/private`, {
                        headers: {Authorization: `Bearer ${token}`},
                    });
                    return res.data;
                },


                initialize: async () => {
                    const token = get().token || localStorage.getItem("auth_token");
                    if (!token) return;

                    set({token, loading: true});

                    try {
                        const userRes = await axios.get<User>(`${API_BASE}/users/me`, {
                            headers: {Authorization: `Bearer ${token}`},
                        });
                        set({user: userRes.data, loading: false});
                    } catch {
                        get().logout(); // token invalid
                    }
                },
            }),
            {
                name: "auth-storage", // key in localStorage
                partialize: (state) => ({token: state.token, user: state.user}),
            }
        )
    )
);

function handleAuthError(err: unknown, set: any, fallbackMessage = "Signup failed") {
    if (axios.isAxiosError(err) && err.response?.data) {
        const data = err.response.data as Auth0Error;

        if (data.description?.rules) {
            const failingRule = data.description.rules.find((r) => !r.verified);
            if (failingRule) toast.error(failingRule.message);
            set({error: "Password requirements not met"});
        } else if (data.message) {
            toast.error(data.message);
            set({error: data.message});
        } else {
            toast.error(fallbackMessage);
            set({error: fallbackMessage});
        }
    } else if (err instanceof Error) {
        toast.error(err.message);
        set({error: err.message});
    } else {
        toast.error(fallbackMessage);
        set({error: fallbackMessage});
    }
}
