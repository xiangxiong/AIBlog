## Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn
uvicorn main:app --reload --port 9000
```
## Environment Variables

Create a `.env` file in the project root and set at least:

```env
DEEPSEEK_API_KEY=your_api_key
DEEPSEEK_MODEL=deepseek-chat
```
Optional:

```env
OPENAI_API_BASE=https://api.deepseek.com
```

If you want to use DashScope's OpenAI-compatible endpoint, set:

```env
OPENAI_API_BASE=https://dashscope.aliyuncs.com/compatible-mode/v1
```
pip freeze > requirements.txt


