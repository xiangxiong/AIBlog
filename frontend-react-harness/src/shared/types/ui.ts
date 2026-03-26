export type ToastTone = "success" | "error" | "info";

export type ToastItem = {
  id: string;
  title: string;
  description: string;
  tone: ToastTone;
};
