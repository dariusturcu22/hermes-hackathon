export type User = {
    name: string;
    type: "volunteer" | "company";
};

export type EventItem = {
    title: string;
    organizer: string;
    location: string;
    time: string;
    date: string
    image: string;

};
