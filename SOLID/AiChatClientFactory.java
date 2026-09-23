public class AiChatClientFactory {
    public static AiChatClient getAiChatClient(String providerName){
        if(providerName.equals("openai")){
            return new OpenAiChatClient();
        }
        else if(providerName.equals("anthropic")){
            return new AnthropicChatClient();
        }
        throw new RuntimeException("Invalid prompt");
    }
}
