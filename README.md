# 📚 Sphinx Documentation (Dev Container Setup)

This repository contains HTML-based [Sphinx](https://www.sphinx-doc.org/) documentation. You can build, preview, and update the documentation easily using Visual Studio Code with a dev container.

Latest version of the documentation can be found here: [XXXX](XXXX)

## 🧰 Prerequisites

- [Docker](https://www.docker.com/) installed and running
- [Visual Studio Code](https://code.visualstudio.com/) installed
- [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) for VS Code

## 🚀 Getting Started

1. **Open the repository in VS Code**  
   Open this folder in VS Code using `File > Open Folder`.

2. **Reopen in Container**  
   When prompted by VS Code, click **"Reopen in Container"**.  
   If you're not prompted:
   - Open the Command Palette (`Ctrl+Shift+P` or `Cmd+Shift+P`)
   - Select: **Dev Containers: Reopen in Container**

   VS Code will now build and start the dev container with all dependencies pre-installed.

## ⚙️ Available Tasks

Once inside the container, you can use the following predefined VS Code tasks:

- **📄 Make HTML**  
  Builds the documentation.
  - Run via Command Palette → `Tasks: Run Task` → **Make html**
  - Output is placed in the `_build/html` directory.

- **🌐 Start Webserver**  
  Serves the built documentation locally at `http://localhost:8000`
  - Run via Command Palette → `Tasks: Run Task` → **Start webserver**

- **🛑 Stop Webserver**  
  Stops the running local server.
  - Run via Command Palette → `Tasks: Run Task` → **Stop webserver**

## 📎 Notes

- If you edit the documentation, rerun **Make html** to see the updates.
- Make sure the server is running when you want to preview your changes in the browser.

## 🤝 Contributing

Feel free to submit pull requests or open issues for improvements or suggestions.

---

Happy documenting! ✨