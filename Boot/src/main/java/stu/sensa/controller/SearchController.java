package stu.sensa.controller;

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import stu.sensa.pojo.QueryResult;

import java.util.ArrayList;
import java.util.List;

@RestController
@RequestMapping("/")
public class SearchController {
    @PostMapping("query")
    public List<QueryResult> doSearch(String query)
    {
        System.out.println(query);
        List<QueryResult> queryResults = new ArrayList<>();
        queryResults.add(new QueryResult("https://www.baidu.com", "百度", "搜索引擎"));
        return queryResults;
    }
}
