import axios from 'axios';
import useSWR from 'swr';

import {Booking, Slot, TimeSlot, User} from './types';

interface BookingAPIData {
    slot_id: number;
    data: {user_id: number; time_slot: TimeSlot; callback: {type: 'EMAIL' | 'URL'; value: string}};
}

export const Fetcher = {
    get_slots: async function () {
        const res = await axios.get<Slot[]>('/api/slots');
        return res.data;
    },
    get_bookings: async function () {
        const res = await axios.get<Booking[]>('/api/bookings', {
            transformResponse: [
                (data: string) => {
                    const parsedData = JSON.parse(data) as BookingAPIData[];
                    return parsedData.map((e) => ({
                        slot_id: e.slot_id,
                        time_slot: e.data.time_slot,
                        user_id: e.data.user_id,
                    }));
                },
            ],
        });
        return res.data;
    },
    get_user: async function (user_id: number) {
        const res = await axios.get<User>(`/api/user/${user_id}`);
        return res.data;
    },
};

export const useSlots = function () {
    return useSWR('SLOTS', Fetcher.get_slots, {dedupingInterval: 60000});
};

export const useBookings = function () {
    return useSWR('BOOKINGS', Fetcher.get_bookings, {dedupingInterval: 60000});
};

export const useUser = function (user_id: number) {
    const fetcher = async function () {
        return Fetcher.get_user(user_id);
    };
    return useSWR(`USER_${user_id}`, fetcher, {dedupingInterval: 60000});
};
