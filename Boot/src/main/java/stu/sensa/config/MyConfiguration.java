package stu.sensa.config;

import com.huaban.analysis.jieba.JiebaSegmenter;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.redis.core.SetOperations;
import org.springframework.data.redis.core.StringRedisTemplate;

import java.util.HashSet;
import java.util.Set;

@Configuration
public class MyConfiguration {
    @Autowired
    StringRedisTemplate redisTemplate;

    @Bean
    public JiebaSegmenter segmenter() {
        return new JiebaSegmenter();
    }

    @Bean
    public Set<String> stopwords() {
        String stopWordsKey = "stopwords";
        Set<String> stopwords =redisTemplate.opsForSet().members(stopWordsKey);
        if (stopwords == null) {
            return new HashSet<>();
        }
        return stopwords;
    }
}
