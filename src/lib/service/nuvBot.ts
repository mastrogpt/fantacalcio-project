import axios from "axios";

export async function chat(input: string, threadId: string): Promise<any> {
  const apiUrl = "https://nuvolaris.dev/api/v1/web/fantatest/chatwidget/chat";
  const headers = {
    "Content-Type": "application/json",
  };
  let requestData;
  if (threadId) requestData = {
    thread_id: threadId,
    message: input,
  };
  else requestData = {
     message: input,
  }

  try {
    const response = await axios.post(apiUrl, requestData, { headers });
    return response
  } catch (error) {
    console.error("Error:", error);
    throw error;
  }
}


