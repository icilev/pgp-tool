#!/usr/bin/env node

import { spawn, execSync } from "child_process";
import { existsSync, readFileSync } from "fs";
import { fileURLToPath } from "url";
import { dirname, join } from "path";
import { get } from "https";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const rootDir = join(__dirname, "..");

// ─── ANSI ──────────────────────────────────────────────────────────────────
const c = {
  reset:          "\x1b[0m",
  bold:           "\x1b[1m",
  dim:            "\x1b[2m",
  italic:         "\x1b[3m",
  cyan:           "\x1b[36m",
  green:          "\x1b[32m",
  yellow:         "\x1b[33m",
  red:            "\x1b[31m",
  magenta:        "\x1b[35m",
  blue:           "\x1b[34m",
  white:          "\x1b[37m",
  brightCyan:     "\x1b[96m",
  brightGreen:    "\x1b[92m",
  brightYellow:   "\x1b[93m",
  brightMagenta:  "\x1b[95m",
  brightBlue:     "\x1b[94m",
  brightWhite:    "\x1b[97m",
  bgBlack:        "\x1b[40m",
  bgCyan:         "\x1b[46m",
  bgGreen:        "\x1b[42m",
};

// ─── LAYOUT ────────────────────────────────────────────────────────────────
const W = Math.min(process.stdout.columns || 72, 72);
const inner = W - 4; // space inside │  …  │

const box = {
  tl: "╭", tr: "╮", bl: "╰", br: "╯",
  h: "─", v: "│",
  tls: "┌", trs: "┐", bls: "└", brs: "┘",
  ml: "├", mr: "┤",
};

function line(char = box.h, n = W) { return char.repeat(n); }

