#!/usr/bin/env node
"use strict";

const fs = require("fs");
const os = require("os");
const path = require("path");
const { execFileSync } = require("child_process");

const ENTRYPOINT_PROMPTS = [
  "t2c_code.prompt.md",
  "t2c_integration_tests.prompt.md",
  "t2c_review.prompt.md",
  "t2c_screen_transition_tests.prompt.md",
];

function repoRoot() {
  return path.resolve(__dirname, "..");
}

function readVersion() {
  const pkg = JSON.parse(fs.readFileSync(path.join(repoRoot(), "package.json"), "utf8"));
  return String(pkg.version).trim();
}

function ensureTargetDir(target) {
  if (!fs.existsSync(target) || !fs.statSync(target).isDirectory()) {
    console.error(`ERROR: target directory does not exist: ${target}`);
    process.exit(1);
  }
}

function copyTree(src, dst) {
  fs.mkdirSync(dst, { recursive: true });
  fs.cpSync(src, dst, { recursive: true });
}

function userDataBaseDir() {
  if (process.platform === "darwin") {
    return path.join(os.homedir(), "Library", "Application Support", "ticket2code");
  }
  if (process.platform === "win32") {
    const localAppData = process.env.LOCALAPPDATA;
    if (localAppData) {
      return path.join(localAppData, "ticket2code");
    }
    return path.join(os.homedir(), "AppData", "Local", "ticket2code");
  }
  const xdgDataHome = process.env.XDG_DATA_HOME;
  if (xdgDataHome) {
    return path.join(xdgDataHome, "ticket2code");
  }
  return path.join(os.homedir(), ".local", "share", "ticket2code");
}

function userCacheDir() {
  if (process.platform === "darwin") {
    return path.join(os.homedir(), "Library", "Caches", "ticket2code");
  }
  if (process.platform === "win32") {
    const localAppData = process.env.LOCALAPPDATA;
    if (localAppData) {
      return path.join(localAppData, "ticket2code", "cache");
    }
    return path.join(os.homedir(), "AppData", "Local", "ticket2code", "cache");
  }
  const xdgCacheHome = process.env.XDG_CACHE_HOME;
  if (xdgCacheHome) {
    return path.join(xdgCacheHome, "ticket2code");
  }
  return path.join(os.homedir(), ".cache", "ticket2code");
}

function userLogsDir() {
  if (process.platform === "darwin") {
    return path.join(os.homedir(), "Library", "Logs", "ticket2code");
  }
  if (process.platform === "win32") {
    const localAppData = process.env.LOCALAPPDATA;
    if (localAppData) {
      return path.join(localAppData, "ticket2code", "logs");
    }
    return path.join(os.homedir(), "AppData", "Local", "ticket2code", "logs");
  }
  const xdgStateHome = process.env.XDG_STATE_HOME;
  if (xdgStateHome) {
    return path.join(xdgStateHome, "ticket2code", "logs");
  }
  return path.join(os.homedir(), ".local", "state", "ticket2code", "logs");
}

function runtimeDir(version) {
  return path.join(userDataBaseDir(), "runtime", version);
}

function assetsDir(version) {
  return path.join(userDataBaseDir(), "assets", version);
}

function projectT2cDir(target) {
  return path.join(target, ".t2c");
}

function projectLockPath(target) {
  return path.join(projectT2cDir(target), "lock.json");
}

function ensureUserRuntime(version) {
  const src = repoRoot();
  const rtDir = runtimeDir(version);
  const asDir = assetsDir(version);

  fs.mkdirSync(rtDir, { recursive: true });
  fs.mkdirSync(asDir, { recursive: true });
  fs.mkdirSync(userCacheDir(), { recursive: true });
  fs.mkdirSync(userLogsDir(), { recursive: true });

  copyTree(path.join(src, "core", "hooks"), path.join(rtDir, "hooks"));
  copyTree(path.join(src, "core", "prompts"), path.join(asDir, "prompts"));
  copyTree(path.join(src, "core", "skills"), path.join(asDir, "skills"));
  copyTree(path.join(src, "workflows"), path.join(asDir, "workflows"));
  fs.copyFileSync(
    path.join(src, "templates", "project", "SETUP.md"),
    path.join(asDir, "SETUP.md")
  );
}

function syncEntrypointPromptsToProject(target) {
  const srcPromptsDir = path.join(repoRoot(), "core", "prompts");
  const dstPromptsDir = path.join(target, ".github", "prompts");
  fs.mkdirSync(dstPromptsDir, { recursive: true });

  for (const promptName of ENTRYPOINT_PROMPTS) {
    fs.copyFileSync(
      path.join(srcPromptsDir, promptName),
      path.join(dstPromptsDir, promptName)
    );
  }
}

