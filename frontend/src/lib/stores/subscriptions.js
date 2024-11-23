import { writable } from "svelte/store";

export const subscriptions = writable([
  { id: 1, name: "넷플릭스", daysLeft: 7, price: 9900, usedToday: false,logoUrl:"/images/netflix.png"},
  { id: 2, name: "애플뮤직", daysLeft: 13, price: 11000, usedToday: false,logoUrl:"/images/applemusic.png" },
  { id: 3, name: "스포티파이", daysLeft: 21, price: 8700, usedToday: false ,logoUrl:"/images/spotify.png"},
]);