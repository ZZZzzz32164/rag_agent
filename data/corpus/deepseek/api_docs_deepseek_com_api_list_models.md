<!-- source: https://api-docs.deepseek.com/api/list-models -->
```
GET /models
```

## /models
Lists the currently available models, and provides metadata about each one, such as its display name, context window, output limit, supported input/output modalities, supported effort levels, and per-protocol API capabilities. Check Models & Pricing for our currently supported models.

## Responses ​
- 200
OK, returns A list of models
- application/json
- Schema
- Example
Schema
Possible values: list
The object type, which is always list .
data
object[]
required
The list of model objects.
Describes a DeepSeek model offering that can be used with the API. Besides the identifier fields, each model carries machine-readable metadata about its capabilities and limits; a metadata field may be omitted when the information is not available for that model.
- Array [
Array [
The model identifier, which can be referenced in the API endpoints.
Possible values: model
The object type, which is always "model".
The organization that owns the model.
The display name of the model, for use in model pickers and model discovery tools.
The total token capacity of the context window, counting both input and output tokens.
The maximum number of output tokens the server allows in a single response, i.e. the maximum accepted value of max_tokens .
Possible values: text , image
The input types the model accepts.
Possible values: text
The media types the model can generate.
effort
object
The effort levels available when thinking mode is enabled.
The effort levels the model supports when thinking mode is enabled, in the recommended display order. These are the values accepted by the reasoning_effort parameter; none , which turns thinking mode off, is not included.
The effort level the server uses when thinking mode is enabled and the request does not specify one. Always one of supported_levels . Only present when the server defines a default for the model.
api_capabilities
object
Model behavior declared per API protocol.
anthropic_messages
object
Capabilities that apply when the model is used through the Anthropic Messages API .
Possible values: leading-only , in-history
How the model picks up an updated system prompt during a conversation.
- leading-only : only the system prompt at the start of the conversation takes effect. To change the system prompt, modify that leading system prompt; system messages appearing later in the history are not treated as system prompt updates.
- in-history : a system message may be appended to the conversation history. The latest system message in the history provides the complete effective system prompt and replaces all earlier ones.
- ]
]
