import { useAppStore } from "../store";
import { Chat } from "../types";

export const useOpenChat = () => {
    const {state, dispatch } = useAppStore();

    const open = (chat: Chat) => {
        dispatch({ type: 'OPEN_CHAT', payload: chat });
    };

    return { open , currentChat: state.currentChat };
};