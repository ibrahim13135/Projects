import React, { createContext, useContext, useReducer, ReactNode } from 'react';
import { User, Chat, Group } from './types';

// Define the state structure
type AppState = {
  user: User | null;
  chats: Chat[] | null;
  groups: Group[] | null;
};

// Define action types
type AppAction =
  | { type: 'SET_USER'; payload: AppState['user'] }
  | { type: 'SET_CHATS'; payload: AppState['chats'] }
  | { type: 'SET_GROUPS'; payload: AppState['groups'] }
  | { type: 'NEW_CHAT'; payload: Chat }
  | { type: 'NEW_GROUP'; payload: Group };

// Reducer function to manage state transitions
const appReducer = (state: AppState, action: AppAction): AppState => {
  switch (action.type) {
    case 'SET_USER':
      return { ...state, user: action.payload };
    case 'SET_CHATS':
      return { ...state, chats: action.payload };
    case 'NEW_CHAT':
      return { ...state, chats: state.chats ? [...state.chats, action.payload] : [action.payload] };
    case 'SET_GROUPS':
      return { ...state, groups: action.payload };
    case 'NEW_GROUP':
      return { ...state, groups: state.groups ? [...state.groups, action.payload] : [action.payload] };
    default:
      return state;
  }
};

// Create a context for the store
const AppContext = createContext<{
  state: AppState;
  dispatch: React.Dispatch<AppAction>;
} | null>(null);

// Context provider to wrap the application
export const AppProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(appReducer, {
    user: null,
    chats: [],
    groups: [],
  });

  return (
    <AppContext.Provider value={{ state, dispatch }}>
      {children}
    </AppContext.Provider>
  );
};

// Custom hook to use the store
export const useAppStore = () => {
    const context = useContext(AppContext);
    if (!context) {
      throw new Error('useAppStore must be used within an AppProvider');
    }
    return context;
};
