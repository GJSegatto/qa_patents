import Image from "next/image";
import Chat from "./components/Chat";
import { ModeToggle } from "./components/mode-toggle";

export default function Home() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-black-100">
      <Chat />
      <ModeToggle />
    </main>
  );
}
