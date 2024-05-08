import { useAppStore } from "../store";
import { Chat, Message } from "../types";
import { useOpenChat } from "./currentChat";

export const useChatActions = () => {
    const {state, dispatch } = useAppStore();
    const {open} = useOpenChat();

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
            data &&
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
            data &&
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
            const chat = state.chats?.find(chat => chat.id === chat_id);
            if (chat) {
                const newChat : Chat = {...chat,
                    messages: chat.messages ? [...chat.messages, data] : [data]
                };
                open(newChat);
                const chats = state.chats?.map(chat => chat.id === chat_id ? newChat : chat) || [];
                console.log(chats);
                dispatch({ type: 'SET_CHATS', payload: chats });
            }

        });
    }

    return {chats: state.chats, create, list, send};
};