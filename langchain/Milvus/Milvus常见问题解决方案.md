# Milvus 常见问题解决方案

## 目录

1. [ModuleNotFoundError: No module named 'pymilvus'](#1-modulenotfounderror-no-module-named-pymilvus)
2. [ConnectionConfigException: Illegal uri: [None]](#2-connectionconfigexception-illegal-uri-none)
3. [如何创建 Milvus Collection](#3-如何创建-milvus-collection)
4. [pymilvus 提供文本向量化方法吗？](#4-pymilvus-提供文本向量化方法吗)
5. [pymilvus[model] 是什么？](#5-pymilvusmodel-是什么)
6. [Connection to huggingface.co timed out](#6-connection-to-huggingfaceco-timed-out)
7. [MilvusException: (code=1100, message=more fieldData has pass in)](#7-milvusexception-code1100-message-more-fielddata-has-pass-in)
8. [AttributeError: 'CustomEmbeddingFunction' object has no attribute 'encode_queries'](#8-attributeerror-customembeddingfunction-object-has-no-attribute-encode_queries)

## 1. ModuleNotFoundError: No module named 'pymilvus'

### 问题描述
运行 Milvus 相关代码时，出现 `ModuleNotFoundError: No module named 'pymilvus'` 错误。

### 解决方案
1. 安装 pymilvus 依赖：
   ```bash
   pip install pymilvus
   ```

2. 更新 requirements.txt 文件，添加 pymilvus 依赖：
   ```
   pymilvus==2.6.5
   ```

3. 验证安装：
   ```bash
   python -c "import pymilvus; print('pymilvus installed successfully')"
   ```

## 2. ConnectionConfigException: Illegal uri: [None]

### 问题描述
连接 Milvus 服务器时，出现 `ConnectionConfigException: Illegal uri: [None]` 错误。

### 解决方案
1. 检查 .env 文件格式，确保环境变量格式正确：
   ```env
   # 错误格式
   CLUSTER_ENDPOINT = "https://example.com"
   
   # 正确格式
   CLUSTER_ENDPOINT=https://example.com
   ```

2. 确保 .env 文件编码正确，没有特殊字符

3. 验证环境变量加载：
   ```python
   import os
   from dotenv import load_dotenv
   load_dotenv()
   print(f"CLUSTER_ENDPOINT: {os.getenv('CLUSTER_ENDPOINT')}")
   ```

## 3. 如何创建 Milvus Collection

### 代码示例

```python
from pymilvus import MilvusClient, DataType

# 初始化客户端
client = MilvusClient(
    uri="https://example.com",
    token="your-token"
)

# 定义集合名称
collection_name = "example_collection"

# 创建集合
client.create_collection(
    collection_name=collection_name,
    dimension=1536,  # 向量维度
    primary_field_name="id",
    primary_field_type=DataType.INT64,
    auto_id=True,  # 自动生成主键
    vector_field_name="vector",
    metric_type="COSINE"  # 相似度度量方式
)

# 验证创建
print(f"当前集合: {client.list_collections()}")
```

## 4. pymilvus 提供文本向量化方法吗？

### 回答
pymilvus 本身**不提供**直接的文本向量化方法。pymilvus 是 Milvus 向量数据库的 Python SDK，主要负责向量数据库操作。

### 文本向量化解决方案

使用专门的嵌入模型将文本转换为向量，如：
1. **Sentence Transformers**（开源）
2. **OpenAI Embeddings**（付费）
3. **Cohere Embeddings**（付费）
4. **HuggingFace Transformers**（开源）

### 代码示例（Sentence Transformers）

```python
from sentence_transformers import SentenceTransformer
from pymilvus import MilvusClient

# 初始化嵌入模型
model = SentenceTransformer('all-MiniLM-L6-v2')

# 初始化 Milvus 客户端
client = MilvusClient(uri="https://example.com", token="your-token")

# 文本向量化
texts = ["这是测试文本1", "这是测试文本2"]
vectors = model.encode(texts).tolist()

# 插入到 Milvus
data = [{"vector": v, "text": t} for v, t in zip(vectors, texts)]
client.insert(collection_name="example_collection", data=data)
```

## 5. pymilvus[model] 是什么？

### 回答
`pymilvus[model]` 是 **pymilvus 的可选依赖包**，专门用于**文本向量化和向量处理**，是 Milvus 官方推出的增强功能模块。

### 核心功能

1. **文本嵌入模型**：提供多种嵌入模型集成
2. **向量重排工具**：优化搜索结果排序
3. **多模态支持**：支持图像、视频等多模态数据向量化
4. **简化的 API**：无需单独安装和管理嵌入模型

### 安装方法

```bash
# 安装特定版本
pip install "pymilvus[model]==2.5.6"

# 安装最新版本
pip install "pymilvus[model]"
```

## 6. Connection to huggingface.co timed out

### 问题描述
使用 `model.DefaultEmbeddingFunction()` 时，出现 `Connection to huggingface.co timed out` 错误。

### 解决方案
创建自定义嵌入函数，避免从外部下载模型：

```python
import hashlib
import numpy as np

class CustomEmbeddingFunction:
    def __init__(self, dim=1536):
        self.dim = dim
    
    def encode_documents(self, docs):
        vectors = []
        for doc in docs:
            # 使用哈希值生成向量
            hash_value = hashlib.sha256(doc.encode('utf-8')).hexdigest()
            vector = []
            for i in range(0, len(hash_value), 8):
                segment = hash_value[i:i+8]
                vector.append(float(int(segment, 16)) / (16**8 - 1))
            # 调整向量维度
            vector = vector[:self.dim] + [0.0] * (self.dim - len(vector))
            vectors.append(np.array(vector))
        return vectors
    
    def encode_queries(self, queries):
        return self.encode_documents(queries)

# 使用自定义嵌入函数
embedding_fn = CustomEmbeddingFunction()
```

## 7. MilvusException: (code=1100, message=more fieldData has pass in)

### 问题描述
插入数据时，出现 `MilvusException: (code=1100, message=more fieldData has pass in: invalid parameter[expected=3][actual=4])` 错误。

### 解决方案

1. **检查向量维度**：确保插入的向量维度与集合定义一致
2. **移除手动 id**：如果集合设置了 `auto_id=True`，不要手动指定 id 字段
3. **匹配字段数量**：确保插入的数据字段数量与集合定义一致

### 代码示例

```python
# 正确的数据结构
data = [
    { "vector": vectors[i], "text": docs[i], "subject": "history" }
    for i in range(len(vectors))
]
```

## 8. AttributeError: 'CustomEmbeddingFunction' object has no attribute 'encode_queries'

### 问题描述
调用 `encode_queries()` 方法时，出现 `AttributeError: 'CustomEmbeddingFunction' object has no attribute 'encode_queries'` 错误。

### 解决方案
在自定义嵌入函数中实现 `encode_queries` 方法：

```python
class CustomEmbeddingFunction:
    # ... 其他方法 ...
    
    def encode_queries(self, queries):
        # 对于简单模型，查询和文档可以使用相同的编码方法
        return self.encode_documents(queries)
```

## 最佳实践

1. **环境变量管理**：使用 `.env` 文件管理敏感配置，确保格式正确
2. **向量维度一致性**：始终确保插入的向量维度与集合定义一致
3. **字段匹配**：插入的数据字段必须与集合定义匹配
4. **自定义嵌入函数**：在网络受限环境下，使用自定义嵌入函数避免外部依赖
5. **集合管理**：定期检查和清理不再使用的集合
6. **错误处理**：添加适当的错误处理机制，提高代码健壮性
7. **文档更新**：保持代码注释和文档与实际代码一致

## 总结

本文档总结了使用 Milvus 向量数据库时常见的问题和解决方案，包括依赖安装、连接配置、集合创建、文本向量化、数据插入和搜索等方面。通过遵循最佳实践和正确的解决方案，可以有效避免和解决 Milvus 使用过程中的各种问题。