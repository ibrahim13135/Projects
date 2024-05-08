import { useAppStore } from "../store";
import { Group, Member,Message } from "../types";

export const useGroupActions = () => {
    const {state, dispatch } = useAppStore();

    const validate = () => {
        if (localStorage.getItem('token') && localStorage.getItem('token') !== 'undefined') {
            return true;
        } else {
            return false;
        }
    }
    
    const create = async (name:string) => {
        validate() &&
        fetch('http://127.0.0.1:5001/group/create', {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('token')
            },
            body: JSON.stringify({name})
        })
        .then(response => response.json())
        .then((data:Group) => {
            dispatch({ type: 'NEW_GROUP', payload: data });
        });
    }

    const list = async () => {
        validate() &&
        fetch('http://127.0.0.1:5001/group/my_groups', {
            method: 'GET',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token') || ''}`
            },
        })
        .then(response => response.json())
        .then((data: Group[]) => {
            // if data has key equal to error, then user is not authenticated
            if (Object.hasOwnProperty.call(data, 'error')) {
                dispatch({ type: 'SET_GROUPS', payload: null });
            } else {
                dispatch({ type: 'SET_GROUPS', payload: data });
            }
        });
    }

    const send = async (group_id: number, content: string) => {
        validate() &&
        fetch(`http://127.0.0.1:5001/group/${group_id}/send`,
        {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token') || ''}`
            },
            body: JSON.stringify({content})
        })
        .then(response => response.json())
        .then((data:Message) => {
            // get this chat from state and edit it
            const group = state.groups?.find(group => group.id === group_id);
            if (group) {
                // replace the chat with the new one
                const newGroup : Group = {...group,
                     messages: group.messages ? [...group.messages, data] : [data]
                    };
                const groups = state.groups?.map(group => group.id === group_id ? newGroup : group) || [];
                dispatch({ type: 'SET_GROUPS', payload: groups });
            }
        });
    }

    const addMember = async (group_id: number, email: string) => {
        validate() &&   
        fetch(`http://127.0.0.1:5001/group/${group_id}/add_member`, {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token') || ''}`
            },
            body: JSON.stringify({email})
        })
        .then(response => response.json())
        .then((data: Member) => {
            const group = state.groups?.find(group => group.id === group_id);
            if (group) {
                const newGroup : Group = {...group,
                     members: group.members ? [...group.members, data] : [data]
                    };
                const groups = state.groups?.map(group => group.id === group_id ? newGroup : group) || [];
                dispatch({ type: 'SET_GROUPS', payload: groups });
            }
        });
    }

    const deleteGroup = async (group_id: number) => {
        validate() &&
        fetch(`http://127.0.0.1:5001/group/${group_id}/delete`, {
            method: 'DELETE',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token') || ''}`
            },
        })
        .then(response => response.json())
        .then(() => {
            const groups = state.groups?.filter(group => group.id !== group_id) || [];
            dispatch({ type: 'SET_GROUPS', payload: groups });
        });
    }

    return {groups: state.groups, create, list, send, addMember, deleteGroup};
}