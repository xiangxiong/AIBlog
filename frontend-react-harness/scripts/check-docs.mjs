import fs from "node:fs";
import path from "node:path";

const projectRoot = path.resolve(import.meta.dirname, "..");

const requiredFiles = [
  "AGENTS.md",
  "ARCHITECTURE.md",
  "README.md",
  "docs/index.md",
  "docs/API.md",
  "docs/CI.md",
  "docs/COVERAGE.md",
  "docs/design-docs/index.md",
  "docs/design-docs/core-beliefs.md",
  "docs/exec-plans/active/add-testing-ci-baseline.md",
  "docs/exec-plans/active/bootstrap-react-frontend.md",
  "docs/exec-plans/active/upgrade-business-shell.md",
  "docs/product-specs/index.md",
  "docs/FRONTEND.md",
  "docs/PLANS.md",
  "docs/QUALITY_SCORE.md",
  "docs/ROUTES.md",
  "docs/STATE.md",
  "docs/TESTING.md",
  "docs/RELIABILITY.md",
  "docs/SECURITY.md"
];

const missing = [];
const empty = [];

for (const relativePath of requiredFiles) {
  const absolutePath = path.join(projectRoot, relativePath);
  if (!fs.existsSync(absolutePath)) {
    missing.push(relativePath);
    continue;
  }

  const contents = fs.readFileSync(absolutePath, "utf8").trim();
  if (contents.length === 0) {
    empty.push(relativePath);
  }
}

if (missing.length > 0 || empty.length > 0) {
  console.error("Documentation guard failed.\n");

  if (missing.length > 0) {
    console.error("Missing files:");
    for (const item of missing) {
      console.error(`- ${item}`);
    }
  }

  if (empty.length > 0) {
    console.error("Empty files:");
    for (const item of empty) {
      console.error(`- ${item}`);
    }
  }

  process.exit(1);
}

console.log(`Documentation guard passed for ${requiredFiles.length} required files.`);
