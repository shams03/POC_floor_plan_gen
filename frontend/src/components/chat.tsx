"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";

interface Message {
  role: "user" | "system";
  content: string;
}

export function Chat() {
  const [message, setMessage] = useState("");
  const [chatHistory, setChatHistory] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [dxfReady, setDxfReady] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!message.trim()) return;

    // Add user message to chat
    setChatHistory((prev) => [...prev, { role: "user", content: message }]);
    setLoading(true);
    setDxfReady(false);

    try {
      // Send message to backend
      console.log("Sending message to backend:", { message });  // Log the request being sent

      const response = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify( { message: message } ),
      });

      const data = await response.json();

      if (response.ok) {
        // Add system response to chat
        setChatHistory((prev) => [
          ...prev,
          { role: "system", content: "Floor plan generated successfully!" },
        ]);
        setDxfReady(true);
      } else {
        throw new Error(data.detail || "Failed to generate floor plan");
      }
    } catch (error) {
      setChatHistory((prev) => [
        ...prev,
        {
          role: "system",
          content: "Error generating floor plan. Please try again.",
        },
      ]);
    } finally {
      setLoading(false);
      setMessage("");
    }
  };

  const handleDownload = async () => {
    try {
      const response = await fetch("http://localhost:8000/api/download");
      if (!response.ok) throw new Error("Failed to download file");

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "floor_plan.dxf");
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      setChatHistory((prev) => [
        ...prev,
        {
          role: "system",
          content: "Error downloading DXF file. Please try again.",
        },
      ]);
    }
  };

  return (
    <Card className="w-full max-w-2xl mx-auto">
      <CardHeader>
        <CardTitle>Floor Plan Generator</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <div className="h-[400px] overflow-y-auto space-y-4 p-4 border rounded-lg">
            {chatHistory.map((msg, index) => (
              <div
                key={index}
                className={`flex ${
                  msg.role === "user" ? "justify-end" : "justify-start"
                }`}
              >
                <div
                  className={`max-w-[70%] p-3 rounded-lg ${
                    msg.role === "user"
                      ? "bg-primary text-primary-foreground"
                      : "bg-muted"
                  }`}
                >
                  {msg.content}
                </div>
              </div>
            ))}
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <Textarea
              placeholder="Describe your floor plan..."
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              disabled={loading}
              className="min-h-[100px]"
            />
            <div className="flex justify-between">
              <Button
                type="submit"
                disabled={loading || !message.trim()}
                className="w-full mr-2"
              >
                {loading ? "Generating..." : "Generate Floor Plan"}
              </Button>
              {dxfReady && (
                <Button
                  onClick={handleDownload}
                  variant="secondary"
                  className="w-full ml-2"
                >
                  Download DXF
                </Button>
              )}
            </div>
          </form>
        </div>
      </CardContent>
    </Card>
  );
}
