export type User = {
    id: number
    name: string
    email: string
    groups: number[]
    chats: number[]
    created_at: string
    created_groups: number[]
}

export type Message = {
    id: number
    content: string
    timestamp: string
    sender_id: number
    chat: number
    seen: boolean
}

export type Chat = {
    id: number
    user1: number
    user2: number
    created_at: string
    messages: Message[]
}

export type Group = {
    id: number
    name: string
    members: number[]
    created_at: string
    creator_id: number
    messages: Message[]
}