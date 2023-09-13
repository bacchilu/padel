import {Booking, TimeSlot} from './types';

export const getSortedTimeSlots = function (bookings: Booking[]) {
    const keys = new Set(bookings.map((b) => `${b.time_slot.date} ${b.time_slot.time}`));
    return [...keys].sort().map<TimeSlot>((k) => {
        const [date, time] = k.split(' ');
        return {date, time: +time};
    });
};

export const getUsers = function (bookings: Booking[], time_slot: TimeSlot, slot_id: number) {
    return bookings
        .filter(
            (booking) =>
                booking.time_slot.date === time_slot.date &&
                booking.time_slot.time === time_slot.time &&
                booking.slot_id === slot_id
        )
        .map((booking) => booking.user_id);
};

export const formatTimeSlot = function (time_slot: TimeSlot) {
    const d = new Date(time_slot.date);
    return `${d.toLocaleDateString()} at ${time_slot.time}`;
};
