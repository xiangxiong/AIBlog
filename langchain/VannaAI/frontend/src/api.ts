import type { ChatResponse, HistoryItem, SchemaResponse } from "./types";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

async function requestJson<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...init?.headers,
    },
    ...init,
  });

  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export function askQuestion(question: string, sessionId: string | null): Promise<ChatResponse> {
  return requestJson<ChatResponse>("/api/chat", {
    method: "POST",
    body: JSON.stringify({
      question,
      session_id: sessionId,
      show_sql: true,
      include_summary: true,
    }),
  });
}

export function fetchHistory(): Promise<HistoryItem[]> {
  return requestJson<HistoryItem[]>("/api/history");
}

export function fetchSchema(): Promise<SchemaResponse> {
  return requestJson<SchemaResponse>("/api/schema");
}
