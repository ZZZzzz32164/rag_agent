<!-- source: https://api-docs.deepseek.com/api/create-message -->
```
POST /anthropic/v1/messages
```

## /anthropic/v1/messages
Creates a model response in the Anthropic Messages API format.
Send the conversation history in messages on each request. Use https://api.deepseek.com/anthropic as the Anthropic SDK's base_url ; the SDK appends /v1/messages . Direct HTTP requests can also use the compatible path /anthropic/messages .
Authenticate with either x-api-key or Authorization: Bearer . If both are supplied, Authorization takes precedence. See the Anthropic API Guide for model mappings, tool-result replay, and compatibility details.
Compatibility fields container , mcp_servers , service_tier , and top_k are ignored.

## Request ​
Header Parameters
The Anthropic SDK sends this header automatically; the service currently ignores it.
Include files-api-2025-04-14 when referencing an uploaded image with source.type of file . Otherwise not required for this endpoint. See the Files API Guide .
- application/json
Body
required
ID of the model to use. Use deepseek-flash or deepseek-v4-pro . Claude model-name aliases are also accepted: claude-opus* maps to deepseek-v4-pro , and other claude* names map to deepseek-flash . See the Anthropic API Guide .
messages
object[]
required
Minimum items: 1
The conversation history. At least one message is required. This API is stateless: include the messages needed for the current turn in every request. Use the top-level system field for the system prompt. When continuing after a tool call, pass back the complete assistant content, including thinking and tool-use blocks, followed by the matching tool results. The service may restore omitted thinking content from tool-call IDs; if recovery is required but fails, the request returns 400 . Preserve the complete content for reliable replay.
- Array [
Array [
oneOf
- User message
- Assistant message
- Latest reminder message
Possible values: user
required
oneOf
- Text content
- User content blocks
string
Minimum items: 1
Place all tool_result blocks before text or image blocks when replying to tool calls.
- Array [
Array [
oneOf
- Text block
- Image block
- Document block
- Tool-result block
Each text block must have type: "text" , with its content in the text field. On input, additional cache_control and citations fields are ignored.
Possible values: text
The text content.
citations
object[]
nullable
Sources cited by this text. Returned when the answer cites results of the web tools; ignored on input.
A source cited by the answer. Returned with the web tools.
- Array [
Array [
Possible values: web_search_result_location
The URL of the cited source.
The title of the cited source, or null when unknown.
Always an empty string.
The answer text of the current text block up to this citation. Unlike the Anthropic API, it is not text quoted from the source.
- ]
]
Image input is supported by deepseek-flash in user messages and tool results. Images in assistant messages are not supported. deepseek-v4-pro does not support image input. See the Vision Guide for image limits.
Possible values: image
required
oneOf
- Base64 image
- Image URL
- Uploaded image file
Possible values: base64
Possible values: image/jpeg , image/png , image/gif , image/webp
The base64-encoded image bytes, without a data-URL prefix.
Possible values: url
An HTTP or HTTPS URL from which the server can download the image.
Requires the request header anthropic-beta: files-api-2025-04-14 .
Possible values: file
The ID of an uploaded image file. See the Files API Guide .
A document for the model to read, supported in user messages. See the File Parsing Guide .
Possible values: document
required
oneOf
- Uploaded file
- Inline text
The request must carry the anthropic-beta: files-api-2025-04-14 header.
Possible values: file
The ID of a file uploaded via the Files API , of the form file-api-... .
Possible values: text
Possible values: text/plain
The text of the document.
Optional. The file name shown to the model for a text source.
Only valid in user messages. Return one result for every pending tool-use ID, with no duplicates, before any text or image blocks.
Possible values: tool_result
The ID of the corresponding tool_use block in the immediately preceding assistant message.
nullable
The tool output as a string or a list of text and image blocks. If omitted or null , the result is empty.
oneOf
- Text content
- Tool-result content blocks
- Null value
string
- Array [
Array [
oneOf
- Text block
- Image block
Each text block must have type: "text" , with its content in the text field. On input, additional cache_control and citations fields are ignored.
Possible values: text
The text content.
citations
object[]
nullable
Sources cited by this text. Returned when the answer cites results of the web tools; ignored on input.
A source cited by the answer. Returned with the web tools.
- Array [
Array [
Possible values: web_search_result_location
The URL of the cited source.
The title of the cited source, or null when unknown.
Always an empty string.
The answer text of the current text block up to this citation. Unlike the Anthropic API, it is not text quoted from the source.
- ]
]
Image input is supported by deepseek-flash in user messages and tool results. Images in assistant messages are not supported. deepseek-v4-pro does not support image input. See the Vision Guide for image limits.
Possible values: image
required
oneOf
- Base64 image
- Image URL
- Uploaded image file
Possible values: base64
Possible values: image/jpeg , image/png , image/gif , image/webp
The base64-encoded image bytes, without a data-URL prefix.
Possible values: url
An HTTP or HTTPS URL from which the server can download the image.
Requires the request header anthropic-beta: files-api-2025-04-14 .
Possible values: file
The ID of an uploaded image file. See the Files API Guide .
- ]
]
null
Ignored. Include any error details in content .
- ]
]
A previous assistant message. Preserve its content blocks when passing it back, including thinking, tool use, and web search results.
Possible values: assistant
required
oneOf
- Text content
- Assistant content blocks
string
Minimum items: 1
- Array [
Array [
oneOf
- Text block
- Thinking block
- Tool-use block
- Server-tool-use block
- Web search result block
- Web fetch result block
Each text block must have type: "text" , with its content in the text field. On input, additional cache_control and citations fields are ignored.
Possible values: text
The text content.
citations
object[]
nullable
Sources cited by this text. Returned when the answer cites results of the web tools; ignored on input.
A source cited by the answer. Returned with the web tools.
- Array [
Array [
Possible values: web_search_result_location
The URL of the cited source.
The title of the cited source, or null when unknown.
Always an empty string.
The answer text of the current text block up to this citation. Unlike the Anthropic API, it is not text quoted from the source.
- ]
]
Possible values: thinking
Thinking content returned by the model. Pass it back unchanged when continuing a tool-call turn in thinking mode.
The signature returned with the thinking block. Preserve it when passing back the block; the input signature is not validated.
Appears in assistant messages. Each tool-use block must have a matching tool-result block in the immediately following user message.
Possible values: tool_use
The tool-call ID. Pass this ID back as tool_result.tool_use_id .
The name of the client tool.
The JSON arguments supplied to the tool, normally an object matching its input_schema .
Returned when the service runs web search, deepseek_web_search or deepseek_read_url . Its matching web_search_tool_result or web_fetch_tool_result appears in the same assistant message; the client does not run this tool.
Possible values: server_tool_use
The server-tool-call ID.
Possible values: web_search , web_fetch , deepseek_web_search , deepseek_read_url
The server-tool arguments as a JSON value, normally an object such as {"query":"..."} . Preserve them when passing back the assistant message.
caller
object
Identifies a direct server-tool call.
Possible values: direct
Possible values: search , deep_search , read_link , image_search , deep_image_search
DeepSeek extension on blocks produced by the web tools: search for web search, deep_search for deep thinking search, read_link for URL reading, and image_search or deep_image_search (during deep thinking search) for image search. Pass it back unchanged.
Possible values: web_search_tool_result
The ID of the associated server_tool_use block.
content
object[]
required
Search results or search-error items. Pass the entire array back unchanged with the assistant message.
- Array [
Array [
oneOf
- Web search result
- Web search error
Possible values: web_search_result
The title of the result page.
The URL of the result page.
Opaque result content. Preserve this value unchanged when passing the result back.
Page-age metadata, when available; may be null .
DeepSeek extension. A plain-text summary of the result for display.
DeepSeek extension. The name of the site, or null when unknown.
DeepSeek extension. The URL of the site icon, or null when unknown.
Possible values: web_search_tool_result_error
Possible values: invalid_tool_input , unavailable , max_uses_exceeded , too_many_requests , query_too_long , request_too_large
The reason the server-side search failed.
- ]
]
Possible values: search , deep_search , read_link , image_search , deep_image_search
DeepSeek extension on blocks produced by the web tools: search for web search, deep_search for deep thinking search, read_link for URL reading, and image_search or deep_image_search (during deep thinking search) for image search. Pass it back unchanged.
Returned for a page opened during deep thinking search ( deepseek_web_search ), or a link read by deepseek_read_url . Pass it back unchanged, including kind and signature . See the Web Tools Guide .
Possible values: web_fetch_tool_result
The ID of the associated server_tool_use block.
required
The fetched page, or the reason the fetch failed.
oneOf
- Web fetch result
- Web fetch error
Possible values: web_fetch_result
The URL of the page.
content
object
required
The page as a text document.
Possible values: document
source
object
Possible values: text
Possible values: text/plain
Always an empty string: the page text is not returned. For read_link , the page is carried in signature .
The page title.
DeepSeek extension, in place of retrieved_at . The publication time of the page, or null when unknown. For a link read from the user message, the date found on the page, in no fixed format; for a page opened during deep thinking search, an RFC 3339 timestamp.
Possible values: web_fetch_tool_result_error
Possible values: url_not_accessible , url_not_allowed , unavailable
The reason the fetch failed. See the Web Tools Guide .
Possible values: search , deep_search , read_link , image_search , deep_image_search
DeepSeek extension on blocks produced by the web tools: search for web search, deep_search for deep thinking search, read_link for URL reading, and image_search or deep_image_search (during deep thinking search) for image search. Pass it back unchanged.
DeepSeek extension. Present on successful read_link results: the page that was read, encrypted. Pass it back unchanged to restore the page into the context.
- ]
]
DeepSeek extension. Gives the model the current date, location, platform and language, like DeepSeek Chat. Place it directly before the user message it belongs to; anywhere else it returns 400 . Works with or without the web tools. See the User Metadata Marker Guide .
Possible values: latest_reminder
<date>,<weekday>,<location>,<platform>,<language> , for example 2026-11-11,Wednesday,Singapore,Web,English .
- ]
]
nullable
The system prompt. Supports only a string, an array of text blocks, or null .
oneOf
- Text content
- System text blocks
- Null value
string
Each text block must have type: "text" , with its content in the text field. On input, additional cache_control and citations fields are ignored.
- Array [
Array [
Possible values: text
The text content.
citations
object[]
nullable
Sources cited by this text. Returned when the answer cites results of the web tools; ignored on input.
A source cited by the answer. Returned with the web tools.
- Array [
Array [
Possible values: web_search_result_location
The URL of the cited source.
The title of the cited source, or null when unknown.
Always an empty string.
The answer text of the current text block up to this citation. Unlike the Anthropic API, it is not text quoted from the source.
- ]
]
- ]
]
null
Possible values: >= 1
The requested output token limit, including thinking tokens. This field is optional at the HTTP API level; the Anthropic SDK requires it. The default and effective limit depend on the model, thinking mode, and reasoning effort. Values above the model limit are capped, and the input plus output must fit within the context window. For certain Claude Code or OpenCode main-agent requests in thinking mode, compatibility handling may raise the effective limit above the requested value, within model and context limits. See Models & Pricing .
Default value: false
If true , return named server-sent events (SSE), ending with message_stop . There is no data: [DONE] message. Otherwise, return one complete message object.
thinking
object
nullable
Controls thinking mode. An explicit thinking.type takes precedence over output_config.effort when selecting the mode. When omitted, effort determines the mode. If neither is set, thinking is enabled by default for deepseek-flash and deepseek-v4-pro .
Possible values: enabled , disabled , adaptive
enabled turns thinking on; disabled turns it off. adaptive is treated as enabled .
Possible values: >= 0
Ignored. This parameter does not set a thinking-token budget.
output_config
object
nullable
Output configuration. Only effort is supported; output-format settings such as format are ignored.
Possible values: none , minimal , low , medium , high , xhigh , ultra , max , null
Controls thinking mode and effort. none disables thinking unless thinking.type explicitly enables it. low , high , and max enable thinking, with high as the default effort. Compatibility aliases: minimal maps to low , medium and xhigh both map to high , and ultra maps to max . An explicit thinking.type determines whether thinking is enabled.
tools
object[]
nullable
Tools available to the model. Supports client-defined tools, the web search server tool, and the deepseek_web_search and deepseek_read_url server tools. Tool names must be unique. An empty list is treated as no tools. cache_control is ignored.
- Array [
Array [
oneOf
- Client tool
- Web search server tool
- DeepSeek web search server tool
- DeepSeek read URL server tool
The application executes this tool after receiving a tool_use block and returns a tool_result block. Omit type for client tools. Providing type selects server-tool parsing; unsupported values such as custom return 422 . cache_control is ignored.
Minimum characters: 1
Maximum characters: 128
Possible values: Value must match regular expression ^[a-zA-Z0-9_-]+$
A unique tool name containing letters, digits, underscores, or hyphens, up to 128 characters.
A description of what the tool does and when to use it.
input_schema
object
required
A valid JSON Schema describing the tool arguments. Its top-level type must be object .
The service executes web searches and returns server_tool_use and web_search_tool_result blocks in the assistant message. Both type values select the same tool.
Possible values: web_search_20250305 , web_search_20260209
Possible values: web_search
Possible values: >= 0
Maximum searches allowed in this request. The default and service-side cap are normally 5; for Claude Code search-subagent compatibility requests, both are 1. Larger values are capped at the applicable limit. A search beyond this limit returns a max_uses_exceeded result.
DeepSeek extension. Lets the model search the web; with thinking enabled, it runs deep thinking search. See the Web Tools Guide .
Possible values: deepseek_web_search
Possible values: deepseek_web_search
Optional. The service does not check it.
DeepSeek extension. Lets the model read the links in the last user message. See the Web Tools Guide .
Possible values: deepseek_read_url
Possible values: deepseek_read_url
Optional. The service does not check it.
- ]
]
nullable
Controls tool selection. Defaults to auto . any is treated as auto and does not force a tool call. Selecting a named client tool requires non-thinking mode. disable_parallel_tool_use is ignored.
oneOf
- Automatic tool choice
- Any tool (automatic)
- Named tool choice
- Disable tool calls
- Null value
The model decides whether to call a tool. This is the default.
Possible values: auto
Ignored; it does not disable parallel tool calls.
Treated as auto ; the model decides whether to call a tool.
Possible values: any
Ignored; it does not disable parallel tool calls.
Selects the named tool. For a client tool, this forces a call in non-thinking mode; selecting it in thinking mode returns a 400 error. Set thinking.type to disabled when forcing a client-tool call.
Possible values: tool
The name of a tool present in tools .
Ignored; it does not disable parallel tool calls.
Disables tool calling, even when tools is provided.
Possible values: none
null
Minimum characters per item: 1
Maximum items: 16
Up to 16 non-empty strings that stop generation. If a string is matched, stop_reason is stop_sequence and stop_sequence contains the matched string.
Possible values: >= 0 and <= 2
Default value: 1
Sampling temperature, between 0 and 2. Higher values produce more varied output. In thinking mode the value is fixed at 1, and the supplied value has no effect. We generally recommend changing either this or top_p , rather than both.
Possible values: > 0 and <= 1
Nucleus sampling probability, greater than 0 and at most 1. For deepseek-flash , thinking mode defaults to 1 and clamps values below 0.95 to 0.95; non-thinking mode always uses 1. For deepseek-v4-pro , thinking mode uses 0.95 when tools are enabled and 1 otherwise, ignoring the supplied value; non-thinking mode uses the supplied value, defaulting to 1. Setting tool_choice to {"type":"none"} disables tool calling.
metadata
object
nullable
Request metadata. Only user_id is supported; other metadata fields are ignored.
A custom end-user identifier. We recommend using only ASCII letters, digits, underscores ( _ ), and hyphens ( - ). The UTF-8 encoded value must not exceed 512 bytes. Do not include personal information. See Rate Limit & Isolation .
safety_check
object
nullable
DeepSeek extension. Set level to high to turn on basic risk control, which reviews the model input and output. See the Model Content Safety Guide .
Possible values: low , high
high : basic risk control. low : the default checks, the same as omitting safety_check .
title
object
nullable
DeepSeek extension. Set {"enabled": true} to have the response carry a short title for the conversation. See the Conversation Title Guide .
Whether to return a conversation title.

