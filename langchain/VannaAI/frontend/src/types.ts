export type ChartConfig = {
  type: "bar" | "line" | "pie" | string;
  x: string | null;
  y: string | null;
  reason: string;
};

export type ChatResponse = {
  session_id: string;
  question: string;
  sql: string | null;
  columns: string[];
  rows: unknown[][];
  row_count: number;
  execution_ms: number;
  chart: ChartConfig | null;
  summary: string | null;
  error: string | null;
};

export type HistoryItem = {
  id: string;
  title: string;
  created_at: string;
  updated_at: string;
};

export type SchemaColumn = {
  table_name: string;
  column_name: string;
  data_type: string;
  is_nullable: boolean;
};

export type SchemaResponse = {
  tables: string[];
  columns: SchemaColumn[];
  foreign_keys: Array<Record<string, string>>;
  prompt_context: string;
};
