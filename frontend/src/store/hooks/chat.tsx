import { useAppStore } from "../store";
import { Chat, Message } from "../types";

export const useChatActions = () => {
    const {state, dispatch } = useAppStore();

    const validate = () => {
        if (localStorage.getItem('token') && localStorage.getItem('token') !== 'undefined') {
            return true;
        } else {
            return false;
        }
    }
    
    const create = async (withEmail:string) => {
        validate() &&
        fetch('http://127.0.0.1:5001/chat/create', {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('token')
            },
            body: JSON.stringify({withEmail})
        })
        .then(response => response.json())
        .then(data => {
            dispatch({ type: 'NEW_CHAT', payload: data });
        });
    }

    const list = async () => {
        validate() &&
        fetch('http://127.0.0.1:5001/chat/list', {
            method: 'GET',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token') || ''}` 
            },
        })
        .then(response => response.json())
        .then(data => {
            dispatch({ type: 'SET_CHATS', payload: data.chats });
        });
    };

    const send = async (chat_id: number, content: string) => {
        validate() &&
        fetch('http://127.0.0.1:5001/chat/send', {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token') || ''}`
            },
            body: JSON.stringify({chat_id, content})
        })
        .then(response => response.json())
        .then((data:Message) => {
            // get this chat from state and edit it
            const chat = state.chats?.find(chat => chat.id === chat_id);
            if (chat) {
                // replace the chat with the new one
                const newChat : Chat = {...chat,
                     messages: chat.messages ? [...chat.messages, data] : [data]
                    };
                const chats = state.chats?.map(chat => chat.id === chat_id ? newChat : chat) || [];
                dispatch({ type: 'SET_CHATS', payload: chats });
            }

        });
    }

    return {chats: state.chats, create, list, send};
};