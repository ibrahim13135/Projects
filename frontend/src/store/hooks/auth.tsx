import { useAppStore } from "../store";

export const useAuthActions = () => {
    const {state, dispatch } = useAppStore();

    const validate = () => {
        if (localStorage.getItem('token') && localStorage.getItem('token') !== 'undefined') {
            return true;
        } else {
            return false;
        }
    }
    
    const me = async () => {
        validate() &&
        fetch('http://127.0.0.1:5001/auth/me', {
            method: 'GET',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token') || ''}` 
            },
        })
        .then(response => response.json())
        .then(data => {
            dispatch({ type: 'SET_USER', payload: data });
        });
    };

    const login = async ({email, password}: {email:string, password:string}) => {
        fetch('http://127.0.0.1:5001/auth/login', {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({email, password})
        })
        .then(response => response.json())
        .then(data => {
            localStorage.setItem('token', data.token);
            me();
        });
    }; 

    const logout = () => {
        fetch('http://127.0.0.1:5001/auth/logout', {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token') || ''}`
            },
        })
        .then(response => response.json())
        .then(() => {
            localStorage.removeItem('token');
            dispatch({ type: 'SET_USER', payload: null });
        });
    };

    const register = async ({email, password, name}: {email:string, password:string, name:string}) => {
        fetch('http://127.0.0.1:5001/auth/register', {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({email, password, name})
        })
        .then(response => response.json())
        .then(data => {
            localStorage.setItem('token', data.token);
            me();
        });
    }

    return { login, logout, user: state.user , me, register };
};