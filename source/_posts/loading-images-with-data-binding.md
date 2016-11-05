---
title: Android Data Binding高级系列之图片加载
date: 2016-08-03 21:38:02
tags: [android, data binding]
categories: [android]
---

有没有尝试安卓数据绑定库？知道怎么使用它加载图片吗？本篇文章将带来两个例子展示如何加载图片。

<!--more-->
> [@ivacf](https://github.com/ivacf)
> **原文地址：**[https://medium.com/android-news/loading-images-with-data-binding-and-picasso-555dad683fdc#.82ohesp2p](https://medium.com/android-news/loading-images-with-data-binding-and-picasso-555dad683fdc#.82ohesp2p)
> **源码地址：**[https://github.com/IceDcap/LoadImageWithDataBinding](https://github.com/IceDcap/LoadImageWithDataBinding)

最近在忙于[Archi](https://github.com/ivacf/archi)项目中的MVVM应用。该应用会下载GitHubAPI上图片并且通过安卓数据绑定库加载到ImageView控件上。本篇博文我将两种加载图片的方法。

下面例子中会使用到Square公司的[Picasso](https://github.com/square/picasso)库，当然你也可以使用其他优秀的图片加载库。

# 使用@BindingAdapter

首先第一种解决方案是使用注解[BindingAdapter](https://developer.android.com/reference/android/databinding/BindingAdapter.html)来创建自定义的xml属性。当该属性以正确的数据类型被设置在布局文件中时，data binding框架就会触发以该注释的方法来执行。我们为该自定义的属性起名为imageUrl其参数类型为String。需要注意的是注解方法必须为static的。

```java

public class ProfileViewModel {

    public String getImageUrl() {
        // The URL will usually come from a model (i.e Profile)
        return "http://cdn.meme.am/instances/60677654.jpg";
    }

    @BindingAdapter({"bind:imageUrl"})
    public static void loadImage(ImageView view, String imageUrl) {
        Picasso.with(view.getContext())
                .load(imageUrl)
                .placeholder(R.drawable.placeholder)
                .into(view);
    }
}
```


当view 模型准备就绪时，就可以创建布局文件并且使用imageUrl属性，自定义属性需要使用相应的命名空间。

```xml

<layout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto" >
    <data>
        <variable
            name="viewModel"
            type="uk.ivanc.imagedatabinding.ProfileViewModel" />
    </data>
    <RelativeLayout
        android:layout_width="match_parent"
        android:layout_height="match_parent">
        <ImageView
            android:layout_width="200dp"
            android:layout_height="200dp"
            app:imageUrl="@{viewModel.imageUrl}" />
    </RelativeLayout>
</layout>
```


最后一步在Activity设置绑定对象

```java
protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    ProfileActivityBinding binding =
            DataBindingUtil.setContentView(this, R.layout.profile_activity);
    binding.setViewModel(new ProfileViewModel(this));
}
```


# ObservableField 和 自定义Picasso的Target
这种方法会加大代码量，但是它的效率非常高。该想法是利用[ObservableField](https://developer.android.com/reference/android/databinding/ObservableField.html)泛型类，使用Drawable对象作为成员类型，并且使用自定义Picasso的[Target](https://square.github.io/picasso/javadoc/com/squareup/picasso/Target.html)共同完成。ObservableField包装Drawable成员，一旦Drawable发生变化时就会通知布局进行刷新。

```java
public class ProfileViewModel {
    // The URL will usually come from a model (i.e Profile)
    static final String IMAGE_URL = "http://cdn.meme.am/instances/60677654.jpg";
    public ObservableField<Drawable> profileImage;
    private BindableFieldTarget bindableFieldTarget;

    public ProfileViewModel(Context context) {
        profileImage = new ObservableField<>();
        // Picasso keeps a weak reference to the target so it needs to be stored in a field
        bindableFieldTarget = new BindableFieldTarget(profileImage, context.getResources());
        Picasso.with(context)
                .load(IMAGE_URL)
                .placeholder(R.drawable.placeholder)
                .into(bindableFieldTarget);
    }

    public class BindableFieldTarget implements Target {

        private ObservableField<Drawable> observableField;
        private Resources resources;

        public BindableFieldTarget(ObservableField<Drawable> observableField, Resources resources) {
            this.observableField = observableField;
            this.resources = resources;
        }

        @Override
        public void onBitmapLoaded(Bitmap bitmap, Picasso.LoadedFrom from) {
            observableField.set(new BitmapDrawable(resources, bitmap));
        }

        @Override
        public void onBitmapFailed(Drawable errorDrawable) {
            observableField.set(errorDrawable);
        }

        @Override
        public void onPrepareLoad(Drawable placeHolderDrawable) {
            observableField.set(placeHolderDrawable);
        }
    }
}
```


BindableFieldTarged类只需要定义一次就可以在整个项目中使用。

在布局文件中我们需要在ImageView控件上指定ProfileViewModel对象的变量。

```xml
<layout xmlns:android="http://schemas.android.com/apk/res/android">
    <data>
        <variable
            name="viewModel"
            type="uk.ivanc.imagedatabinding.ProfileViewModel" />
    </data>
    <RelativeLayout
        android:layout_width="match_parent"
        android:layout_height="match_parent">
        <ImageView
            android:layout_width="200dp"
            android:layout_height="200dp"
            android:src="@{viewModel.profileImage}"/>
    </RelativeLayout>
</layout>
```

最后，和之前一样，在Activity设置绑定。

好了，就是这些了。两种方法都能实现图片的加载。但是我还是推荐你使用第一个，因为它的代码量很少，而且可读性也很好。