function writeLockFile(target, version) {
  const payload = {
    schema: "t2c-lock/v1",
    version: version,
    installed_at: new Date().toISOString(),
    runtime_path: runtimeDir(version),
    assets_path: assetsDir(version),
  };
  const lockPath = projectLockPath(target);
  fs.mkdirSync(path.dirname(lockPath), { recursive: true });
  fs.writeFileSync(lockPath, JSON.stringify(payload, null, 2) + "\n", "utf8");
}

function readLockedVersion(target) {
  const lockPath = projectLockPath(target);
  if (!fs.existsSync(lockPath)) {
    return "";
  }
  try {
    const payload = JSON.parse(fs.readFileSync(lockPath, "utf8"));
    return typeof payload.version === "string" ? payload.version : "";
  } catch (err) {
    return "";
  }
}

function detectPython() {
  for (const candidate of ["python3", "python"]) {
    try {
      const out = execFileSync(candidate, ["--version"], {
        stdio: ["ignore", "pipe", "pipe"],
      })
        .toString()
        .trim();
      return { command: candidate, version: out };
    } catch (err) {
      // try next candidate
    }
  }
  return null;
}

function initCommand(target) {
  const src = repoRoot();
  ensureTargetDir(target);
  const version = readVersion();

  console.log(`Installing ticket2code hybrid runtime into: ${target}`);

  for (const rel of [
    ".t2c/state",
    "docs/report",
    "docs/test/integration",
    "docs/test/screen-transition",
  ]) {
    fs.mkdirSync(path.join(target, rel), { recursive: true });
  }

  ensureUserRuntime(version);
  syncEntrypointPromptsToProject(target);
  writeLockFile(target, version);

  const configPath = path.join(target, ".t2c", "config.yaml");
  if (!fs.existsSync(configPath)) {
    fs.copyFileSync(
      path.join(src, "templates", "project", "ticket2code.config.yaml"),
      configPath
    );
  }

  const envPath = path.join(target, ".env.local");
  if (!fs.existsSync(envPath)) {
    fs.copyFileSync(
      path.join(src, "templates", "project", "env.local.example"),
      path.join(target, ".env.local.example")
    );
  }

  console.log("Done.");
  console.log("Next steps:");
  console.log(`1) Edit ${configPath}`);
  console.log(`2) Create ${path.join(target, ".env.local")} from .env.local.example`);
  console.log(`3) Runtime path: ${runtimeDir(version)}`);
  console.log(`4) Assets path: ${assetsDir(version)}`);
  console.log(`5) Entrypoint prompts path: ${path.join(target, ".github", "prompts")}`);
  console.log(`6) Run: t2c doctor --target-dir ${target}`);
  return 0;
}

function uninstallCommand(target, purge) {
  ensureTargetDir(target);
  console.log(`Removing ticket2code hybrid install metadata from: ${target}`);

  const t2cDir = projectT2cDir(target);
  if (fs.existsSync(t2cDir)) {
    fs.rmSync(t2cDir, { recursive: true, force: true });
  }

  const promptsDir = path.join(target, ".github", "prompts");
  for (const promptName of ENTRYPOINT_PROMPTS) {
    const promptPath = path.join(promptsDir, promptName);
    if (fs.existsSync(promptPath)) {
      fs.rmSync(promptPath);
    }
  }

  console.log("Removed project-local .t2c metadata and t2c prompt entrypoints.");

  if (purge) {
    const userDirs = [userDataBaseDir(), userCacheDir(), userLogsDir()];
    for (const dir of userDirs) {
      if (fs.existsSync(dir)) {
        fs.rmSync(dir, { recursive: true, force: true });
        console.log(`Removed shared user-level directory: ${dir}`);
      }
    }
    console.log("Purged shared user-level runtime/assets/cache/logs.");
  } else {
    console.log("Shared user-level runtime/assets were not removed.");
    console.log("Re-run with --purge to also remove them, or delete them manually.");
  }
  return 0;
}

