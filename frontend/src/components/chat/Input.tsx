import React  from 'react';
import { useChatActions } from '../../store/hooks/chat';
import { useOpenChat } from '../../store/hooks/currentChat';
import data from '@emoji-mart/data'
import Picker from '@emoji-mart/react'



const Input : React.FC = () => {
  const { send } = useChatActions();
  const { currentChat } = useOpenChat();
  const [message, setMessage] = React.useState<string>('');
  const [showEmojiPicker, setShowEmojiPicker] = React.useState<boolean>(false);



  const handleSend = (e: React.FormEvent) => {
    e.preventDefault();
    if (!message) return;
    if (!currentChat) return;
    send(currentChat.id, message);
    setMessage('');
  }

    return (
    <div
        className="flex flex-row items-center h-16 rounded-xl bg-white w-full px-4"
      >
        <form onSubmit={handleSend} className="flex w-full">
          {/* <div>
            <button
              className="flex items-center justify-center text-gray-400 hover:text-gray-600"
            >
              <svg
                className="w-5 h-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13"
                ></path>
              </svg>
            </button>
          </div> */}

          <div className="flex-grow ml-4">
            <div className="relative w-full">

              <input
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                placeholder="Type your message..."
                type="text"
                className="flex w-full bg-slate-500 border rounded-xl focus:outline-none focus:border-indigo-300 pl-4 h-10"
              />
              <button
                type="button"
                onClick={() => setShowEmojiPicker(!showEmojiPicker)}
                className="absolute flex items-center justify-center h-full w-12 right-0 top-0 text-gray-400 hover:text-gray-600"
              >
                <svg
                  className="w-6 h-6"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  ></path>
                </svg>
              </button>
              {showEmojiPicker && (
                <div className="absolute bottom-14 right-0 z-10">
                  <Picker data={data} onEmojiSelect={({native}:{native:string}) => setMessage(message + native)} />
                </div>
              )}
            </div>
          </div>

          <div className="ml-4">
            <button
              type="submit"
              className="flex items-center justify-center bg-indigo-500 hover:bg-indigo-600 rounded-xl text-white px-4 py-1 flex-shrink-0"
            >
              <span>Send</span>
              <span className="ml-2">
                <svg
                  className="w-4 h-4 transform rotate-45 -mt-px"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
                  ></path>
                </svg>
              </span>
            </button>
          </div>
        </form>
      </div>
    );
}

export default Input;
