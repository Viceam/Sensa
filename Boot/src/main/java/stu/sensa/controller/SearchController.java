package stu.sensa.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import stu.sensa.pojo.QueryResult;

@RestController
@RequestMapping("/")
public class SearchController {
    @PostMapping("query")
    public QueryResult[] doSearch(String query) {
        return null;
    }
}
