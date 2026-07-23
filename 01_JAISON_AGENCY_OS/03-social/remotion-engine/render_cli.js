const { execSync } = require("child_process");
const path = require("path");
const fs = require("fs");

// Command line usage: node render_cli.js [props.json] [outPath]
const args = process.argv.slice(2);
const propsFile = args[0];
const outPath = args[1] || path.join(__dirname, "..", "generated_media", "jaison_reel_output.mp4");

let propsArg = "";
if (propsFile && fs.existsSync(propsFile)) {
  propsArg = `--props="${path.resolve(propsFile)}"`;
}

console.log("🚀 Rozpoczynanie renderowania Jaison OS Reel przez Remotion...");
const renderCmd = `npx remotion render src/index.ts JaisonReel "${path.resolve(outPath)}" ${propsArg}`;
console.log(`Executing: ${renderCmd}`);

try {
  execSync(renderCmd, { cwd: __dirname, stdio: "inherit" });
  console.log(`✅ Sukces! Wygenerowano wideo Remotion w: ${outPath}`);
} catch (err) {
  console.error("❌ Błąd renderowania Remotion:", err);
  process.exit(1);
}
