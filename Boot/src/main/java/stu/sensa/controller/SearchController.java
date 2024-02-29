package stu.sensa.controller;
import com.huaban.analysis.jieba.JiebaSegmenter;
import com.huaban.analysis.jieba.SegToken;
import org.apache.hc.client5.http.classic.HttpClient;
import org.apache.hc.client5.http.classic.methods.HttpPost;
import org.apache.hc.client5.http.impl.classic.CloseableHttpClient;
import org.apache.hc.client5.http.impl.classic.CloseableHttpResponse;
import org.apache.hc.client5.http.impl.classic.HttpClients;
import org.apache.hc.core5.http.ContentType;
import org.apache.hc.core5.http.HttpEntity;
import org.apache.hc.core5.http.HttpResponse;
import org.apache.hc.core5.http.io.entity.EntityUtils;
import org.apache.hc.core5.http.io.entity.StringEntity;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.*;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import stu.sensa.pojo.QueryResult;

import java.lang.reflect.Type;
import java.util.*;
import java.util.stream.Collectors;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

@RestController
@RequestMapping("/")
public class SearchController {
    @Autowired
    private StringRedisTemplate redisTemplate;

    @Autowired
    private JiebaSegmenter segmenter;

    @Autowired
    Set<String> stopwords;

    @PostMapping("query")
    public List<QueryResult> doSearch(String query)
    {
        //分词
        List<SegToken> s = segmenter.process(query, JiebaSegmenter.SegMode.SEARCH);
        //存储文章及其对应的TF-IDF值
        Map<String, Double> articleScores = new HashMap<>();
        //反向索引为zset
        ZSetOperations zSetOperations = redisTemplate.opsForZSet();
        ListOperations listOperations = redisTemplate.opsForList();

        // 对查询语句的每一个分词
        for (SegToken token:s) {
            String word = token.word;

            //去除停止词
            if(stopwords.contains(word)) {
                continue;
            }

            String indexKey = "idx:" + word;

            // 包含该关键词的文章以及其tf-idf值 取前30个
            Set<ZSetOperations.TypedTuple<String>> articlesWithScores =
                    zSetOperations.reverseRangeByScoreWithScores(indexKey, 0, Double.MAX_VALUE, 0, 50);

            if(articlesWithScores == null) {
                continue;
            }

            // 相关的文章
            for (ZSetOperations.TypedTuple<String> articleWithScore : articlesWithScores) {
                String articleId = articleWithScore.getValue();
                Double tfidfValue = articleWithScore.getScore();
                // 累加每篇文章的TF-IDF值
                articleScores.merge(articleId, tfidfValue, Double::sum);
            }
        }

        Map<String, Double> distances = faissSearch(query, 30);

        // 没有任何文章与搜索的关键词有关
        if(articleScores.isEmpty()) {
            return Collections.emptyList();
        }

        // 对所有文章按照累计的TF-IDF值进行排序
        List<Map.Entry<String, Double>> sortedArticles = articleScores.entrySet().stream()
                .sorted(Map.Entry.<String, Double>comparingByValue().reversed())
                .collect(Collectors.toList());

        // 提取排序后的文章编号列表
        List<String> sortedArticleIds = sortedArticles.stream()
                .map(Map.Entry::getKey)
                .collect(Collectors.toList());

        // 构造结果
        List<QueryResult> queryResults = new ArrayList<>();
        for(String article:sortedArticleIds) {
            String url = (String) listOperations.index(article, 0);
            String title = (String) listOperations.index(article, 1);
            queryResults.add(new QueryResult(url, title, ""));
        }
//        queryResults.add(new QueryResult("https://www.baidu.com", "百度", "搜索引擎"));

        return queryResults;
    }

    @GetMapping("/red")
    public String test1() {
        Map<String, Double> map = faissSearch("中国画不能单纯延续传统", 10);
        for (Map.Entry<String, Double> entry : map.entrySet()) {
            System.out.println("Index: " + entry.getKey() + ", Distance: " + entry.getValue());
        }
        return "ok";
    }

    /**
     * 发送查询到 FAISS 服务器并解析响应
     *
     * @param query 要搜索的查询文本
     * @param k 返回的最近邻个数
     * @return 一个包含索引和距离的映射
     */
    private Map<String, Double> faissSearch(String query, Integer k) {
        // 创建 HttpClient 实例
        try (CloseableHttpClient client = HttpClients.createDefault()) {

            // 构建 JSON 请求体
            Map<String, Object> data = new HashMap<>();
            data.put("query", query);
            data.put("k", k);
            String requestBody = new Gson().toJson(data);

            // 构建 HttpPost 请求
            HttpPost post = new HttpPost("http://localhost:5000/search");
            post.setEntity(new StringEntity(requestBody, ContentType.APPLICATION_JSON));

            // 发送请求并获取响应
            try (CloseableHttpResponse response = client.execute(post)) {

                // 解析响应体
                HttpEntity responseEntity = response.getEntity();
                String responseBody = EntityUtils.toString(responseEntity);
                System.out.println(responseBody);

                Gson gson = new Gson();


                Type listType = new TypeToken<List<Map<String, Object>>>(){}.getType();
                List<Map<String, Object>> list = gson.fromJson(responseBody, listType);

                Map<String, Double> resultMap = new HashMap<>();
                for (Map<String, Object> item : list) {
                    String index = (String) item.get("index");
                    Double distance = ((Number) item.get("distance")).doubleValue();
                    resultMap.put(index, distance);
                }
                return resultMap;
            }
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }

}
