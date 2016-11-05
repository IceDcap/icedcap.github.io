安卓动画框架把动画分为三类，分别是View动画、帧动画、属性动画

View动画
========
View动画种类
--------

|名称|标签|子类|效果|
|：--|：--|：--|：--|
|平移动画|`<translate>`|`TranslateAnimation`|移动View|
|缩放动画|`<scale>`|`ScaleAnimation`|方法或者缩小View|
|旋转动画|`<rotate>`|`RotateAnimation`|旋转View|
|透明度动画|`<alpha>`|`AlphaAnimation`|改变View的透明度|

View动画的使用可以通过xml或者java代码的形式实现：
XML形式：将这个文件保存为`res/anim/filename.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<set xmlns:android="http://schemas.android.com/apk/res/android"
    android:interpolator="@[package:]anim/interpolator_resource"
    android:shareInterpolator=["true" | "false"] >
    <alpha
        android:fromAlpha="float"
        android:toAlpha="float" />
    <scale
        android:fromXScale="float"
        android:toXScale="float"
        android:fromYScale="float"
        android:toYScale="float"
        android:pivotX="float"
        android:pivotY="float" />
    <translate
        android:fromXDelta="float"
        android:toXDelta="float"
        android:fromYDelta="float"
        android:toYDelta="float" />
    <rotate
        android:fromDegrees="float"
        android:toDegrees="float"
        android:pivotX="float"
        android:pivotY="float" />
    <set>
        ...
    </set>
</set>
```

自定义View动画
----------
源码的ApiDemos，Rotate3dAnimation。

帧动画
-------
帧动画是顺序播放一组预先定义好的图片，类似于电影播放。框架提供了一个类`AnimationDrawable`来时用帧动画。通过XML来定义一个`AnimationDrawable`：
```xml
<?xml version="1.0" encoding="utf-8"?>
<animation-list xmlns:android="http://schemas.android.com/apk/res/android"
    android:oneshot="false">
    <item android:drawable="@drawable/rocket_thrust1" android:duration="200" />
    <item android:drawable="@drawable/rocket_thrust2" android:duration="200" />
    <item android:drawable="@drawable/rocket_thrust3" android:duration="200" />
</animation-list>
```

将上述的`Drawable`作为View背景并通过`Drawable`来播放动画即可：
```java
ImageView rocketImage = (ImageView) findViewById(R.id.rocket_image);
rocketImage.setBackgroundResource(R.drawable.rocket_thrust);

rocketAnimation = (AnimationDrawable) rocketImage.getBackground();
rocketAnimation.start();
```

帧动画的使用比较简单，但是比较容易引起OOM，所以在使用的时候应该尽量避免使用过多尺寸较大的图片。

View动画的特殊使用场景
===========

View动画除了上述提到四种动画表现形式外，它还可以在一些其他场景中使用。例如，在`ViewGroup`中控制子View的出场方式，在Activity中实现不同Activity切换时的效果。

LayoutAnimation
--------------
该类作用于`ViewGroup`

```xml

```

Activity的切换效果
-----------------

方法使用`overridePendingTransition(int enter, int exit)`,该方法必须在`startActivity(intent)` 或者`finish()`之后调用才能生效。

Fragment的切换效果
-----------------
`FragmentTransaction`类中的`setCustomAnimations()`方法来添加切换动画。这个切换动画只能使用View动画，不能使用属性动画，因为它是API11引入的。

属性动画
================
属性动画是API11引入的，和View动画不同，它的作用对象进行了扩展，属性动画可以应用于任何对象，甚至可以没有对象。此外，属性动画像比较于View动画的效果也加强了，不仅仅只支持View动画的四种动画效果，它可以实行多姿多彩形形色色的动画效果。

属性动画主要包括`ValueAnimator` `ObjectAnimator` 和 `AnimatorSet`三个类。

使用属性动画
-----------
属性动画可以应用于任何的对象不仅仅只针对View，默认情况下，属性动画的时间间隔是300ms，默认帧率是10ms/帧。其实现效果是：在一个时间间隔内完成队形从一个属性值到另外一个属性值的改变过程。

使用方法：


理解插值器和估值器
--------------
`TimeInterpolator`是时间插值器，根据时间流逝的百分比来计算出当前属性值改变的百分比。系统提供了几个插值器比如`LinearInterpolator` `AccelerateDecelerateInterator`等。
`TypeEvaluator`类型估值器，根据当前属性的改变的百分比来计算改变后的属性值。系统预置了有`IntEvaluator` `FloatEvaluator`和`ArgbEvaluator`


属性动画的监听器
--------------
有两个接口用于监听属性动画，分别是`AnimatorUpdateListener`和`AnimatorListener`


对任意属性做动画
---------

属性动画的工作原理
-------------

使用动画注意事项
=============

> OOM问题
> 内存泄露问题 （无限循环的动画需要及时停止）
> 兼容性问题
> View动画问题
> 不要使用px
> 动画元素的交互
> 硬件加速 （建议开启）













