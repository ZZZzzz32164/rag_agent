<!-- source: https://api-docs.deepseek.com/api/asr -->
```
POST /v1/tools/asr
```

## /v1/tools/asr
Transcribe an audio file into text. The whole file is sent in one request and the complete transcript is returned. See the Speech to Text guide for the languages, limits, errors and billing.

## Request ​
- multipart/form-data
Body
required
The audio file: 16-bit PCM WAV or Ogg Opus. See the Speech to Text guide for the limits.

## Responses ​
- 200
OK, returns the transcript.
- application/json
- Schema
- Example
Schema
The request ID.
The transcript.
The duration of the audio, in milliseconds.
```
{ "request_id": "0b8c1c7e-3c0e-4d0f-9d3a-5f2a6f7e8b90", "text": "What is the weather like in Shanghai today?", "duration_ms": 3200 }
```
