"use client"

import { useState } from "react"
import "react-chat-elements/dist/main.css"
import { MessageBox } from "react-chat-elements"

export default function Chat() {
    const [messages, setMessages] = useState<{ role: string, content: string}[]>([])
    const [input, setInput] = useState("")

    async function sendMessage() {
        if(!input.trim()) return

        const user_input = input
        
        //Adiciona msg do user no estado local
        setMessages((prev) => [...prev, {role: "user", content: user_input}])

        setInput("")

        const res = await fetch("http://127.0.0.1:8000/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question: input }),
        })

        const data = await res.json()

        // Adiciona resposta do agente no chat
        setMessages((prev) => [...prev, { role: "agent", content: data.answer }])

        
    }

    function handleKeyDown(e: React.KeyboardEvent<HTMLInputElement>) {
      if(e.key === "Enter") {
        e.preventDefault()
        sendMessage()
      }
    }

    return (
    <div className="flex flex-col w-lg mx-auto p-4 border rounded-2xl shadow-md">
      <div className="flex-1 overflow-y-auto space-y-2 mb-4">
        {messages.map((msg, i) => (
            <MessageBox
                key={i}
                position={msg.role === "user" ? "right" : "left"}
                type={'text'}
                title={msg.role === "user" ? "Você" : "Assistente"}
                titleColor="blue"
                text={msg.content}
                notch={false}
                className="text-black no-underline cursor-default pointer-events-none"
            />
        ))}
      </div>

      <div className="flex">
        <input
          className="flex-1 border rounded-l-xl p-2"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Digite sua pergunta..."
        />
        <button
          className="bg-blue-500 text-white p-2 rounded-r-xl"
          onClick={sendMessage}
        >
          Enviar
        </button>
      </div>
    </div>
  )
}