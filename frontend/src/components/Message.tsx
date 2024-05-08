import React from 'react'
import { Message } from '../store/types'
import { User } from '../store/types';
import { useUserActions } from '../store/hooks/user';
import { useAuthActions } from '../store/hooks/auth';
import getColorFromString from '../func/Color';


const MessageCard : React.FC<{message: Message}> = ({message}) => {
    const { getUserInfo } = useUserActions();
    const {user} = useAuthActions();
    const [sender, setSender] = React.useState<User | null>(null);
    const [color, setColor] = React.useState<string>('');
    
    React.useEffect(() => {
        if (user?.id === message.sender_id) {
            setSender(user);
            setColor(getColorFromString(user.name));
            return;
        }
        getUserInfo(message.sender_id).then((user) => {
            if (!user) return;
            setSender(user);
            setColor(getColorFromString(user.name));
        });
    }, []);
    
  return (
    <>
       <div className="p-3 rounded-lg" key={message.id}>
            <div style = {user?.id === message.sender_id ? {flexDirection: "row-reverse"} : {flexDirection: "row"}} className="flex items-center">
                <div style={{backgroundColor: `#${color}`}} className="flex items-center justify-center h-10 w-10 rounded-full flex-shrink-0">
                    {sender?.name[0]}
                </div>
                <div
                    className="relative mx-3 text-sm bg-white py-2 px-4 shadow rounded-xl"
                >
                    <div className="text-gray-800">
                        {message.content}
                    </div>
                    <div className="text-xs text-gray-500">
                        {new Date(message?.timestamp).toLocaleTimeString()}
                    </div>
                </div>
            </div>
        </div>
    </>
  )
}

export default MessageCard