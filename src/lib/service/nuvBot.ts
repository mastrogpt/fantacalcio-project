import axios from "axios";

export interface ChatInput {
  message: string;
  file?: any; 
  threadId?: string;
}

export async function chat(input: ChatInput): Promise<any> {
  //console.log("INPUT", input);
  const apiUrl = "https://nuvolaris.dev/api/v1/web/fantatest/chatwidget/chat";
  const headers = {
    "Content-Type": "application/json",
  };

  const requestData = {
    message: input.message,
    ...(input.threadId && { thread_id: input.threadId }),
    ...(input.file && { attachments: input.file }),
  };

  try {
    const response = await axios.post(apiUrl, requestData, { headers });
    return response;
  } catch (error) {
    console.error("Error:", error);
    throw error;
  }
}
