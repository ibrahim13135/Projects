import React from 'react';
import { Chat, User } from '../../store/types';
import { useUserActions } from '../../store/hooks/user';
import { useAuthActions } from '../../store/hooks/auth';
import getColorFromString from '../../func/Color'
import { useOpenChat } from '../../store/hooks/currentChat';

const ChatCard : React.FC<{chat: Chat}> = ({chat}) => {
    const { getUserInfo } = useUserActions();
    const { open } = useOpenChat();
    const {user} = useAuthActions();
    const [friend, setFriend] = React.useState<User | null>(null);

    React.useEffect(() => {
        if (!user) return;
        const friendId = chat.users.find((id) => id !== user?.id);
        if (!friendId) return;
        getUserInfo(friendId).then((user) => {
            setFriend(user);
        });
    }, [user]);
        
        
        
    return (
        <button
            onClick={() => open(chat)}
            key={chat.id}
            className="flex flex-row items-center hover:bg-gray-100 rounded-xl p-2"
            >
            <div
                className="flex items-center justify-center h-8 w-8 bg-indigo-200 rounded-full overflow-hidden"
            >
                <img
                src={`https://placehold.co/100x100/${getColorFromString(friend?.name as string)}/31343C?font=oswald&text=${friend?.name[0]}`}
                alt="Avatar"
                className="h-full w-full"
            />
            </div>
            <div className="ml-2 text-sm font-semibold">{friend?.name}</div>
        </button>
    );
}

export default ChatCard;
