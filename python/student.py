import re
import json

def main(arg1: str) -> dict:
    # 使用正则表达式提取被 ```json 和 ``` 包裹的内容
    match = re.search(r'```json\s*([\s\S]*?)\s*```', arg1)
    if not match:
        raise ValueError("输入字符串中未找到有效的 JSON 数据")
    
    # 提取 JSON 字符串
    json_str = match.group(1).strip()
    
    try:
        # 将 JSON 字符串解析为 Python 字典
        result_dict = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON 解析失败: {e}")
    
    # 返回包含解析结果的字典
    return {
        "result": result_dict,
    }

if __name__ == "__main__":
    # 测试数据：包含JSON数据的字符串
    test_input = """
```json
[
    {
        "title": "统计全校各科目平均分",
        "sql": "SELECT subject, ROUND(AVG(score), 2) AS avg_score FROM student_scores GROUP BY subject ORDER BY avg_score DESC;"
    },
    {
        "title": "按学期统计各科目平均分",
        "sql": "SELECT subject, semester, ROUND(AVG(score), 2) AS avg_score FROM student_scores GROUP BY subject, semester ORDER BY semester, avg_score DESC;"
    }
]
```
"""
    
    try:
        result = main(test_input)
        print("解析结果:")
        print(result)
    except Exception as e:
        print(f"错误: {e}")



