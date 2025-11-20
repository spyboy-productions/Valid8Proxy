<h4 align="center">If you find this GitHub repo useful, please consider giving it a star! ⭐️</h4>

<p align="center">
    <a href="https://spyboy.in/twitter">
      <img src="https://img.shields.io/badge/-Twitter-black?logo=twitter&style=for-the-badge">
    </a>
    &nbsp;
    <a href="https://spyboy.in/">
      <img src="https://img.shields.io/badge/-spyboy.in-black?logo=google&style=for-the-badge">
    </a>
    &nbsp;
    <a href="https://spyboy.blog/">
      <img src="https://img.shields.io/badge/-spyboy.blog-black?logo=wordpress&style=for-the-badge">
    </a>
    &nbsp;
    <a href="https://spyboy.in/Discord">
      <img src="https://img.shields.io/badge/-Discord-black?logo=discord&style=for-the-badge">
    </a>
</p>

<img width="100%" src="https://github.com/spyboy-productions/Valid8Proxy/blob/main/image/vald%20(1).png" />

<br>

Valid8Proxy is a fast and efficient tool designed for fetching, validating, and storing working proxies (`HTTP`, `HTTPS`, `SOCKS4`, `SOCKS5`, and `Mixed`).  
Perfect for web scraping, OSINT, automation, or network testing.

---

## 🚀 Run Online Free on Google Colab

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/spyboy-productions/Valid8Proxy/blob/main/valid8proxy.ipynb)

---

## ⭐ Features

- **Supports Multiple Proxy Protocols**  
  HTTP, HTTPS, SOCKS4, SOCKS5, and Mixed mode.

- **Fetches Proxies from Multiple Live Sources**

- **High-Speed Concurrent Validation**  
  Multi-threaded validation using ThreadPoolExecutor.

- **Accurate Proxy Extraction**  
  Strict regex-based `IP:PORT` extraction.

- **Customizable Validation**  
  Choose timeout, threads, test URL, and count.

- **Early Stop Mechanism**  
  Stops automatically after your desired number of valid proxies.

- **Save Valid Proxies to File**

- **Supports Piped Input (`--no-fetch`)**  
  Validate your own proxy lists directly.

- **Cross-Platform**  
  Works on Linux, macOS, Windows, and Termux.

---

## 🧪 Installation

```bash
git clone https://github.com/spyboy-productions/Valid8Proxy.git
cd Valid8Proxy
pip3 install -r requirements.txt
python3 Valid8Proxy.py -h
````

---

## ▶️ Example Usage

### 🔎 Find 10 working proxies (mixed)

```bash
python3 Valid8Proxy.py --type mixed --count 10
```

### 🚀 Find 20 HTTP proxies using 100 threads

```bash
python3 Valid8Proxy.py --type http --count 20 --workers 100
```

### ⏱ Validate proxies using 3-second timeout

```bash
python3 Valid8Proxy.py --timeout 3
```

### 🌐 Test using a custom website

```bash
python3 Valid8Proxy.py --test-url https://google.com
```

### 💾 Save results to a custom file

```bash
python3 Valid8Proxy.py --save working_proxies.txt
```

### 📥 Validate proxies from a text file

```bash
cat proxies.txt | python3 Valid8Proxy.py --no-fetch --count 5
```

### 🆘 Help

```bash
python3 Valid8Proxy.py --help
```

---

## 🧰 Command Line Options

| Command                                        | Description                                       |
| ---------------------------------------------- | ------------------------------------------------- |
| `python3 Valid8Proxy.py --help`                | Show help menu                                    |
| `--type [http/https/socks4/socks5/mixed/auto]` | Select proxy protocol *(default: mixed)*          |
| `--count N`                                    | Number of working proxies to find *(default: 10)* |
| `--workers N`                                  | Thread count for validation *(default: 50)*       |
| `--timeout N`                                  | Per-proxy timeout *(default: 6)*                  |
| `--test-url URL`                               | Custom website to test proxies                    |
| `--save file.txt`                              | Save valid proxies to file                        |
| `--no-fetch`                                   | Read proxies from STDIN instead of fetching       |
| `--version`                                    | Show script version (if implemented)              |

---

## 🗂 Validate Your Own Proxies (separate tool)

```bash
python Validator.py
```

Follow prompts to:

* Input your proxy file
* Choose how many to validate
* Get a list of working proxies

---

## 🤝 Contribution

Contributions and feature requests are welcome!
Open an issue or submit a Pull Request anytime.

#### 💬 Need help?

👉 [Join the Discord](https://discord.gg/ZChEmMwE8d)

[![Discord Server](https://discord.com/api/guilds/726495265330298973/embed.png)](https://discord.gg/ZChEmMwE8d)

---

## ▶️ Video Guide

🎥 **YouTube Video:**
[https://www.youtube.com/watch?v=FWFFAbgC8Bo](https://www.youtube.com/watch?v=FWFFAbgC8Bo)

---

## 📸 Screenshots

<a href="https://youtu.be/FWFFAbgC8Bo?si=kUfH4H9HUkqdnksI">
<img width="100%" src="https://github.com/spyboy-productions/Valid8Proxy/blob/main/image/weqdeqe.png" />
</a>

---

<h4 align="center">If this project helped you, please consider giving it a ⭐ on GitHub!</h4>
