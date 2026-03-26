import fs from "node:fs";
import path from "node:path";

const projectRoot = path.resolve(import.meta.dirname, "..");
const srcRoot = path.join(projectRoot, "src");

const sourceFiles = collectFiles(srcRoot).filter((filePath) =>
  /\.(ts|tsx)$/.test(filePath)
);

const errors = [];

for (const filePath of sourceFiles) {
  const source = fs.readFileSync(filePath, "utf8");
  const imports = [...source.matchAll(/from\s+["']([^"']+)["']/g)].map((match) => match[1]);

  for (const specifier of imports) {
    if (!specifier.startsWith(".")) {
      continue;
    }

    const resolvedTarget = resolveImport(filePath, specifier);
    if (!resolvedTarget || !resolvedTarget.startsWith(srcRoot)) {
      continue;
    }

    const fromCategory = getCategory(filePath);
    const toCategory = getCategory(resolvedTarget);

    if (!isAllowed(fromCategory, toCategory, filePath, resolvedTarget)) {
      errors.push(
        `${formatPath(filePath)} cannot import ${formatPath(resolvedTarget)} (${fromCategory} -> ${toCategory})`
      );
    }
  }
}

if (errors.length > 0) {
  console.error("Architecture guard failed:\n");
  for (const error of errors) {
    console.error(`- ${error}`);
  }
  process.exit(1);
}

console.log(`Architecture guard passed for ${sourceFiles.length} source files.`);

function collectFiles(directory) {
  const entries = fs.readdirSync(directory, { withFileTypes: true });
  const results = [];

  for (const entry of entries) {
    const fullPath = path.join(directory, entry.name);
    if (entry.isDirectory()) {
      results.push(...collectFiles(fullPath));
    } else {
      results.push(fullPath);
    }
  }

  return results;
}

function resolveImport(fromFile, specifier) {
  const basePath = path.resolve(path.dirname(fromFile), specifier);
  const candidates = [
    basePath,
    `${basePath}.ts`,
    `${basePath}.tsx`,
    path.join(basePath, "index.ts"),
    path.join(basePath, "index.tsx")
  ];

  return candidates.find((candidate) => fs.existsSync(candidate));
}

function getCategory(filePath) {
  const relative = path.relative(srcRoot, filePath).split(path.sep);

  if (relative[0] === "app") {
    return "app";
  }

  if (relative.length === 1 && relative[0] === "main.tsx") {
    return "app";
  }

  if (relative[0] === "shared") {
    return "shared";
  }

  if (relative[0] === "domains") {
    const domainName = relative[1];
    const layer = relative[2];
    return `domain:${domainName}:${layer}`;
  }

  return "unknown";
}

function isAllowed(fromCategory, toCategory, fromFile, targetFile) {
  if (toCategory === "shared") {
    return true;
  }

  if (fromCategory === "app") {
    return toCategory === "app" || (toCategory.startsWith("domain:") && toCategory.endsWith(":ui"));
  }

  if (fromCategory === "shared") {
    return toCategory === "shared";
  }

  if (fromCategory.startsWith("domain:")) {
    const [_, fromDomain, fromLayer] = fromCategory.split(":");
    if (!toCategory.startsWith("domain:")) {
      return false;
    }
    const [__, toDomain, toLayer] = toCategory.split(":");

    if (fromDomain !== toDomain) {
      return false;
    }

    if (fromLayer === "ui") {
      return ["ui", "service", "types"].includes(toLayer);
    }

    if (fromLayer === "service") {
      return ["service", "types"].includes(toLayer);
    }

    if (fromLayer === "types") {
      return toLayer === "types" && path.dirname(fromFile) === path.dirname(targetFile);
    }
  }

  return false;
}

function formatPath(filePath) {
  return path.relative(projectRoot, filePath);
}