function pad(str, width) {
  const visible = str.replace(/\x1b\[[0-9;]*m/g, "");
  return str + " ".repeat(Math.max(0, width - visible.length));
}

function row(content, color = c.dim) {
  const padded = pad(content, inner);
  console.log(`${color}${box.v}${c.reset}  ${padded}  ${color}${box.v}${c.reset}`);
}

function topBorder(color = c.dim)    { console.log(`${color}${box.tl}${line(box.h, W - 2)}${box.tr}${c.reset}`); }
function botBorder(color = c.dim)    { console.log(`${color}${box.bl}${line(box.h, W - 2)}${box.br}${c.reset}`); }
function midBorder(color = c.dim)    { console.log(`${color}${box.ml}${line(box.h, W - 2)}${box.mr}${c.reset}`); }
function emptyRow(color = c.dim)     { row("", color); }

// ─── CONFIG ────────────────────────────────────────────────────────────────
let config = { host: "127.0.0.1", port: 5000 };

function loadEnv() {
  const envPath = join(rootDir, ".env");
  if (existsSync(envPath)) {
    readFileSync(envPath, "utf-8").split("\n").forEach((line) => {
      const m = line.match(/^(\w+)=(.*)$/);
      if (m) {
        if (m[1] === "PORT") config.port = parseInt(m[2]) || 5000;
        if (m[1] === "HOST") config.host = m[2] || "127.0.0.1";
      }
    });
  }
}

function getUrl() {
  const h = config.host === "127.0.0.1" || config.host === "0.0.0.0"
    ? "localhost" : config.host;
  return `http://${h}:${config.port}`;
}

// ─── CHECKS ────────────────────────────────────────────────────────────────
function checkGnuPG() {
  try {
    const v = execSync("gpg --version", { encoding: "utf-8" });
    const m = v.match(/gpg \(GnuPG\) ([\d.]+)/);
    return m ? m[1] : "unknown";
  } catch { return null; }
}

function checkVenv() {
  return existsSync(join(rootDir, "venv"));
}

function getPythonPath() {
  const p = join(rootDir, "venv", "bin", "python");
  return existsSync(p) ? p : "python3";
}

function checkPipUpdates(pythonPath) {
  try {
    const out = execSync(
      `${pythonPath} -m pip list --outdated --format=columns 2>/dev/null`,
      { encoding: "utf-8", timeout: 10000 }
    );
    return out.trim().split("\n")
      .filter((l) => l.trim() && !l.startsWith("Package") && !l.startsWith("---"));
  } catch { return null; }
}

function fetchJson(url) {
  return new Promise((resolve, reject) => {
    get(url, { headers: { "User-Agent": "pgp-tool-cli" } }, (res) => {
      let data = "";
      res.on("data", (chunk) => (data += chunk));
      res.on("end", () => {
        try { resolve(JSON.parse(data)); }
        catch { reject(new Error("Invalid JSON")); }
      });
    }).on("error", reject);
  });
}

async function checkGitHubUpdates() {
  try {
    const local = execSync("git rev-parse HEAD", { encoding: "utf-8", cwd: rootDir }).trim();
    const data  = await fetchJson("https://api.github.com/repos/icilev/pgp-tool/commits/main");
    if (!data.sha) return { upToDate: null };
    if (local === data.sha) return { upToDate: true };
    return {
      upToDate:    false,
      localShort:  local.slice(0, 7),
      remoteShort: data.sha.slice(0, 7),
      message:     data.commit?.message?.split("\n")[0] || "",
      date:        data.commit?.author?.date
                     ? new Date(data.commit.author.date).toLocaleDateString("fr-FR")
                     : "",
    };
  } catch { return { upToDate: null }; }
}

// ─── LOGO ──────────────────────────────────────────────────────────────────
function printBanner(mode) {
  const logoLines = [
    `${c.brightCyan}${c.bold} ██████╗  ██████╗ ██████╗    ████████╗ ██████╗  ██████╗ ██╗${c.reset}`,
    `${c.brightCyan}${c.bold} ██╔══██╗██╔════╝ ██╔══██╗   ╚══██╔══╝██╔═══██╗██╔═══██╗██║${c.reset}`,
    `${c.cyan}${c.bold} ██████╔╝██║  ███╗██████╔╝      ██║   ██║   ██║██║   ██║██║${c.reset}`,
    `${c.cyan}${c.bold} ██╔═══╝ ██║   ██║██╔═══╝       ██║   ██║   ██║██║   ██║██║${c.reset}`,
    `${c.blue}${c.bold} ██║     ╚██████╔╝██║           ██║   ╚██████╔╝╚██████╔╝███████╗${c.reset}`,
    `${c.blue}${c.bold} ╚═╝      ╚═════╝ ╚═╝           ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝${c.reset}`,
  ];

  const modeTag = mode === "dev"
    ? `${c.bgBlack}${c.brightYellow}${c.bold}  DEV  ${c.reset}`
    : `${c.bgBlack}${c.brightGreen}${c.bold}  PROD  ${c.reset}`;

  console.log();
  logoLines.forEach((l) => console.log(" " + l));
  console.log();
  console.log(
    `  ${c.dim}Secure PGP Operations${c.reset}  ${c.dim}·${c.reset}  Encrypt · Decrypt · Sign · Verify  ${modeTag}`
  );
  console.log();
}

// ─── SYSTEM CHECK BOX ──────────────────────────────────────────────────────
function printSystemCheck(venvOk, gpgVersion) {
  const accent = c.brightCyan;

  topBorder(accent);
  row(`${c.bold}${c.brightWhite}  SYSTEM CHECK${c.reset}`, accent);
  midBorder(accent);
  emptyRow(accent);

  // venv
  const venvStatus = venvOk
    ? `${c.brightGreen}${c.bold}● READY${c.reset}`
    : `${c.red}${c.bold}● MISSING${c.reset}`;
  row(`  ${c.dim}venv${c.reset}       ${pad("", 6)} ${venvStatus}`, accent);

  // gpg
  const gpgStatus = gpgVersion
    ? `${c.brightGreen}${c.bold}● v${gpgVersion}  READY${c.reset}`
    : `${c.red}${c.bold}● NOT INSTALLED${c.reset}`;
  row(`  ${c.dim}GnuPG${c.reset}      ${pad("", 6)} ${gpgStatus}`, accent);

  emptyRow(accent);
  botBorder(accent);
  console.log();
}

// ─── UPDATES BOX (auto-apply) ──────────────────────────────────────────────
async function applyUpdates(pythonPath) {
  const accent = c.brightMagenta;

  // Run checks in parallel
  const [outdated, github] = await Promise.all([
    Promise.resolve(checkPipUpdates(pythonPath)),
    checkGitHubUpdates(),
  ]);

  topBorder(accent);
  row(`${c.bold}${c.brightWhite}  UPDATES${c.reset}`, accent);
  midBorder(accent);
  emptyRow(accent);

  // ── GitHub
  if (github.upToDate === null) {
    row(`  ${c.dim}github${c.reset}     ${pad("", 6)} ${c.dim}● unreachable${c.reset}`, accent);
  } else if (github.upToDate) {
    row(`  ${c.dim}github${c.reset}     ${pad("", 6)} ${c.brightGreen}${c.bold}● up to date${c.reset}`, accent);
  } else {
    row(`  ${c.dim}github${c.reset}     ${pad("", 6)} ${c.brightYellow}${c.bold}● pulling…  ${c.dim}${github.localShort} → ${github.remoteShort}${c.reset}`, accent);
    if (github.message) {
      row(`  ${c.dim}  "${github.message}"${github.date ? `  ${github.date}` : ""}${c.reset}`, accent);
    }
    try {
      execSync("git pull --ff-only", { cwd: rootDir, stdio: "pipe" });
      row(`  ${c.dim}          ${pad("", 6)}${c.reset} ${c.brightGreen}${c.bold}● pulled ✓${c.reset}`, accent);
    } catch {
      row(`  ${c.dim}          ${pad("", 6)}${c.reset} ${c.red}${c.bold}● pull failed — run manually${c.reset}`, accent);
    }
  }

  emptyRow(accent);

  // ── pip
  if (outdated === null) {
    row(`  ${c.dim}pip${c.reset}        ${pad("", 6)} ${c.dim}● unreachable${c.reset}`, accent);
  } else if (outdated.length === 0) {
    row(`  ${c.dim}pip${c.reset}        ${pad("", 6)} ${c.brightGreen}${c.bold}● up to date${c.reset}`, accent);
  } else {
    row(`  ${c.dim}pip${c.reset}        ${pad("", 6)} ${c.brightYellow}${c.bold}● upgrading ${outdated.length} package(s)…${c.reset}`, accent);
    outdated.forEach((pkg) => {
      const [name, cur, latest] = pkg.trim().split(/\s+/);
      if (name && cur && latest) {
        row(`  ${c.dim}  ${pad(name, 18)} ${c.yellow}${cur}${c.reset} ${c.dim}→${c.reset} ${c.brightGreen}${latest}${c.reset}`, accent);
      }
    });
    try {
      execSync(`${pythonPath} -m pip install -r requirements.txt --upgrade -q 2>/dev/null`, {
        cwd: rootDir, stdio: "pipe",
      });
      row(`  ${c.dim}          ${pad("", 6)}${c.reset} ${c.brightGreen}${c.bold}● upgraded ✓${c.reset}`, accent);
    } catch {
      row(`  ${c.dim}          ${pad("", 6)}${c.reset} ${c.red}${c.bold}● upgrade failed — run manually${c.reset}`, accent);
    }
  }

  emptyRow(accent);
  botBorder(accent);
  console.log();
}

// ─── SERVER READY BOX ──────────────────────────────────────────────────────
function printServerReady() {
  const url    = getUrl();
  const accent = c.brightGreen;

  console.log();
  topBorder(accent);
  row(`${c.brightGreen}${c.bold}  ◉  SERVER ONLINE${c.reset}`, accent);
  midBorder(accent);
  emptyRow(accent);
  row(`  ${c.dim}Local${c.reset}   ${c.dim}→${c.reset}   ${c.brightGreen}${c.bold}${c.italic}${url}${c.reset}`, accent);
  emptyRow(accent);
  botBorder(accent);
  console.log();
  console.log(`  ${c.dim}ctrl+c to stop  ·  auto-reload enabled${c.reset}`);
  console.log();
}

// ─── HTTP LOG ──────────────────────────────────────────────────────────────
const METHOD_COLOR = {
  GET:    c.brightCyan,
  POST:   c.brightMagenta,
  PUT:    c.brightYellow,
  DELETE: c.red,
  PATCH:  c.brightBlue,
};

function printRequest(method, path, status) {
  const now = new Date().toLocaleTimeString("fr-FR", { hour12: false });
  const mc  = METHOD_COLOR[method] || c.white;
  const sc  = status.startsWith("2") ? c.brightGreen
            : status.startsWith("3") ? c.brightCyan
            : status.startsWith("4") ? c.brightYellow
            : c.red;

  const mPad  = pad(`${mc}${c.bold}${method}${c.reset}`, 4 + mc.length + c.bold.length + c.reset.length);
  const sPad  = `${sc}${c.bold}${status}${c.reset}`;
  const dot   = status.startsWith("2") ? `${c.brightGreen}●${c.reset}` : `${c.brightYellow}●${c.reset}`;

  console.log(`  ${c.dim}${now}${c.reset}  ${dot}  ${mPad}  ${c.dim}${path}${c.reset}  ${sPad}`);
}

// ─── MAIN ──────────────────────────────────────────────────────────────────
async function main() {
  const args    = process.argv.slice(2);
  const command = args[0] || "dev";

  console.clear();
  loadEnv();
  printBanner(command);

  // ── System check
  const venvOk    = checkVenv();
  const gpgVersion = checkGnuPG();

  printSystemCheck(venvOk, gpgVersion);

  if (!gpgVersion) {
    console.log(`  ${c.red}${c.bold}GnuPG is required.${c.reset}  Install with:  ${c.brightCyan}brew install gnupg${c.reset}\n`);
    process.exit(1);
  }

  // Auto-setup venv + deps if missing (for npm start)
  if (!venvOk) {
    console.log(`  ${c.brightYellow}No venv found — setting up automatically…${c.reset}\n`);
    try {
      execSync("python3 -m venv venv", { cwd: rootDir, stdio: "inherit" });
    } catch {
      console.log(`  ${c.red}Failed to create venv. Is python3 installed?${c.reset}\n`);
      process.exit(1);
    }
  }

  // Always check that pip deps are installed (fast if already installed)
  {
    const py = getPythonPath();
    try {
      execSync(`${py} -m pip install -r requirements.txt -q 2>/dev/null`, {
        cwd: rootDir,
        stdio: "pipe",
      });
    } catch {
      console.log(`  ${c.red}Failed to install Python dependencies.${c.reset}\n`);
      process.exit(1);
    }
  }

  // ── Updates (auto-apply)
  await applyUpdates(getPythonPath());

  // ── Start Flask
  if (command === "dev" || command === "start") {
    const pythonPath = getPythonPath();
    const appPath    = join(rootDir, "app.py");

    const child = spawn(pythonPath, [appPath], {
      cwd: rootDir,
      stdio: ["inherit", "pipe", "pipe"],
      env: {
        ...process.env,
        FLASK_ENV: command === "dev" ? "development" : "production",
        PYTHONUNBUFFERED: "1",
      },
    });

    let serverReady = false;

    const onOutput = (data) => {
      const output = data.toString();

      if ((output.includes("Running on") || output.includes("Serving Flask app")) && !serverReady) {
        serverReady = true;
        printServerReady();
        setTimeout(() => {
          try { execSync(`open "${getUrl()}"`, { stdio: "ignore" }); } catch {}
        }, 500);
        return;
      }

      // HTTP request log
      const reqMatch = output.match(/(GET|POST|PUT|DELETE|PATCH)\s+([^\s]+).*?(\d{3})/);
      if (reqMatch) {
        printRequest(reqMatch[1], reqMatch[2], reqMatch[3]);
        return;
      }

      // Silence Flask noise
      if (/WARNING|\* Debug|\* Serving|\* Running|\* Restarting|\* Detected|Press CTRL/.test(output)) return;

      if (output.trim()) {
        console.log(`  ${c.dim}${output.trim()}${c.reset}`);
      }
    };

    child.stdout.on("data", onOutput);
    child.stderr.on("data", onOutput);

    child.on("close", (code) => {
      console.log();
      console.log(code === 0 || code === null
        ? `  ${c.dim}Server stopped gracefully.${c.reset}`
        : `  ${c.red}${c.bold}Server exited with code ${code}${c.reset}`
      );
      console.log();
    });

    process.on("SIGINT", () => {
      console.log(`\n\n  ${c.dim}Shutting down…${c.reset}\n`);
      child.kill("SIGINT");
    });

  } else if (command === "setup") {
    console.log(`\n  ${c.brightCyan}Setting up project…${c.reset}\n`);
    execSync("mkdir -p data keys && chmod 700 data keys", { cwd: rootDir });
    const py = getPythonPath();
    execSync(`${py} -m pip install -r requirements.txt --quiet`, { cwd: rootDir, stdio: "inherit" });
    console.log(`\n  ${c.brightGreen}${c.bold}✓ Setup complete${c.reset}\n`);

  } else {
    console.log(`\n  ${c.yellow}Unknown command: ${command}${c.reset}`);
    console.log(`\n  ${c.dim}dev${c.reset}    Start development server`);
    console.log(`  ${c.dim}start${c.reset}  Start production server`);
    console.log(`  ${c.dim}setup${c.reset}  Setup dependencies\n`);
  }
}

main().catch((err) => {
  console.error(`\n  ${c.red}${c.bold}Error:${c.reset} ${err.message}\n`);
  process.exit(1);
});
