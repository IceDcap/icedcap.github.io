---
title: Android Data Binding系列之添加变量
date: 2016-07-28 20:06:18
tags: [android, data binding]
categories: [android]
---

>**原文地址：**[https://medium.com/google-developers/android-data-binding-adding-some-variability-1fe001b3abcc#.ko5u93ul6](https://medium.com/google-developers/android-data-binding-adding-some-variability-1fe001b3abcc#.ko5u93ul6)

# 不再需要View id
你是否曾经看到其他人的布局会有一些疑问，他们布局中的数据是在哪里`set`和`get`的呢?或许你会想[删掉`findViewById`][eliminating-findViewById]是做出了伟大的第一步，但是我们看到仍然存在大量的样板代码。其实Android Data Binding还可以进一步减少代码量。

<!--more-->

# 使用View Holder模式
让我们先讨论在应用中展示用户信息的情况。上篇[博文][Android Data Binding系列之include标签]中,我已经展示了使用Android Studio生成View Holder模式下的类文件，并且使用他们为视图设置数据的过程：

```xml
user_info.xml
<?xml version="1.0" encoding="utf-8"?>
<layout xmlns:android="http://schemas.android.com/apk/res/android">
    <LinearLayout
            android:orientation="vertical"
            android:layout_width="match_parent"
            android:layout_height="match_parent">
        <ImageView
                android:id="@+id/userImage"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"/>
        <TextView
                android:id="@+id/userFirstName"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"/>

        <TextView
                android:id="@+id/userLastName"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"/>
    </LinearLayout>
</layout>
```


接下来，为视图设置数据
```java
private void setUser(User user, ViewGroup root) {
    UserInfoBinding binding = UserInfoBinding.inflate(getLayoutInflater(), root, true);
    binding.userFirstName.setText(user.firstName);
    binding.userLastName.setText(user.lastName);
    binding.userImage.setImageBitmap(user.image);
}
```

这种模式看上去要比使用`findViewById`简洁得多，但是依旧存在向上述代码块中的样板代码。幸运的是，Data Binding为我们提供了表达式（包含Lambda表达式）来摆脱这些样板代码，该表达式声明在布局文件中。

# 在布局中使用表达式

首先，你要在layout标签下添加data标签来关联表达式中相应的变量。接下来，你就可以使用表达式为每个控件定义相应的属性了。如下：

```xml
<?xml version="1.0" encoding="utf-8"?>
<layout xmlns:android="http://schemas.android.com/apk/res/android">
    <data>
        <variable
            name="user"
            type="com.example.myapp.model.User"/>
    </data>
    <LinearLayout
            android:orientation="vertical"
            android:layout_width="match_parent"
            android:layout_height="match_parent">
        <ImageView
                android:src="@{user.image}"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"/>
        <TextView
                android:text="@{user.firstName}"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"/>

        <TextView
                android:text="@{user.lastName}"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"/>
    </LinearLayout>
</layout>
```


在标签上为控件绑定的表达式需要以`@{...}`格式来定义。上述代码块中的表达式直接为相应的控件分配了用户`image` `firstName`和`lastName`的资源和文本。所以在这种情况下你就省去写样板代码的时间了，是不是很愉快?但是我们依然不清楚是使用了哪个`User`，所以你需要在代码中分配它：

```java
private void setUser(User user, ViewGroup root) {
    UserInfoBinding binding = UserInfoBinding.inflate(getLayoutInflater(), root, true);
    binding.setUser(user);
}
```


很简单，不是吗?

你可以看到在上述布局文件中已经完全摆脱控件id的声明，而对于View Holder模式依然需要id来尝试生成对应的类。使用表达式会将数据直接绑定到了布局中的每个控件上，因此就不再需要访问相应的view对象。也就不再需要id来生成相应的view holder类。

在使用Data Binding库之前，我们经常因为控件数据的设定时的数据为空而导致应用崩溃。然而Data Binding库之后就再也不用担心这种情况发生了。数据绑定表达式会在布局中检查每一个控件控价是否存在，所以如果不存在就不会有代码去执行更新。

使用表达式不代表就弃用View Holder模式。很多情况下，依然要使用ViewHolder模式，例如，当你想直接访问view holder对象以及它的一些字段时。


# include标签的使用

使用`include`标签的情况下是否依然生效呢？答案是必然的。就像[View Holder模式能应用在`include`标签][Android Data Binding系列之include标签]下一样，表达式也是可以的。例如，有些`TextView`控件单独声明在另外一个布局中，下面我们使用`include`来包含它：

```xml
user_name.xml
<?xml version="1.0" encoding="utf-8"?>
<layout xmlns:android="http://schemas.android.com/apk/res/android">
    <data>
        <variable
                name="user"
                type="com.example.myapp.model.User"/>
    </data>

    <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="match_parent"
            android:orientation="horizontal">
        <TextView
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:text="@{user.firstName}"/>

        <TextView
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:text="@{user.lastName}"/>
    </LinearLayout>
</layout>
```

user变量可以分配在布局以外的地方，如下。

```xml
<?xml version="1.0" encoding="utf-8"?>
<layout xmlns:android="http://schemas.android.com/apk/res/android"
        xmlns:app="http://schemas.android.com/apk/res-auto">
    <data>
        <variable
                name="user"
                type="com.example.myapp.model.User"/>
    </data>
    <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="match_parent"
            android:orientation="vertical">
        <ImageView
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:src="@{user.image}"/>
        <include
                layout="@layout/user_name"
                app:user="@{user}"/>
    </LinearLayout>
</layout>
```


不论何时，user变量都会被分配（*binding.setUser(...)*）,被包含的布局中的user变量也会被得到，因为在宿主布局中使用*app:user="@{user}"*。再次注意，因为直接访问被包含布局中的views是不必要的，所有在被包含的布局中定义id也是不必要的。


# 展望

接下来，我将继续介绍Android Data Binding在轻量数据上的绑定,这样在应用到你的程序中会带来很多好处。或许你之前看到社区的一些评论在抱怨安卓代码丑陋却一直没有好的办法改善。如果你想得到更全面了解，先看看谷歌官方指南[Data Binding Guide][Data-Binding-Guide]

[eliminating-findViewById]: http://icedcap.github.io/2016/07/26/Binding%E7%B3%BB%E5%88%97%E5%89%8D%E4%BC%A0%E4%B9%8B%E4%B8%8D%E5%86%8D%E4%BD%BF%E7%94%A8findViewById/
[Android Data Binding系列之include标签]: http://icedcap.github.io/2016/07/27/Android-Data-Binding%E7%B3%BB%E5%88%97%E4%B9%8Binclude%E6%A0%87%E7%AD%BE/
[Data-Binding-Guide]: https://developer.android.com/topic/libraries/data-binding/index.html


---------------------------------------

> 该系列文章目录：
>   [Android Data Binding系列前传之不再使用findViewById](http://icedcap.github.io/2016/07/26/Binding%E7%B3%BB%E5%88%97%E5%89%8D%E4%BC%A0%E4%B9%8B%E4%B8%8D%E5%86%8D%E4%BD%BF%E7%94%A8findViewById/)
>   [Android Data Binding系列之include标签](http://icedcap.github.io/2016/07/27/Android-Data-Binding%E7%B3%BB%E5%88%97%E4%B9%8Binclude%E6%A0%87%E7%AD%BE/)
>   Android Data Binding系列之添加变量
>   [Android Data Binding系列之表达你所要表达的](http://icedcap.github.io/2016/07/28/Android-Data-Binding-Adding-some-variability/)
>   [Android Data Binding系列之大事件](http://icedcap.github.io/2016/07/30/android-data-binding-the-big-event/)