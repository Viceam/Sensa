package stu.sensa.pojo;

public class QueryResult {
    private String url;
    private String title;
    private String snippet;

    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        this.url = url;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getSnippet() {
        return snippet;
    }

    public void setSnippet(String snippet) {
        this.snippet = snippet;
    }

    public QueryResult(String url, String title, String snippet) {
        this.url = url;
        this.title = title;
        this.snippet = snippet;
    }
}
