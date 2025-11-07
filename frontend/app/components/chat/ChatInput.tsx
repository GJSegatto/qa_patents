"use client";

type ChatInputProps = {
  value: string;
  disabled?: boolean;
  isTyping?: boolean;
  placeholder?: string;
  onChange: (v: string) => void;
  onSend: () => void;
  onSkip?: () => void;
};

export default function ChatInput({
  value,
  disabled,
  isTyping,
  placeholder,
  onChange,
  onSend,
  onSkip,
}: ChatInputProps) {
  function handleKeyDown(e: React.KeyboardEvent<HTMLInputElement>) {
    if (
      (e.key === "Enter" || (e.key === "Enter" && (e.ctrlKey || e.metaKey))) &&
      !disabled &&
      !isTyping
    ) {
      e.preventDefault();
      onSend();
    }
  }

  const showSkip = Boolean(isTyping && onSkip);

  return (
    <div className="flex shadow-sm border rounded-xl overflow-hidden bg-card">
      <input
        className="flex-1 p-3 bg-background text-foreground border-0 outline-none"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder={placeholder}
        disabled={disabled}
        autoFocus
      />

      <button
        className={`px-6 py-3 transition-colors font-bold text-sm ${
          showSkip
            ? "bg-muted text-foreground hover:bg-muted/80 cursor-pointer"
            : disabled
            ? "cursor-not-allowed bg-muted text-muted-foreground"
            : "bg-primary text-primary-foreground hover:bg-primary/90 cursor-pointer"
        }`}
        onClick={showSkip ? onSkip : onSend}
        disabled={disabled && !showSkip}
      >
        {showSkip ? "Pular" : "Enviar"}
      </button>
    </div>
  );
}
