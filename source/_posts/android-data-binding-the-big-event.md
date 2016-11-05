---
title: Android Data Binding系列之大事件
date: 2016-07-30 09:10:00
tags: [android, data binding]
categories: [android]
---


> **原文地址：**[https://medium.com/google-developers/android-data-binding-the-big-event-2697089dd0d7#.1egx4awlx](https://medium.com/google-developers/android-data-binding-the-big-event-2697089dd0d7#.1egx4awlx)

在之前的文章中，我已经探讨了关于[如何删掉*findViewById*][Android Data Binding系列前传之不再使用findViewById],并且在一些情况下[删掉id][Android Data Binding系列之添加变量]。还有一件事是我没有在文章中明确提及的那就是如何处理事件监听器，例如[*View’s OnClickListener*](https://developer.android.com/reference/android/view/View.OnClickListener.html)和[*TextView’s TextWatcher*](https://developer.android.com/reference/android/text/TextWatcher.html)。

安卓数据绑定库提供了三种机制来处理事件监听器（对象监听、方法引用、Lambda表达式），你可以使用其中任何一种机制来服务你的程序。这三种不会使用传统的*onClick*方法，也不会使用反射机制，所以它的效率是非常高的。

<!--more-->

# 监听对象

通常情况下为视图设置监听器都是通过setXxxLinister()或者addXxxLinister()方法。但是有了数据绑定库之后就可以抛弃这两种方法了：

```xml
<View android:onClickListener="@{callbacks.clickListener}" .../>
```


监听器的取得需要一个`getter`或者`public`的字段：

```java
public class Callbacks {
    public View.OnClickListener clickListener;
}
```


当然在数据绑定库之前就有的一个很方便的监听器定义`onClick`：

```xml
<View android:onClick="@{listeners.clickListener}" .../>
```


绑定监听对象常常应用在你的程序已经使用了这些监听器,但是在大多数情况下,你需要使用另外两种机制。

# 方法引用

有了方法引用，你可以hook这个方法来单独作为事件监听方法，对于任何静态的或者实例化的方法只要是参数和返回类型和侦听器相同都可以被hook到。例如：

```xml
<EditText
    android:afterTextChanged="@{callbacks::nameChanged}" .../>
```


*Callbacks*类的*nameChanged*方法声明如下：

```java
public class Callbacks {
    public void nameChanged(Editable editable) {
        //...
    }
}
```


在布局文件标签中要使用"android"命名空间和侦听器相匹配的方法名。

你也可以绑定中做一些逻辑操作，注意这种操作不被推荐使用（降低代码可读性）：

```xml
<EditText android:afterTextChanged=
    "@{user.hasName?callbacks::nameChanged:callbacks::idChanged}"
    .../>
```


在大多数情况下，加入逻辑操作是非常好的一种选择。当你可以将额外的信息传递给方法时也会变得容易得多。所以接下来的这种机制Lambda表达式来改善代码可读性。


# Lambda表达式

你可以提供一个lambda表达式然后把参数传递给你的方法，例如：

```xml
<EditText
 android:afterTextChanged="@{(e)->callbacks.textChanged(user, e)}"
 ... />
```


*textChanged*方法所携带的参数如下：

```java
public class Callbacks {
    public void textChanged(User user, Editable editable) {
        if (user.hasName()) {
            //...
        } else {
            //...
        }
    }
}
```


如果你不需要监听器中的任何参数，你可以使用如下表达式删除他们：

```xml
<EditText
 android:afterTextChanged="@{()->callbacks.textChanged(user)}"
 ... />
```


但是你不能只是删掉布局文件中的参数，还要把对应的*textChanged*方法中的参数删掉，不然编译不会通过的。还要注意一点，不能空缺部分参数要么全部书写要么就全部删除。

在方法引用和Lambda表达式中的执行效率也是不一样的。使用方法引用的表达式会在初始化的时候就会执行，而使用Lambda表达式，会在事件发生时才会去执行。

举个例子，当回调变量还没有被`set`的时候，我们使用方法引用，表达式会评估一个null值并且不会有监听器被设置。而使用Lambda表达式，监听器总是被设置并且当事件发生时才会去评估。正常情况下，这些差别是无关紧要的，但是当有一个返回值的时候，默认的Java值会被返回，例如：

```xml
<View android:onLongClick="@{()->callbacks.longClick()}" …/>
```


当回调为null时，将会返回一个false。你可以使用一个长的表达式来返回你想要返回的值，例如：

```xml
<View android:onLongClick="@{()->callbacks == null ? true : callbacks.longClick()}"…/>
```


你应该尽量避免这种情况的发生，保证你不会有表达式得到null值。

Lambda表达式通常被作为方法引用使用在同一属性上，所以你可以很简单在二者之间切换使用。


# 使用哪个？
三种机制最稳定的是Lambda表达式，它允许你给回调传入不同的参数甚至要比监听器本身提供的参数还要多。

在许多情况下，你的回调会得到和监听方法一样都参数。在这种情况下，方法引用提供了更为简短的表达式写法，这样也提高了代码的可读性。

在你的应用中使用和Android Data Binding库来代替传统事件监听的代码时，一定要准备好监听器对象其次就是把它设置到相应的view上。你可以将监听器作为变量传递到布局文件中，并且把它分配到相应的控件上。


---------------------------------------

> 该系列文章目录：
>   [Android Data Binding系列前传之不再使用findViewById][Android Data Binding系列前传之不再使用findViewById]
>   [Android Data Binding系列之include标签][Android Data Binding系列之include标签]
>   [Android Data Binding系列之添加变量][Android Data Binding系列之添加变量]
>   [Android Data Binding系列之表达你所要表达的][Android Data Binding系列之表达你所要表达的]
>   Android Data Binding系列之大事件



[Android Data Binding系列前传之不再使用findViewById]: http://icedcap.github.io/2016/07/26/Binding%E7%B3%BB%E5%88%97%E5%89%8D%E4%BC%A0%E4%B9%8B%E4%B8%8D%E5%86%8D%E4%BD%BF%E7%94%A8findViewById/
[Android Data Binding系列之include标签]: http://icedcap.github.io/2016/07/27/Android-Data-Binding%E7%B3%BB%E5%88%97%E4%B9%8Binclude%E6%A0%87%E7%AD%BE/
[Android Data Binding系列之添加变量]: http://icedcap.github.io/2016/07/28/Android-Data-Binding-Adding-some-variability/
[Android Data Binding系列之表达你所要表达的]: http://icedcap.github.io/2016/07/29/android-data-binding-express-yourself/