#         {
#   "arg1": "<think>\n首先，用户的问题是：“查询全校各科目平均分情况”。这翻译成英文是：“Query the average score of each subject across the entire school.”\n\n从之前的系统提示中，我需要生成 JSON 格式的 SQL 查询数组。每个 SQL 查询必须与问题直接相关，并从不同维度分析数据。最多生成10个 SQL 查询。\n\n问题焦点是“全校各科目平均分”，所以核心是计算每个科目的平均分。但系统要求从不同维度分析数据，所以我需要思考其他相关的维度。\n\n回顾表结构：\n- student_scores 表有字段：id, student_id, student_name, class_name, subject, score, exam_date, semester, grade, created_at, updated_at\n\n关键维度：\n- 按科目分组计算平均分。\n- 其他可能维度：学期（semester）、年级（grade）、班级（class_name）、时间（exam_date 或 semester）。\n\n系统要求：涉及全量的应查询SQL以学期聚合。意思是如果查询涉及全校全量数据，应该按学期聚合。但问题指定了“全校”，所以可能需要考虑学期。\n\n问题说“全校各科目平均分”，没有指定学期，所以我应该考虑所有学期，或者按学期分组。\n\n从之前的响应中，它生成了三个 SQL：\n1. 直接平均分\n2. 及格率\n3. 成绩分布\n\n这些都与科目相关，但从不同角度。\n\n现在，我需要生成最多10个 SQL 查询，每个从不同维度。\n\n可能的维度：\n1. 按科目计算平均分（核心）。\n2. 按科目和学期计算平均分，以查看趋势。\n3. 按科目和年级计算平均分。\n4. 按科目和班级计算平均分（但问题说“全校”，所以可能不按班级）。\n5. 计算每个科目的最高分、最低分。\n6. 计算每个科目的标准差或方差，以看分数分布。\n7. 按考试日期分析，但可能太细，最好按学期。\n8. 计算每个科目的及格率（如之前）。\n9. 计算每个科目的优秀率（如分数>=90）。\n10. 按性别或其他，但表中没有性别字段，所以不能。\n\n表中字段没有性别，只有给定的字段。\n\n所以，可能的 SQL 查询：\n1. 全校各科目平均分。\n2. 各科目平均分按学期分组。\n3. 各科目平均分按年级分组。\n4. 各科目成绩分布（优秀、良好、及格、不及格）。\n5. 各科目及格率。\n6. 各科目最高分和最低分。\n7. 各科目分数标准差（如果支持，但MySQL有STDDEV函数）。\n8. 各科目平均分随时间趋势（按学期或考试日期）。\n9. 各科目参与考试的学生数量。\n10. 各科目分数中位数（但MySQL没有直接中位数函数，可能需要复杂查询）。\n\n系统说“涉及全量的应查询SQL以学期聚合”，所以对于全校查询，应该考虑按学期聚合。\n\n问题没有指定学期，所以我应该生成一些按学期分组的查询。\n\n但核心是“各科目平均分”，所以第一个应该是简单的按科目分组平均分。\n\n然后，从不同维度：\n- 时间维度：按学期\n- 年级维度\n- 统计维度：及格率、分布等\n\n最多10个，所以我可以选择最相关的。\n\n列出可能查询：\n1. SELECT subject, AVG(score) AS avg_score FROM student_scores GROUP BY subject ORDER BY avg_score DESC;\n2. SELECT subject, semester, AVG(score) AS avg_score FROM student_scores GROUP BY subject, semester ORDER BY subject, semester;\n3. SELECT subject, grade, AVG(score) AS avg_score FROM student_scores GROUP BY subject, grade ORDER BY subject, grade;\n4. SELECT subject, COUNT(*) AS student_count, AVG(score) AS avg_score FROM student_scores GROUP BY subject;\n5. SELECT subject, \n     COUNT(CASE WHEN score >= 90 THEN 1 END) AS excellent_count,\n     COUNT(CASE WHEN score >= 75 AND score < 90 THEN 1 END) AS good_count,\n     COUNT(CASE WHEN score >= 60 AND score < 75 THEN 1 END) AS pass_count,\n     COUNT(CASE WHEN score < 60 THEN 1 END) AS fail_count\n   FROM student_scores GROUP BY subject;\n6. SELECT subject, ROUND(COUNT(CASE WHEN score >= 60 THEN 1 END) * 100.0 / COUNT(*), 2) AS pass_rate FROM student_scores GROUP BY subject;\n7. SELECT subject, MAX(score) AS max_score, MIN(score) AS min_score FROM student_scores GROUP BY subject;\n8. SELECT subject, STDDEV(score) AS std_dev FROM student_scores GROUP BY subject;  -- 如果MySQL支持，MySQL有STDDEV或STDDEV_POP\n9. SELECT subject, semester, AVG(score) AS avg_score, \n     COUNT(*) AS exam_count \n   FROM student_scores \n   GROUP BY subject, semester \n   ORDER BY semester, subject;\n10. 或许按班级，但问题说全校，所以可能不必要。\n\n系统说“从不同维度分析数据”，所以应该覆盖多个方面。\n\n在之前的响应中，它只生了三个，但系统说最多10个，我可以生成更多，但不要过度。\n\n问题比较简单，所以可能不需要10个。但系统说“最多10个”，所以我可以生成少于10个。\n\n在之前的响应中，它生了三个，所以可能3-5个是合理的。\n\n但为了完整，我可以生成几个。\n\n确保 SQL 语法正确，并考虑性能优化。例如，使用 GROUP BY 时，确保索引。\n\n输出格式必须是 JSON 数组，每个元素有 \"title\" 和 \"sql\"，如之前。\n\n输出以 ```json 开始。\n\n所以，结构：\n```json\n[\n  {\n    \"title\": \"描述\",\n    \"sql\": \"SQL 语句\"\n  },\n  ...\n]\n```\n\n现在，定义查询：\n1. 核心：各科目平均分\n2. 按学期：各科目平均分按学期\n3. 按年级：各科目平均分按年级\n4. 成绩分布：各科目分数段分布\n5. 及格率：各科目及格率\n6. 极值：各科目最高最低分\n7. 标准差：各科目分数标准差\n8. 考试次数：各科目考试参与人数或次数\n9. 按班级？但全校，可能不。\n10. 时间趋势：按考试日期聚合，但可能太细，用学期。\n\n既然系统说“以学期聚合”，我应该优先学期。\n\n所以，列表：\n- 全校各科目平均分\n- 各科目平均分按学期\n- 各科目平均分按年级\n- 各科目成绩分布\n- 各科目及格率\n- 各科目最高分和最低分\n- 各科目分数标准差\n- 各科目考试学生数量（去重学号）\n- 各科目平均分和方差\n\nMySQL 有 VARIANCE() 函数吗？标准 SQL 有，但检查。\n\n在 MySQL，有 VARIANCE() 或 VAR_POP()。\n\n但为了简单，假设支持。\n\n现在，生成 JSON。\n\n首先，标题应该描述查询。\n\n例如：\n- \"统计全校各科目平均分\"\n- \"按学期统计各科目平均分\"\n- 等等。\n\n确保 SQL 正确。\n\n使用 ROUND 来格式化分数，如之前。\n\n在平均分上使用 ROUND(AVG(score), 2)\n\n在计数时，使用 COUNT(*)\n\n对于及格率，使用 CASE WHEN\n\n现在，写 SQL。\n\n1. 全校各科目平均分：\n   SELECT subject, ROUND(AVG(score), 2) AS avg_score FROM student_scores GROUP BY subject ORDER BY avg_score DESC;\n\n2. 按学期：\n   SELECT subject, semester, ROUND(AVG(score), 2) AS avg_score FROM student_scores GROUP BY subject, semester ORDER BY subject, semester;\n\n3. 按年级：\n   SELECT subject, grade, ROUND(AVG(score), 2) AS avg_score FROM student_scores GROUP BY subject, grade ORDER BY subject, grade;\n\n4. 成绩分布：\n   SELECT subject, \n          COUNT(CASE WHEN score >= 90 THEN 1 END) AS excellent_count,\n          COUNT(CASE WHEN score >= 75 AND score < 90 THEN 1 END) AS good_count,\n          COUNT(CASE WHEN score >= 60 AND score < 75 THEN 1 END) AS pass_count,\n          COUNT(CASE WHEN score < 60 THEN 1 END) AS fail_count\n   FROM student_scores GROUP BY subject;\n\n5. 及格率：\n   SELECT subject, ROUND(COUNT(CASE WHEN score >= 60 THEN 1 END) * 100.0 / COUNT(*), 2) AS pass_rate FROM student_scores GROUP BY subject ORDER BY pass_rate DESC;\n\n6. 最高最低分：\n   SELECT subject, MAX(score) AS max_score, MIN(score) AS min_score FROM student_scores GROUP BY subject;\n\n7. 标准差：\n   SELECT subject, ROUND(STDDEV(score), 2) AS std_dev FROM student_scores GROUP BY subject;  -- MySQL 有 STDDEV 或 STDDEV_POP？ 标准是 STDDEV或STDDEV_SAMP，但常用STDDEV。在MySQL，是STDDEV_POP()或STD()？检查文档。 在MySQL 5.7+，有STDDEV_POP()。 但为了兼容，使用STDDEV()如果支持。 在标准SQL，是STDDEV_SAMP for sample, STDDEV_POP for population. 但许多数据库支持STDDEV as sample. 在MySQL，STDDEV() is an alias for STDDEV_SAMP(). 所以使用STDDEV(score)。\n\n8. 考试学生数量：按科目统计唯一学生数。\n   SELECT subject, COUNT(DISTINCT student_id) AS unique_students FROM student_scores GROUP BY subject;\n\n9. 平均分和考试次数：\n   SELECT subject, ROUND(AVG(score), 2) AS avg_score, COUNT(*) AS exam_count FROM student_scores GROUP BY subject;\n\n10. 按学期和科目的平均分趋势：\n    SELECT semester, subject, ROUND(AVG(score), 2) AS avg_score FROM student_scores GROUP BY semester, subject ORDER BY semester, subject;\n\n但我已经有按学期的了。\n\n或许添加一个查询显示各科目平均分的变化 over time。\n\n但 since 有 semester, 可以按学期。\n\n现在，我有9个查询了。可以选择一些。\n\n问题焦点是平均分，所以核心是平均分，其他是补充。\n\n在之前的响应，它只用了3个，所以可能不需要太多。\n\n但系统说“最多10个”，所以我可以生成5-7个。\n\n为了安全，生成5个左右。\n\n选择最相关的：\n- 直接平均分\n- 按学期\n- 按年级\n- 成绩分布\n- 及格率\n\n这些覆盖了主要维度。\n\n在输出中，使用 ORDER BY 来排序，通常按平均分或科目。\n\n在 JSON，每个有 \"title\" 和 \"sql\"。\n\n输出以 ```json 开始。\n\n所以，最终输出。\n</think>```json\n[\n    {\n        \"title\": \"统计全校各科目平均分\",\n        \"sql\": \"SELECT subject, ROUND(AVG(score), 2) AS avg_score FROM student_scores GROUP BY subject ORDER BY avg_score DESC;\"\n    },\n    {\n        \"title\": \"按学期统计各科目平均分\",\n        \"sql\": \"SELECT subject, semester, ROUND(AVG(score), 2) AS avg_score FROM student_scores GROUP BY subject, semester ORDER BY semester, avg_score DESC;\"\n    },\n    {\n        \"title\": \"按年级统计各科目平均分\",\n        \"sql\": \"SELECT subject, grade, ROUND(AVG(score), 2) AS avg_score FROM student_scores GROUP BY subject, grade ORDER BY grade, avg_score DESC;\"\n    },\n    {\n        \"title\": \"统计各科目成绩分布\",\n        \"sql\": \"SELECT subject, COUNT(CASE WHEN score >= 90 THEN 1 END) AS excellent_count, COUNT(CASE WHEN score >= 75 AND score < 90 THEN 1 END) AS good_count, COUNT(CASE WHEN score >= 60 AND score < 75 THEN 1 END) AS pass_count, COUNT(CASE WHEN score < 60 THEN 1 END) AS fail_count FROM student_scores GROUP BY subject;\"\n    },\n    {\n        \"title\": \"统计各科目及格率\",\n        \"sql\": \"SELECT subject, ROUND(COUNT(CASE WHEN score >= 60 THEN 1 END) * 100.0 / COUNT(*), 2) AS pass_rate FROM student_scores GROUP BY subject ORDER BY pass_rate DESC;\"\n    }\n]\n```"
# }