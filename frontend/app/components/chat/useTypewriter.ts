"use client";

import { useRef, useState } from "react";

type Opts = {
  chunkSize?: number;
  delayMs?: number;
  onTick: (slice: string) => void;
  onDone?: () => void;
};

export default function useTypewriter({
  chunkSize = 2,
  delayMs = 30,
  onTick,
  onDone,
}: Opts) {
  const [isTyping, setIsTyping] = useState(false);

  const runIdRef = useRef(0);
  const timeoutRef = useRef<number | null>(null);

  function clearTimer() {
    if (timeoutRef.current !== null) {
      window.clearTimeout(timeoutRef.current);
      timeoutRef.current = null;
    }
  }

  function start(fullText: string) {
    const myRun = ++runIdRef.current;
    setIsTyping(true);
    let i = 0;

    function step() {
      if (myRun !== runIdRef.current) return;

      i = Math.min(i + chunkSize, fullText.length);
      onTick(fullText.slice(0, i));

      if (i >= fullText.length) {
        clearTimer();
        setIsTyping(false);
        onDone?.();
        return;
      }
      clearTimer();
      timeoutRef.current = window.setTimeout(step, delayMs);
    }

    step();
  }

  function cancel() {
    runIdRef.current++;
    clearTimer();
    setIsTyping(false);
  }

  return { isTyping, start, cancel };
}
