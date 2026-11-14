<!-- source: https://api-docs.deepseek.com/api/create-response -->
```
POST /responses
```

## /responses
Creates a model response in the OpenAI Responses API format.
The API is stateless : responses and conversations are not stored on the server. For multi-turn conversations, the client needs to send the full conversation history in input on each request. Please refer to the Responses API Guide for details, including the full parameter compatibility tables.

## Request ​
- application/json
Body
required
Possible values: deepseek-flash , deepseek-v4-pro
ID of the model to use. Use deepseek-flash or deepseek-v4-pro .
nullable
The input to the model. Either a plain string (treated as a single user message), or a list of input items.
Supported input item types are message / function_call / function_call_output / custom_tool_call / custom_tool_call_output / reasoning / web_search_call ; other types are ignored. Message roles can be user / assistant / system / developer ( developer is treated as system with deepseek-flash and as user with deepseek-v4-pro ). With the deepseek-flash model, input_image content parts are supported in user / system / developer message items and in the output of function_call_output / custom_tool_call_output items; images in assistant messages return a 400 error. In user messages, input_file with a file_id references an uploaded file, see File Parsing ; file_url is not supported.
At least one of input and instructions is required.
With the web tools or safety_check set to high , some input items are not accepted. See the Web Tools guide .
oneOf
- Text input
- Input item list
string
An input item. Supported types are message / function_call / function_call_output / custom_tool_call / custom_tool_call_output / reasoning / web_search_call ; other types are ignored. reasoning and function_call items are automatically merged into the adjacent assistant message by the server. A web_search_call item returned by a previous response can be passed back to restore its search results into the context. Please refer to the Responses API Guide for the pass-back rules in multi-turn conversations.
- Array [
Array [
Possible values: message , function_call , function_call_output , custom_tool_call , custom_tool_call_output , reasoning , web_search_call
The type of the input item. For message items, this field can be omitted if role is present. custom_tool_call / custom_tool_call_output items are used together with the apply_patch custom tool. web_search_call items restore the search results of a previous server-side search.
Possible values: user , assistant , system , developer
For message items. The role of the message author. developer is treated as system with deepseek-flash and as user with deepseek-v4-pro .
For message items, the message content, either a plain string or a list of input_text / output_text / input_image content parts. For reasoning items, a list of reasoning_text content parts.
oneOf
- Text content
- Array of content parts
string
- Array [
Array [
oneOf
- Text content part
- Image content part
- File content part
- Reasoning text content part
Possible values: input_text , output_text
The type of the content part.
The text content.
An image content part. Processed as a real image. Allowed in user / system / developer message items and in the output of function_call_output / custom_tool_call_output items; images in assistant messages return a 400 error.
Possible values: input_image
The type of the content part, in this case input_image .
The image source, either an http(s) URL of the image (max 8192 characters) or a base64-encoded data URL ( data:image/jpeg;base64,... ). Supported formats: JPEG, PNG, GIF, and WebP. Mutually exclusive with file_id : passing neither returns a 400 error ("input_image must have image_url or file_id"); passing both returns a 400 error ("input_image cannot have both image_url and file_id").
Possible values: low , high , original , auto
Controls how the image is processed. low downsamples the image to 512x512 (faster, cheaper). high , original , and auto keep the original image. Ignored when file_id is set.
The ID of an image file uploaded via the Files API , of the form file-api-... . Mutually exclusive with image_url ; detail is ignored when file_id is set.
References a file uploaded via the Files API. Allowed in user message items. See the File Parsing guide .
Possible values: input_file
The type of the content part, in this case input_file .
The ID of the uploaded file, of the form file-api-... .
Possible values: reasoning_text
The type of the content part, in this case reasoning_text .
The chain-of-thought text content.
- ]
]
For function_call / function_call_output items. The ID pairing a function call with its output. Must be non-empty and unique, and every function_call must have a matching function_call_output .
For function_call items. The name of the function to call.
For function_call items. The arguments to call the function with, in JSON format.
For function_call_output / custom_tool_call_output items. The output of the tool call, either a plain string or a list of input_text / input_image content parts.
oneOf
- Text output
- Array of content parts
string
- Array [
Array [
oneOf
- Text content part
- Image content part
- File content part
- Reasoning text content part
Possible values: input_text , output_text
The type of the content part.
The text content.
An image content part. Processed as a real image. Allowed in user / system / developer message items and in the output of function_call_output / custom_tool_call_output items; images in assistant messages return a 400 error.
Possible values: input_image
The type of the content part, in this case input_image .
The image source, either an http(s) URL of the image (max 8192 characters) or a base64-encoded data URL ( data:image/jpeg;base64,... ). Supported formats: JPEG, PNG, GIF, and WebP. Mutually exclusive with file_id : passing neither returns a 400 error ("input_image must have image_url or file_id"); passing both returns a 400 error ("input_image cannot have both image_url and file_id").
Possible values: low , high , original , auto
Controls how the image is processed. low downsamples the image to 512x512 (faster, cheaper). high , original , and auto keep the original image. Ignored when file_id is set.
The ID of an image file uploaded via the Files API , of the form file-api-... . Mutually exclusive with image_url ; detail is ignored when file_id is set.
References a file uploaded via the Files API. Allowed in user message items. See the File Parsing guide .
Possible values: input_file
The type of the content part, in this case input_file .
The ID of the uploaded file, of the form file-api-... .
Possible values: reasoning_text
The type of the content part, in this case reasoning_text .
The chain-of-thought text content.
- ]
]
- ]
]
A system-level instruction, inserted as the first system message of the model's context.
reasoning
object
nullable
Configuration of the thinking mode.
Possible values: none , low , high , max
Controls the thinking mode toggle and the thinking effort. none disables thinking mode; low / high / max enable thinking mode. If not set, the model's default thinking behavior is used (enabled by default). For compatibility with existing software, minimal is accepted and mapped to low , and medium / xhigh are accepted and mapped to high .
An upper bound for the number of tokens that can be generated in the response, including both the visible output tokens and the reasoning tokens.
Default value: false
If set to true , the response is streamed as semantic server-sent events. The final event is response.completed / response.incomplete / response.failed (there is no data: [DONE] message). Please refer to the Responses API Guide for the full event list.
Possible values: >= 0 and <= 2
Default value: 1
What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. Has no effect in thinking mode.
Possible values: >= 0 and <= 1
An alternative to sampling with temperature, called nucleus sampling. The effective value depends on the model and mode:
- deepseek-flash : In thinking mode, the default is 1.0 and values below 0.95 are treated as 0.95. In non-thinking mode, it is fixed at 1.0 and the value you pass is ignored.
- deepseek-v4-pro : In thinking mode, it is fixed at 0.95 when tool calling is enabled, or 1.0 otherwise; the value you pass is ignored. Setting tool_choice to none disables tool calling even when tools is provided. In non-thinking mode, the value you pass is used, with a default of 1.0.
text
object
nullable
Configuration of the text output.
format
object
The output format. {"type": "text"} (default) for plain text; {"type": "json_object"} for JSON mode; {"type": "json_schema", "name": ..., "schema": ...} for structured output conforming to the given JSON Schema.
If text is omitted or null , or format is omitted, plain text is used. When a format object is provided, type is required.
Possible values: text , json_object , json_schema
The name of the schema. Required when type is json_schema .
The JSON Schema that the output must conform to. Required when type is json_schema .
tools
object[]
nullable
A list of tools the model may call. Function names must be non-empty, at most 128 characters, match ^[a-zA-Z0-9_-]+$ , and be unique across all tools. function tools are supported; web_search is supported with deepseek-v4-pro ; other built-in tool types are ignored. Please refer to the Responses API Guide for details.
A tool the model may call. function defines a function tool — note that in the Responses API format, name / parameters and other function fields are at the top level of the tool object. custom defines a custom tool; only {"type": "custom", "name": "apply_patch"} is supported, and other names return a 400 error. web_search enables server-side web search and is supported with deepseek-v4-pro . deepseek_web_search and deepseek_read_url are the web tools; they cannot be declared together with web_search . See the Web Tools guide .
- Array [
Array [
Possible values: function , custom , web_search , deepseek_web_search , deepseek_read_url
The type of the tool: function , custom (only apply_patch ), web_search ( deepseek-v4-pro only), deepseek_web_search or deepseek_read_url .
For function and custom tools. The name of the tool. For function tools, must be non-empty, at most 128 characters, match ^[a-zA-Z0-9_-]+$ , and be unique across all tools. For custom tools, must be apply_patch .
For function tools. A description of what the function does, used by the model to choose when and how to call the function.
parameters
object
The parameters the functions accepts, described as a JSON Schema object. See the Tool Calls Guide for examples, and the JSON Schema reference for documentation about the format.
Omitting parameters defines a function with an empty parameter list.
- ]
]
nullable
Controls which (if any) tool is called by the model.
none means the model will not call any tool and instead generates a message.
auto (default) means the model can pick between generating a message or calling one or more tools.
required means the model must call one or more tools.
Specifying a particular tool via {"type": "function", "name": "my_function"} forces the model to call that tool.
oneOf
- Tool choice mode
- Named tool choice
string
Possible values: none , auto , required
Forces the model to call the specified tool. name is required when type is function .
Possible values: function
The name of the function to call. Required when type is function .
Possible values: >= 0 and <= 20
Default value: null
An integer between 0 and 20 specifying the number of most likely tokens to return at each token position, each with an associated log probability.
A custom end-user identifier. We recommend using only ASCII letters, digits, underscores ( _ ), and hyphens ( - ). The UTF-8 encoded value must not exceed 512 bytes. Do not include user privacy information.
- It can be used to distinguish user identities on your side to help us with content safety review, for KVCache isolation, and for scheduling isolation. For more details, please refer to Rate Limit & Isolation
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
OK, returns a response object
- application/json
- Schema
- Example
Schema
A unique identifier for the response.
Possible values: response
The object type, which is always response .
The Unix timestamp (in seconds) of when the response was created.
Possible values: in_progress , completed , incomplete , failed
The status of the response.
The error object when the response failed, with code and message fields.
incomplete_details
object
nullable
The details about why the response is incomplete. The reason field can be max_output_tokens or content_filter .
Possible values: max_output_tokens , content_filter
The model used for the response.
output
object[]
required
The list of output items generated by the model. In thinking mode, the chain-of-thought is returned as a reasoning item before the message item. Function calls are returned as function_call items.
An output item generated by the model. message items carry the assistant text, reasoning items carry the chain-of-thought, function_call items represent function calls, custom_tool_call items represent custom tool calls (such as apply_patch ), web_search_call items represent server-side web searches ( deepseek-v4-pro only), and tool_search_call items represent tool searches. With the web tools, every tool call is a web_search_call item with the extension fields kind , page , signature and error .
- Array [
Array [
Possible values: message , reasoning , function_call , custom_tool_call , web_search_call , tool_search_call
The type of the output item: message / reasoning / function_call / custom_tool_call / web_search_call / tool_search_call .
The unique ID of the output item.
Possible values: in_progress , completed , incomplete
The status of the output item.
Possible values: assistant
For message items. Always assistant .
content
object[]
For message items, a list of output_text content parts. For reasoning items, a list of reasoning_text content parts carrying the chain-of-thought in plain text.
- Array [
Array [
Possible values: output_text , reasoning_text
- ]
]
For function_call / custom_tool_call / tool_search_call items. An identifier used when passing the tool output back to the API.
For function_call / custom_tool_call items. The name of the function or custom tool to call.
For function_call items. The arguments to call the function with, as generated by the model in JSON format. Note that the model does not always generate valid JSON, and may hallucinate parameters not defined by your function schema. Validate the arguments in your code before calling your function.
Possible values: search , deep_search , read_link , image_search , deep_image_search
DeepSeek extension on blocks produced by the web tools: search for web search, deep_search for deep thinking search, read_link for URL reading, and image_search or deep_image_search (during deep thinking search) for image search. Pass it back unchanged.
For web_search_call items. type is search (with queries and sources ), open_page (with url ) or find_in_page (with url and pattern ). With the web tools, each element of sources also carries title , snippet , site_name , site_icon and published_at for display.
DeepSeek extension, for web_search_call items that opened or read a page: url , title and published_at . The page text is not returned.
DeepSeek extension, for successful read_link calls. The page, encrypted. Pass it back unchanged so that the page is restored into the context.
DeepSeek extension, for failed web_search_call items ( status is failed ). code is unavailable , url_not_accessible or url_not_allowed .
- ]
]
DeepSeek extension. The conversation title, present only when the request enabled title and a title was generated. In streaming responses, read it from response.title in the final event.
usage
object
nullable
Token and server-tool usage statistics for the response. Null in initial streaming events; read usage from the final response.
Number of input tokens.
input_tokens_details
object
Breakdown of the input tokens.
Number of input tokens that hit the context cache. See Context Caching .
Number of output tokens.
output_tokens_details
object
Breakdown of the output tokens.
Number of reasoning (chain-of-thought) tokens generated by the model.
Possible values: >= 0
DeepSeek extension. Tokens of the safety review, already included in output_tokens . Present only when safety_check is high .
Total number of tokens used in the request (input + output).
server_tool_use
object
Successful server-side web search and page-fetch counts, separate from token usage. Present only when one of the counts is greater than zero; otherwise omitted. All fields are present when this object is returned. In streaming responses, read response.usage from the terminal response.completed, response.incomplete, or response.failed event. These are cumulative counts, not deltas. See Server tool usage .
Possible values: >= 0
Number of successful web search queries. A search with multiple queries can add more than one; failed queries and queries with no results are not counted. This field can be used as a basis for billing.
Possible values: >= 0
Number of successful page fetches performed by open_page or find_in_page. Failed attempts are not counted. With the web tools, finding text in a page is not counted. This field can be used as a basis for billing.
Possible values: >= 0
With the web tools. Number of successful image searches. This field can be used as a basis for billing.
OK, returns a streamed sequence of semantic server-sent events. Each event has an event field for the event type and an incrementing sequence_number . The final event is response.completed / response.incomplete / response.failed (there is no data: [DONE] message). Please refer to the Responses API Guide for the full event list.
- text/event-stream
- Schema
- Example
Schema
- Array [
Array [
object
- ]
]
