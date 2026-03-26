import { useSyncExternalStore } from "react";
import type { SessionUser } from "../types/session";

const SESSION_KEY = "frontend-react-harness/session";
const listeners = new Set<() => void>();
let currentSession = readSessionFromStorage();

export function setSession(session: SessionUser) {
  localStorage.setItem(SESSION_KEY, JSON.stringify(session));
  currentSession = session;
  emitChange();
}

export function clearSession() {
  localStorage.removeItem(SESSION_KEY);
  currentSession = null;
  emitChange();
}

export function getSession() {
  return currentSession;
}

export function useSession() {
  return useSyncExternalStore(subscribe, getSession, () => null);
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

function readSessionFromStorage() {
  if (typeof window === "undefined") {
    return null;
  }

  const raw = localStorage.getItem(SESSION_KEY);
  if (!raw) {
    return null;
  }

  try {
    return JSON.parse(raw) as SessionUser;
  } catch {
    localStorage.removeItem(SESSION_KEY);
    return null;
  }
}
