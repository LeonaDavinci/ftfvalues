// Production server entry. chdir's to the project so `next start` finds
// .next + next.config without relying on the shell's working directory.
import { createRequire } from "module";

const projectDir = "C:\\Users\\star\\WorkBuddy\\2026-06-23-02-05-48\\ftfvalues-web";
process.chdir(projectDir);

const require = createRequire(import.meta.url);
const next = require("next");
const http = require("http");

const port = parseInt(process.env.PORT || "3000", 10);
const app = next({ dev: false, port });
const handle = app.getRequestHandler();

app.prepare().then(() => {
  http
    .createServer((req, res) => handle(req, res))
    .listen(port, "127.0.0.1", () => {
      console.log("> Ready on http://127.0.0.1:" + port);
    });
});
