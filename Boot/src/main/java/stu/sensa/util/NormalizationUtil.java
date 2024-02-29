package stu.sensa.util;

import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

public class NormalizationUtil {

    public static void main(String[] args) {
        Map<String, Double> articleScores = new HashMap<>();
        Map<String, Double> distances = new HashMap<>();

        // 假设articleScores和distances已经被填充了数据
        articleScores.put("news1", 373.2);
        articleScores.put("news2", 183.2);
        articleScores.put("news3", 53.2);
        articleScores.put("news11", 13.2);
        articleScores.put("news13", 5.2);

        distances.put("news1", 0.0);
        distances.put("news2", 0.10028178989887238);
        distances.put("news3", 0.212349);
        distances.put("news4", 0.310393924);
        distances.put("news5", 0.45123);


        normalizeDistances(distances, articleScores);

        System.out.println(distances);
    }

    public static void normalizeDistances(Map<String, Double> distances, Map<String, Double> articleScores) {
        if(distances.isEmpty()) return;

        // 找到距离的最大值和最小值
        double minDistance = Collections.min(distances.values());
        double maxDistance = Collections.max(distances.values());

        // 找到TF-IDF得分的最大值和最小值
        double minScore = Collections.min(articleScores.values());
        double maxScore = Collections.max(articleScores.values());

        // 如果只有一个距离值，或者所有距离值都相等，则将其设置为TF-IDF得分范围的中点
        if (distances.size() == 1 || minDistance == maxDistance) {
            double averageScore = (minScore + maxScore) / 2.0;
            distances.replaceAll((k, v) -> averageScore);
            return;
        }

        // 归一化距离到TF-IDF得分的范围，使得距离越小，归一化得分越大
        for (Map.Entry<String, Double> entry : distances.entrySet()) {
            double normalizedDistance = (maxDistance - entry.getValue()) / (maxDistance - minDistance) * (maxScore - minScore) + minScore;
            distances.put(entry.getKey(), normalizedDistance);
        }
    }
}
