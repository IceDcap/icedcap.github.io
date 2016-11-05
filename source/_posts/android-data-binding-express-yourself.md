---
title: Android Data Binding系列之表达你所要表达的
date: 2016-07-29 20:42:26
tags: [android, data binding]
categories: [android]
---

>**原文地址：**[https://medium.com/google-developers/android-data-binding-express-yourself-c931d1f90dfe#.j4adry90k](https://medium.com/google-developers/android-data-binding-express-yourself-c931d1f90dfe#.j4adry90k)


# 比访问字段还要多一点
在[上一篇文章][android-data-binding-adding-some-variability]的讨论中，你学会了在布局文件中使用变量。举个例子，使用如下表达式为`TextView`设置用户名：

```xml
android:text="@{user.firstName}"
```

<!--more-->

*User*类可以被声明为一个简单的JavaBean（POJO）

```java
public class User {
    public String firstName;
    public String lastName;
    public Bitmap image;
}
```


注意这里为了演示所需将模型类声明为public的字段，为了保证代码健壮性不建议这样使用，而是按照javaBean规范严格书写。对于布局中的表达式也要保证简短清晰不希望出现长表达式，除此之外我们也不希望开发者在表达式中添加类似于*getFirstName()* 或者 *getLastName()*的方法，这些都会使得表达式不具有可读性。表达式解析器会为这些字段自动寻找Java Bean中所对应的访问器名称(getXxx()或isXxx())。当你的类中含有字段访问方法(getXxx()),相同的表达式都能工作的很好：

```java
public class User {
    private String firstName;
    private String lastName;
    private Bitmap image;

    public String getFirstName() { return firstName; }
    public String getLastName() { return lastName; }
    public Bitmap getImage() { return image; }
}
```


如果它不能找到类似与getXxx()的方法，它仍然可以通过其他方法例如xxx()进行寻找，所以你不比担心javaBean的声明问题，你可以使用*user.hasFriend*去访问javaBean中的*hasFriend()*方法

安卓数据绑定表达式语法也支持数组的访问，它使用方括号，和在Java代码中使用一样：

```
android:text="@{user.friends[0].firstName}"
```


你也可以使用方括号应用在`List`或者`Map`集合上，其实方括号的使用和“get”方法一样便捷。

安卓数据绑定表达式还支持几乎所有的java语言表达式，包括方法调用，三目表达式和数学操作。但是你不能使用的太过分：

```
android:text='@{user.adult ? ((user.male ? "Mr. " : "Ms. ") + user.lastName) : (user.firstName instanceof String ? user.firstName : "kid") }'
```


没人愿意阅读上述的代码！除了明显的字符串之外其他都是难读的三目操作，这样代码维护是很难的。为了帮自己未来将要遇到坑,把你的复杂的表达式写到模型代码中吧。

除此之外，还建议大家使用null的合并运算符号`??`,如下所示：

```
android:text="@{user.firstName ?? user.userName}"
```


上述代码等价于

```
android:text="@{user.firstName != null ? user.firstName : user.userName}"
```


还有一个很牛逼的功能，你可以在表达式中为要用到的资源直接进行数学运算：

```
android:padding="@{@dim/textPadding + @dim/headerPadding}"
```


这样可以在Java代码中省去很多数据的定义。又多少次你想对布局或者控件的长宽值进行加减操作？这个问题之前是不支持在style中进行操作的。Data Binding解决了这个问题，这简直太牛逼了。

你还可以通过资源方法*[getString](https://developer.android.com/reference/android/content/res/Resources.html#getString%28int,%20java.lang.Object...%29)*、 *[getQuantityString](https://developer.android.com/reference/android/content/res/Resources.html#getQuantityString%28int,%20int,%20java.lang.Object...%29)* 和 *[getFranction](https://developer.android.com/reference/android/content/res/Resources.html#getFraction%28int,%20int,%20int%29)*分别使用字符串，数值以及分数。你只需要向资源传递参数就可以获得：

```
android:text="@{@string/nameFormat(user.firstName, user.lastName)}"
```


# 空指针异常

安卓数据绑定表达式还解决了一个很实用的问题，就是它会制动检测空值。这就意味着你不需要额外去判断变量是否为空：

```
android:text="@{user.firstName ?? user.userName}"
```


如果*user*为空，那么*user.firstName*和*user.userName*也为空，`text`就赋值为空，并且不会抛出*NullPointerException*异常。

这不意味着就不可能抛出空指针异常了，如果你编写了如下表达式

```
android:text="@{com.example.StringUtils.capitalize(user.firstName)}"
```


并且你*StringUtils*中的*capitalize*方法如下：

```java
public static String capitalize(String str) {
    return Character.toUpperCase(str.charAt(0)) + str.substring(1);
}
```


很清楚往*capitalize*方法中传递一个null，必然会抛出*NullPointerException*异常。

# import标签

在上面的例子中，表达式声明的过长，不利于代码的可读性。其实长出来的部分就是方法类包名，其实是可以单独将包名和单独提取出来的：

```xml
<data>
    <variable
        name="user"
        type="com.example.myapp.model.User"/>
    <import
        type="com.example.StringUtils"/>
</data>
```

现在我们的表达式可以这样书写了

```
android:text="@{StringUtils.capitalize(user.firstName)}"
```


# 还有什么呢？

在上面的例子中我们发现表达式就和Java语句一样。如果你认为它能起作用，它就可能会，所以大胆的去尝试吧！

如果你有一些疑问，可以查阅Data Binding Guide中的[Binding Syntax][Binding Syntax]部分


---------------------------------------

> 该系列文章目录：
>   [Android Data Binding系列前传之不再使用findViewById](http://icedcap.github.io/2016/07/26/Binding%E7%B3%BB%E5%88%97%E5%89%8D%E4%BC%A0%E4%B9%8B%E4%B8%8D%E5%86%8D%E4%BD%BF%E7%94%A8findViewById/)
>   [Android Data Binding系列之include标签](http://icedcap.github.io/2016/07/27/Android-Data-Binding%E7%B3%BB%E5%88%97%E4%B9%8Binclude%E6%A0%87%E7%AD%BE/)
>   [Android Data Binding系列之添加变量][android-data-binding-adding-some-variability]
>   Android Data Binding系列之表达你所要表达的
>   [Android Data Binding系列之大事件](http://icedcap.github.io/2016/07/30/android-data-binding-the-big-event/)
  


[Binding Syntax]: https://developer.android.com/topic/libraries/data-binding/index.html#expression_language
[android-data-binding-adding-some-variability]: http://icedcap.github.io/2016/07/28/Android-Data-Binding-Adding-some-variability/