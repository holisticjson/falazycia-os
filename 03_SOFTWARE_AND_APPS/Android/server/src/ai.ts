import http from 'http';

const NVIDIA_API_KEY = process.env.NVIDIA_API_KEY || '';
const NVIDIA_BASE_URL = 'https://integrate.api.nvidia.com/v1/chat/completions';
const DEFAULT_MODEL = 'meta/llama-3.1-70b-instruct';

export interface ChatMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

/**
 * Helper to fetch GCP metadata token for default service account when running on GCP VM.
 */
async function getGCPMetadataToken(): Promise<string | null> {
  try {
    const response = await fetch(
      'http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token',
      {
        headers: { 'Metadata-Flavor': 'Google' },
      }
    );
    if (!response.ok) return null;
    const data = await response.json() as { access_token: string };
    return data.access_token;
  } catch (error) {
    // Fallback/null if running locally or outside GCP Compute Engine
    return null;
  }
}

/**
 * Queries Vertex AI Search (Discovery Engine) Website Data Store using GCP Service Account.
 */
export async function queryVertexAISearch(query: string): Promise<string[]> {
  const projectId = process.env.VERTEX_PROJECT_ID || 'holistic-broker';
  const dataStoreId = process.env.VERTEX_DATA_STORE_ID || '';

  if (!dataStoreId) {
    return [];
  }

  const token = await getGCPMetadataToken();
  if (!token) {
    console.log('Vertex AI: Unable to retrieve GCP metadata token (local dev or service account missing).');
    return [];
  }

  const url = `https://discoveryengine.googleapis.com/v1alpha/projects/${projectId}/locations/global/collections/default_collection/dataStores/${dataStoreId}/servingConfigs/default_search:search`;

  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({
        query: query,
        pageSize: 3,
      }),
    });

    if (!response.ok) {
      console.error(`Vertex AI Search Error: ${response.status} ${await response.text()}`);
      return [];
    }

    const data = await response.json() as any;
    const results: string[] = [];

    if (data.results && Array.isArray(data.results)) {
      for (const res of data.results) {
        const parts: string[] = [];
        const document = res.document;
        if (document) {
          if (document.derivedStructData) {
            const struct = document.derivedStructData;
            if (struct.title) parts.push(`Title: ${struct.title}`);
            if (struct.link) parts.push(`Link: ${struct.link}`);
            if (struct.snippets && Array.isArray(struct.snippets)) {
              const snippetText = struct.snippets
                .map((s: any) => s.snippet)
                .filter(Boolean)
                .join(' ');
              if (snippetText) parts.push(`Content: ${snippetText}`);
            }
          }
        }
        if (parts.length > 0) {
          results.push(parts.join('\n'));
        }
      }
    }

    return results;
  } catch (err) {
    console.error('Vertex AI Search error:', err);
    return [];
  }
}

export async function proxyChatStream(
  messages: ChatMessage[],
  model: string = DEFAULT_MODEL,
  res: http.ServerResponse
): Promise<void> {
  if (!NVIDIA_API_KEY) {
    res.writeHead(500, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: 'NVIDIA_API_KEY is not configured on the server.' }));
    return;
  }

  try {
    // Retrieve Vertex AI Search context if data store is configured and query has user messages
    const userMessages = messages.filter(m => m.role === 'user');
    if (userMessages.length > 0 && process.env.VERTEX_DATA_STORE_ID) {
      const lastUserQuery = userMessages[userMessages.length - 1].content;
      console.log(`Vertex AI Search: Querying database context for: "${lastUserQuery}"`);
      const contextResults = await queryVertexAISearch(lastUserQuery);
      if (contextResults.length > 0) {
        console.log(`Vertex AI Search: Successfully retrieved ${contextResults.length} records.`);
        const contextSystemPrompt = `Wyszukane informacje z oficjalnej bazy wiedzy jaison.pl:\n\n${contextResults.join('\n---\n')}\n\nUżyj powyższego kontekstu do precyzyjnego i zwięzłego sformułowania odpowiedzi, zachowując styl Ghost v2 (zwięźle, w punkt, bez korporacyjnego lania wody).`;
        
        // Prepend context as a system instruction
        messages.unshift({
          role: 'system',
          content: contextSystemPrompt
        });
      }
    }

    const payload = {
      model: model,
      messages: messages,
      temperature: 0.7,
      max_tokens: 1024,
      stream: true,
    };

    res.writeHead(200, {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
    });

    const response = await fetch(NVIDIA_BASE_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${NVIDIA_API_KEY}`,
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const errorText = await response.text();
      res.write(`data: ${JSON.stringify({ error: `NVIDIA API Error: ${errorText}` })}\n\n`);
      res.end();
      return;
    }

    if (!response.body) {
      res.write(`data: ${JSON.stringify({ error: 'No response body received from NVIDIA API' })}\n\n`);
      res.end();
      return;
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value, { stream: true });
      res.write(chunk);
    }

    res.end();
  } catch (error: any) {
    console.error('Error in LLM proxy:', error);
    res.write(`data: ${JSON.stringify({ error: error.message || 'Internal server error in LLM proxy' })}\n\n`);
    res.end();
  }
}
