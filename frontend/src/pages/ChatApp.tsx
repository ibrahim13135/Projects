import React from 'react';

// bar
import Logo from '../components/LeftBar/Logo';
import ProfileCard from '../components/LeftBar/ProfileCard';
import ChatList from '../components/LeftBar/ChatList';

// chat
import Board from '../components/chat/Board';


const ChatApp: React.FC = () => {  

  return (
    <div className="flex h-screen antialiased text-gray-800">
        <div className="flex flex-row h-full w-full overflow-x-hidden">

          <div className="flex flex-col flex-shrink-0  p-4 w-60 bg-white gap-4">
            <Logo />

            <ProfileCard />

            <ChatList />
          </div>

          
            <div className="flex flex-col flex-shrink-0 flex-auto bg-gray-100 p-4">
              <Board />

            </div>

        </div>
      </div>
  );
};

export default ChatApp;
