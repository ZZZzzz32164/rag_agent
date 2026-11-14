<!-- source: https://api-docs.deepseek.com/api/ocr -->
```
POST /v1/tools/ocr
```

## /v1/tools/ocr
Recognize the text in a PDF, Word or PowerPoint document or in an image, and return the result page by page. The file is not stored in the Files API. See the OCR guide for the limits, errors and billing.

## Request ​
- multipart/form-data
Body
required
The file to recognize, sent with a file name. See the OCR guide for the supported formats and limits.
Possible values: text_recognition , rich_layout_recognition
text_recognition extracts text directly from Word and PowerPoint files without images and recognizes other files page by page. rich_layout_recognition recognizes every file page by page. See the OCR guide for the output.

## Responses ​
- 200
OK, returns the recognition result of every page.
- application/json
- Schema
- Example
Schema
The recognition ID, of the form ocr-... .
Possible values: ocr.result
The object type, which is always ocr.result .
The Unix timestamp (in seconds) of when the recognition was created.
Possible values: text_recognition , rich_layout_recognition
The purpose of the request.
The number of pages, equal to the length of pages .
pages
object[]
required
The recognition result of every page, in page order.
- Array [
Array [
The page number, starting from 0.
The raw model output for the page, without any cleanup.
Possible values: stop , length
stop when the page was recognized completely; length when the output reached the limit and the page text is incomplete.
- ]
]
usage
object
required
The token usage of all pages. For reference only; not used for billing.
The OCR input tokens of all pages. For reference only; not used for billing.
The OCR output tokens of all pages. For reference only; not used for billing.
The sum of input_tokens and output_tokens .
```
{ "id": "ocr-9b2f4c1e-5d7a-4e3b-8f21-6c0a9d4e7b12", "object": "ocr.result", "created": 1762790000, "purpose": "text_recognition", "page_count": 1, "pages": [ { "index": 0, "text": "DeepSeek API\n\nThe DeepSeek API uses an API format compatible with OpenAI and Anthropic.", "finish_reason": "stop" } ], "usage": { "input_tokens": 1536, "output_tokens": 412, "total_tokens": 1948 } }
```
