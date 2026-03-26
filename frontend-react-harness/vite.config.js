import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";
export default defineConfig({
    plugins: [react()],
    server: {
        host: "0.0.0.0",
        port: 4173
    },
    test: {
        environment: "jsdom",
        setupFiles: "./tests/setup.ts",
        globals: true,
        css: true,
        coverage: {
            provider: "v8",
            reporter: ["text", "html", "json-summary"],
            reportsDirectory: "./coverage",
            include: ["src/**/*.ts", "src/**/*.tsx"],
            exclude: [
                "src/main.tsx",
                "src/app/app.css"
            ]
        }
    }
});
