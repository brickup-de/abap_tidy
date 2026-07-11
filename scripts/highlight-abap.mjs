import { readdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { createHighlighter } from "shiki";

const PUBLIC_DIR = path.resolve(import.meta.dirname, "..", "public");

// Both passes below do surgical string replacement on the exact
// "shiki-pending" marker text, never a full HTML parse + re-serialize of
// the whole file. A full DOM round-trip (previously tried with
// node-html-parser) mis-closes Hugo's --minify unquoted attribute values
// like `href=/clean-code/>` as self-closing tags, silently corrupting
// unrelated markup (e.g. moving sidebar/navbar links' text outside their
// <a> tags) across the entire page.
const HTML_PENDING_RE =
  /<div class="?shiki-pending"?[^>]*>\s*<pre>([\s\S]*?)<\/pre>\s*<\/div>/g;

// RSS/XML output (hextra's list.rss.xml) renders page .Content through the
// same codeblock render hook, then HTML-escapes the whole fragment once more
// (`{{ .Content | html }}`) to embed it as XML text, so the marker shows up
// double-escaped there.
const XML_PENDING_RE =
  /&lt;div class="shiki-pending" data-lang="abap"&gt;&lt;pre&gt;([\s\S]*?)&lt;\/pre&gt;&lt;\/div&gt;/g;

// Go's html/template (used by Hugo) always escapes "<", ">", "&" as the
// named entities below, and numeric-encodes any other character it decides
// to escape (currently '"', "'", "+" — but this covers whichever ones show
// up as ABAP syntax evolves, without needing to list them by hand).
function decodeEntitiesOnce(str) {
  return str
    .replace(/&#x([0-9a-fA-F]+);/g, (_, hex) => String.fromCodePoint(parseInt(hex, 16)))
    .replace(/&#(\d+);/g, (_, dec) => String.fromCodePoint(Number(dec)))
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&amp;/g, "&");
}

function encodeEntitiesOnce(str) {
  return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

async function findOutputFiles(dir) {
  const entries = await readdir(dir, { withFileTypes: true });
  const files = await Promise.all(
    entries.map((entry) => {
      const fullPath = path.join(dir, entry.name);
      if (entry.isDirectory()) return findOutputFiles(fullPath);
      if (entry.isFile() && /\.(html|xml)$/.test(entry.name)) return [fullPath];
      return [];
    }),
  );
  return files.flat();
}

function highlightAbap(highlighter, code) {
  return highlighter.codeToHtml(code, {
    lang: "abap",
    themes: { light: "github-light", dark: "github-dark" },
    defaultColor: false,
  });
}

function processHtml(highlighter, content) {
  if (!HTML_PENDING_RE.test(content)) return null;
  HTML_PENDING_RE.lastIndex = 0;

  return content.replace(HTML_PENDING_RE, (_match, escapedCode) => {
    const code = decodeEntitiesOnce(escapedCode);
    return highlightAbap(highlighter, code);
  });
}

function processXml(highlighter, content) {
  if (!XML_PENDING_RE.test(content)) return null;
  XML_PENDING_RE.lastIndex = 0;

  return content.replace(XML_PENDING_RE, (_match, escapedCode) => {
    const code = decodeEntitiesOnce(escapedCode);
    return encodeEntitiesOnce(highlightAbap(highlighter, code));
  });
}

async function main() {
  const highlighter = await createHighlighter({
    langs: ["abap"],
    themes: ["github-light", "github-dark"],
  });

  const files = await findOutputFiles(PUBLIC_DIR);
  let changed = 0;

  for (const file of files) {
    const content = await readFile(file, "utf8");
    if (!content.includes("shiki-pending")) continue;

    const updated = file.endsWith(".xml")
      ? processXml(highlighter, content)
      : processHtml(highlighter, content);
    if (updated === null) continue;

    await writeFile(file, updated);
    changed++;
  }

  highlighter.dispose();
  console.log(`highlight-abap: updated ${changed} file(s)`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
