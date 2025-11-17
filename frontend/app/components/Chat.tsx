"use client";

import { useEffect, useRef, useState } from "react";
import MessageBubble from "./chat/MessageBubble";
import MarkdownRenderer from "./chat/MarkdownRenderer";
import LoadingBubble from "./chat/LoadingBubble";
import ChatInput from "./chat/ChatInput";
import useTypewriter from "./chat/useTypewriter";
import { LLMModelsList } from "./llm-models-list";
import SearchPatent from "./chat/SearchPatent"

type Msg = { role: "user" | "agent"; content: string };

export default function Chat() {
  const [messages, setMessages] = useState<Msg[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [selectedModel, setSelectedModel] = useState("gpt-5-nano")

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const fullAnswerRef = useRef<string>("");

  const {
    isTyping,
    start: startTyping,
    cancel,
  } = useTypewriter({
    onTick: (slice) => {
      setMessages((prev) => {
        if (!prev.length) return prev;
        const copy = [...prev];
        const last = copy[copy.length - 1];
        if (last.role === "agent") {
          copy[copy.length - 1] = { ...last, content: slice };
        }
        return copy;
      });
    },
  });

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  async function chat() {
    if (!input.trim() || isLoading || isTyping) return;

    const userText = input;
    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: userText }]);
    setIsLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Accept": "application/json",
        },
        body: JSON.stringify({ 
          question: userText,
          model: selectedModel
        }),
      });

      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      const answer =
        (typeof data === "string" ? data : data?.answer) ?? data?.message ?? "";
      if (!answer) {
        setMessages((prev) => [
          ...prev,
          { role: "agent", content: "Sem conteúdo na resposta da API." },
        ]);
        return;
      }
      fullAnswerRef.current = answer;
      setMessages((prev) => [...prev, { role: "agent", content: "" }]);

      setTimeout(() => {
        startTyping(answer);
      }, 0);
    } catch (e) {
      console.error("[chat] erro:", e);
      setMessages((prev) => [
        ...prev,
        {
          role: "agent",
          content: "Erro: Não foi possível conectar com o servidor",
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  }

  async function search(id:string) {
    if (isLoading || isTyping) return
    setMessages(prev => [...prev, { role: "user", content: `Pesquisar patente: ${id}` }])
    setIsLoading(true)
    try {
      const res = await fetch("http://127.0.0.1:8000/search", {
        method: "POST",
        headers: { "Content-Type":"application/json" },
        body: JSON.stringify({ patentId: id })
      })
      const data = await res.json()
      const answer = data?.answer ?? JSON.stringify(data)
      fullAnswerRef.current = answer
      setMessages(prev => [...prev, { role: "agent", content: "" }])
      startTyping(answer)
    } catch (e) {
      setMessages(prev => [...prev, { role: "agent", content: "Erro na busca de patente" }])
    } finally {
      setIsLoading(false)
    }
  }

  function skipTyping() {
    if (!isTyping) return;
    const full = fullAnswerRef.current;
    cancel();
    setMessages((prev) => {
      if (!prev.length) return prev;
      const copy = [...prev];
      const last = copy[copy.length - 1];
      if (last.role === "agent") {
        copy[copy.length - 1] = { ...last, content: full };
      }
      return copy;
    });
  }

  return (
    <div className="flex flex-col h-full w-full p-4">
      <div className="border rounded-2xl p-2 h-full overflow-hidden flex flex-col mb-4 bg-card text-card-foreground">
        <div className="py-2">
          <LLMModelsList
            selectedModel={selectedModel}
            onModelSelect={setSelectedModel}
          />
        </div>
        {messages.length === 0 && !isLoading ? (
          <div className="flex items-center justify-center h-full text-muted-foreground">
            <h3 className="text-md font-semibold">
              Inicie uma conversa fazendo uma pergunta sobre patentes...
            </h3>
          </div>
        ) : (
          <div
            className="
              space-y-4 overflow-y-auto
              [&::-webkit-scrollbar]:w-2
              [&::-webkit-scrollbar-track]:rounded-full
              [&::-webkit-scrollbar-track]:bg-muted
              [&::-webkit-scrollbar-thumb]:rounded-full
              [&::-webkit-scrollbar-thumb]:bg-border
            "
          >
            {messages.map((m, i) =>
              m.role === "agent" ? (
                <MessageBubble key={i} role="agent" title="Assistente">
                  <MarkdownRenderer content={m.content} />
                </MessageBubble>
              ) : (
                <MessageBubble key={i} role="user" title="Você">
                  {m.content}
                </MessageBubble>
              )
            )}

            {isLoading && !isTyping && (
              <div className="w-full flex px-2 justify-start">
                <LoadingBubble />
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      <div className="pt-4 border-t flex items-stretch gap-1">
        <SearchPatent role="user" onSearch={search}/>
        <div className="flex-1">
          <ChatInput
            value={input}
            onChange={setInput}
            onSend={chat}
            onSkip={skipTyping}
            isTyping={isTyping}
            disabled={isLoading || isTyping}
            placeholder={
              isLoading || isTyping
                ? "Aguarde a resposta..."
                : "Digite sua pergunta..."
            }
          />
        </div>
      </div>
    </div>
  );
}
