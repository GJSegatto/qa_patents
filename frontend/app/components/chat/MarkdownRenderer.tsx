"use client";

import ReactMarkdown from "react-markdown";

export default function MarkdownRenderer({ content }: { content: string }) {
  return (
    <ReactMarkdown
      components={{
        p: ({ children }) => <p className="mb-2 last:mb-0">{children}</p>,
        h1: ({ children }) => (
          <h1 className="text-lg font-bold mb-2">{children}</h1>
        ),
        h2: ({ children }) => (
          <h2 className="text-base font-bold mb-2">{children}</h2>
        ),
        h3: ({ children }) => (
          <h3 className="text-sm font-bold mb-2">{children}</h3>
        ),
        ul: ({ children }) => (
          <ul className="list-disc list-inside mb-2 space-y-1">{children}</ul>
        ),
        ol: ({ children }) => (
          <ol className="list-decimal list-inside mb-2 space-y-1">
            {children}
          </ol>
        ),
        li: ({ children }) => <li className="mb-0.5">{children}</li>,
        code: ({ children, className }) => {
          const isInline = !className;
          return isInline ? (
            <code className="bg-muted border border-border text-foreground px-1 py-0.5 rounded text-sm">
              {children}
            </code>
          ) : (
            <code className="block bg-muted border border-border text-foreground p-3 rounded-lg text-sm overflow-x-auto">
              {children}
            </code>
          );
        },
        strong: ({ children }) => (
          <strong className="font-bold">{children}</strong>
        ),
        em: ({ children }) => <em className="italic">{children}</em>,
      }}
    >
      {content}
    </ReactMarkdown>
  );
}
