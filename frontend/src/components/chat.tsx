"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";

interface FloorPlanData {
  floor_plan: {
    dimensions: {
      total_area: number;
      unit: string;
    };
    rooms: Array<{
      name: string;
      width: number;
      height: number;
      position: { x: number; y: number };
      doors: Array<{ position: string; width: number }>;
      windows?: Array<{ position: string; width: number }>;
    }>;
  };
}

interface Message {
  role: "user" | "system";
  content: string;
  data?: FloorPlanData;
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
      console.log("Sending message to backend:", { message }); // Log the request being sent

      const response = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: message }),
      });

      const data = await response.json();

      if (response.ok) {
        // Add system response to chat with JSON data
        setChatHistory((prev) => [
          ...prev,
          {
            role: "system",
            content: "Floor plan generated successfully!",
            data: data.data, // Store the JSON data
          },
        ]);
        setDxfReady(true);
      } else {
        throw new Error(data.detail || "Failed to generate floor plan");
      }
    } catch (error: unknown) {
      const errorMessage =
        error instanceof Error ? error.message : "An unknown error occurred";
      setChatHistory((prev) => [
        ...prev,
        {
          role: "system",
          content: `Error generating floor plan: ${errorMessage}`,
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
    } catch (error: unknown) {
      const errorMessage =
        error instanceof Error ? error.message : "An unknown error occurred";
      setChatHistory((prev) => [
        ...prev,
        {
          role: "system",
          content: `Error downloading DXF file: ${errorMessage}`,
        },
      ]);
    }
  };

  return (
    <Card className="w-full max-w-2xl mx-auto h-[calc(100vh-2rem)] flex flex-col overflow-y-auto overflow-x-auto">
      <CardHeader>
        <CardTitle>Floor Plan Generator</CardTitle>
      </CardHeader>
      <CardContent className="flex-1 flex flex-col">
        <div className="flex-1 flex flex-col space-y-4">
          <div className="flex-1 overflow-y-auto space-y-4 p-4 border rounded-lg">
            {chatHistory.map((msg, index) => (
              <div
                key={index}
                className={`flex ${
                  msg.role === "user" ? "justify-end" : "justify-start"
                }`}
              >
                <div
                  className={`max-w-[85%] p-3 rounded-lg ${
                    msg.role === "user"
                      ? "bg-primary text-primary-foreground"
                      : "bg-muted"
                  }`}
                >
                  <div className="break-words">{msg.content}</div>
                  {msg.data && (
                    <pre className="mt-2 p-2 bg-background rounded text-sm overflow-x-auto whitespace-pre-wrap break-words">
                      {JSON.stringify(msg.data, null, 2)}
                    </pre>
                  )}
                </div>
              </div>
            ))}
          </div>

          {dxfReady && (
            <div className="flex justify-center py-2">
              <Button
                onClick={handleDownload}
                variant="secondary"
                className="w-full max-w-xs"
              >
                Download DXF
              </Button>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <Textarea
              placeholder="Describe your floor plan..."
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              disabled={loading}
              className="min-h-[100px] resize-none"
            />
            <Button
              type="submit"
              disabled={loading || !message.trim()}
              className="w-full"
            >
              {loading ? "Generating..." : "Generate Floor Plan"}
            </Button>
          </form>
        </div>
      </CardContent>
    </Card>
  );
}
