# cys-2024


# PhishZilla

## Overview
This Telegram bot is designed to enhance cybersecurity by detecting potential phishing attempts. It analyzes messages for phishing by checking the grammar, sender ID, and the links contained within the messages. This tool aims to provide a first line of defense for users by alerting them to suspicious messages that could potentially harm their digital security.

## Features
- **Link Analysis:** Scrutinizes URLs to determine if they lead to known phishing sites.
- **Grammar Checking:** Evaluates the grammar of the text to identify common errors found in phishing attempts.
- **Sender Verification:** Checks sender IDs against databases of known phishing sources.

## Prerequisites
Before you start using this bot, ensure you have Python 3.6 or higher and pip (Python package installer) installed on your machine. Additionally, the following Python packages are required:
- `onnxruntime`
- `torch`
- `tf2onnx`
- `skl2onnx`
- `nlpcloud`
- `huggingface_hub`

You can install all required packages using the following command:

```bash
pip install onnxruntime torch tf2onnx skl2onnx nlpcloud huggingface_hub

