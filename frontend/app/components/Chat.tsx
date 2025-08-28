"use client";
import { useState } from "react";

export default function Chat() {
    const [messages, setMessages] = useState<{ role: string; content: string}[]>([]);
    const [input, setInput] = useState("");

    async function sendMessage() {
        if(!input.trim()) return;
        
        //Adiciona msg do user no estado local
        setMessages((prev) => [...prev, {role: "user", content: input}]);

        const res = await fetch("http://127.0.0.1:8000/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question: input }),
        });

        const data = await res.json();

        // Adiciona resposta do agente no chat
        setMessages((prev) => [...prev, { role: "agent", content: data.answer }]);

        setInput("");
    }

    return (
    <div className="flex flex-col max-w-md mx-auto p-4 border rounded-2xl shadow-md">
      <div className="flex-1 overflow-y-auto space-y-2 mb-4">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`p-2 rounded-xl  ${
              msg.role === "user" ? "bg-blue-200 self-end text-red-500" : "bg-gray-200 self-start text-green-500"
            }`}
          >
            {msg.content}
          </div>
        ))}
      </div>

      <div className="flex">
        <input
          className="flex-1 border rounded-l-xl p-2"
          value={input}
          onChange={(e) => setInput(e.target.value)}
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
  );
}