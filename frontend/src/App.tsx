import React, { useEffect } from 'react';
import { Route, Routes } from 'react-router-dom';
import { useAuthActions } from './store/hooks/auth';
import { useChatActions } from './store/hooks/chat';
import { useGroupActions } from './store/hooks/group';


import Layout from './pages/Layout';
import Signin from './pages/Signin';
import Signup from './pages/Signup';

import ChatApp from './pages/ChatApp'




const App: React.FC  = () => {
  const {user,me} = useAuthActions();
  const {list} = useChatActions();
  const {list: groupList} = useGroupActions();


  useEffect(() => {
    me();
  }, []);

  useEffect(() => {
    if(user){
      list();
      groupList();
    }
  }, [user]);
    
  return(
    <>
    <Routes>
      <Route path="/" element={<Layout />} >
        {user ? <Route index element={<ChatApp />} /> : <Route index element={<Signin />} />}
        <Route path="/signup" element={<Signup />} />
        <Route path="/login" element={<Signin />} />
      </Route>
    </Routes>
    </>
    )
  };

export default App;
