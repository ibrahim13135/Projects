import React from 'react';
import Message from '../Message';
import { useOpenChat } from '../../store/hooks/currentChat';
import Input from './Input';
import socket from '../../server';

const Board : React.FC = () => {
    const { currentChat } = useOpenChat();
    const chat = currentChat;
    const messages = chat?.messages;

    socket.on("new_message", (data) => {
      console.log("Received new message:", data.content);
  });
  

    return (
      <>
        <div className="flex flex-col h-full overflow-x-auto mb-4">
        <div className="flex flex-col h-full">
            <div key={chat?.id} className="flex flex-col">
              <div className="text-sm text-gray-500 text-center mt-4">{chat?.created_at}</div>
              <div className="flex flex-col h-full overflow-y-auto">
                {messages && messages.map((message) => (
                  <Message key={message.id} message={message} />
                  ))}
              </div>
            </div>
        </div>
      </div>
      {currentChat &&
        <Input />
      }
      </>
    );
}

export default Board;
