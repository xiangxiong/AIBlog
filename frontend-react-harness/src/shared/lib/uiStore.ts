import { useSyncExternalStore } from "react";
import type { ToastItem, ToastTone } from "../types/ui";

type UiState = {
  toasts: ToastItem[];
};

const listeners = new Set<() => void>();
let state: UiState = {
  toasts: []
};

export function useUiState() {
  return useSyncExternalStore(subscribe, getSnapshot, getSnapshot);
}

export function pushToast(input: {
  title: string;
  description: string;
  tone?: ToastTone;
}) {
  const toast: ToastItem = {
    id: createToastId(),
    title: input.title,
    description: input.description,
    tone: input.tone ?? "info"
  };

  state = {
    ...state,
    toasts: [...state.toasts, toast]
  };
  emitChange();

  window.setTimeout(() => {
    dismissToast(toast.id);
  }, 3200);
}

export function dismissToast(id: string) {
  const nextToasts = state.toasts.filter((toast) => toast.id !== id);
  if (nextToasts.length === state.toasts.length) {
    return;
  }

  state = {
    ...state,
    toasts: nextToasts
  };
  emitChange();
}

export function clearToasts() {
  if (state.toasts.length === 0) {
    return;
  }

  state = {
    ...state,
    toasts: []
  };
  emitChange();
}

function subscribe(listener: () => void) {
  listeners.add(listener);
  return () => {
    listeners.delete(listener);
  };
}

function emitChange() {
  for (const listener of listeners) {
    listener();
  }
}

function getSnapshot() {
  return state;
}

function createToastId() {
  return `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
}
