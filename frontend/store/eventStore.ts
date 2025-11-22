import {create} from "zustand";
import {devtools} from "zustand/middleware";

export interface Event {
    id: number;
    title: string;
    description: string;
    location: string;
    date_start: string;
    date_end: string;
    difficulty: string;
    duration_minutes: number;
    proposed_points: number;
    final_points?: number;
    max_participants: number;
    organization_id: number;
    organization_name?: string;
    status: string;
    created_at: string;
    updated_at: string;
}

interface EventState {
    events: Event[];
    loading: boolean;
    error: string | null;
    fetchEvents: (params?: {
        organization_id?: number;
        status?: string;
        difficulty?: string;
        skip?: number;
        limit?: number;
    }) => Promise<void>;
    getEventById: (id: number) => Event | undefined;
    searchEventsByName: (query: string) => Event[];
}

export const useEventStore = create<EventState>()(
    devtools((set, get) => ({
        events: [],
        loading: false,
        error: null,

        fetchEvents: async (params = {}) => {
            set({loading: true, error: null});
            try {
                const query = new URLSearchParams();
                if (params.organization_id) query.append("organization_id", params.organization_id.toString());
                if (params.status) query.append("status", params.status);
                if (params.difficulty) query.append("difficulty", params.difficulty);
                if (params.skip) query.append("skip", params.skip.toString());
                if (params.limit) query.append("limit", params.limit.toString());

                const res = await fetch(`http://localhost:8000/events?${query.toString()}`);
                const data = await res.json();

                if (!res.ok) throw new Error(data.detail || "Failed to fetch events");

                set({events: data.data, loading: false});
            } catch (err: unknown) {
                // eslint-disable-next-line @typescript-eslint/ban-ts-comment
                // @ts-expect-error
                set({error: err.message || "Unknown error", loading: false});
            }
        },

        getEventById: (id: number) => {
            return get().events.find((e) => e.id === id);
        },

        searchEventsByName: (query: string) => {
            return get().events.filter((e) =>
                e.title.toLowerCase().includes(query.toLowerCase())
            );
        },
    }))
);
