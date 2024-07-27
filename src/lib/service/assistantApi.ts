import axios from "axios";

export async function chat(input: string): Promise<any> {
  const apiUrl = "https://nuvolaris.dev/api/v1/web/fantatest/chatwidget/chat";
  const headers = {
    "Content-Type": "application/json",
  };

  const requestData = {
    input: input,
    site: "nuvolaris"
  };

  try {
    const response = await axios.post(apiUrl, requestData, { headers });
    return response.data.output;
  } catch (error) {
    console.error("Error:", error);
    throw error;
  }
}

export async function contactUs(input: string): Promise<any> {
  const apiUrl = "https://nuvolaris.dev/api/v1/web/mastrogptest/waitlist/chat";
  const headers = {
    "Content-Type": "application/json",
  };

  const requestData = {
    input: input,
    site: "nuvolaris"
  };

  try {
    const response = await axios.post(apiUrl, requestData, { headers });
    return response.data.output;
  } catch (error) {
    console.error("Error:", error);
    throw error;
  }
}


export async function notifySlack(userMessage: string) {
  const headers = {
    "Content-Type": "application/json",
  };
  const data = {
    text: userMessage,
  };

  axios
    .post("https://nuvolaris.dev/api/v1/web/mastrogptest/waitlist/slack", data, {
      headers,
    })
    .then((response) => {
      console.log(response.status);
    })
    .catch((error) => {
      console.error(error);
    });
}


