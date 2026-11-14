<!-- source: https://api-docs.deepseek.com/api/list-files -->
```
GET /files
```

## /files
Returns a list of files that belong to the user, with cursor-based pagination.

## Request ​
Query Parameters
A file_id cursor for pagination. Returns files listed after this one.
Possible values: >= 1 and <= 1000
Default value: 1000
The number of files to return. Must be between 1 and 1000.
Default value: asc
Possible values: asc , desc
Sort order by creation time. asc for ascending, desc for descending.
Possible values: user_data , text_recognition , rich_layout_recognition
Only return files with the given purpose.

## Responses ​
- 200
OK, returns a list of file object .
- application/json
- Schema
- Example
Schema
Possible values: list
The object type, which is always list .
data
object[]
required
The list of file objects.
Describes a file that has been uploaded to the Files API. A file uploaded with an OCR purpose is returned only after parsing succeeds.
- Array [
Array [
The file identifier, of the form file-api-... , which can be referenced in chat completion requests.
Possible values: file
The object type, which is always file .
The size of the file in bytes.
The Unix timestamp (in seconds) of when the file was created.
The name of the file.
Possible values: user_data , text_recognition , rich_layout_recognition
The intended purpose of the file.
The Unix timestamp (in seconds) of when the file expires. Only present when an expiration was set at upload time.
- ]
]
The ID of the first file in the list. Useful as a pagination cursor.
The ID of the last file in the list. Useful as a pagination cursor.
Whether there are more files beyond this page.
```
{ "object": "list", "data": [ { "id": "file-api-0a1b2c3d4e5f60718293a4b5c6d7e8f9", "object": "file", "bytes": 102400, "created_at": 1700000000, "filename": "image.jpg", "purpose": "user_data" } ], "first_id": "file-api-0a1b2c3d4e5f60718293a4b5c6d7e8f9", "last_id": "file-api-0a1b2c3d4e5f60718293a4b5c6d7e8f9", "has_more": false }
```
