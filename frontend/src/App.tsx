import React, {useEffect, useState} from 'react';
import { useAuthActions } from './store/hooks/auth';
import { useGroupActions } from './store/hooks/group';

const App: React.FC = () => {
  const [message, setMessage] = useState<string>('');

  const { user, login, me } = useAuthActions();
  const { groups, create, deleteGroup, addMember, list, send } = useGroupActions();

  const handleLogin = () => {
    login({email: 'hasan@gmail.com' , password: 'password123'});
  }

  const handleCreateGroup = () => {
    create('My Group');
  }

  const handleAddMember = (group_id:number) => {
    addMember(group_id, 'user@gmail.com');
  }

  useEffect(() => {
    me();
    list();
  }, []);

  // register({email: 'hasan@gmail.com', password: 'password123', name: 'Hasan'});
  console.log(groups);
  
  
  return (
    <div className="h-screen flex items-center flex-col p-4 gap-5">
      <h1 className="text-3xl font-bold">Welcome {user?.name || 'to Chat App'}</h1>
      <div className="flex gap-5">
        <button onClick={handleLogin} className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
          Login
        </button>

        <button onClick={handleCreateGroup} className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
          Create Group
        </button>
      </div>

        <div className="flex flex-col gap-2 text-yellow-400">
          {groups && groups?.map(group => (
            <div key={group.id} className="bg-gray-100 p-2 gap-2 flex flex-col rounded">
              <h2 className="font-bold">{group.name}</h2>
              <p>{group.id}</p>
              <p>{group.messages?.map(message => message.content).join(', ')}</p>
              <p>{group.members?.map(member => member.name).join(', ')}</p>

              <div className="flex gap-2">
                <input
                  value={message}
                  onChange={e => setMessage(e.target.value)}
                  className="border border-gray-400 p-1 rounded" 
                  placeholder="Type a message"
                type="text"/>
                <button onClick={() => send(group.id, message)} className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-1 px-2 rounded">
                  Send Message
                </button>
              </div>

              <div className="flex gap-2 w-full justify-around ">
                <button onClick={() => deleteGroup(group.id)} className="bg-red-500 hover:bg-red-700 text-white font-bold py-1 px-2 rounded">
                  Delete
                </button>
                <button onClick={() => handleAddMember(group.id)} className="bg-green-500 hover:bg-green-700 text-white font-bold py-1 px-2 rounded">
                  Add Member
                </button>
              </div>
            </div>
          ))}
        </div>

    </div>
  );
};

export default App;
