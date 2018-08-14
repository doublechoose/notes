##  是什么

*A type-safe **HTTP client** for Android and Java*

## 为什么

简单易用，快速高效

下表出自http://blog.csdn.net/xiangzhihong8/article/details/51979129

| 使用          | 单次请求  | 7个请求   | 25个请求   |
| ----------- | ----- | ------ | ------- |
| AsyncTask   | 941ms | 4539ms | 13957ms |
| Volley      | 560ms | 2202ms | 4275ms  |
| Retrofit2.0 | 312ms | 889ms  | 1059ms  |

## 怎么用

**API接口：https://api.github.com/users/doublechoose **

#### 准备工作

- 在`build.gradle`文件中`dependencies`下添加依赖：

```
compile 'com.squareup.retrofit2:retrofit:2.2.0'
compile 'com.squareup.retrofit2:converter-gson:2.2.0'
```

- 在`AndroidManifest.xml`添加网络权限

```
<uses-permission android:name="android.permission.INTERNET"/>
```

#### model

- 新建一个`User.java`

```java
public class User {
    private String name;

    public String getName() {
        return name;
    }
  
    public void setName(String name) {
        this.name = name;
    }
}
```

#### interface

- 新建一个`GitHubService.java` 

```java
public interface GitHubService {
    @GET("/users/{user}")
    Call<User> repo(@Path("user")String user);
}
```

#### 调用

```java
Retrofit retrofit = new Retrofit.Builder()
        .baseUrl("https://api.github.com")//设置url
        .addConverterFactory(GsonConverterFactory.create())//设置使用gson转换
        .build();

GitHubService service = retrofit.create(GitHubService.class);

Call<User> model = service.repo("doublechoose");
//请求数据
model.enqueue(new Callback<User>() {
    @Override
    public void onResponse(Call<User> call, Response<User> response) {
        Log.d(TAG, "onResponse: "+response.body().getName());
    }
    @Override
    public void onFailure(Call<User> call, Throwable t) {
        Log.e(TAG, "onFailure: ", t);
    }
});
```
