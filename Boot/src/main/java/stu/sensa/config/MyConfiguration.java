package stu.sensa.config;

import com.huaban.analysis.jieba.JiebaSegmenter;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class MyConfiguration {
    @Bean
    public String hello() {
        return "hello world!";
    }

    @Bean
    public JiebaSegmenter segmenter() {
        return new JiebaSegmenter();
    }
}
