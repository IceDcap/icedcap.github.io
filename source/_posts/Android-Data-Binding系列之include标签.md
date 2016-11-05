---
title: Android Data Binding系列之include标签
date: 2016-07-27 22:05:30
tags: [android, data binding]
categories: [android]
---

> **原文地址：**[https://medium.com/google-developers/android-data-binding-that-include-thing-1c8791dd6038#.ab89v8uka](https://medium.com/google-developers/android-data-binding-that-include-thing-1c8791dd6038#.ab89v8uka)

在上一篇博文中你已经看到了在AndroidStudio1.5或者更高版本上使用Data Binding来代替`findViewById`是多么的方便，其实它的原理是使用View Holder模式，类似于ListView中的ViewHolder。[如下描述](https://developer.android.com/training/improving-layouts/smooth-scrolling.html)

<!--more-->

```
Making ListView Scrolling Smooth

The key to a smoothly scrolling ListView is to keep the application’s main 
thread (the UI thread) free from heavy processing. Ensure you do any disk 
access, network access, or SQL access in a separate thread. To test the status 
of your app, you can enable StrictMode.

```

上篇文章中我已经展示了在AndroidStudio中怎样将单个布局文件生成一个类来充当View Holder角色的。但是对于多个布局，尤其使用`<include>`标签后包括另外一个布局的情况下，Data Binding是否还支持呢？如果支持它又该如何操作呢？

事实上，Data Binding是支持的，但是每一个包含的布局将生成不同的类。下面是一个例子

```xml
hello_world.xml
<layout xmlns:android="http://schemas.android.com/apk/res/android">
    <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="match_parent"
            android:orientation="vertical">

        <TextView
                android:id="@+id/hello"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"/>
        <include
                android:id="@+id/included"
                layout="@layout/included_layout"/>
    </LinearLayout>
</layout>


included_layout.xml
<?xml version="1.0" encoding="utf-8"?>
<layout xmlns:android="http://schemas.android.com/apk/res/android">
    <TextView
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:id="@+id/world"/>
</layout>
```


如下你可以使用两个`TextView`对象
```java
HelloWorldBinding binding = HelloWorldBinding.inflate(getLayoutInflater());
binding.hello.setText("Hello");
binding.included.world.setText("World");
```


被包含的布局文件也和普通布局文件遵循一样的规则：需要为`<include>`标签添加一个ID这样才能在类中生成对应的字段。被包含的布局也已经生成了自己所对应的类和相应的字段。所有已经定义了ID的控件在不同布局文件中会共享，这样也有利于开发者进行识别。例如，如果你包含同一个布局两次时：

```xml
<layout xmlns:android="http://schemas.android.com/apk/res/android">
    <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="match_parent"
            android:orientation="vertical">

        <TextView
                android:id="@+id/hello"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"/>
        <include
                android:id="@+id/world1"
                layout="@layout/included_layout"/>
        <include
                android:id="@+id/world2"
                layout="@layout/included_layout"/>
    </LinearLayout>
</layout>
```


两个`world`的布局所对应的类也很容易得到：

```java
HelloWorldBinding binding = HelloWorldBinding.inflate(getLayoutInflater());
binding.hello.setText("Hello");
binding.world1.world.setText("First World");
binding.world2.world.setText("Second World");
```


记得要给`<include>`标签一个ID，否则在类中将不会为他分配字段。当然也要记得为`<include>`的布局中的标签设置ID。这样，在对程序预编译的时候就会为该视图分配对应的类和字段。

如果你仔细观察生成的类文件，你会感觉他们在任何时候都是使用的同一个类。例如，如果你定义了一个*goodbye_world.xml*布局并且其中包含了*included_layout.xml*布局，那么它看上去像是系统只会为他生成一个类。（译者注：这里看似是一个类是在使用上给人的感觉，但是本质上系统会为不同的布局文件分别生成对应的类）


---------------------------------------

> 该系列文章目录：
>   [Android Data Binding系列前传之不再使用findViewById](http://icedcap.github.io/2016/07/26/Binding%E7%B3%BB%E5%88%97%E5%89%8D%E4%BC%A0%E4%B9%8B%E4%B8%8D%E5%86%8D%E4%BD%BF%E7%94%A8findViewById/)
>   Android Data Binding系列之include标签
>   [Android Data Binding系列之添加变量](http://icedcap.github.io/2016/07/28/Android-Data-Binding-Adding-some-variability/)
>   [Android Data Binding系列之表达你所要表达的](http://icedcap.github.io/2016/07/28/Android-Data-Binding-Adding-some-variability/)
>   [Android Data Binding系列之大事件](http://icedcap.github.io/2016/07/30/android-data-binding-the-big-event/)
