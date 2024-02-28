package stu.sensa.controller;
import com.huaban.analysis.jieba.JiebaSegmenter;
import com.huaban.analysis.jieba.SegToken;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.*;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import stu.sensa.pojo.QueryResult;

import java.util.*;
import java.util.stream.Collectors;

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
        String key = "news_num";

        ListOperations operations = redisTemplate.opsForList();
        Object ret = operations.index("news1", 1);
//        operations.set("fortest", 777);
//        Object r2 = operations.get("fortest");
        System.out.println(ret);
        return "成功" + ret;
    }

}
