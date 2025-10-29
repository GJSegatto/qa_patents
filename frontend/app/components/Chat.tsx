"use client"

import { useState, useEffect, useRef } from "react"
import "react-chat-elements/dist/main.css"
import { MessageBox } from "react-chat-elements"

import ReactMarkdown from 'react-markdown'

export default function Chat() {
    const [messages, setMessages] = useState<{ role: string, content: string}[]>([])
    const [input, setInput] = useState("")
    const [isLoading, setIsLoading] = useState(false)
    const messagesEndRef = useRef<HTMLDivElement>(null)

    async function sendMessage() {
        if(!input.trim() || isLoading) return

        const user_input = input
        
        //Adiciona msg do user no estado local
        setMessages((prev) => [...prev, {role: "user", content: user_input}])

        setInput("")
        setIsLoading(true)

        try {
          const res = await fetch("http://127.0.0.1:8000/chat", {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
                "Accept": "application/json"
              },
              body: JSON.stringify({ question: user_input }),
          })

          if (!res.ok) {
            throw new Error(`HTTP error! status: ${res.status}`)
          }

          const data = await res.json()
          setMessages((prev) => [...prev, { role: "agent", content: data.answer }])

        } catch (error) {
          setMessages((prev) => [...prev, { role: "agent", content: "Erro: Não foi possível conectar com o servidor" }])
        } finally {
          setIsLoading(false)
        }
    }

    function handleKeyDown(e: React.KeyboardEvent<HTMLInputElement>) {
      if(e.key === "Enter" && !isLoading) {
        e.preventDefault()
        sendMessage()
      }
    }

    const scrollToBottom = () => {
      messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
    }

    useEffect(() => {
      scrollToBottom()
    }, [messages, isLoading])

    const LoadingAnimation = () => (
      <div className="p-4 rounded-lg bg-gray-800">
        <div className="text-sm font-semibold mb-4 text-gray-400">
          Assistente
        </div>
        <div className="flex items-center space-x-1">
          <div className="flex space-x-1">
            <div className="w-2 h-2 bg-white rounded-full animate-bounce [animation-delay:-0.3s]"></div>
            <div className="w-2 h-2 bg-white rounded-full animate-bounce [animation-delay:-0.15s]"></div>
            <div className="w-2 h-2 bg-white rounded-full animate-bounce"></div>
          </div>
        </div>
      </div>
    )

    return (
    <div className="flex flex-col h-full w-full p-4">
        <div className="border rounded-2xl p-4 h-full overflow-hidden flex flex-col mb-4">
        {messages.length === 0 && !isLoading ? (
          <div className="flex items-center justify-center h-full text-muted-foreground">
            <h3 className="text-md font-semibold">Inicie uma conversa fazendo uma pergunta sobre patentes...</h3>
          </div>
        ) : (
          <div className="space-y-4 overflow-y-auto custom-scrollbar [&::-webkit-scrollbar]:w-2 [&::-webkit-scrollbar-track]:rounded-full [&::-webkit-scrollbar-track]:bg-gray-100 [&::-webkit-scrollbar-thumb]:rounded-full [&::-webkit-scrollbar-thumb]:bg-gray-800 dark:[&::-webkit-scrollbar-track]:bg-neutral-700 dark:[&::-webkit-scrollbar-thumb]:bg-gray-800">
            {messages.map((msg, i) => (
              <div 
                key={i} 
                className={`w-full flex px-2 ${msg.role === "user" ? "justify-end" : "justify-start"}`}
              >
                <div className="max-w-[70%] w-auto">
                  {msg.role === "agent" ? (
                    // Mensagem do agente com Markdown
                    <div className="p-4 rounded-lg bg-gray-800">
                      <div className="text-sm font-semibold mb-2 text-gray-400">
                        Assistente
                      </div>
                      <div className="text-white">
                        <ReactMarkdown 
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
                              <code className="bg-gray-200 px-1 py-0.5 rounded text-sm">{children}</code>
                            ) : (
                              <code className="block bg-gray-200 p-2 rounded text-sm overflow-x-auto">{children}</code>
                            );
                          },
                          strong: ({ children }) => <strong className="font-bold">{children}</strong>,
                          em: ({ children }) => <em className="italic">{children}</em>
                        }}
                      >
                        {msg.content}
                      </ReactMarkdown>
                      </div>
                    </div>
                  ) : (
                    <div className="p-4 rounded-lg bg-gray-800">
                      <div className="text-sm font-semibold mb-2 text-gray-400">
                        Você
                      </div>
                      <div className="text-white">
                        {msg.content}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            ))}

            {isLoading && (
              <div className="w-full flex px-2 justify-start">
                <div className="max-w-[70%] w-auto">
                  <LoadingAnimation />
                </div>
              </div>
            )}
            <div ref={messagesEndRef}/>
          </div>
        )}
      </div>
      
      <div className="pt-4 border-t">
        <div className="flex shadow-sm border rounded-xl overflow-hidden">
          <input
            className="flex-1 p-3 bg-background text-foreground border-0 outline-none"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={isLoading ? "Aguarde a resposta..." : "Digite sua pergunta..."}
            disabled={isLoading}
          />
          <button
            className={`text-primary-foreground bg-gray-800 px-6 py-3 transition-colors font-bold text-sm font-semibold text-white ${
              isLoading 
                ? "cursor-not-allowed" 
                : "hover:bg-primary/90 cursor-pointer"
            }`}
            onClick={sendMessage}
            disabled={isLoading}
          >
            Enviar
          </button>
        </div>
      </div>
      
    </div>
  )
}