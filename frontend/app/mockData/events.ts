import { slugify } from "../utils/slugify";

export const events = [
  {
    title: "Clean the Park",
    organizer: "Green Volunteers",
    slug: slugify("Clean the Park-Green Volunteers"),
    location: "Central Park",
    time: "10:00 - 13:00",
    image: "/event1.jpg",
    date: "2025-01-14",
    description: "Join us for a community cleanup!"
  },
  {
    title: "Food Donation",
    organizer: "Helping Hands",
    slug: slugify("Food Donation-Helping Hands"),
    location: "City Shelter",
    time: "14:00 - 16:00",
    image: "/event2.jpg",
    date: "2025-01-20",
    description: "Help distribute food to families in need."
  },
  {
    title: "Beach Cleanup",
    organizer: "Ocean Lovers",
    slug: slugify("Beach Cleanup-Ocean Lovers"),
    location: "Sunny Beach",
    time: "08:00 - 09:00",
    image: "/event3.jpg",
    date: "2025-01-22",
    description: "Clean the beach and recycle waste."
  }
];
