package stu.sensa.controller;
import com.huaban.analysis.jieba.JiebaSegmenter;
import com.huaban.analysis.jieba.SegToken;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import stu.sensa.pojo.QueryResult;

import java.util.ArrayList;
import java.util.List;

@RestController
@RequestMapping("/")
public class SearchController {
    @Autowired
    private RedisTemplate redisTemplate;
    private JiebaSegmenter segmenter;

    public SearchController(JiebaSegmenter segmenter, String hello) {
        this.segmenter = segmenter;
    }

    @PostMapping("query")
    public List<QueryResult> doSearch(String query)
    {
        List<SegToken> s = segmenter.process(query, JiebaSegmenter.SegMode.SEARCH);
        for (SegToken token:s) {
            System.out.println(token.word);
        }
        List<QueryResult> queryResults = new ArrayList<>();
        queryResults.add(new QueryResult("https://www.baidu.com", "百度", "搜索引擎"));
        return queryResults;
    }
}
