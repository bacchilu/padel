import React from 'react';
import {createRoot} from 'react-dom/client';

import {useBookings, useSlots, useUser} from './hooks';
import {formatTimeSlot, getSortedTimeSlots, getUsers} from './utils';
import {TimeSlot} from './types';

const UserLabel: React.FC<{user_id: number}> = function ({user_id}) {
    const {data: user} = useUser(user_id);
    if (user === undefined) return null;

    return <span className="me-2">{user.user}</span>;
};

const Cell: React.FC<{time_slot: TimeSlot; slot_id: number}> = function ({time_slot, slot_id}) {
    const {data: bookings} = useBookings();
    if (bookings === undefined) return null;

    const users = getUsers(bookings, time_slot, slot_id);
    const userLabels = users.map((user_id) => <UserLabel key={user_id} user_id={user_id} />);
    return <td>{userLabels}</td>;
};

const Table = function () {
    const {data: slots} = useSlots();
    const {data: bookings} = useBookings();

    if (slots === undefined || bookings === undefined)
        return (
            <div className="spinner-border" role="status">
                <span className="visually-hidden">Loading...</span>
            </div>
        );

    const slotColumns = slots.map((slot) => (
        <th key={slot.id} scope="col">
            {slot.name}
        </th>
    ));

    const sortedTimeSlots = getSortedTimeSlots(bookings);
    const rows = sortedTimeSlots.map((time_slot) => {
        const cells = slots.map((slot) => <Cell key={slot.id} time_slot={time_slot} slot_id={slot.id} />);
        return (
            <tr key={`${time_slot.date} ${time_slot.time}`}>
                <th scope="row">{formatTimeSlot(time_slot)}</th>
                {cells}
            </tr>
        );
    });

    return (
        <table className="table table-bordered">
            <thead>
                <tr>
                    <th scope="col">#</th>
                    {slotColumns}
                </tr>
            </thead>
            <tbody>{rows}</tbody>
        </table>
    );
};

const App = function () {
    return (
        <>
            <h1>Hello Padel!</h1>
            <Table />
        </>
    );
};

createRoot(document.getElementById('app')!).render(<App />);
