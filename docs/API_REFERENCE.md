# Local JSON API

Implemented with Python's standard library; no third-party packages are required.
Default base URL: \`http://127.0.0.1:8765\`.

| Method | Path | Purpose |
|---|---|---|
| GET | \`/api/health\` | API name, version, project root |
| GET | \`/api/status\` | Python and NASM/Make/QEMU availability, image status |
| GET | \`/api/files\` | Relative paths and byte sizes of project files |
| GET | \`/api/settings\` | Read \`config/app_settings.json\` |
| POST | \`/api/commands\` | Execute one allowlisted project command |

Example request: \`POST /api/commands\` with JSON body \`{"command":"build"}\`.

Allowed command names are \`build\`, \`verify\`, \`lint\`, and \`clean\`. Arbitrary shell commands, source writes, physical disk writes, and CMOS writes are not exposed. Commands use fixed argument arrays without a shell, have a 180-second timeout, and return captured output truncated to 12,000 characters.

## Security

- Server refuses to bind to non-loopback addresses.
- POST requests are accepted only from loopback clients.
- Request bodies are limited to 16 KiB.
- This is a local developer API, not an authenticated production service. Do not expose it through a tunnel or reverse proxy.
