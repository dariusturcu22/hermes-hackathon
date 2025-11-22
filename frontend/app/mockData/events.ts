import { slugify } from "../utils/slugify";

export const events = [
  {
    title: "Clean the Park",
    organizer: "Green Volunteers",
    slug: slugify("Clean the Park-Green Volunteers"),
    location: "Central Park",
    time: "10:00 - 13:00",
    date: "2025-01-14",
    image: "/event1.jpg",
    description: `
Join us for a community cleanup! 
We will be collecting trash and recyclables,
and helping restore the beauty of the park.
    `,
  },

  {
    title: "Food Donation",
    organizer: "Helping Hands",
    slug: slugify("Food Donation-Helping Hands"),
    location: "City Shelter",
    time: "14:00 - 16:00",
    date: "2025-01-20",
    image: "/event2.jpg",
    description: `
Help deliver and distribute food to families in need.
Every contribution matters!
    `,
  },

  {
    title: "Beach Cleanup",
    organizer: "Ocean Lovers",
    slug: slugify("Beach Cleanup-Ocean Lovers"),
    location: "Sunny Beach",
    time: "08:00 - 09:00",
    date: "2025-01-22",
    image: "/event3.jpg",
    description: `
Join our community effort to clean the beach and recycle waste.
Let's make a difference!
    `,
  },

];
