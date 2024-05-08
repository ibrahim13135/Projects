import { User } from '../types';

export const useUserActions = () => {

    const validate = () => {
        if (localStorage.getItem('token') && localStorage.getItem('token') !== 'undefined') {
            return true;
        } else {
            return false;
        }
    }

    const getUserInfo = async (id: number) => {
        if (!validate()) return null;
        const user = await fetch(`http://127.0.0.1:5001/user/${id}`, {
            method: 'GET',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token') || ''}`
            },
        })
        .then(response => response.json())
        .then((data: User) => {
            return data;
        });
        return user;
    }
    

    return { getUserInfo };
};