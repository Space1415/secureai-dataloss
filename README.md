# Masquerade MCP: Redact. Replace. Retain Control.

[![Demo video](https://github.com/user-attachments/assets/27e1580b-6fde-474c-8e88-44e77c3fb6a0)](https://github.com/user-attachments/assets/80b1d8ac-a012-41ce-8e92-64d567f2427f)

🤐 **Problem:** Tools like Claude or GPT are incredibly powerful, but they require raw input. If you're dealing with contracts, medical records, internal documents, code files, or chat messages, that's risky.

🛡️ **Solution:** Masquerade acts as a privacy firewall for your content. Just provide a **file path** or **text content**, and Masquerade will:

  - Automatically detect sensitive data (names, emails, dates, entities, API keys, etc.)
  - Redact the sensitive data
  - Let you preview before sending to an LLM

## Supported Content Types

### 📄 PDF Documents
- Contracts, medical records, legal documents
- Automatic page-by-page redaction
- Creates both redacted and highlighted versions

### 💻 Code Files
- **Languages:** Python, JavaScript, TypeScript, Java, C++, C#, PHP, Ruby, Go, Rust, Swift, Kotlin, Scala, R, MATLAB, Bash, PowerShell, SQL, HTML, CSS, XML, JSON, YAML, TOML, INI, Config files, Environment files, Dockerfiles
- Preserves code structure and syntax
- Redacts sensitive data like API keys, passwords, personal information

### 💬 Text Content
- Chat messages, prompts, emails, documents
- Real-time text redaction
- Perfect for sensitive conversations

## Architecture

![Image](https://github.com/user-attachments/assets/96002c8b-5839-4499-814e-e603d95e7c82)

1. **User Input**: The user asks Claude to redact content by providing a file path or text.
2. **Content Processing**: MCP reads the content and converts it to text (if needed).
3. **Sensitive Data Detection**: The text is sent to Tinfoil (an isolated AI platform using Llama 3.3 70B) to identify sensitive data.
4. **Redaction**: MCP removes the sensitive data and creates redacted versions.
5. **Summary Return**: MCP sends Claude a summary with:
    - Masked versions of the sensitive data
    - Redaction counts
    - Paths to redacted files (for files)
    - Redacted text content (for text)
6. **Querying with Claude**: The user can use the redacted content with Claude safely.

## Installation

[![Setup video](https://github.com/user-attachments/assets/1402cd40-34df-4776-a8e4-f07d6f20c90b)](https://github.com/user-attachments/assets/76dedb64-1ef5-4ab4-afe1-11f399b3653b)

1. Install [Claude desktop](https://claude.ai/download)
1. Get [Tinfoil](https://tinfoil.sh) API key (create account and API key)
1. Configure environment

<details open>
<summary><strong>Option 1: Automated</strong></summary>

```bash
curl -O https://raw.githubusercontent.com/postralai/masquerade/main/setup.sh && bash setup.sh
```

4. Restart Claude desktop app (if successfully configured)

</details>

<details>
<summary><strong>Option 2: Manual (click to expand)</strong></summary>

4. Create a virtual environment with **Python ">=3.10, <=3.12"**

```bash
python3.12 -m venv pdfmcp
source pdfmcp/bin/activate
python --version
```

5. Install this repo with the command below

```bash
pip install git+https://github.com/postralai/masquerade@main
```

6. Automate the Claude config setup (and skip the next steps)

```bash
python -m masquerade.configure_claude
```

7. Get Python path: `which python`
1. Get MCP file path: `python -c "import masquerade as m; print(f'{m.__path__[0]}/mcp_universal_redaction.py')"`
1. Add (1) Python path, (2) MCP file path, and (3) Tinfoil API key to the JSON below and add that to `claude_desktop_config.json`. Instructions to find the config file are in the image below.
1. Restart Claude

```json
{
  "mcpServers": {
    "universal-redaction": {
      "command": "/path/to/python", // Run `which python`
      "args": ["/path/to/mcp_universal_redaction.py"], // Run `python -c "import masquerade as m; print(f'{m.__path__[0]}/mcp_universal_redaction.py')"`
      "env": {
        "TINFOIL_API_KEY": "your_api_key" // Create Tinfoil account and paste API key
      }
    }
  }
}
```

![Image](https://github.com/user-attachments/assets/cfa56a1a-bec0-40e5-95d9-f4f36c43b95a)

</details>

## How to use?

### PDF Documents
```
"Redact sensitive information from this PDF: /path/to/document.pdf"
```

### Code Files
```
"Redact sensitive data from this code file: /path/to/config.py"
"Remove API keys and passwords from: /path/to/.env"
```

### Text Content
```
"Redact this chat message: 'Hi John, my email is john.doe@company.com and my phone is 555-123-4567'"
"Remove personal information from this text: [paste your text here]"
```

### Universal Redaction
```
"Redact this content: /path/to/file.txt"
"Process this for sensitive data: [any file path or text]"
```

**Note:** Don't upload the original content to Claude, only provide the file path or text directly.

## Features

### 🔍 Smart Detection
- **Personal Information:** Names, emails, phone numbers, addresses
- **Business Data:** Company names, IDs, contract numbers
- **Technical Data:** API keys, passwords, database credentials
- **Dates:** Birth dates, sensitive timestamps

### 🛡️ Privacy Protection
- **Local Processing:** Content stays on your machine
- **AI-Powered Detection:** Uses isolated Tinfoil AI for sensitive data detection
- **Reversible Masking:** Original data is masked, not permanently deleted
- **Multiple Formats:** Handles PDFs, code files, and text seamlessly

### 📊 Detailed Reporting
- **Redaction Summary:** Count of redactions per page/section
- **Masked Data Preview:** See what was redacted without exposing original
- **File Management:** Automatic creation of redacted versions

## Contributing

If you have a fix or improvement, feel free to submit a pull request. For significant changes, please open an issue first to discuss your proposed updates.

See the [Developer section](docs/developers.md) for the installation of this repository.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Need Help?

For questions and common issues, please see the [FAQ section](docs/faq.md) or open an issue on GitHub.
