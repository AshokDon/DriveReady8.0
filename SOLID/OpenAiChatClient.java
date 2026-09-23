import java.awt.*;

public class OpenAiChatClient implements AiChatClient{

    public void completePrompt(String prompt){
        System.out.println("Response from Open AI: " + prompt);
    }

    @Override
    public void chat(String prompt) {
        completePrompt(prompt);
    }
}
