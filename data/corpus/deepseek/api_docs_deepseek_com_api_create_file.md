<!-- source: https://api-docs.deepseek.com/api/create-file -->
```
POST /files
```

## /files
Upload an image file that can later be referenced by its file_id in chat completion requests.
Supported formats: JPEG, PNG, GIF, and WebP. The format is detected from the file content. See the Files API guide for details.
To upload documents, set purpose to text_recognition or rich_layout_recognition and send it before the file field. See the File Parsing guide .

## Request ​
- multipart/form-data
Body
required
Possible values: user_data , text_recognition , rich_layout_recognition
The intended purpose of the uploaded file. When uploading a document, send this field before file . See the Files API guide for the file types each purpose accepts.
The file to upload. The accepted file types depend on purpose .
Possible values: created_at
The anchor for the expiration. Must be created_at if provided, and is required together with expires_after[seconds] .
Possible values: >= 3600 and <= 2592000
The lifetime of the file in seconds, between 3600 (1 hour) and 2592000 (30 days). Required together with expires_after[anchor] . Omit both expires_after fields to keep the file permanently.

## Responses ​
- 200
OK, returns the uploaded file object .
- application/json
- Schema
- Example
Schema
The file identifier, of the form file-api-... , which can be referenced in chat completion requests.
Possible values: file
The object type, which is always file .
The size of the file in bytes.
The Unix timestamp (in seconds) of when the file was created.
The name of the file.
Possible values: user_data , text_recognition , rich_layout_recognition
The intended purpose of the file.
The Unix timestamp (in seconds) of when the file expires. Only present when an expiration was set at upload time.
```
{ "id": "file-api-0a1b2c3d4e5f60718293a4b5c6d7e8f9", "object": "file", "bytes": 102400, "created_at": 1700000000, "filename": "image.jpg", "purpose": "user_data" }
```
