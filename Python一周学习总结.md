# Python 学习总结（核心要点）

## 1. Flask框架基础
- **应用初始化与运行**：学习了如何创建Flask应用实例并启动服务器
- **路由系统**：掌握了使用`@app.route()`装饰器定义路由和视图函数
- **Cookie操作**：学会了设置、获取和删除Cookie，用于客户端状态管理
- **Session管理**：理解了基于服务器的会话管理，包括Session的添加、获取和删除

## 2. MVC架构设计
- **模块化设计**：使用Blueprint实现了模块化路由管理，将用户和文章功能分离
- **控制器实现**：创建了独立的控制器文件，实现了功能的封装和复用
- **路由注册**：通过`app.register_blueprint()`将模块路由注册到主应用
- **拦截器机制**：
  - 全局拦截器：使用`@app.before_request`实现全局请求拦截
  - 模块级拦截器：在Blueprint中使用`@blueprint.before_request`实现模块级拦截

## 3. ORM数据库操作
- **自定义ORM类**：实现了简单的ORM类，封装了数据库连接和查询操作
- **数据库连接**：使用psycopg2连接PostgreSQL数据库
- **面向对象查询**：通过类方法实现了面向对象的数据库查询
- **SQLAlchemy框架**：了解了SQLAlchemy的基本概念和功能，包括：
  - 高级SQL表达式语言
  - 数据库迁移支持
  - 多种数据库后端支持
  - 异步操作支持

## 4. 项目环境与依赖管理
- **虚拟环境**：学会了创建和激活Python虚拟环境
- **依赖管理**：使用`pip freeze > requirements.txt`生成项目依赖清单
- **核心依赖库**：
  - Flask 3.0.2：Web框架.
  - SQLAlchemy 2.0.44：ORM框架.
  - psycopg2-binary 2.9.11：PostgreSQL数据库驱动.
  - 各种Flask扩展：Flask-Login、Flask-Migrate等.

## 5. 学习资源
- Flask官方教程：https://osgeo.cn/flask/
- Python官方教程：https://docs.python.org/zh-cn/3/tutorial/index.html

## 6. 代码结构与组织
- 采用了清晰的目录结构，分离了不同功能模块
- 实现了从简单到复杂的Flask应用演进
- 包含了多个示例文件，展示了不同阶段的学习成果

## 总结
本周主要学习了Flask Web框架的核心概念和实践应用，包括路由系统、状态管理、MVC架构设计以及ORM数据库操作。通过多个示例文件，从简单的Flask应用逐步演进到复杂的MVC架构和ORM数据库操作，构建了完整的Web应用开发知识体系。同时，掌握了Python项目的环境管理和依赖管理方法，为后续的深入学习打下了坚实的基础。