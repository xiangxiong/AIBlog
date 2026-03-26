import "@testing-library/jest-dom/vitest";
import { afterEach, beforeEach, vi } from "vitest";
import { cleanup } from "@testing-library/react";
import { clearToasts } from "../src/shared/lib/uiStore";
import { clearSession } from "../src/shared/lib/session";

beforeEach(() => {
  localStorage.clear();
  clearSession();
  clearToasts();
});

afterEach(() => {
  cleanup();
  localStorage.clear();
  clearSession();
  clearToasts();
  vi.useRealTimers();
});
