"use client";
import { useState, useCallback, useRef } from 'react';

// 定义消息类型
export interface Message {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

interface UseDeepSeekStreamReturn {
  output: string;          // 当前累积的回复内容
  isLoading: boolean;      // 是否正在生成
  error: string | null;    // 错误信息
  streamChat: (messages: Message[], apiKey: string) => Promise<void>;
  stop: () => void;        // 手动停止生成
  reset: () => void;       // 重置状态
}

export const useDeepSeekStream = (): UseDeepSeekStreamReturn => {
  const [output, setOutput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  // 用于中断请求
  const abortControllerRef = useRef<AbortController | null>(null);

  const reset = useCallback(() => {
    setOutput('');
    setError(null);
    setIsLoading(false);
  }, []);

  const stop = useCallback(() => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      abortControllerRef.current = null;
      setIsLoading(false);
    }
  }, []);

  const streamChat = useCallback(async (messages: Message[], apiKey: string) => {
    reset();
    setIsLoading(true);
    abortControllerRef.current = new AbortController();

    try {
      const response = await fetch('https://api.deepseek.com/chat/completions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${apiKey}`,
        },
        body: JSON.stringify({
          model: 'deepseek-chat', // 或者 'deepseek-reasoner'
          messages: messages,
          stream: true, // 必须开启流式
          temperature: 1.3,
        }),
        signal: abortControllerRef.current.signal,
      });

      if (!response.ok) {
        const errJson = await response.json();
        throw new Error(errJson.error?.message || `HTTP Error: ${response.status}`);
      }

      if (!response.body) throw new Error('ReadableStream not supported.');

      const reader = response.body.getReader();
      const decoder = new TextDecoder('utf-8');
      let buffer = ''; // 用于处理分包的缓存

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        // 解码当前二进制块并追加到 buffer
        const chunk = decoder.decode(value, { stream: true });
        buffer += chunk;

        // SSE 格式通常是: data: {...}\n\n
        const lines = buffer.split('\n');
        
        // 最后一行可能不完整，保留在 buffer 中等待下一次拼接
        buffer = lines.pop() || ''; 

        for (const line of lines) {
          const trimmedLine = line.trim();
          if (!trimmedLine.startsWith('data: ')) continue;
          
          const dataStr = trimmedLine.slice(6); // 去掉 'data: ' 前缀

          if (dataStr === '[DONE]') {
            // 流结束标志
            break;
          }

          try {
            const data = JSON.parse(dataStr);
            // 兼容 OpenAI 格式： choices[0].delta.content
            const content = data.choices?.[0]?.delta?.content || '';
            
            if (content) {
              setOutput((prev) => prev + content);
            }
          } catch (e) {
            console.warn('JSON Parse Error for line:', line, e);
          }
        }
      }
    } catch (err: any) {
      if (err.name === 'AbortError') {
        console.log('Stream aborted by user');
      } else {
        setError(err.message || 'Something went wrong');
      }
    } finally {
      setIsLoading(false);
      abortControllerRef.current = null;
    }
  }, [reset]);

  return { output, isLoading, error, streamChat, stop, reset };
};