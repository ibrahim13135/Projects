import React, {useEffect} from 'react';
import { useChatActions } from './store/hooks/chat';
import { useAuthActions } from './store/hooks/auth';

const App: React.FC = () => {
  const { chats, create, list, send } = useChatActions();
  const [chatId, setChatId] = React.useState<number>(0);
  const [content, setContent] = React.useState<string>("");

  const { login, me } = useAuthActions();

  const handleCreate = () => {
    create('use@gmail.com');
  }

  const handleLogin = () => {
    login({email: 'hasan@gmail.com' , password: 'password123'});
  }

  const handleSend = () => {
    if (!chatId || !content) return;
    send(chatId, content);
  }

  useEffect(() => {
    me();
    list();
  }, []);

  
  return (
    <div className="h-screen flex items-center flex-col justify-center gap-5">
      <div className="flex gap-5">
        <button onClick={handleCreate} className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
          Create Chat
        </button>
        <button onClick={handleLogin} className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
          Login
        </button>
      </div>
      <div className="flex flex-col gap-5">
        {chats && chats.map(chat => (
          <div
            className="flex flex-col gap-5 bg-gray-600 p-2 rounded-lg text-blue-600"
            key={chat.id}>
            {chat.id} - {chat.user1}  - {chat.user2}
            {chat.messages && chat.messages.map(message => (
              // message card
              <div
                className="bg-gray-300 p-2 rounded-lg"
                key={message.id}>
                {message.content}
              </div>
            ))}
          </div>
        ))}
        <div className="flex gap-5 flex-col">
              <input 
                className=""
                value={chatId}
                onChange={(e) => setChatId(+e.target.value)}
                type="number" />
              <input
                className=""
                value={content}
                onChange={(e) => setContent(e.target.value)}
                type="text" />
              <button onClick={handleSend} className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                Send
              </button>
        </div>
      </div>
    </div>
  );
};

export default App;
