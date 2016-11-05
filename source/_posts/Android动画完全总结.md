---
title: Android动画完全总结
date: 2016-06-21 22:09:04
tags: [android, animation, animator]
categories: [android]
---

Android动画分为三种：View动画、帧动画、属性动画。View动画主要通过对场景的对象进行不断的做平移、缩放、旋转和透明度变化从而产生动画的效果。帧动画通过顺序播放一组图片集达到动画效果，如果图片尺寸过大或者加载数量很大容易导致OOM。属性动画是API11引进的新特性，可以说它是最万能的动画框架，在低版本上可以使用兼容库[NineOldAndroids](https://github.com/JakeWharton/NineOldAndroids/)。

<!--more-->

## View动画
View动画的使用很简单，可以通过下表提供的类和XML标签来表示：

|名称|标签|子类|效果|
|:--|:--|:--|:--|
|平移动画|`<translate>`|`TranslateAnimation`|移动View|
|缩放动画|`<scale>`|`ScaleAnimation`|放大或者缩小View|
|旋转动画|`<rotate>`|`RotateAnimation`|旋转View|
|透明度动画|`<alpha>`|`AlphaAnimation`|改变View的透明度|

<p style="text-align: center;">
    <img src="pic/anim/animation_classes.png">
</p>
上图是安卓Framework为我们提供animation包(*frameworks/base/core/java/android/view/animation/..*)，可以看到除了表中提到的四种动画效果外大部分都是以Interpolator为后缀的插值器类

View的四种动画效果分别对应着四个类和XML中的四个标签。谷歌官方建议我们使用XML的形式完成View动画。
首先在`res/anim/filename.xml`创建动画的XML文件。下面`xml`代码是View动画固定语法。
```xml
<?xml version="1.0" encoding="utf-8"?>
<set xmlns:android="http://schemas.android.com/apk/res/android"
    android:interpolator="@[package:]anim/interpolator_resource"
    android:shareInterpolator=["true"|"false"]>
    <alpha
        android:formAlpha="float"
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
        android:fromDegrees="flaot"
        android:toDegrees="float"
        android:pivotX="float"
        android:pivotY="float" />
    <set>
        ...
    </set>
</set>
```

通过标签`<set>`可以看出View动画可以是单个动画也可以是一系列的动画集合组成。`<set>`标签对于`AnimationSet`类，它可以包含若干个动画，或者又可以包含其它的`<set>`集合。

- `<set>`集合有两个属性：
**android:interpolator** ----作用于动画的插值器，控制着动画推进的速度，后续详解。
**android:shareInterpolator** ----表示集合里的动画是否与集合公用一个插值器，如果不指定，那么集合里的动画就要单独指定或者使用默认的插值器

- `<alpha>`表示透明度动画，对应`AlphaAnimation`类，它可以改变View透明度，属性如下：
**android:fromAlpha**  ----Float,透明度起始值，从0.0f~1.0f 分别代表不透明到透明的偏移值
**android:toAlpha**  ----Float,透明度结束值，从0.0f~1.0f 分别代表不透明到透明的偏移值

- `<scale>`表示缩放动画，对应`ScaleAnimation`类，它的属性如下：
**android:fromXScale**  ----Float,水平方向缩放起始值，1.0表示没有变化， 比如0.5
**android:toXScale**  ---- Float,水平方向缩放结束值，1.0表示没有变化， 比如 1.2
**android:fromYScale**  ----Float,竖直方向缩放起始值，1.0表示没有变化
**android:toYScale**  ----Float,竖直方向缩放结束值，1.0表示没有变化
**android:pivotX**   ----缩放轴点x的坐标
**android:pivotY**  ----缩放轴点y的坐标

- `<translate>`表示平移动画，对应`TranslateAnimation`类，它可以使View在水平或者竖直方向上进行平移动画。它的属性如下：
**android:fromXDelta** ----x的起始值，比如0、0%、0%p
**android:toXDelta** ----x的结束值，比如100、100%、100%p
**android:fromYDelta** ----y的起始值
**android:toYDelta** ----y的结束值
> -100%~100%表示相对自己的百分值 
 -100%p~100%p表示相对它的父亲的百分值   
 没有任何后缀的float值，表示一个绝对值

- `<rotate>`表示旋转动画，对应`RotateAnimation`类，它可以使View具有旋转的动画效果，它的属性如下：
**android:fromDegrees** ----开始角度，比如0
**android:toDegrees**   ----结束角度，比如180
**android:pivotX**   ----旋转轴点x的坐标
**android:pivotY**  ----旋转轴点y的坐标

除了以上属性外，还有一些常用的属性：
> **android:duration** ----动画持续的事件
 **android:fillAfter**  ----动画结束以后View是否停留在结束位置，true表示View停留在结束位置，false则不停留。

下面是一个实际的例子
```xml
<set android:shareInterpolator="false">
    <scale
        android:interpolator="@android:anim/accelerate_decelerate_interpolator"
        android:fromXScale="1.0"
        android:toXScale="1.4"
        android:fromYScale="1.0"
        android:toYScale="0.6"
        android:pivotX="50%"
        android:pivotY="50%"
        android:fillAfter="false"
        android:duration="700" />
    <set android:interpolator="@android:anim/decelerate_interpolator">
        <scale
           android:fromXScale="1.4"
           android:toXScale="0.0"
           android:fromYScale="0.6"
           android:toYScale="0.0"
           android:pivotX="50%"
           android:pivotY="50%"
           android:startOffset="700"
           android:duration="400"
           android:fillBefore="false" />
        <rotate
           android:fromDegrees="0"
           android:toDegrees="-45"
           android:toYScale="0.0"
           android:pivotX="50%"
           android:pivotY="50%"
           android:startOffset="700"
           android:duration="400" />
    </set>
</set>
```
在java代码中也很简单
```java
View target = findViewById(R.id.animTarget);
Animation animation = AnimationUtils.loadAnimation(this, R.anim.anim_target);
target.startAnimation(animation);
```
<p style="text-align:center;">
    <img src="pic/anim/xiaoguo1.gif">
</p>

除了在XML文件中定义View动画外，还可以通过代码创建View动画对象来实现。例如
```java
AlphaAnimation alphaAnimation = new AlphaAnimation(0, 1);
alphaAnimation.setDuration(300);
mTarget.startAnimation(alphaAnimation);
```
上述代码会产生由透明到不透明的动画效果，使用java代码也很简单，如果监控整个动画过程可以使用`AnimationListener`接口来实现
```java
    /**
     * <p>An animation listener receives notifications from an animation.
     * Notifications indicate animation related events, such as the end or the
     * repetition of the animation.</p>
     */
    public static interface AnimationListener {
        /**
         * <p>Notifies the start of the animation.</p>
         *
         * @param animation The started animation.
         */
        void onAnimationStart(Animation animation);

        /**
         * <p>Notifies the end of the animation. This callback is not invoked
         * for animations with repeat count set to INFINITE.</p>
         *
         * @param animation The animation which reached its end.
         */
        void onAnimationEnd(Animation animation);

        /**
         * <p>Notifies the repetition of the animation.</p>
         *
         * @param animation The animation which was repeated.
         */
        void onAnimationRepeat(Animation animation);
    }
```

## 帧动画
帧动画的原理很简单，框架使用`AnimationDrawable`类应用帧动画，它的使用也是通过XML定义一组可播放飞图片集，在java代码中应用与目标View。例如定义res/drawable/frame_animation.xml文件
```xml
<?xml version="1.0" encoding="utf-8"?>
<animation-list xmlns:android="http://schemas.android.com/apk/res/android"
    android:oneshot="false">
    <item android:drawable="@drawable/pic1" android:durable="300"/>
    <item android:drawable="@drawable/pic2" android:durable="300"/>
    <item android:drawable="@drawable/pic3" android:durable="300"/>
</animation-list>
```

接下来，在java代码中作为Drawable使用
```java
View target = findViewById(R.id.animTarget);
target.setBackgroundResource(R.drawable.frame_animation);
AnimationDrawable drawable = (AnimationDrawable)traget.getBackground();
drawable.start();
```
**注意：** 使用帧动画一定减少图片加载数量和图片的尺寸，从而避免OOM。

## View动画的应用
View动画不仅仅可以作用在View对象上，也可以应用在Activity、Fragment和ViewGroup上。

### Activity之间的转场动画
Activity之间应用最多的效果就是左进左出，右进右出的转场效果。通常在调用`startActivity`和`finish`方法后使用`overridePendingTransition`方法。
```java
    //启动Activity
    startActivity(new Intent(this, AnimActivity.class));
    overridePendingTransition(R.anim.anim_left_in, R.anim.anim_left_out);

    //退出Activity
    @Override
    public void finish() {
        super.finish();
        overridePendingTransition(R.anim.anim_right_in, R.anim.anim_right_out);
    }
```
res/anim/anim_left_out.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<set xmlns:android="http://schemas.android.com/apk/res/android"
     android:duration="300">
    <translate android:fromXDelta="0%"
               android:fromYDelta="0%"
               android:toXDelta="-100%"
               android:toYDelta="0%"/>

</set>
```
res/anim/anim_left_in.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<set xmlns:android="http://schemas.android.com/apk/res/android"
     android:duration="300">
    <translate android:fromXDelta="100%"
               android:fromYDelta="0%"
               android:toXDelta="0%"
               android:toYDelta="0%"/>
</set>
```
res/anim/anim_right_in.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<set xmlns:android="http://schemas.android.com/apk/res/android"
     android:duration="300">
    <translate android:fromXDelta="-100%"
               android:fromYDelta="0%"
               android:toXDelta="0%"
               android:toYDelta="0%"/>
</set>
```
res/anim/anim_right_out.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<set xmlns:android="http://schemas.android.com/apk/res/android"
     android:duration="300">
    <translate android:fromXDelta="0%"
               android:fromYDelta="0%"
               android:toXDelta="100%"
               android:toYDelta="0%"/>
</set>
```

对于Fragment来说，它是3.0引入的为了兼容性使用support-v4包可以使用`FragmentTransaction#setCustomAnimations()`方法进行切换效果的设置。

### 应用于ViewGroup
在编写布局文件的时候可以发现布局标签中有一个`android:layoutAnimation`属性，如下图所示
<p style="text-align: center;">
    <img src="pic/anim/layoutAnimation.png">
</p>
根据属性名字可以看出肯定是和View动画相关，我们为其设置一个anim的xml文件，具体看看是如何工作的。
首先写了一个布局文件并将布局标签设置layoutAnimation属性
```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
              android:layout_width="match_parent"
              android:layout_height="match_parent"
              android:background="#84CCA0BB"
              android:layoutAnimation="@anim/anim_layout"
              android:orientation="vertical">
    <TextView
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_margin="4dp"
        android:gravity="center"
        android:text="@string/app_name"/>
    ...
</LinearLayout>
```

再看一下anim_layout.xml文件
```xml
<?xml version="1.0" encoding="utf-8"?>
<layoutAnimation xmlns:android="http://schemas.android.com/apk/res/android"
    android:animation="@anim/anim_right_in"
    android:animationOrder="normal"
    android:delay="0.5"
    android:interpolator="@android:interpolator/linear">

</layoutAnimation>
```
对于`<layoutAnimation>`的属性如下图所示：
<p style="text-align: center;">
    <img src="pic/anim/layotAnimationProperty.png">
</p>

- **android:animationOrder**属性是设置布局中的子View播放循序分别是`normal` `random`和`reverse`
- **android:delay** 子元素之间播放的延迟，比如子元素动画时间周期为300ms，那么0.5表示每个子元素都要延迟150ms，第一个子元素延迟150ms第二个元素延迟300ms，以此类推...达到所有子元素出场有一种顿挫感，如下图的效果：
<p style="text-align:center;">
    <img src="pic/anim/layoutAnim_xiaoguo.gif">
</p>

从上述动画效果可以看出`layoutAnimation`将作用于该布局下的所有子View。它经常使用在`ListView`控件中用于item的出场方式的酷炫效果展示。

在animation包中(*frameworks/base/core/java/android/view/animation/..*)我们可以看到`LayoutAnimationController`类，从名字上看它就是`layoutAnimation`的代码实现部分。我们可以通过如下java代码实现：
```java
ListView listview = (ListView)findViewById(R.id.listView);
Animation animation = AnimationUtil.loadAnimation(this, R.id.anim_right_in);
LayoutAnimationController controller = new LayoutAnimationController(animation);
controller.setDelay(0.5f);
controller.setOrder(LayoutAnimationController.ORDER_NORMAL);
listview.setLayoutAnimation(controller);
```

## 属性动画
属性动画是3.0引入的，所以要想实现兼容性可以使用[NineOldAndroids](https://github.com/JakeWharton/NineOldAndroids/)。属性动画的引入大大完善了安卓对于复杂动画效果的把控。它和View动画不同，它直接作用于属性，而属性可以是任何对象的属性，甚至可以是空对象。无论该目标对象是否在窗口上进行绘制，属性动画会在一个指定的时间里改变属性的值（目标对象的字段<成员变量>），所以要使用自定义动画的时候就可以通过改变指定属性值来操作动画。安卓Framework为属性动画单独写了一个包位于*frameworks/base/core/java/android/animation/..*如下图所示：
<p style="text-align: center;">
    <img src="pic/anim/animator_classes.png">
</p>

`Animator`是属性动画的基类，它声明了一些属性动画的特征；`ValueAnimator`类继承自`Animator`并维护着一个唯一的`AnimationHandler``Runnable`用于调度`Animator`，除此之外还要维护属性动画中重要的概念插值器和估值器；`ObjectAnimator`是一个*final*类并且继承自`ValueAnimator`，该类将利用目标对象以及它的属性进行每一帧动画的估值和插值操作从而流畅的完成动画效果；`AnimatorSet`也是一个*final*的并且继承自`Animator`，它的作用和View动画中的`AnimationSet`一样用于存储和播放多个属性动画的集合。

### 应用属性动画
和View动画类似，属性动画也可以通过XML或者java代码实现，不过谷歌官方建议使用java代码应用属性动画。这是因为使用java代码来实现比较简单，更重要的一点是，在很多情况下目标对象的属性的起始值是不确定的，而且属性动画多应用于自定义的复杂动画需要自己实现目标对象和它的属性。
声明xml文件和View动画略有不同:
> 文件位置： **res/animator/filename.xml**
> 编译后的资源类型：`ValueAnimator`、`ObjectAnimator`、`AnimatorSet`
> 资源引用：Java：`R.animator.filename`      XML:`@[package:]animator/filename`
> 语法如下：

```xml
<set
  android:ordering=["together" | "sequentially"]>

    <objectAnimator
        android:propertyName="string"
        android:duration="int"
        android:valueFrom="float | int | color"
        android:valueTo="float | int | color"
        android:startOffset="int"
        android:repeatCount="int"
        android:repeatMode=["repeat" | "reverse"]
        android:valueType=["intType" | "floatType"]/>

    <animator
        android:duration="int"
        android:valueFrom="float | int | color"
        android:valueTo="float | int | color"
        android:startOffset="int"
        android:repeatCount="int"
        android:repeatMode=["repeat" | "reverse"]
        android:valueType=["intType" | "floatType"]/>

    <set>
        ...
    </set>
</set>
```

和View动画类似，根元素可以使用`<set>`包裹`<objectAnimator>`和`<valueAnimator>`,也可以使用后两者直接作为跟元素。

- `<set>`元素表示持有其他动画元素（`<objectAnimator>`、 `<valueAnimator>`、 `<set>`）的容器，该元素代表AnimatorSet类。
**android:ordering** ----指定播放集合的顺序，可以是`sequentially`代表顺序播放该集合内的动画属性；也可以是`together`，若不指定该属性**默认情况下**就是`together`它代表在同一时间内播放动画属性。

- `<objectAnimator>`在特定的时间内指定一个对象的属性动画，代表ObjectAnimator类。
**android:propertyName** ----String类型，**必填属性！**该属性代表属性动画的名称，例如对于一个视图对象可以指定"alpha"或者"backgroundColor" 。objectAnimator属性不会在XML中设置target属性，所以  就需要在java代码中setTarget方法来设置然后才能启动动画。
**android:valueTo** ---- float、int、color类型，**必填属性！**动画结束时的属性值，颜色值需要六位十六进制的数字值（例如#333333）
**android:valueFrom** ----float、int、color类型，动画开始时属性值，如果不指定将从属性的get方法中取得 ，颜色值需要六位十六进制的数字值（例如#333333）   
**android:duration** ----int类型，以毫秒为计算单位的动画时间，默认300ms
**android:startOffset** ---- int类型，在代码中通过start()方法启动动画后的延迟毫秒数。
**android:repeatCount** ----int类型，动画重复次数。如果设置了-1将无限次的重复，如果设置1动画启动后到结束将再次执行一次也就是重复一次，默认情况下是0，动画执行一次。
**android:repeatMode** ----int类型，重复模式，当android:repeatCount="-1"时该属性才起作用，设置为"reverse"将有一个相反方向的动画效果，设为"repeat"将继续循环播放动画
**android:valueType** ----关键字，如果依据颜色值进行动画就不要指定这个属性。动画框架将自动操作颜色值的属性动画。

|Value|描述|
|:--|:--|
|intType|integer类型的属性动画|
|floatType（默认）|float类型的属性动画|

- `<animator>`在特定的时间里执行一个动画效果，java代码中代表ValueAnimator类。
**android:valueTo** ----float、int、color类型，**必填属性！**动画结束时的属性值，颜色值需要六位十六进制的数字值（例如#333333）
**android:valueFrom** ----float、int、color类型，**必填属性！**动画开始时属性值 ，颜色值需要六位十六进制的数字值（例如#333333）
**android:duration** ----int类型，以毫秒为计算单位的动画时间，默认300ms
**android:startOffset** ----int类型，在代码中通过start()方法启动动画后的延迟毫秒数。
**android:repeatCount** ----int类型，动画重复次数。如果设置了-1将无限次的重复，如果设置1动画启动后到结束将再次执行一次也就是重复一次，默认情况下是0，动画执行一次。
**android:repeatMode** ----int类型，重复模式，当android:repeatCount="-1"时该属性才起作用，设置为"reverse"将有一个相反方向的动画效果，设为"repeat"将继续循环播放动画
**android:valueType** ----关键字，如果依据颜色值进行动画就不要指定这个属性。动画框架将自动操作颜色值的属性动画。

|Value|描述|
|:--|:--|
|intType|integer类型的属性动画|
|floatType（默认）|float类型的属性动画|

例子：创建res/animator/property_animator.xml文件
```xml
<set android:ordering="sequentially">
    <set>
        <objectAnimator
            android:propertyName="x"
            android:duration="500"
            android:valueTo="400"
            android:valueType="intType"/>
        <objectAnimator
            android:propertyName="y"
            android:duration="500"
            android:valueTo="300"
            android:valueType="intType"/>
    </set>
    <objectAnimator
        android:propertyName="alpha"
        android:duration="500"
        android:valueTo="1f"/>
</set>
```
为了能把动画跑起来，必须将该XML在Java代码中inflate为AnimatorSet对象，并且在动画启动之前设置目标对象。通过调用setTarget()方法设置一个单独的目标对象。
```java
AnimatorSet set = (AnimatorSet) AnimatorInflater.loadAnimator(myContext,
    R.anim.property_animator);
set.setTarget(myObject);
set.start();
```
我们的目标对象是一个透明度为0.2的View控件，通过xml中的属性可以看出，View控件的动画轨迹应该先是向右下角平移紧接着渐变色变为完全不透明的过程。但是编译完成后安装在测试机上的效果只有颜色透明度的变化没有View的平移动画。这又是为什么呢？带着这个问题继续探索属性动画。

### 插值器和估值器工作原理
`TimeInterpolator`时间插值器作为一个接口，它的作用是根据时间流逝的百分比来计算出当前属性值改变的百分率。
```java
/**
 * A time interpolator defines the rate of change of an animation. This allows animations
 * to have non-linear motion, such as acceleration and deceleration.
 */
public interface TimeInterpolator {

    /**
     * Maps a value representing the elapsed fraction of an animation to a value that represents
     * the interpolated fraction. This interpolated value is then multiplied by the change in
     * value of an animation to derive the animated value at the current elapsed animation time.
     *
     * @param input A value between 0 and 1.0 indicating our current point
     *        in the animation where 0 represents the start and 1.0 represents
     *        the end
     * @return The interpolation value. This value can be more than 1.0 for
     *         interpolators which overshoot their targets, or less than 0 for
     *         interpolators that undershoot their targets.
     */
    float getInterpolation(float input);
}
```
框架中实现该接口的类如下表所示：

|类/接口|描述|
|:--|:--|
|[AccelerateDecelerateInterpolator](https://developer.android.com/reference/android/view/animation/AccelerateDecelerateInterpolator.html)|先加速后减速的插值效果|
|[AccelerateInterpolator](https://developer.android.com/reference/android/view/animation/AccelerateInterpolator.html)|加速的插值效果|
|[AnticipateInterpolator](https://developer.android.com/reference/android/view/animation/AnticipateInterpolator.html)|开始后退接着向前的一个效果，也就是说时间消逝比例从负方向增加一点然后在从正方向上增加到1|
|[AnticipateOvershootInterpolator](https://developer.android.com/reference/android/view/animation/AnticipateOvershootInterpolator.html)|开始后退接着超出最大比例最后返回最大值，也就是说时间消逝比例先是从负方向上增加一点然后在从正方向上增加到1并且不停还要继续增加最后恢复到1|
|[BounceInterpolator](https://developer.android.com/reference/android/view/animation/BounceInterpolator.html)|弹跳效果|
|[CycleInterpolator](https://developer.android.com/reference/android/view/animation/CycleInterpolator.html)|在一个指定循环次数中进行重复播放|
|[DecelerateInterpolator](https://developer.android.com/reference/android/view/animation/DecelerateInterpolator.html)|开始后减速的插值效果|
|[LinearInterpolator](https://developer.android.com/reference/android/view/animation/LinearInterpolator.html)|线性匀速效果|
|[OvershootInterpolator](https://developer.android.com/reference/android/view/animation/OvershootInterpolator.html)|事件流逝比例超出1然后在返回|
|[TimeInterpolator](https://developer.android.com/reference/android/animation/TimeInterpolator.html)|时间插值器接口|

这几种差值算法的实现可以通过源码来查看，每种插值器对应的效果可以通过[AnimationEasingFunctions](https://github.com/daimajia/AnimationEasingFunctions)库来查看。

`TypeEvaluator`类型估值器，也是一个接口。它根据当前属性改变的百分比来计算改变后的属性值。
```java
/**
 * Interface for use with the {@link ValueAnimator#setEvaluator(TypeEvaluator)} function. Evaluators
 * allow developers to create animations on arbitrary property types, by allowing them to supply
 * custom evaluators for types that are not automatically understood and used by the animation
 * system.
 *
 * @see ValueAnimator#setEvaluator(TypeEvaluator)
 */
public interface TypeEvaluator<T> {

    /**
     * This function returns the result of linearly interpolating the start and end values, with
     * <code>fraction</code> representing the proportion between the start and end values. The
     * calculation is a simple parametric calculation: <code>result = x0 + t * (x1 - x0)</code>,
     * where <code>x0</code> is <code>startValue</code>, <code>x1</code> is <code>endValue</code>,
     * and <code>t</code> is <code>fraction</code>.
     *
     * @param fraction   The fraction from the starting to the ending values
     * @param startValue The start value.
     * @param endValue   The end value.
     * @return A linear interpolation between the start and end values, given the
     *         <code>fraction</code> parameter.
     */
    public T evaluate(float fraction, T startValue, T endValue);

}
```
框架中提供了几种估值器，当然我们可以实现`TypeEvaluator`接口自定义估值器。

|类/接口|描述|
|:--|:--|
|[IntEvaluator](https://developer.android.com/reference/android/animation/IntEvaluator.html)|默认为int类型属性进行估值计算|
|[FloatEvaluator](https://developer.android.com/reference/android/animation/FloatEvaluator.html)|默认为float类型属性进行估值计算|
|[ArgbEvaluator](https://developer.android.com/reference/android/animation/ArgbEvaluator.html)|默认为颜色属性进行估值计算，返回类型为颜色的16进制值|
|FloatArrayEvaluator|默认为float[]类型属性进行估值计算|
|IntArrayEvaluator|默认为int[]类型属性进行估值计算|
|PointFEvaluator|默认为PointF类型属性进行估值计算|
|RectEvaluator|默认为Rect类型属性进行估值计算|
|[TypeEvaluator](https://developer.android.com/reference/android/animation/TypeEvaluator.html)||

属性动画中利用时间插值器和估值器实现动画每一帧的变化，如下图所示
<p style="text-align: center;">
    <img src="pic/anim/animation-linear.png">
</p>
上图显示的是使用`LinearInterpolator`和`IntEvaluator`，在40ms的`duration`中，目标对象的x属性由0到40的变化过程。**动画默认的刷新率为10ms/帧**，所以40ms中被分为5帧来刷新。考虑第四帧(x=30 t=30ms)的时候，由于此时时间流逝的百分比为30/40，那么对于`LinearInterpolator`来说取值也是3/4的。
```java
/**
 * An interpolator where the rate of change is constant
 */
@HasNativeInterpolator
public class LinearInterpolator extends BaseInterpolator implements NativeInterpolatorFactory {
    ...
    public float getInterpolation(float input) {
        return input;
    }
    ...
}
```
取得插值后，将交给估值器来具体计算当前属性的变化值，这里使用的是`IntEvaluator`估值器，下面看看它的具体实现
```java
public class IntEvaluator implements TypeEvaluator<Integer> {
    public Integer evaluate(float fraction, Integer startValue, Integer endValue) {
        int startInt = startValue;
        return (int)(startInt + fraction * (endValue - startInt));
    }
}
```
由插值器计算出来的插值将作为估值器的`fraction`参数进行传入，故得到当前的属性值为(0+3/4*(40-0))=30。故当前x的属性为30
了解了插值器和估值算法，还要了解属性动画的监听器

###  属性动画的监听器
与View动画的监听器`AnimationListener`不同，属性动画提供了几个监听器其中有两个是经常被用到的它们分别是`ValueAnimator#AnimatorUpdateListener`和`Animator#AnimatorListener`
```java
    public static interface AnimatorUpdateListener {
        /**
         * <p>Notifies the occurrence of another frame of the animation.</p>
         *
         * @param animation The animation which was repeated.
         */
        void onAnimationUpdate(ValueAnimator animation);

    }
```
```java
    public static interface AnimatorListener {
        /**
         * <p>Notifies the start of the animation.</p>
         *
         * @param animation The started animation.
         */
        void onAnimationStart(Animator animation);

        /**
         * <p>Notifies the end of the animation. This callback is not invoked
         * for animations with repeat count set to INFINITE.</p>
         *
         * @param animation The animation which reached its end.
         */
        void onAnimationEnd(Animator animation);

        /**
         * <p>Notifies the cancellation of the animation. This callback is not invoked
         * for animations with repeat count set to INFINITE.</p>
         *
         * @param animation The animation which was canceled.
         */
        void onAnimationCancel(Animator animation);

        /**
         * <p>Notifies the repetition of the animation.</p>
         *
         * @param animation The animation which was repeated.
         */
        void onAnimationRepeat(Animator animation);
    }
```
`Animator#AnimatorListener`主要监听动画的开始、结束、取消和重复的时间节点，框架也提供了`AnimatorListenerAdapter`类，它整合了`Animator#AnimatorListener`和`Animator#AnimatorPauseListener`两个接口，方便开发者有选择的实现相应的方法。`ValueAnimator#AnimatorUpdateListener`接口会监听整个动画过程，即每10ms进行刷新时都会回调该接口用于更新属性值。

有了插值器和估值器的概念再加上对监听器的了解，我们来深入源代码探究属性动画的工作原理。

### 属性动画深入分析
<p style="text-align: center;">
    <img src="pic/anim/valueanimator.png">
</p>
根据前文的了解以及上图所示的类结构可以得出：

- `ValueAnimator`对象会跟踪整个动画过程，例如动画播放了多久、当前属性值是多少。
- `ValueAnimator`类中封装了一个`TimeInterpolator`时间插值器和一个`TypeEvaluator`估值器。
- 启动一个动画可以创建`ValueAnimator`对象并且给它传入目标对象属性的起始值和一个结束值，用于动画期间(`duration`)目标对象的启动时的状态和结束时的状态。当调用`start()`方法时，动画启动。在整个动画过程中，`ValueAnimator`计算时间流逝百分率(取值范围[0,1])。
- 当完成时间流逝百分比后会调用`TimeInterpolator`根据插值算法得出当前的插值。并调用`TypeEvaluator`根据估值算法以及传入的插值和起始值结束值计算出当前的属性值。

`ObjectAnimator`类继承自`ValueAnimator`并且实现了所有的方法，下面通过分析它的源码深入了解属性动画框架的工作原理。`ObjectAnimator`创建时传入的参数`ObjectAnimator.ofInt(Object target, String propertyName, int... values)`,笔者这里先猜想下：属性动画必定会通过反射机制或者其他的方法对`target`的`propertyName`进行每一帧的set或get方法，通过上文字的`ValueAnimator#AnimatorUpdateListener`接口利用插值器和估值器计算出当前帧的目标属性的值，那么对于目标对象来说一定要具有该属性的set方法。这也可能是前文中使用属性动画时对平移效果不起作用的原因吧。

下面就从`ObjectAnimator`的`start`方法开始吧！
```java
    @Override
    public void start() {
        // See if any of the current active/pending animators need to be canceled
        AnimationHandler handler = sAnimationHandler.get();
        if (handler != null) {
            int numAnims = handler.mAnimations.size();
            for (int i = numAnims - 1; i >= 0; i--) {
                if (handler.mAnimations.get(i) instanceof ObjectAnimator) {
                    ObjectAnimator anim = (ObjectAnimator) handler.mAnimations.get(i);
                    if (anim.mAutoCancel && hasSameTargetAndProperties(anim)) {
                        anim.cancel();
                    }
                }
            }
            numAnims = handler.mPendingAnimations.size();
            for (int i = numAnims - 1; i >= 0; i--) {
                if (handler.mPendingAnimations.get(i) instanceof ObjectAnimator) {
                    ObjectAnimator anim = (ObjectAnimator) handler.mPendingAnimations.get(i);
                    if (anim.mAutoCancel && hasSameTargetAndProperties(anim)) {
                        anim.cancel();
                    }
                }
            }
            numAnims = handler.mDelayedAnims.size();
            for (int i = numAnims - 1; i >= 0; i--) {
                if (handler.mDelayedAnims.get(i) instanceof ObjectAnimator) {
                    ObjectAnimator anim = (ObjectAnimator) handler.mDelayedAnims.get(i);
                    if (anim.mAutoCancel && hasSameTargetAndProperties(anim)) {
                        anim.cancel();
                    }
                }
            }
        }
        if (DBG) {
            Log.d(LOG_TAG, "Anim target, duration: " + getTarget() + ", " + getDuration());
            for (int i = 0; i < mValues.length; ++i) {
                PropertyValuesHolder pvh = mValues[i];
                Log.d(LOG_TAG, "   Values[" + i + "]: " +
                    pvh.getPropertyName() + ", " + pvh.mKeyframes.getValue(0) + ", " +
                    pvh.mKeyframes.getValue(1));
            }
        }
        super.start();
    }
```
这段代码先是取出由`AnimationHandler`维护的所有属性动画包括当前动画、等待动画和延迟动画。如果和当前作用的目标相同就会取消这个动画。接着调用`super.start()`，在父类`ValueAnimator`的start方法中又干了些什么呢？继续往下看
```java
    @Override
    public void start() {
        start(false);
    }

    private void start(boolean playBackwards) {
        if (Looper.myLooper() == null) {
            throw new AndroidRuntimeException("Animators may only be run on Looper threads");
        }
        mReversing = playBackwards;
        mPlayingBackwards = playBackwards;
        if (playBackwards && mSeekFraction != -1) {
            if (mSeekFraction == 0 && mCurrentIteration == 0) {
                // special case: reversing from seek-to-0 should act as if not seeked at all
                mSeekFraction = 0;
            } else if (mRepeatCount == INFINITE) {
                mSeekFraction = 1 - (mSeekFraction % 1);
            } else {
                mSeekFraction = 1 + mRepeatCount - (mCurrentIteration + mSeekFraction);
            }
            mCurrentIteration = (int) mSeekFraction;
            mSeekFraction = mSeekFraction % 1;
        }
        if (mCurrentIteration > 0 && mRepeatMode == REVERSE &&
                (mCurrentIteration < (mRepeatCount + 1) || mRepeatCount == INFINITE)) {
            // if we were seeked to some other iteration in a reversing animator,
            // figure out the correct direction to start playing based on the iteration
            if (playBackwards) {
                mPlayingBackwards = (mCurrentIteration % 2) == 0;
            } else {
                mPlayingBackwards = (mCurrentIteration % 2) != 0;
            }
        }
        int prevPlayingState = mPlayingState;
        mPlayingState = STOPPED;
        mStarted = true;
        mStartedDelay = false;
        mPaused = false;
        updateScaledDuration(); // in case the scale factor has changed since creation time
        AnimationHandler animationHandler = getOrCreateAnimationHandler();
        animationHandler.mPendingAnimations.add(this);
        if (mStartDelay == 0) {
            // This sets the initial value of the animation, prior to actually starting it running
            if (prevPlayingState != SEEKED) {
                setCurrentPlayTime(0);
            }
            mPlayingState = STOPPED;
            mRunning = true;
            notifyStartListeners();
        }
        animationHandler.start();
    }    
```
可以看到属性动画要运行在有`Looper`的线程中，经过一系列的判断和一些字段的赋值后，会调用`animationHandler.start()`方法。
```java
    protected static class AnimationHandler implements Runnable {
        // The per-thread list of all active animations
        /** @hide */
        protected final ArrayList<ValueAnimator> mAnimations = new ArrayList<ValueAnimator>();

        // Used in doAnimationFrame() to avoid concurrent modifications of mAnimations
        private final ArrayList<ValueAnimator> mTmpAnimations = new ArrayList<ValueAnimator>();

        // The per-thread set of animations to be started on the next animation frame
        /** @hide */
        protected final ArrayList<ValueAnimator> mPendingAnimations = new ArrayList<ValueAnimator>();

        /**
         * Internal per-thread collections used to avoid set collisions as animations start and end
         * while being processed.
         * @hide
         */
        protected final ArrayList<ValueAnimator> mDelayedAnims = new ArrayList<ValueAnimator>();
        private final ArrayList<ValueAnimator> mEndingAnims = new ArrayList<ValueAnimator>();
        private final ArrayList<ValueAnimator> mReadyAnims = new ArrayList<ValueAnimator>();

        private final Choreographer mChoreographer;
        private boolean mAnimationScheduled;

        private AnimationHandler() {
            mChoreographer = Choreographer.getInstance();
        }

        ...
        public void start() {
            scheduleAnimation();
        }

        private void scheduleAnimation() {
            if (!mAnimationScheduled) {
                mChoreographer.postCallback(Choreographer.CALLBACK_ANIMATION, this, null);
                mAnimationScheduled = true;
            }
        }
        ...
    }
```
`AnimationHandler`是继承自`Runnable`，其中维护着6个`ValueAnimator`列表，分别用于当前动画列表、临时列表、等待下一帧动画的列表、延迟动画列表、结束时动画列表和开始时动画列表。在`start`方法中调用`scheduleAnimation`方法，使用`Choreographer`类的`postCallback`(框架隐藏方法)来发送下一帧的回调，在`Choreographer`内部的代码就不贴出了，它是利用Handler机制进行转发最终会执行当前的`Runnable`。之后进入`doAnimationFrame`方法。
```java
        private void doAnimationFrame(long frameTime) {
            // mPendingAnimations holds any animations that have requested to be started
            // We're going to clear mPendingAnimations, but starting animation may
            // cause more to be added to the pending list (for example, if one animation
            // starting triggers another starting). So we loop until mPendingAnimations
            // is empty.
            while (mPendingAnimations.size() > 0) {
                ArrayList<ValueAnimator> pendingCopy =
                        (ArrayList<ValueAnimator>) mPendingAnimations.clone();
                mPendingAnimations.clear();
                int count = pendingCopy.size();
                for (int i = 0; i < count; ++i) {
                    ValueAnimator anim = pendingCopy.get(i);
                    // If the animation has a startDelay, place it on the delayed list
                    if (anim.mStartDelay == 0) {
                        anim.startAnimation(this);
                    } else {
                        mDelayedAnims.add(anim);
                    }
                }
            }
            // Next, process animations currently sitting on the delayed queue, adding
            // them to the active animations if they are ready
            int numDelayedAnims = mDelayedAnims.size();
            for (int i = 0; i < numDelayedAnims; ++i) {
                ValueAnimator anim = mDelayedAnims.get(i);
                if (anim.delayedAnimationFrame(frameTime)) {
                    mReadyAnims.add(anim);
                }
            }
            int numReadyAnims = mReadyAnims.size();
            if (numReadyAnims > 0) {
                for (int i = 0; i < numReadyAnims; ++i) {
                    ValueAnimator anim = mReadyAnims.get(i);
                    anim.startAnimation(this);
                    anim.mRunning = true;
                    mDelayedAnims.remove(anim);
                }
                mReadyAnims.clear();
            }

            // Now process all active animations. The return value from animationFrame()
            // tells the handler whether it should now be ended
            int numAnims = mAnimations.size();
            for (int i = 0; i < numAnims; ++i) {
                mTmpAnimations.add(mAnimations.get(i));
            }
            for (int i = 0; i < numAnims; ++i) {
                ValueAnimator anim = mTmpAnimations.get(i);
                if (mAnimations.contains(anim) && anim.doAnimationFrame(frameTime)) {
                    mEndingAnims.add(anim);
                }
            }
            mTmpAnimations.clear();
            if (mEndingAnims.size() > 0) {
                for (int i = 0; i < mEndingAnims.size(); ++i) {
                    mEndingAnims.get(i).endAnimation(this);
                }
                mEndingAnims.clear();
            }

            // If there are still active or delayed animations, schedule a future call to
            // onAnimate to process the next frame of the animations.
            if (!mAnimations.isEmpty() || !mDelayedAnims.isEmpty()) {
                scheduleAnimation();
            }
        }
```
上述代码比较长，可以通过注释了解这个过程。首先从`mPendingAnimations`等待列表中取出`ValueAnimator`对象，并且克隆当前等待列表，然后清除所有原列表中的对象。遍历克隆的列表，判断是否要延迟启动，如果不是则调用`startAnimation(AnimationHandler handler)`方法，若需要延迟启动，则将克隆列表中所有`ValueAnimator`对象添加到`mDelayedAnims`延迟列表中；接着处理延迟列表，经过`delayedAnimationFrame`判断是否唤醒当前的动画如果唤醒的话将`ValueAnimator`对象添加到`mReadyAnims`准备列表中；接下来处理`mReadyAnims`列表，遍历该列表取出`ValueAnimator`对象并调用`startAnimation(AnimationHandler handler)`方法同时将该对象在延迟列表中清除并且设置当前动画状态`anim.mRunning = true`，遍历结束后将`mReadyAnims`列表清除；下一步将处理`mAnimations`动画列表，通过遍历将当前要启动的动画倒装在临时列表`mTmpAnimations`，遍历临时列表调用`anim.doAnimationFrame(frameTime)`方法，通过该方法的返回值判断是否为动画的最后一帧，若是，则将`ValueAnimator`对象添加到`mEndingAnims`结束动画列表。遍历结束后清除临时列表`mTmpAnimations`；最后遍历`mEndingAnims`结束列表调用`endAnimation()`方法，遍历结束后清除`mEndingAnims`列表。通过6个列表的顺序遍历结束后，还要判断`mAnimations`和`mDelayedAnims`两个列表，只要任何一个不为空还会调用`scheduleAnimation`方法，这样就形成了循环进行下一轮的6种列表的遍历调用。

通过上述这段代码只知道`mPendingAnimations`中的数据是在之前`start`方法中添加的，那么`mAnimations`列表中的数据是在哪添加的呢？下面我们看一下`startAnimation(AnimationHandler handler)`方法
```java
    private void startAnimation(AnimationHandler handler) {
        if (Trace.isTagEnabled(Trace.TRACE_TAG_VIEW)) {
            Trace.asyncTraceBegin(Trace.TRACE_TAG_VIEW, getNameForTrace(),
                    System.identityHashCode(this));
        }
        initAnimation();
        handler.mAnimations.add(this);
        if (mStartDelay > 0 && mListeners != null) {
            // Listeners were already notified in start() if startDelay is 0; this is
            // just for delayed animations
            notifyStartListeners();
        }
    }
```
可以看到首先调用`initAnimation`方法，然后将当前的`ValueAnimator`添加到`mAnimations`列表中，最后如果是延迟启动的动画会回调监听器的`onAnimationStart`方法。
```java
    final boolean doAnimationFrame(long frameTime) {
        if (mPlayingState == STOPPED) {
            mPlayingState = RUNNING;
            if (mSeekFraction < 0) {
                mStartTime = frameTime;
            } else {
                long seekTime = (long) (mDuration * mSeekFraction);
                mStartTime = frameTime - seekTime;
                mSeekFraction = -1;
            }
        }
        if (mPaused) {
            if (mPauseTime < 0) {
                mPauseTime = frameTime;
            }
            return false;
        } else if (mResumed) {
            mResumed = false;
            if (mPauseTime > 0) {
                // Offset by the duration that the animation was paused
                mStartTime += (frameTime - mPauseTime);
            }
        }
        // The frame time might be before the start time during the first frame of
        // an animation.  The "current time" must always be on or after the start
        // time to avoid animating frames at negative time intervals.  In practice, this
        // is very rare and only happens when seeking backwards.
        final long currentTime = Math.max(frameTime, mStartTime);
        return animationFrame(currentTime);
    }
```
对于`doAnimationFrame`这里的逻辑很清晰，通过一路判断确定当前帧的时间点。返回`animationFrame`方法。
```java
    boolean animationFrame(long currentTime) {
        boolean done = false;
        switch (mPlayingState) {
        case RUNNING:
        case SEEKED:
            float fraction = mDuration > 0 ? (float)(currentTime - mStartTime) / mDuration : 1f;
            if (mDuration == 0 && mRepeatCount != INFINITE) {
                // Skip to the end
                mCurrentIteration = mRepeatCount;
                if (!mReversing) {
                    mPlayingBackwards = false;
                }
            }
            if (fraction >= 1f) {
                if (mCurrentIteration < mRepeatCount || mRepeatCount == INFINITE) {
                    // Time to repeat
                    if (mListeners != null) {
                        int numListeners = mListeners.size();
                        for (int i = 0; i < numListeners; ++i) {
                            mListeners.get(i).onAnimationRepeat(this);
                        }
                    }
                    if (mRepeatMode == REVERSE) {
                        mPlayingBackwards = !mPlayingBackwards;
                    }
                    mCurrentIteration += (int) fraction;
                    fraction = fraction % 1f;
                    mStartTime += mDuration;
                } else {
                    done = true;
                    fraction = Math.min(fraction, 1.0f);
                }
            }
            if (mPlayingBackwards) {
                fraction = 1f - fraction;
            }
            animateValue(fraction);
            break;
        }

        return done;
    }
```
上述代码可以看到`fraction`是时间流逝的百分比用于插值器的传入参数。通过判断时间流逝百分率若大于等于1代表已经完成动画或者进行重复动画过程，再经过判断`mRepeatCount`到底是进行重复动画还是真的结束。若小于1代表要继续下一帧动画则调用`animateValue`方法。
```java
    void animateValue(float fraction) {
        fraction = mInterpolator.getInterpolation(fraction);
        mCurrentFraction = fraction;
        int numValues = mValues.length;
        for (int i = 0; i < numValues; ++i) {
            mValues[i].calculateValue(fraction);
        }
        if (mUpdateListeners != null) {
            int numListeners = mUpdateListeners.size();
            for (int i = 0; i < numListeners; ++i) {
                mUpdateListeners.get(i).onAnimationUpdate(this);
            }
        }
    }
```
`animateValue`方法将交个`PropertyValuesHolder`类的`calculateValue`方法进行属性值的修改工作，接着回调`onAnimationUpdate`接口。

以上过程就是启动动画后播放每一帧时候修改属性值的过程，接下来观察属性值的起始值和结束值的设置过程以及动画过程中设置属性值的过程。下面还是要在代码中找真相:
```java
    public void setupStartValues() {
        initAnimation();

        final Object target = getTarget();
        if (target != null) {
            final int numValues = mValues.length;
            for (int i = 0; i < numValues; ++i) {
                mValues[i].setupStartValue(target);
            }
        }
    }
```
在`ObjectAnimator`类中覆写`setupStartValues`方法中可以看到先是初始化动画包括设置get和set以及初始化估值器；接着会调用`PropertyValuesHolder`类的`setupStartValue`方法，`setupStartValue`方法中会执行`setupValue`方法
```java
    private void setupValue(Object target, Keyframe kf) {
        if (mProperty != null) {
            Object value = convertBack(mProperty.get(target));
            kf.setValue(value);
        }
        try {
            if (mGetter == null) {
                Class targetClass = target.getClass();
                setupGetter(targetClass);
                if (mGetter == null) {
                    // Already logged the error - just return to avoid NPE
                    return;
                }
            }
            Object value = convertBack(mGetter.invoke(target));
            kf.setValue(value);
        } catch (InvocationTargetException e) {
            Log.e("PropertyValuesHolder", e.toString());
        } catch (IllegalAccessException e) {
            Log.e("PropertyValuesHolder", e.toString());
        }
    }
```
可以看到如果`mProperty`属性初始值没有给出，将通过反射调用目标对象的`get`方法进行取值操作。取得属性值后将赋值给`Keyframe`关键帧。

`PropertyValuesAnimator`封装着`mSetter`和`mGetter`的`Method`对象，并且通过`setupSetterOrGetter`方法来初始化，首先是通过JNI调用来使用set方法用于更改属性值，当JNI调用失败时使用反射拿到set方法改变属性值。JNI调用的效率远远大于反射机制。

通过以上代码的分析，可以得出如下结论：属性动画要求目标对象提供get和set方法，属性动画根据外界传递的属性的初始值和最终值，计算动画过程中每一帧属性的值并且通过JNI调用或者反射来设置新的属性值。所以在之前的应用中View对象平移效果没有生效的原因就是View类中setX方法和setY方法只是一个赋值过程并没有重绘View，所以没有达到预期的效果。

### 完善属性动画
依据上述的分析，对于目标对象应用属性动画必须要满足下面的条件：

- 目标对象必须提供其属性的set方法，如果动画启动后没有传递起始值，那么还需要该属性的get方法，因为由框架调用get方法取得当前的起始值。若没有提供get方法程序肯定会crash。
- 目标对象的set方法对属性的改变必须通过某种方法表现出来，对于之前的View平移就是因为没有通过重新刷新导致动画没有效果。这种情况不会导致程序crash只会导致没有动画效果。

针对这两个条件，谷歌官方也提供了3种解决方案

1. 如果有权限的话，完善get和set方法。
2. 使用另外一个类来包装目标类，间接提供get方法和set方法
3. 使用`ValueAnimator`或者`Animator`监听整个动画过程，自己实现属性的改变。

对于之前的View平移无效果的解决办法，只能使用后两种来解决。而第二种是最简单的方法，那么我们就自定义一个包装类来覆写get和set方法。之后笔者会展示使用`Animator`自定义动画的例子。

为了解决之前平移无效果的例子，我们需要使用java代码来代替xml
```java
    private void performAnimator(Object target) {
        ObjectAnimator x = ObjectAnimator.ofInt(target, "x", 400);
        x.setDuration(500);
        ObjectAnimator y = ObjectAnimator.ofArgb(target, "y", 300);
        y.setDuration(500);
        AnimatorSet set = new AnimatorSet();
        set.playTogether(x, y);
        ObjectAnimator alpha = ObjectAnimator.ofFloat(target, "alpha", 1f);
        alpha.setDuration(500);
        AnimatorSet baseSet = new AnimatorSet();
        baseSet.playSequentially(set, alpha);
        baseSet.start();
    }
```
自定义包装类完善目标对象的set方法
```java
    private static class ViewWrapper {
        private View mView;

        public ViewWrapper(View view) {
            mView = view;
        }

        public int getX() {
            return mView.getLeft();
        }

        public int getY() {
            return mView.getTop();
        }

        public void setX(int delta) {
            mView.setX(delta);
            mView.requestLayout();
        }

        public void setY(int delta) {
            mView.setY(delta);
            mView.requestLayout();
        }

        public float getAlpha(){
            return 0f;
        }
        public void setAlpha(float delta){
            mView.setAlpha(delta);
        }
    }
```
编译代码后得到apk再安装在测试机上，属性动画生效了。具体的效果这里就不贴出了。对于自定义属性动画来说例如下图的效果

<p style="text-align: center;">
    <img src="pic/anim/custom_animator.gif">
</p>
目标对象为白色小球它将围绕圆心在既定轨道上做环绕的动画。如何实现这个效果呢？其实也很简单，这里使用复杂的`Animator`类从底层来实现，这也是学习复杂动画必备知识。有助于更好的理解属性动画框架。
首先自定义小球辅助类
```java
    class Circle {
        float mStartEndSegment;
        float mRadius;
        PointF mStartPoint = new PointF();
        PointF mRadiusPoint = new PointF();

        Circle(float startX, float startY, float radius) {
            mStartPoint.set(startX, startY);
            mRadius = radius;
            mRadiusPoint.set(startX, startY + radius);
            mStartEndSegment = radius * 2;
        }
    }
```
可以看到声明了四个字段分别是直径、半径、起始坐标和圆心坐标。接着往下看，我们自定义一个类继承自`Animator`类。
```java
    static class MyAnimator extends Animator {
        boolean mStop = true;
        boolean mShouldStop;
        Circle mCircle;
        WeakReference<View> mTarget;
        WeakReference<ValueAnimator> mAnimator;
        float mValue;
        static MyAnimator sMyAnimator;

        private MyAnimator(View target, Circle circle) {
            mCircle = circle;
            mTarget = new WeakReference<View>(target);
            final ValueAnimator va = ValueAnimator.ofFloat(0f, 360f);
            va.setRepeatCount(ValueAnimator.INFINITE);
            mAnimator = new WeakReference<ValueAnimator>(va);
            mAnimator.get().addUpdateListener(new ValueAnimator.AnimatorUpdateListener() {
                @Override
                public void onAnimationUpdate(ValueAnimator animation) {
                    final float degree = (float) animation.getAnimatedValue();
                    if (mShouldStop && degree >= 0f && degree < 1f) {
                        setDegree(0f);
                        mStop = true;
                        cancel();
                        return;
                    }
                    setDegree(degree);
                }
            });
        }

        static MyAnimator newInstance(View target, Circle circle) {
            if (null == sMyAnimator) {
                sMyAnimator = new MyAnimator(target, circle);
            }
            return sMyAnimator;
        }

        void setDegree(float degree) {
            mValue = degree;
            View clipView = mTarget.get();
            float x = mCircle.mRadiusPoint.x + MathUtils.sin(degree) * mCircle.mRadius;
            float y = mCircle.mRadiusPoint.y - MathUtils.cos(degree) * mCircle.mRadius;
            clipView.setX(x - clipView.getWidth() / 2);
            clipView.setY(y - clipView.getHeight() / 2);
        }

        public boolean isStop() {
            return mStop;
        }

        public void setShouldStop(boolean shouldStop) {
            mShouldStop = shouldStop;
        }

        @Override
        public long getStartDelay() {
            Animator a = mAnimator.get();
            return null == a ? 0 : a.getDuration();
        }

        @Override
        public void setStartDelay(long startDelay) {
            Animator a = mAnimator.get();
            if (a != null) {
                a.setStartDelay(startDelay);
            }
        }

        @Override
        public Animator setDuration(long duration) {
            Animator a = mAnimator.get();
            if (a != null) {
                a.setDuration(duration);
            }
            return this;
        }

        @Override
        public long getDuration() {
            Animator a = mAnimator.get();
            return a == null ? 0 : a.getDuration();
        }

        @Override
        public void setInterpolator(TimeInterpolator value) {
            Animator a = mAnimator.get();
            if (a != null) {
                a.setInterpolator(value);
            }
        }

        @Override
        public boolean isRunning() {
            Animator a = mAnimator.get();
            return a != null && a.isRunning();
        }

        @Override
        public void start() {
//            super.start();
            Animator a = mAnimator.get();
            if (a != null) {
                mStop = false;
                a.start();
            }
        }

        @Override
        public void end() {
            super.end();
            Animator a = mAnimator.get();
            if (a != null) {
                a.end();
            }
        }

        @Override
        public void cancel() {
            super.cancel();
            Animator a = mAnimator.get();
            if (a != null) {
                a.cancel();
            }
        }

        @Override
        public void addListener(AnimatorListener listener) {
            Animator a = mAnimator.get();
            if (a != null) {
                a.addListener(listener);
            }
        }

        @Override
        public void setupEndValues() {
            super.setupEndValues();
            Animator a = mAnimator.get();
            if (a != null) {
                a.setupEndValues();
            }
        }

        @Override
        public void setupStartValues() {
            super.setupStartValues();
            Animator a = mAnimator.get();
            if (a != null) {
                a.setupStartValues();
            }
        }

    }
```
可以看到在初始化过程中使用了[0f,360f]的角度值，它代表动画过程中从0到360数值的变化过程，我们通过回调`onAnimationUpdate`方法具体改变目标对象位置的在`setDegree`方法中。可以看到从底层实现的过程思路很清晰就是通过每一帧的回调更改属性值来完成。


## 注意事项
1. OOM问题，帧动画最容易导致该问题，应避免使用帧动画
2. 内存泄露，这个问题是使用属性动画的常见问题，对于View动画不会出现这个问题。我们经常使用属性动画进行无限循环播放，对于这类动画需要在Android各个组件生命周期结束后及时停止，否则会导致组件无法释放造成内存泄露
3. 兼容性，属性动画是3.0以后引入的，可以使用库[NineOldAndroids](https://github.com/JakeWharton/NineOldAndroids/)
4. View动画问题，View动画只是对View的影像做动画，而不是真正的改变View的状态。
5. 使用dp，在动画行进过程中要尽量使用dp
6. 硬件加速，使用动画时建议开启硬件加速，可以保证动画流畅性。

## 知名的动画库
[https://github.com/wasabeef/awesome-android-ui/blob/master/pages/Animation.md](https://github.com/wasabeef/awesome-android-ui/blob/master/pages/Animation.md)

## 参考
[https://developer.android.com/guide/topics/resources/animation-resource.html](https://developer.android.com/guide/topics/resources/animation-resource.html)
[https://developer.android.com/guide/topics/graphics/prop-animation.html](https://developer.android.com/guide/topics/graphics/prop-animation.html)
[https://github.com/JakeWharton/NineOldAndroids](https://github.com/JakeWharton/NineOldAndroids/)
[AnimationEasingFunctions](https://github.com/daimajia/AnimationEasingFunctions)