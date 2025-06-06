import { Chat } from "@/components/chat";

export default function Home() {
  return (
    <main className="min-h-screen p-4 md:p-8 relative bg-black">
      {/* Background pattern */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#8080800a_1px,transparent_1px),linear-gradient(to_bottom,#8080800a_1px,transparent_1px)] bg-[size:24px_24px] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_0%,#000_70%,transparent_100%)]" />

      {/* Gradient overlay */}
      <div className="absolute inset-0 bg-gradient-to-b from-background/80 via-background/50 to-background" />

      {/* Content */}
      <div className="relative">
        <Chat />
      </div>
    </main>
  );
}
