export interface Slot {
    id: number;
    name: string;
}

export interface TimeSlot {
    date: string;
    time: number;
}

export interface Booking {
    slot_id: number;
    time_slot: TimeSlot;
    user_id: number;
}

export interface User {
    id: number;
    user: string;
}