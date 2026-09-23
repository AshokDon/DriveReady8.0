public class AnthropicChatClient implements AiChatClient {

    public void getResponse(String prompt){
        System.out.println("Response from Anthropic AI: " + prompt);
    }

    @Override
    public void chat(String prompt) {
        getResponse(prompt);
    }
}