function upgradeCommand(target) {
  const src = repoRoot();
  ensureTargetDir(target);
  const version = readVersion();

  console.log(`Upgrading ticket2code hybrid runtime in: ${target}`);

  fs.mkdirSync(path.join(target, ".t2c", "state"), { recursive: true });
  ensureUserRuntime(version);
  syncEntrypointPromptsToProject(target);
  writeLockFile(target, version);

  const configPath = path.join(target, ".t2c", "config.yaml");
  if (!fs.existsSync(configPath)) {
    fs.copyFileSync(
      path.join(src, "templates", "project", "ticket2code.config.yaml"),
      configPath
    );
  }

  console.log("Upgrade completed");
  console.log(`Runtime path: ${runtimeDir(version)}`);
  console.log(`Assets path: ${assetsDir(version)}`);
  console.log(`Entrypoint prompts path: ${path.join(target, ".github", "prompts")}`);
  return 0;
}

function doctorCommand(target) {
  let missing = false;
  ensureTargetDir(target);

  let version = readLockedVersion(target);
  if (!version) {
    version = readVersion();
  }

  const projectChecks = [
    ".t2c/config.yaml",
    ".t2c/lock.json",
    ".t2c/state",
    ".github/prompts/t2c_code.prompt.md",
    ".github/prompts/t2c_integration_tests.prompt.md",
    ".github/prompts/t2c_review.prompt.md",
    ".github/prompts/t2c_screen_transition_tests.prompt.md",
    ".env.local",
  ];

  const userChecks = [
    path.join(runtimeDir(version), "hooks", "safety-guard.json"),
    path.join(runtimeDir(version), "hooks", "scripts", "pre_tool_guard.py"),
    path.join(assetsDir(version), "prompts", "t2c_code.prompt.md"),
    path.join(assetsDir(version), "skills", "jira-pbi-analysis", "SKILL.md"),
    path.join(assetsDir(version), "workflows", "code", "code-agent.md"),
  ];

  for (const rel of projectChecks) {
    if (fs.existsSync(path.join(target, rel))) {
      console.log(`OK   ${rel}`);
    } else {
      console.log(`MISS ${rel}`);
      missing = true;
    }
  }

  for (const full of userChecks) {
    if (fs.existsSync(full)) {
      console.log(`OK   ${full}`);
    } else {
      console.log(`MISS ${full}`);
      missing = true;
    }
  }

  // Python is required at skill runtime (OCR, Excel, Figma, hooks), not for the CLI.
  const python = detectPython();
  if (python) {
    console.log(`OK   python runtime (${python.command}: ${python.version})`);
  } else {
    console.log("WARN python runtime not found (required to run t2c skills)");
  }

  if (missing) {
    console.log("Doctor check failed. Missing required files.");
    return 1;
  }

  console.log("Doctor check passed.");
  return 0;
}

function parseArgs(argv) {
  const command = argv[0];
  let targetDir = process.cwd();
  let purge = false;

  for (let i = 1; i < argv.length; i += 1) {
    if (argv[i] === "--target-dir") {
      if (i + 1 >= argv.length) {
        console.error("ERROR: --target-dir requires a value.");
        process.exit(1);
      }
      targetDir = argv[i + 1];
      i += 1;
    } else if (argv[i] === "--purge") {
      purge = true;
    }
  }

  return { command, targetDir: path.resolve(targetDir), purge };
}

function printHelp() {
  console.log("Usage: t2c <command> [--target-dir <path>]");
  console.log("");
  console.log("Commands:");
  console.log("  init         Install hybrid runtime into a target project (alias: install)");
  console.log("  upgrade      Refresh runtime/assets and lock in a target project");
  console.log("  uninstall    Remove project-local .t2c metadata and t2c prompt entrypoints");
  console.log("  doctor       Validate install state (project + user-level + python runtime)");
  console.log("");
  console.log("Options:");
  console.log("  --target-dir <path>   Target project directory (defaults to current directory).");
  console.log("  --purge               With uninstall, also remove shared user-level runtime/assets/cache/logs.");
  console.log("  -v, --version         Print the ticket2code version and exit.");
  console.log("  -h, --help            Print this help message and exit.");
}

function main() {
  const argv = process.argv.slice(2);

  if (argv.length === 0 || argv[0] === "-h" || argv[0] === "--help") {
    printHelp();
    return 0;
  }

  if (argv[0] === "-v" || argv[0] === "--version" || argv[0] === "version") {
    console.log(readVersion());
    return 0;
  }

  const { command, targetDir, purge } = parseArgs(argv);

  switch (command) {
    case "init":
    case "install":
      return initCommand(targetDir);
    case "uninstall":
      return uninstallCommand(targetDir, purge);
    case "upgrade":
      return upgradeCommand(targetDir);
    case "doctor":
      return doctorCommand(targetDir);
    default:
      console.error(`Unsupported command: ${command}`);
      printHelp();
      return 1;
  }
}

process.exit(main());
