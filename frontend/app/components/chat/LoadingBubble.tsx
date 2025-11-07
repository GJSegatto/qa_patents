"use client";

export default function LoadingBubble() {
  return (
    <div className="p-4 rounded-lg bg-muted border border-border max-w-[70%] w-auto">
      <div className="text-sm font-semibold mb-4 text-muted-foreground">
        Assistente
      </div>
      <div className="flex items-center space-x-1">
        <div className="flex space-x-1">
          <div className="w-2 h-2 rounded-full animate-bounce [animation-delay:-0.3s] bg-foreground/80"></div>
          <div className="w-2 h-2 rounded-full animate-bounce [animation-delay:-0.15s] bg-foreground/70"></div>
          <div className="w-2 h-2 rounded-full animate-bounce bg-foreground/60"></div>
        </div>
      </div>
    </div>
  );
}
