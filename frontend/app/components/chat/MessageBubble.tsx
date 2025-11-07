"use client";

import { PropsWithChildren } from "react";

type Role = "user" | "agent";

type MessageBubbleProps = PropsWithChildren<{
  role: Role;
  title?: string;
  className?: string;
}>;

export default function MessageBubble({
  role,
  title,
  className,
  children,
}: MessageBubbleProps) {
  const isAgent = role === "agent";
  const base =
    "p-4 rounded-lg border border-border max-w-[70%] w-auto " +
    (isAgent
      ? "bg-muted text-foreground"
      : "bg-secondary text-secondary-foreground");

  return (
    <div
      className={`w-full flex px-2 ${
        isAgent ? "justify-start" : "justify-end"
      }`}
    >
      <div className={`${base} ${className || ""}`}>
        {title && (
          <div className="text-sm font-semibold mb-2 text-muted-foreground">
            {title}
          </div>
        )}
        <div>{children}</div>
      </div>
    </div>
  );
}
