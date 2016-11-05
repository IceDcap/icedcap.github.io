layout: android
title: Android Data Binding系列前传之不再使用findViewById
date: 2016-07-26 22:03:08
tags: [android, data binding]
categories: [android]
---

> 随着Android6.0发布Android Data Binding库已经有一年的时间了，在这一年的时间里版本不断更新升级，也渐渐的被大家使用起来。大多数使用者的反馈是‘一旦使用就根本停不下来的节奏’。关于该库更详细的介绍可以查阅谷歌官方文档，下面链接是介绍Data Binding的视频，感兴趣的童鞋可以看看[data-binding-android-boyar-mount](https://realm.io/cn/news/data-binding-android-boyar-mount/)。
> 
> 今天笔者就该库带来一个系列的译文。首先，是本篇博客，笔者起得名字为前传：不再使用`findViewById` 
> **原文地址：**[https://medium.com/google-developers/no-more-findviewbyid-457457644885#.qiy8zrz52](https://medium.com/google-developers/no-more-findviewbyid-457457644885#.qiy8zrz52)

在使用Android Studio开发Android应用时，很少有人知道有一个减少代码方便开发的特性，它就是Data Binding。使用该特性可以带来很多好处，我将在后续系列文章中介绍。但是我想最最明显的好处就是可以消除带有`findViewById`的代码。

<!--more-->

在项目中写如下代码是不是把你写的都犯颈椎病了呢？

```java
TextView hello = (TextView) findViewById(R.id.hello);
```

其实是有工具可以消除这些重复的代码的（译者注：有一些优秀的第三方库如[ButterKnife](https://github.com/JakeWharton/butterknife)），但是现在谷歌官方发布的AndroidStudio1.5及其以上版本是可以完成消除`findViewById`这些代码的。

首先，你必须重新编辑你应用的build.gradle文件，并且在`android`脚本块中添加如下代码：

```xml
android {
    ...
    dataBinding {
        enabled = true
    }
    ...
}
```

接下来的事情就是修改布局文件了，我们使用`<layout>`标签包裹在布局文件最外一层。和原先代码对比，最外层是`<layout>`标签，而不是`ViewGroup`标签。

```xml
<layout xmlns:android="http://schemas.android.com/apk/res/android"
        xmlns:tools="http://schemas.android.com/tools">
    <RelativeLayout
            android:layout_width="match_parent"
            android:layout_height="match_parent"
            android:paddingLeft="@dimen/activity_horizontal_margin"
            android:paddingRight="@dimen/activity_horizontal_margin"
            android:paddingTop="@dimen/activity_vertical_margin"
            android:paddingBottom="@dimen/activity_vertical_margin"
            tools:context=".MainActivity">

        <TextView
                android:id="@+id/hello"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"/>

    </RelativeLayout>
</layout>
```

**layout**标签会告诉Android Studio这个布局在编译时应采取额外的处理,就是帮XML文件中的所有标签找到（建立）对应的Views并且为接下来对view对象的操作进行注释。如果不在布局文件最外层添加`layout`标签是不会做这一步的操作。因此你可以在新项目中你喜欢的地方使用该标签。

接下来的事情你需要在代码中标明在运行时需要加载的布局文件。由于Eclair版本（Android2.1）没有依赖新框架的变化即使用预加载布局文件方式加载布局。所以该特性只能在Android2.1以上版本奏效。所以在项目中要注意版本变化带来的影响。

对于如下Activity代码

```java
setContentView(R.layout.hello_world);
TextView hello = (TextView) findViewById(R.id.hello);
hello.setText("Hello World"); // for example, but you'd use
                                  // resources, right?
```

可以使用以下代码替代

```java
HelloWorldBinding binding = DataBindingUtil.setContentView(this, R.layout.hello_world);
binding.hello.setText("Hello World"); // you should use resources!
```

在这里你可以看到**HelloWorldBinding**类,它是由hello_world.xml文件生成。并且带有"@+id/hello"的View被分配为final的字段`hello`，并且在Java代码中可以直接使用。这样就可以省去`findViewById`的过程来使用View对象。真是方便啊！

事实证明这种方式要比`findViewById`访问View对象要简单的多，而且速度方面也优秀于`findViewById`。绑定过程是将所有布局中已经分配了id的视图单向传递为final的view字段域。而使用`findViewById`会每次都在视图层级中进行寻找。这也是Data Binding要快于`findViewById`的原因。

还有一件事你将看到，就是变量名变为暗棕色（hello_world.xml变成HelloWorldBinding类），所以如果你将id设为"@+id/hello_text"那么对应的字段名也变为**helloText**。

当使用inflate方法来加载`RecyclerView`, `ViewPager`, 或者其他不能被setting the Activity contents的控件的布局时，你就需要使用生成类型安全的方法来生成类。有几个版本LayoutInflater与之匹配,所以使用一个最适合你的方式，例如：

```java
HelloWorldBinding binding = HelloWorldBinding.inflate(getLayoutInflater(), container, attachToContainer);
```

如果你不想依附ViewGroup容器来inflate视图，而又不得不要获取inflate的视图层级。你就可以使用getRoot()方法来绑定

```java
linearLayout.addView(binding.getRoot());
```

现在，你可能还在疑惑，假如我有不同view配置的布局文件将怎么处理呢？布局预处理和运行时视图加载策略会关注这些问题：为生成的类添加视图IDs（字段名）并且在它们还没被inflated的时候设为null。

很神奇，不是吗？该库最好的一点就是没有使用反射机制或者任何其他在运行时使用的高成本技术。它是非常容易应用在当前应用中的，并且让你的代码书写更简单，开发效率更高，布局加载更敏捷。



---------------------------------------

> 该系列文章目录：
>   Android Data Binding系列前传之不再使用findViewById
>   [Android Data Binding系列之include标签](http://icedcap.github.io/2016/07/27/Android-Data-Binding%E7%B3%BB%E5%88%97%E4%B9%8Binclude%E6%A0%87%E7%AD%BE/)
>   [Android Data Binding系列之添加变量](http://icedcap.github.io/2016/07/28/Android-Data-Binding-Adding-some-variability/)
>   [Android Data Binding系列之表达你所要表达的](http://icedcap.github.io/2016/07/28/Android-Data-Binding-Adding-some-variability/)
>   [Android Data Binding系列之大事件](http://icedcap.github.io/2016/07/30/android-data-binding-the-big-event/)
