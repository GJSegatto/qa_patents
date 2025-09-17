"use client"

import { useState, useEffect, useRef } from "react"
import "react-chat-elements/dist/main.css"
import { MessageBox } from "react-chat-elements"

import ReactMarkdown from 'react-markdown'

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
    <div className="flex flex-col h-full w-full p-4">
        <div className="border rounded-2xl p-4 h-full overflow-hidden flex flex-col mb-4">
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full text-muted-foreground">
            <h3 className="text-md font-semibold">Inicie uma conversa fazendo uma pergunta sobre patentes...</h3>
          </div>
        ) : (
          <div className="space-y-4 overflow-y-auto custom-scrollbar [&::-webkit-scrollbar]:w-2 [&::-webkit-scrollbar-track]:rounded-full [&::-webkit-scrollbar-track]:bg-gray-100 [&::-webkit-scrollbar-thumb]:rounded-full [&::-webkit-scrollbar-thumb]:bg-blue-300 dark:[&::-webkit-scrollbar-track]:bg-neutral-700 dark:[&::-webkit-scrollbar-thumb]:bg-blue-400">
            {messages.map((msg, i) => (
              <div 
                key={i} 
                className={`w-full flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
              >
                <div className="max-w-[80%] w-auto">
                  {msg.role === "agent" ? (
                    // Mensagem do agente com Markdown
                    <div className={`p-4 rounded-lg ${msg.role === "user" ? "bg-blue-500 ml-auto" : "bg-gray-100 dark:bg-gray-800"}`}>
                      <div className="text-sm font-semibold mb-2 text-gray-600 dark:text-gray-400">
                        Assistente
                      </div>
                      <ReactMarkdown 
                        //className="prose prose-sm max-w-none dark:prose-invert prose-p:my-2 prose-headings:my-3 prose-ul:my-2 prose-ol:my-2 prose-li:my-0"
                        components={{ 
                          p: ({ children }) => <p className="mb-2 last:mb-0">{children}</p>,
                          h1: ({ children }) => <h1 className="text-lg font-bold mb-2">{children}</h1>,
                          h2: ({ children }) => <h2 className="text-base font-bold mb-2">{children}</h2>,
                          h3: ({ children }) => <h3 className="text-sm font-bold mb-2">{children}</h3>,
                          ul: ({ children }) => <ul className="list-disc list-inside mb-2">{children}</ul>,
                          ol: ({ children }) => <ol className="list-decimal list-inside mb-2">{children}</ol>,
                          li: ({ children }) => <li className="mb-1">{children}</li>,
                          code: ({ children, className }) => {
                            const isInline = !className;
                            return isInline ? (
                              <code className="bg-gray-200 dark:bg-gray-700 px-1 py-0.5 rounded text-sm">{children}</code>
                            ) : (
                              <code className="block bg-gray-200 dark:bg-gray-700 p-2 rounded text-sm overflow-x-auto">{children}</code>
                            );
                          },
                          strong: ({ children }) => <strong className="font-bold">{children}</strong>,
                          em: ({ children }) => <em className="italic">{children}</em>
                        }}
                      >
                        {msg.content}
                      </ReactMarkdown>
                    </div>
                  ) : (
                    // Mensagem do usuário com MessageBox original
                    <MessageBox
                        position={msg.role === "user" ? "right" : "left"}
                        type={'text'}
                        title={msg.role === "user" ? "Você" : "Assistente"}
                        titleColor="#1f2937"
                        text={msg.content}
                        notch={false}
                        styles={{
                          color: "#1f2937",
                          backgroundColor: "#4382e9ff"
                        }}
                        className="text-foreground no-underline cursor-default pointer-events-none"
                    />
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
      
      <div className="p-4 border-t">
        <div className="flex shadow-sm border rounded-xl overflow-hidden">
          <input
            className="flex-1 p-3 bg-background text-foreground border-0 outline-none"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Digite sua pergunta sobre patentes..."
          />
          <button
            className="bg-primary text-primary-foreground px-6 py-3 hover:bg-primary/90 transition-colors font-bold"
            style={{
              color: "#1f2937",
              backgroundColor: "#4382e9ff"
            }}
            onClick={sendMessage}
          >
            Enviar
          </button>
        </div>
      </div>
      
    </div>
  )
}