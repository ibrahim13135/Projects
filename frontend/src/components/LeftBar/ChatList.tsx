import React, { useState } from 'react'
import { useChatActions } from '../../store/hooks/chat';
import ChatCard from './ChatCard';

const ChatList : React.FC = () => {
    const { chats, create } = useChatActions();
    const [email, setEmail] = useState<string>('');

    const CreateChat = (e: React.FormEvent) => {
        e.preventDefault();
        if (!email) return;
        create(email);
        setEmail('');
    }

  return (
    <div className="flex flex-col space-y-1 mt-4 -mx-2 overflow-y-auto">
        <div className="flex flex-row items-center p-2 relative">
            <form onSubmit={CreateChat}>
                <input
                    value={email}
                    required
                    onChange={(e) => setEmail(e.target.value)}
                    className="bg-transparent outline-none focus:bg-gray-100 hover:bg-gray-100  p-2 rounded-xl w-full"
                    placeholder="Create chat with"
                    type="email" name="" id="" />
                <button
                type='submit'
                className="bg-indigo-500 hover:bg-indigo-600 rounded-full w-12 h-10 p-2 right-0 text-white absolute">+</button>
            </form>
        </div>
        {chats && chats.map((chat) => (
            <ChatCard key={chat.id} chat={chat} />
        ))}
    </div>
  )
}

export default ChatList