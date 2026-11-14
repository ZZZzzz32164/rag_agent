<!-- source: https://api-docs.deepseek.com/api/delete-file -->
```
DELETE /files/:file_id
```

## /files/:file_id
Deletes a file.

## Request ​
Path Parameters
The ID of the file to delete.

## Responses ​
- 200
OK, returns the deletion status.
- application/json
- Schema
- Example
Schema
The ID of the deleted file.
Possible values: file
The object type, which is always file .
Whether the file was successfully deleted.
```
{ "id": "file-api-0a1b2c3d4e5f60718293a4b5c6d7e8f9", "object": "file", "deleted": true }
```
