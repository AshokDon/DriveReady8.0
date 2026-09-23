public class ChatService {
    //private OpenAiChatClient openAiChatClient;

    private AiChatClient aiChatClient;

    public ChatService(String providerName){
       // this.aiChatClient = aiChatClient;
        this.aiChatClient = AiChatClientFactory.getAiChatClient(providerName);
    }

    public void chat(String prompt){
        aiChatClient.chat(prompt);
    }
}
