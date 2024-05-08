import React from 'react';
import { useAuthActions } from '../../store/hooks/auth';
import getColorFromString from '../../func/Color'

const ProfileCard : React.FC = () => {
    const { user } = useAuthActions();
    const firstLetter = user?.name?.charAt(0).toUpperCase() || 'unknown';
    
    return (
        <div className="flex flex-col items-center bg-indigo-100 border border-gray-200 w-full py-6 px-4 rounded-lg">
            <div className="h-20 w-20 rounded-full border overflow-hidden">
            <img
                src={`https://placehold.co/50x50/${getColorFromString(user?.name as string)}/31343C?font=oswald&text=${firstLetter}`}
                alt="Avatar"
                className="h-full w-full"
            />
            </div>
            <div className="text-sm font-semibold mt-2">{user?.name}</div>
        </div>
    );
}

export default ProfileCard;
