"use client";
import React, { useState } from 'react';
import { useDeepSeekStream, Message } from './useDeepSeekStream'; // 引入上面的 Hook
import ReactMarkdown from 'react-markdown'; // 如果没装这个库，可以直接显示纯文本

const DeepSeekDemo: React.FC = () => {
  const [apiKey, setApiKey] = useState('sk-8f48c967cbe44f2d915d3e06e1297d62');
  const [input, setInput] = useState('');
  // 简单的历史记录管理
  const [messages, setMessages] = useState<Message[]>([]);
  
  const { output, isLoading, error, streamChat, stop } = useDeepSeekStream();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || !apiKey) return;

    // 1. 构建新的消息历史
    const newMessages: Message[] = [
      ...messages,
      { role: 'user', content: input }
    ];

    // 更新 UI 显示用户提问
    setMessages(newMessages);
    setInput('');

    // 2. 发起流式请求
    // 注意：DeepSeek 的 API 是无状态的，需要把历史记录传过去
    await streamChat(newMessages, apiKey);

    // 3. 请求结束后，把最终完整的 output 存入历史记录，以便下一次对话
    // 注意：由于闭包问题，这里不能直接读 output，通常做法是在 useEffect 监听 output 变化
    // 但为了 demo 简单，我们在流结束后手动拼装一个 assistant 消息
    // *在实际生产中，建议使用 useEffect 监听 isLoading 变为 false 时更新 messages*
  };

  // 当流结束时，将结果同步回 messages 列表（为了支持多轮对话）
  React.useEffect(() => {
    if (!isLoading && output) {
      setMessages((prev) => {
        // 防止重复添加，检查最后一条是否已经是 assistant 的完整回复
        const lastMsg = prev[prev.length - 1];
        if (lastMsg.role === 'user') {
          return [...prev, { role: 'assistant', content: output }];
        }
        return prev;
      });
    }
  }, [isLoading, output]);

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '20px', fontFamily: 'sans-serif' }}>
      <h1>DeepSeek Stream Demo</h1>
      
      {/* 配置区域 */}
      <div style={{ marginBottom: '20px', padding: '10px', background: '#f5f5f5', borderRadius: '8px' }}>
        <label style={{ display: 'block', marginBottom: '5px' }}>DeepSeek API Key:</label>
        <input 
          type="password" 
          value={apiKey}
          onChange={(e) => setApiKey(e.target.value)}
          placeholder="sk-..."
          style={{ width: '100%', padding: '8px', boxSizing: 'border-box' }}
        />
      </div>

      {/* 聊天显示区域 */}
      <div style={{ 
        border: '1px solid #ddd', 
        borderRadius: '8px', 
        height: '500px', 
        overflowY: 'auto', 
        padding: '20px',
        marginBottom: '20px',
        backgroundColor: '#fff'
      }}>
        {messages.map((msg, idx) => (
          <div key={idx} style={{ 
            marginBottom: '15px', 
            textAlign: msg.role === 'user' ? 'right' : 'left' 
          }}>
            <div style={{ 
              display: 'inline-block', 
              padding: '10px 15px', 
              borderRadius: '10px',
              backgroundColor: msg.role === 'user' ? '#007bff' : '#e9ecef',
              color: msg.role === 'user' ? '#fff' : '#333',
              maxWidth: '80%',
              textAlign: 'left'
            }}>
              <strong>{msg.role === 'user' ? 'You' : 'DeepSeek'}:</strong>
              {/* 如果没有 react-markdown，直接用 <pre>{msg.content}</pre> */}
              <ReactMarkdown>{msg.content}</ReactMarkdown>
            </div>
          </div>
        ))}

        {/* 正在生成的流式内容显示区 (当 isLoading 为 true 时显示实时数据) */}
        {isLoading && (
          <div style={{ textAlign: 'left', marginBottom: '15px' }}>
            <div style={{ 
              display: 'inline-block', 
              padding: '10px 15px', 
              borderRadius: '10px',
              backgroundColor: '#e9ecef',
              color: '#333',
              maxWidth: '80%'
            }}>
              <strong>DeepSeek (Thinking...):</strong>
              <ReactMarkdown>{output}</ReactMarkdown>
              <span style={{ display: 'inline-block', width: '8px', height: '15px', backgroundColor: '#333', animation: 'blink 1s infinite' }}>|</span>
            </div>
          </div>
        )}

        {error && <div style={{ color: 'red', marginTop: '10px' }}>Error: {error}</div>}
      </div>

      {/* 输入区域 */}
      <form onSubmit={handleSubmit} style={{ display: 'flex', gap: '10px' }}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="输入你的问题..."
          disabled={isLoading}
          style={{ flex: 1, padding: '10px', borderRadius: '4px', border: '1px solid #ddd' }}
        />
        {isLoading ? (
          <button 
            type="button" 
            onClick={stop} 
            style={{ padding: '10px 20px', backgroundColor: '#dc3545', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
          >
            停止
          </button>
        ) : (
          <button 
            type="submit" 
            disabled={!input || !apiKey}
            style={{ padding: '10px 20px', backgroundColor: '#28a745', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', opacity: (!input || !apiKey) ? 0.6 : 1 }}
          >
            发送
          </button>
        )}
      </form>
    </div>
  );
};

export default DeepSeekDemo;