## Responses ​
- 200 (No streaming)
- 200 (Streaming)
- 400 (Bad request)
OK, returns a message object. Its content may include text, thinking, and tool-use blocks.
- application/json
- Schema
- Example
Schema
Unique identifier for this message.
Possible values: message
Possible values: assistant
The model identifier supplied in the request. When using a Claude-compatible model name, the response retains that name.
content
object[]
required
Generated content blocks. Preserve the full content when adding this assistant turn to the next request.
- Array [
Array [
oneOf
- Text block
- Thinking output
- Tool-use block
- Server tool use output
- Web search result block
- Web fetch result block
Each text block must have type: "text" , with its content in the text field. On input, additional cache_control and citations fields are ignored.
Possible values: text
The text content.
citations
object[]
nullable
Sources cited by this text. Returned when the answer cites results of the web tools; ignored on input.
A source cited by the answer. Returned with the web tools.
- Array [
Array [
Possible values: web_search_result_location
The URL of the cited source.
The title of the cited source, or null when unknown.
Always an empty string.
The answer text of the current text block up to this citation. Unlike the Anthropic API, it is not text quoted from the source.
- ]
]
Possible values: thinking
The generated thinking content. Return this block unchanged when continuing a thinking-mode tool conversation.
Opaque signature returned with the thinking block; preserve it when replaying the block.
Appears in assistant messages. Each tool-use block must have a matching tool-result block in the immediately following user message.
Possible values: tool_use
The tool-call ID. Pass this ID back as tool_result.tool_use_id .
The name of the client tool.
The JSON arguments supplied to the tool, normally an object matching its input_schema .
Describes a tool call executed by the service. Request-level search counts are reported separately in usage.server_tool_use ; the client does not execute this call.
Possible values: server_tool_use
Identifier of the server tool call.
Name of the server tool: web_search for web search. With the web tools, the declared tool that enabled the capability: deepseek_web_search for searches and the steps of deep thinking search, or deepseek_read_url for URL reading.
Arguments supplied to the server tool as a JSON value, normally an object. With the web tools, input.action is search , open_page , find_in_page or read_link .
caller
object
required
Possible values: direct
Possible values: search , deep_search , read_link , image_search , deep_image_search
DeepSeek extension on blocks produced by the web tools: search for web search, deep_search for deep thinking search, read_link for URL reading, and image_search or deep_image_search (during deep thinking search) for image search. Pass it back unchanged.
Possible values: web_search_tool_result
The ID of the associated server_tool_use block.
content
object[]
required
Search results or search-error items. Pass the entire array back unchanged with the assistant message.
- Array [
Array [
oneOf
- Web search result
- Web search error
Possible values: web_search_result
The title of the result page.
The URL of the result page.
Opaque result content. Preserve this value unchanged when passing the result back.
Page-age metadata, when available; may be null .
DeepSeek extension. A plain-text summary of the result for display.
DeepSeek extension. The name of the site, or null when unknown.
DeepSeek extension. The URL of the site icon, or null when unknown.
Possible values: web_search_tool_result_error
Possible values: invalid_tool_input , unavailable , max_uses_exceeded , too_many_requests , query_too_long , request_too_large
The reason the server-side search failed.
- ]
]
Possible values: search , deep_search , read_link , image_search , deep_image_search
DeepSeek extension on blocks produced by the web tools: search for web search, deep_search for deep thinking search, read_link for URL reading, and image_search or deep_image_search (during deep thinking search) for image search. Pass it back unchanged.
Returned for a page opened during deep thinking search ( deepseek_web_search ), or a link read by deepseek_read_url . Pass it back unchanged, including kind and signature . See the Web Tools Guide .
Possible values: web_fetch_tool_result
The ID of the associated server_tool_use block.
required
The fetched page, or the reason the fetch failed.
oneOf
- Web fetch result
- Web fetch error
Possible values: web_fetch_result
The URL of the page.
content
object
required
The page as a text document.
Possible values: document
source
object
Possible values: text
Possible values: text/plain
Always an empty string: the page text is not returned. For read_link , the page is carried in signature .
The page title.
DeepSeek extension, in place of retrieved_at . The publication time of the page, or null when unknown. For a link read from the user message, the date found on the page, in no fixed format; for a page opened during deep thinking search, an RFC 3339 timestamp.
Possible values: web_fetch_tool_result_error
Possible values: url_not_accessible , url_not_allowed , unavailable
The reason the fetch failed. See the Web Tools Guide .
Possible values: search , deep_search , read_link , image_search , deep_image_search
DeepSeek extension on blocks produced by the web tools: search for web search, deep_search for deep thinking search, read_link for URL reading, and image_search or deep_image_search (during deep thinking search) for image search. Pass it back unchanged.
DeepSeek extension. Present on successful read_link results: the page that was read, encrypted. Pass it back unchanged to restore the page into the context.
- ]
]
Possible values: end_turn , max_tokens , stop_sequence , tool_use , refusal , null
Why generation stopped: natural completion, output limit, a stop sequence, a client tool call, or content filtering. Null in message_start.
The matched stop sequence, or null when no stop sequence was matched.
stop_details
object
nullable
Present when the model content safety review refuses the response ( stop_reason is refusal ). See the Model Content Safety Guide .
Possible values: refusal
Always null .
Names the blocked images when images in the request fail the review; otherwise null .
DeepSeek extension. The conversation title, present only when the request enabled title and a title was generated. Not related to the title of search results and citations.
usage
object
required
Possible values: >= 0
Input tokens not served from the context cache. Total input tokens equal input_tokens + cache_read_input_tokens + cache_creation_input_tokens.
Possible values: 0
Always 0. Anthropic-style cache creation is not used; context caching is automatic.
Possible values: >= 0
Input tokens served from the context cache.
Possible values: >= 0
Generated output tokens, including thinking tokens when thinking is enabled. In message_delta this is the cumulative count, not an increment.
output_tokens_details
object
Breakdown of output_tokens . Present when thinking is enabled or safety_check is high .
Possible values: >= 0
Thinking tokens, already included in output_tokens .
Possible values: >= 0
DeepSeek extension. Tokens of the safety review, already included in output_tokens . Present only when safety_check is high .
Possible values: standard
server_tool_use
object
Server-side web search and fetch counts, separate from token usage. Present only when at least one of the counts is greater than zero; otherwise omitted. All fields are present when this object is returned. Read the final message's usage for non-streaming responses or the final message_delta.usage for streaming responses. These counts are cumulative, not deltas. See Server tool usage .
Possible values: >= 0
Number of server-side web search attempts, including failed attempts and attempts exceeding max_uses .
Possible values: >= 0
Number of successful server-side web searches that returned nonempty results. Failed attempts and empty results are not counted. This field can be used as a basis for billing.
Possible values: >= 0
With the web tools. Number of fetch result blocks in the response, including errors. For display only.
Possible values: >= 0
With the web tools. Number of billed page fetches.
Possible values: >= 0
With the web tools. Number of billed image searches.
```
{ "id": "e6ef6a63-a078-4f53-a73b-38c8d1d46310", "type": "message", "role": "assistant", "model": "deepseek-flash", "content": [{"type": "text", "text": "Hello!"}], "stop_reason": "end_turn", "stop_sequence": null, "usage": { "input_tokens": 12, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0, "output_tokens": 3, "service_tier": "standard" } }
```
OK, returns SSE events in the order message_start → content block events → message_delta → message_stop . A ping event or keep-alive comment may appear between events. There is no data: [DONE] message. Accumulate tool input JSON fragments until the content block ends before parsing them. See Streaming .
A connection that closes before message_stop is an incomplete response. Errors after streaming has started may terminate the connection without an Anthropic error event.
- text/event-stream
- Schema
- Example
Schema
Normal message events have an event name matching the JSON type. A normal stream ends with message_stop. Ping events and keep-alive comments may appear between events; no data: [DONE] is emitted. A timeout may instead return an unnamed data event containing an error object before closing the connection. An interrupted stream without message_stop is incomplete.
- Array [
Array [
oneOf
- message_start
- content_block_start
- content_block_delta
- content_block_stop
- message_delta
- message_stop
- ping
Possible values: message_start
message
object
required
Unique identifier for this message.
Possible values: message
Possible values: assistant
The model identifier supplied in the request. When using a Claude-compatible model name, the response retains that name.
content
object[]
required
Generated content blocks. Preserve the full content when adding this assistant turn to the next request.
- Array [
Array [
oneOf
- Text block
- Thinking output
- Tool-use block
- Server tool use output
- Web search result block
- Web fetch result block
Each text block must have type: "text" , with its content in the text field. On input, additional cache_control and citations fields are ignored.
Possible values: text
The text content.
citations
object[]
nullable
Sources cited by this text. Returned when the answer cites results of the web tools; ignored on input.
A source cited by the answer. Returned with the web tools.
- Array [
Array [
Possible values: web_search_result_location
The URL of the cited source.
The title of the cited source, or null when unknown.
Always an empty string.
The answer text of the current text block up to this citation. Unlike the Anthropic API, it is not text quoted from the source.
- ]
]
Possible values: thinking
The generated thinking content. Return this block unchanged when continuing a thinking-mode tool conversation.
Opaque signature returned with the thinking block; preserve it when replaying the block.
Appears in assistant messages. Each tool-use block must have a matching tool-result block in the immediately following user message.
Possible values: tool_use
The tool-call ID. Pass this ID back as tool_result.tool_use_id .
The name of the client tool.
The JSON arguments supplied to the tool, normally an object matching its input_schema .
Describes a tool call executed by the service. Request-level search counts are reported separately in usage.server_tool_use ; the client does not execute this call.
Possible values: server_tool_use
Identifier of the server tool call.
Name of the server tool: web_search for web search. With the web tools, the declared tool that enabled the capability: deepseek_web_search for searches and the steps of deep thinking search, or deepseek_read_url for URL reading.
Arguments supplied to the server tool as a JSON value, normally an object. With the web tools, input.action is search , open_page , find_in_page or read_link .
caller
object
required
Possible values: direct
Possible values: search , deep_search , read_link , image_search , deep_image_search
DeepSeek extension on blocks produced by the web tools: search for web search, deep_search for deep thinking search, read_link for URL reading, and image_search or deep_image_search (during deep thinking search) for image search. Pass it back unchanged.
Possible values: web_search_tool_result
The ID of the associated server_tool_use block.
content
object[]
required
Search results or search-error items. Pass the entire array back unchanged with the assistant message.
- Array [
Array [
oneOf
- Web search result
- Web search error
Possible values: web_search_result
The title of the result page.
The URL of the result page.
Opaque result content. Preserve this value unchanged when passing the result back.
Page-age metadata, when available; may be null .
DeepSeek extension. A plain-text summary of the result for display.
DeepSeek extension. The name of the site, or null when unknown.
DeepSeek extension. The URL of the site icon, or null when unknown.
Possible values: web_search_tool_result_error
Possible values: invalid_tool_input , unavailable , max_uses_exceeded , too_many_requests , query_too_long , request_too_large
The reason the server-side search failed.
- ]
]
Possible values: search , deep_search , read_link , image_search , deep_image_search
DeepSeek extension on blocks produced by the web tools: search for web search, deep_search for deep thinking search, read_link for URL reading, and image_search or deep_image_search (during deep thinking search) for image search. Pass it back unchanged.
Returned for a page opened during deep thinking search ( deepseek_web_search ), or a link read by deepseek_read_url . Pass it back unchanged, including kind and signature . See the Web Tools Guide .
Possible values: web_fetch_tool_result
The ID of the associated server_tool_use block.
required
The fetched page, or the reason the fetch failed.
oneOf
- Web fetch result
- Web fetch error
Possible values: web_fetch_result
The URL of the page.
content
object
required
The page as a text document.
Possible values: document
source
object
Possible values: text
Possible values: text/plain
Always an empty string: the page text is not returned. For read_link , the page is carried in signature .
The page title.
DeepSeek extension, in place of retrieved_at . The publication time of the page, or null when unknown. For a link read from the user message, the date found on the page, in no fixed format; for a page opened during deep thinking search, an RFC 3339 timestamp.
Possible values: web_fetch_tool_result_error
Possible values: url_not_accessible , url_not_allowed , unavailable
The reason the fetch failed. See the Web Tools Guide .
Possible values: search , deep_search , read_link , image_search , deep_image_search
DeepSeek extension on blocks produced by the web tools: search for web search, deep_search for deep thinking search, read_link for URL reading, and image_search or deep_image_search (during deep thinking search) for image search. Pass it back unchanged.
DeepSeek extension. Present on successful read_link results: the page that was read, encrypted. Pass it back unchanged to restore the page into the context.
- ]
]
Possible values: end_turn , max_tokens , stop_sequence , tool_use , refusal , null
Why generation stopped: natural completion, output limit, a stop sequence, a client tool call, or content filtering. Null in message_start.
The matched stop sequence, or null when no stop sequence was matched.
stop_details
object
nullable
Present when the model content safety review refuses the response ( stop_reason is refusal ). See the Model Content Safety Guide .
Possible values: refusal
Always null .
Names the blocked images when images in the request fail the review; otherwise null .
DeepSeek extension. The conversation title, present only when the request enabled title and a title was generated. Not related to the title of search results and citations.
usage
object
required
Possible values: >= 0
Input tokens not served from the context cache. Total input tokens equal input_tokens + cache_read_input_tokens + cache_creation_input_tokens.
Possible values: 0
Always 0. Anthropic-style cache creation is not used; context caching is automatic.
Possible values: >= 0
Input tokens served from the context cache.
Possible values: >= 0
Generated output tokens, including thinking tokens when thinking is enabled. In message_delta this is the cumulative count, not an increment.
output_tokens_details
object
Breakdown of output_tokens . Present when thinking is enabled or safety_check is high .
Possible values: >= 0
Thinking tokens, already included in output_tokens .
Possible values: >= 0
DeepSeek extension. Tokens of the safety review, already included in output_tokens . Present only when safety_check is high .
Possible values: standard
server_tool_use
object
Server-side web search and fetch counts, separate from token usage. Present only when at least one of the counts is greater than zero; otherwise omitted. All fields are present when this object is returned. Read the final message's usage for non-streaming responses or the final message_delta.usage for streaming responses. These counts are cumulative, not deltas. See Server tool usage .
Possible values: >= 0
Number of server-side web search attempts, including failed attempts and attempts exceeding max_uses .
Possible values: >= 0
Number of successful server-side web searches that returned nonempty results. Failed attempts and empty results are not counted. This field can be used as a basis for billing.
Possible values: >= 0
With the web tools. Number of fetch result blocks in the response, including errors. For display only.
Possible values: >= 0
With the web tools. Number of billed page fetches.
Possible values: >= 0
With the web tools. Number of billed image searches.
Possible values: content_block_start
Possible values: >= 0
Zero-based index of the content block.
required
oneOf
- Text block
- Thinking output
- Tool-use block
- Server tool use output
- Web search result block
- Web fetch result block
Each text block must have type: "text" , with its content in the text field. On input, additional cache_control and citations fields are ignored.
Possible values: text
The text content.
citations
object[]
nullable
Sources cited by this text. Returned when the answer cites results of the web tools; ignored on input.
A source cited by the answer. Returned with the web tools.
- Array [
Array [
Possible values: web_search_result_location
The URL of the cited source.
The title of the cited source, or null when unknown.
Always an empty string.
The answer text of the current text block up to this citation. Unlike the Anthropic API, it is not text quoted from the source.
- ]
]
Possible values: thinking
The generated thinking content. Return this block unchanged when continuing a thinking-mode tool conversation.
Opaque signature returned with the thinking block; preserve it when replaying the block.
Appears in assistant messages. Each tool-use block must have a matching tool-result block in the immediately following user message.
Possible values: tool_use
The tool-call ID. Pass this ID back as tool_result.tool_use_id .
The name of the client tool.
The JSON arguments supplied to the tool, normally an object matching its input_schema .
Describes a tool call executed by the service. Request-level search counts are reported separately in usage.server_tool_use ; the client does not execute this call.
Possible values: server_tool_use
Identifier of the server tool call.
Name of the server tool: web_search for web search. With the web tools, the declared tool that enabled the capability: deepseek_web_search for searches and the steps of deep thinking search, or deepseek_read_url for URL reading.
Arguments supplied to the server tool as a JSON value, normally an object. With the web tools, input.action is search , open_page , find_in_page or read_link .
caller
object
required
Possible values: direct
Possible values: search , deep_search , read_link , image_search , deep_image_search
DeepSeek extension on blocks produced by the web tools: search for web search, deep_search for deep thinking search, read_link for URL reading, and image_search or deep_image_search (during deep thinking search) for image search. Pass it back unchanged.
Possible values: web_search_tool_result
The ID of the associated server_tool_use block.
content
object[]
required
Search results or search-error items. Pass the entire array back unchanged with the assistant message.
- Array [
Array [
oneOf
- Web search result
- Web search error
Possible values: web_search_result
The title of the result page.
The URL of the result page.
Opaque result content. Preserve this value unchanged when passing the result back.
Page-age metadata, when available; may be null .
DeepSeek extension. A plain-text summary of the result for display.
DeepSeek extension. The name of the site, or null when unknown.
DeepSeek extension. The URL of the site icon, or null when unknown.
Possible values: web_search_tool_result_error
Possible values: invalid_tool_input , unavailable , max_uses_exceeded , too_many_requests , query_too_long , request_too_large
The reason the server-side search failed.
- ]
]
Possible values: search , deep_search , read_link , image_search , deep_image_search
DeepSeek extension on blocks produced by the web tools: search for web search, deep_search for deep thinking search, read_link for URL reading, and image_search or deep_image_search (during deep thinking search) for image search. Pass it back unchanged.
Returned for a page opened during deep thinking search ( deepseek_web_search ), or a link read by deepseek_read_url . Pass it back unchanged, including kind and signature . See the Web Tools Guide .
Possible values: web_fetch_tool_result
The ID of the associated server_tool_use block.
required
The fetched page, or the reason the fetch failed.
oneOf
- Web fetch result
- Web fetch error
Possible values: web_fetch_result
The URL of the page.
content
object
required
The page as a text document.
Possible values: document
source
object
Possible values: text
Possible values: text/plain
Always an empty string: the page text is not returned. For read_link , the page is carried in signature .
The page title.
DeepSeek extension, in place of retrieved_at . The publication time of the page, or null when unknown. For a link read from the user message, the date found on the page, in no fixed format; for a page opened during deep thinking search, an RFC 3339 timestamp.
Possible values: web_fetch_tool_result_error
Possible values: url_not_accessible , url_not_allowed , unavailable
The reason the fetch failed. See the Web Tools Guide .
Possible values: search , deep_search , read_link , image_search , deep_image_search
DeepSeek extension on blocks produced by the web tools: search for web search, deep_search for deep thinking search, read_link for URL reading, and image_search or deep_image_search (during deep thinking search) for image search. Pass it back unchanged.
DeepSeek extension. Present on successful read_link results: the page that was read, encrypted. Pass it back unchanged to restore the page into the context.
Possible values: content_block_delta
Possible values: >= 0
Zero-based index of the content block.
required
oneOf
- Text delta
- Thinking delta
- Signature delta
- Tool input delta
- Citations delta
Possible values: text_delta
Append this text to the current text block.
Possible values: thinking_delta
Append this text to the current thinking block.
Possible values: signature_delta
Signature for the completed thinking block.
Possible values: input_json_delta
A fragment of the tool input JSON. Concatenate all fragments for this block, then parse the JSON after content_block_stop.
Adds one citation to the current text block. Returned with the web tools.
Possible values: citations_delta
citation
object
required
A source cited by the answer. Returned with the web tools.
Possible values: web_search_result_location
The URL of the cited source.
The title of the cited source, or null when unknown.
Always an empty string.
The answer text of the current text block up to this citation. Unlike the Anthropic API, it is not text quoted from the source.
Possible values: content_block_stop
Possible values: >= 0
Zero-based index of the content block.
Possible values: message_delta
delta
object
required
Possible values: end_turn , max_tokens , stop_sequence , tool_use , refusal
The final reason generation stopped.
The matched stop sequence, or null when no stop sequence was matched.
stop_details
object
nullable
Present when the model content safety review refuses the response ( stop_reason is refusal ). See the Model Content Safety Guide .
Possible values: refusal
Always null .
Names the blocked images when images in the request fail the review; otherwise null .
DeepSeek extension. The conversation title, present only when the request enabled title and a title was generated.
usage
object
required
Possible values: >= 0
Input tokens not served from the context cache. Total input tokens equal input_tokens + cache_read_input_tokens + cache_creation_input_tokens.
Possible values: 0
Always 0. Anthropic-style cache creation is not used; context caching is automatic.
Possible values: >= 0
Input tokens served from the context cache.
Possible values: >= 0
Generated output tokens, including thinking tokens when thinking is enabled. In message_delta this is the cumulative count, not an increment.
output_tokens_details
object
Breakdown of output_tokens . Present when thinking is enabled or safety_check is high .
Possible values: >= 0
Thinking tokens, already included in output_tokens .
Possible values: >= 0
DeepSeek extension. Tokens of the safety review, already included in output_tokens . Present only when safety_check is high .
Possible values: standard
server_tool_use
object
Server-side web search and fetch counts, separate from token usage. Present only when at least one of the counts is greater than zero; otherwise omitted. All fields are present when this object is returned. Read the final message's usage for non-streaming responses or the final message_delta.usage for streaming responses. These counts are cumulative, not deltas. See Server tool usage .
Possible values: >= 0
Number of server-side web search attempts, including failed attempts and attempts exceeding max_uses .
Possible values: >= 0
Number of successful server-side web searches that returned nonempty results. Failed attempts and empty results are not counted. This field can be used as a basis for billing.
Possible values: >= 0
With the web tools. Number of fetch result blocks in the response, including errors. For display only.
Possible values: >= 0
With the web tools. Number of billed page fetches.
Possible values: >= 0
With the web tools. Number of billed image searches.
Possible values: message_stop
Possible values: ping
- ]
]
Invalid request, for example an empty messages array or unpaired tool results. Errors use the Anthropic structure {type: "error", error: {type, message}} , where error.type follows the HTTP status: invalid_request_error (400, 422), authentication_error (401), billing_error (402), permission_error (403), not_found_error (404), request_too_large (413), rate_limit_error (429), timeout_error (408, 504), overloaded_error (503) and api_error (500 and others). See Error Codes for the causes of each status.
- application/json
- Schema
- Example
Schema
Possible values: error
Always error .
error
object
required
The error type, such as invalid_request_error or rate_limit_error .
A description of the error.
```
{ "type": "error", "error": { "type": "invalid_request_error", "message": "messages: at least one message is required" } }
```
