---
title: 通过模仿最美应用详情页来谈谈安卓中View滑动解决方案
date: 2016-05-21 22:27:24
tags: [android, view, scroll]
categories: [android]
---
# 前言
处理View滑动事件并且执行酷炫效果是安卓上层开发的一个难点。与纯自定义View控件相比，实现View滑动效果又可以从动画的角度出发；但是针对滑动后保留控件的事件对象来说动画又存在短板；若从代码复杂度来说实现简单的View滑动又可以通过View自身提供的`scrollTo`和`scrollBy`方法辅以Scroller对象来实现；针对复杂滑动效果还是要通过自定义控件处理好各个View事件序列的事件分发和消费逻辑。

本篇通过模仿最美应用滑动操作效果来探讨下在Android中实现View滑动的这几种方案，并且对比各方案的优劣性。
<!-- more -->

首先，我们来仔细观察最美应用详情页的滑动动画效果。

<p style="text-align: center;">
<img src="pic/view_scroll/screenshot_zuimei.gif">
</p>

对于最美应用详情页可以在布局上分解为两部分（这里不讨论底部的footer bar），上半部分是一个16:9的图片背景下半部分可以看成是一个存放详情内容的容器(实际上是一个VebView容器，这里为了演示方便采用普通的组件显示内容)。按上滑和下拉两个动作分析的话又可以将组件分解成几部分。首先是下拉动作，头部图片背景有一个拉伸的动画；滑动释放后恢复到原来的位置，图片背景恢复到原来尺寸。对于上滑动作来说，头部图片随着上滑动作滑出屏幕，文本内容区域也随之上滑，可以观察到文本区域上滑速度要大于头部图片区域，上滑叠加部分由文本区域覆盖头部图片；当文本区域内的三个按钮（收藏、分享和下载）滑动到顶部的时候将和顶部返回按钮对齐并且钉于此处。

**注意** 这里去掉了底部的工具栏和下滑弹出APP大按钮，而只是简单分析该页面的主体滑动效果。该效果还是很普通很常见的，我们经常可以看到优秀的App应用于此效果，例如本人最爱的音乐app网易云音乐中歌手简介的页面。

**分析** 安卓中滑动效果的产生需要用户交互即由滑动事件的产生，再到操作View视图，变换其位置。详细的：由用户点击事件开始，到滑动屏幕，再到松开手指的这个过程里，连续的变换View视图的位置以及View动画来实现形形色色的滑动效果。其实这个原理很简单，核心内容就是操作View事件，变化View属性。

虽然原理简单两句话就概括了，但是在实际开发中确是有一定难度的，尤其是对一些初级开发者来说。不过没关系慢慢理解View框架尤其是View事件分发和View的绘制原理。随着练习的深入慢慢的对这类问题就得心应手了，笔者也准备在后续写两篇关于View事件分发和View视图渲染的文章。虽然网络上已经有很多大牛写了很多关于这类问题的高质量文章，但是为了进一步加深对View框架的理解还是需要自己去实践自己去挖坑再去填坑这样才能真正吃透安卓框架。

本文的主题是探讨View滑动解决方案，为了不偏离主题，本文将实现一个简略版的滑动效果页面。对于文中涉及到的View事件分发和View绘制原理将不做解释（后续笔者会来填坑）。下面来看看我们的解决方案：

# 解决方案

## 动画框架初显身手
动画框架中有移动的动画效果，无论是应用View动画还是属性动画都可以实现平移的效果。那么问题来了，属性动画是从Android3.0以后引入的如何保证版本兼容性呢？不要着急，还记得笔者上篇博文吗，对，就是使用`nineoldandroids`库，该库看似是将View应用了属性动画，其实不然，它的实现原理是在3.0以后的版本应用Android提供的属性动画框架，而对于3.0之前的版本则是应用了View动画。View动画有一个短板，那就是它在动画结束后会恢复View之初的模样。虽然可以通过`setFillAfter(true)`或者`android:fillAfter="true"`方法来保持View结束时的残影，但是不能真正改变View的属性，例如，当我们应用View动画进行平移操作时，等到动画结束后我们不能真正改变View的位置。怎么办呢？笔者想到了最笨的方法，使用两个View一个是开始时的状态一个是结束时的状态，在动画未开时前隐藏结束态的View，待到动画结束后隐藏开始态的View，使结束态的View可见。这样是不是太麻烦了呢？没有办法，这就是拆了东墙补西墙的道理，动画框架存在这样的缺点，致使我们采用这种不是办法的办法。

通过以上分析，对于版本要求苛刻，复杂的滑动效果、并且对于操作View对象强烈的需求是不建议使用动画来解决的。相反对于版本要求明朗(具备使用属性动画的条件)下，使用属性动画来实现滑动效果还是很方便的。

使用动画实现滑动操作的代码很简单，这里采用`nineoldandroids`库
```xml
dependencies {
    ...
    compile 'com.nineoldandroids:library:2.4.0+'    
}
```
```java
ObjectAnimator animator = ObjectAnimator.ofFloat(mToolbar, "Y", isTopToolbar ? mToolbarTop : 24);
animator.start();
```
对于更详细的动画操作可以查阅笔者上篇[博文](http://icedcap.github.io/2016/05/16/%E5%8A%A8%E7%94%BB%E6%80%BB%E7%BB%93/)

## 简单粗暴的使用scrollTo方法
`View`类中提供了两个滑动操作的方法，它们分别是`scrollTo`和`scrollBy`。通过阅读这两个方法的源码，我们了解到`scrollTo(int x, int y)`方法是滑动到目标位置。而`scrollBy(int x, int y)`方法则是在原有位置上相对水平方向和竖直方向移动多少个像素，其本质是调用`scrollTo`方法。
```java
    /**
     * Set the scrolled position of your view. This will cause a call to
     * {@link #onScrollChanged(int, int, int, int)} and the view will be
     * invalidated.
     * @param x the x position to scroll to
     * @param y the y position to scroll to
     */
    public void scrollTo(int x, int y) {
        if (mScrollX != x || mScrollY != y) {
            int oldX = mScrollX;
            int oldY = mScrollY;
            mScrollX = x;
            mScrollY = y;
            invalidateParentCaches();
            onScrollChanged(mScrollX, mScrollY, oldX, oldY);
            if (!awakenScrollBars()) {
                postInvalidateOnAnimation();
            }
        }
    }

    /**
     * Move the scrolled position of your view. This will cause a call to
     * {@link #onScrollChanged(int, int, int, int)} and the view will be
     * invalidated.
     * @param x the amount of pixels to scroll by horizontally
     * @param y the amount of pixels to scroll by vertically
     */
    public void scrollBy(int x, int y) {
        scrollTo(mScrollX + x, mScrollY + y);
    }
```
值得注意的是一旦使用`scrollTo`方法，会触发`onScrollChanged`方法的回调。

**注意** 虽然`scrollTo`方法实现了View的滑动，但是它是一次性的滑动。若要实现连续的滑动效果就需要配合多线程或者通过[Handler](http://icedcap.github.io/2016/05/12/%E6%B7%B1%E5%85%A5%E7%90%86%E8%A7%A3Handler%E6%9C%BA%E5%88%B6/)机制来辅助。解决了连续滑动的效果后，`scrollTo`还有一个致命的缺点：那就是它只能移动控件中的内容。

这里给出使用`scrollTo`方法应用在`TextView`控件上的效果。

```java
final TextView target = (TextView)findViewById(R.id.target_view);
        target.postDelayed(new Runnable() {
            @Override
            public void run() {
                target.scrollBy(-100, 0);
            }
        }, 1000);
```
<p style="text-align: center; ">
<table>
   <tr>
       <td><img src="pic/view_scroll/before_scrollto.png"/></td>
       <td><img src="pic/view_scroll/after_scrollto.png"/></td>
   </tr>
</table>
</p>
可以明显看到在加入上述代码后`TextView`控件中的内容向右移动了100个像素。所以应用`scrollTo`方法实现View控件的整体滑动是不切实际的，我们需要另找途径来完成。

我们在源码中找到了`Scroller`和`OverScroller`类，这两个类都是对滑动操作的封装类，在官方文档介绍中`OverScroller`在某些情况下需要代替`Scroller`类使用，而且许多滑动控件例如`ListView`都是操作`OverScroller`类来完成的。这里我们来简单使用`Scroller`类来完成一个连续的滑动。

在阅读`Scroller`源码的时候发现，该类并没有实际的对View进行位移操作，而只是存储一些滑动变量，和一些计算位移变化的方法而已。文档中给出了一个简单的用法例子如下：
```java
    private Scroller mScroller = new Scroller(context);
    ...
    public void zoomIn() {
        // Revert any animation currently in progress
        mScroller.forceFinished(true);
        // Start scrolling by providing a starting point and
        // the distance to travel
        mScroller.startScroll(0, 0, 100, 0);
        // Invalidate to request a redraw
        invalidate();
    }
```
通过例子，这才恍然大悟，真正实现滑动效果的方法是`invalidate`重画View视图。在重绘View之前`startScroll`方法又干了些什么？

```java
    /**
     * Start scrolling by providing a starting point and the distance to travel.
     * The scroll will use the default value of 250 milliseconds for the
     * duration.
     * 
     * @param startX Starting horizontal scroll offset in pixels. Positive
     *        numbers will scroll the content to the left.
     * @param startY Starting vertical scroll offset in pixels. Positive numbers
     *        will scroll the content up.
     * @param dx Horizontal distance to travel. Positive numbers will scroll the
     *        content to the left.
     * @param dy Vertical distance to travel. Positive numbers will scroll the
     *        content up.
     */
    public void startScroll(int startX, int startY, int dx, int dy) {
        startScroll(startX, startY, dx, dy, DEFAULT_DURATION);
    }

    /**
     * Start scrolling by providing a starting point, the distance to travel,
     * and the duration of the scroll.
     * 
     * @param startX Starting horizontal scroll offset in pixels. Positive
     *        numbers will scroll the content to the left.
     * @param startY Starting vertical scroll offset in pixels. Positive numbers
     *        will scroll the content up.
     * @param dx Horizontal distance to travel. Positive numbers will scroll the
     *        content to the left.
     * @param dy Vertical distance to travel. Positive numbers will scroll the
     *        content up.
     * @param duration Duration of the scroll in milliseconds.
     */
    public void startScroll(int startX, int startY, int dx, int dy, int duration) {
        mMode = SCROLL_MODE;
        mFinished = false;
        mDuration = duration;
        mStartTime = AnimationUtils.currentAnimationTimeMillis();
        mStartX = startX;
        mStartY = startY;
        mFinalX = startX + dx;
        mFinalY = startY + dy;
        mDeltaX = dx;
        mDeltaY = dy;
        mDurationReciprocal = 1.0f / (float) mDuration;
    }
```
很明显在这里初始化`Scroller`的滑动参数变量，主要包括起始坐标、结束坐标，水平和竖直方向上的滑动距离以及持续事件等变量。在初始所有变量后就可以调用`invalidate`方法，该方法会引起View的重绘过程，致使调用`draw`方法(这个坑会在后续博文中填补)。`draw`方法会回调`computeScroll`方法，而`View`中的`computeScroll`方法只是一个空实现方法，所有我们重写该方法，在该方法下调用`mScroller.computeScrollOffset()`方法来判断当前的滑动是否已经完成，若没有完成我们就可以调用`scrollTo`方法，并且执行`postInvalidate`反复的重绘View视图，这样就解决了单独使用`scrollTo`方法造成的只移动控件内容的效果。

模仿最美应用这个效果就可以应用以下代码来实现了。
**注意：** 为了简化操作这里不去监听滑动操作的过程，取而代之的则是利用按钮进行上滑和下拉的操作。对于复杂的操作和功能模块也一并舍弃。这里自定义一个View并继承自`LinearLayout`(暂且不去实现上滑过程中上部视图与下部视图的速度差，因为线性布局无法产生这种效果)。为了实验效果类名起的也比较随意`StretchByScrollerView`，首先完成View的构造器

```java
public StretchByScrollerView(Context context) {
        super(context);
        init(context);
}

private void init(Context context) {
        mContext = context;
        mScroller = new Scroller(context);
        setOrientation(LinearLayout.VERTICAL);
        DisplayMetrics displayMetrics = new DisplayMetrics();
        WindowManager manager = (WindowManager) mContext.getSystemService(Context.WINDOW_SERVICE);
        manager.getDefaultDisplay().getMetrics(displayMetrics);
        mScreenWidth = displayMetrics.widthPixels;
        mScreenHeight = displayMetrics.heightPixels;

        mImgHeight = (int) (mScreenWidth * ((float) 9 / 16));
        mImageView = new ImageView(context);
        mImageView.setImageDrawable(mContext.getDrawable(R.drawable.img_bg));
        addView(mImageView, mScreenWidth, mImgHeight);

        final LayoutInflater inflater = LayoutInflater.from(mContext);
        mTitleBar = inflater.inflate(R.layout.title_bar, null, false);
        addView(mTitleBar, new LayoutParams(-1, -2));

        mToolbar = inflater.inflate(R.layout.tools_bar, null, false);
        LayoutParams toolsbarParam = new LayoutParams(-1, -2);
        toolsbarParam.setMargins(0, 50, 0, 50);
        addView(mToolbar, toolsbarParam);
        mToolbar.addOnLayoutChangeListener(new OnLayoutChangeListener() {
            @Override
            public void onLayoutChange(View v, int left, int top, int right, int bottom, int oldLeft, int oldTop, int oldRight, int oldBottom) {
                mToolbar.removeOnLayoutChangeListener(this);
                mToolbarTop = mToolbar.getTop();
            }
        });


        LayoutParams params = new LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.MATCH_PARENT);
        params.setMarginStart(40);
        params.setMarginEnd(40);
        TextView textView = new TextView(context);
        String text = mContext.getString(R.string.details_content);
        textView.setText(text);
        textView.setLineSpacing(1, 1.5f);
        textView.setBackgroundColor(Color.WHITE);
        addView(textView, params);

}
```
在该View下放入三个子View分别是`mImageView`头部的图片背景、`mTitleBar`文章标题以及应用图标等和`textView`文章内容(这里简化使用了`TextView`控件存放纯文本内容，实际中应该采用`WebView`从服务器中加载文章内容)

接下来完成滑动的接口
```java
    public void scroll(int y) {
        int scrollY = getScrollY();
        int deltaY = y - scrollY;
        mScroller.startScroll(0, scrollY, 0, deltaY, 800);
        invalidate();
    }

    @Override
    public void computeScroll() {
        if (mScroller.computeScrollOffset()) {
            scrollTo(mScroller.getCurrX(), mScroller.getCurrY());
            if (isScaleImg) {
                stretchImg(mScroller.getCurrY());
            }
            postInvalidate();
        }
    }

```

通过调用`scroll`方法只是单独的滑动当前的View，如下图所示的效果：

<p style="text-align: center;">
    <img src="pic/view_scroll/scroller.gif">
</p>


为了达到原应用的效果需要对头部的背景图片进行缩放操作，这里采用最简单的方法：
```java
    public void stretchImg(int scrollY) {
        int factor = Math.abs(scrollY);
        float scaleSize = (float) (factor * 2 + mImgHeight) / mImgHeight;
        mImageView.setScaleX(scaleSize);
        mImageView.setScaleY(scaleSize);
    }
```

通过按钮模拟上滑和下拉两个操作来调用上面的滑动接口，具体代码如下：
```java
    private void scrollDown() {
        final int imgHeight = mStretchByScrollerView.getImgHeight();
        final int destY = (int) (imgHeight * (1.0f / 5));
        mStretchByScrollerView.setScaleImg(true);
        mStretchByScrollerView.scroll(-destY);
        mStretchByScrollerView.postDelayed(new Runnable() {
            @Override
            public void run() {
                mStretchByScrollerView.scroll(0);
            }
        }, 800);
    }

    private void scrollUp() {
        mStretchByScrollerView.setScaleImg(false);
        final int destHeight = mStretchByScrollerView.getImgHeight() + mStretchByScrollerView.getTitlebarHeight();
        mStretchByScrollerView.scroll(destHeight);
        mStretchByScrollerView.postDelayed(new Runnable() {
            @Override
            public void run() {
                mStretchByScrollerView.setToolBarVisiblity(View.INVISIBLE);
                setToolbarVisiblity(View.VISIBLE);
            }
        },500);

    }
```
最终的效果如下图所示

<p style="text-align: center;">
    <img src="pic/view_scroll/full_demo.gif"/>
</p>

从最终的效果图来看还是和原版效果相差甚远。首先是下拉，由于这里对`ImageView`控件调用`setScaleX`和`setScaleY`方法进行图片拉伸效果，由于每次传入的参数和拉伸的中点是变化的，导致图片会覆盖底层的View，解决办法就是调整图片拉伸的算法使之适应下拉扩展的距离。其次，在原版的上滑过程中，图片区域上滑速度要明显小于底层内容视图的上滑速度，读者可以在回到文章的开头仔细观察原版滑动效果。针对这个问题，就要否定前文继承`LinearLayout`的实现了，因为`LinearLayout`中的每个子View是线性排布的，对于操纵父容器作为一个整体进行滑动时，每个子View也将按着线性顺序进行滑动，不会出现顿挫的滑动效果，除非将每个子View拆解为单独的个体进行滑动。

下面就针对这些复杂的问题应用最后的大招，从底层出发，彻底改变每个View的滑动效果。

## 从底层出发---操作`measure` `layout`过程并且修改View的`LayoutParam`
View的绘制过程要经历`measure` `layout` 和`draw`三个过程。`LayoutParam`在这三个过程中扮演着重要角色，简单来说，它将控制View的大小以及布局位置等。所以通过连续改变`LayoutParam`位置参数就可以实现View的动态滑动效果。

这里为了整体实现滑动效果，需要拦截滑动事件不再使用按钮进行模拟上滑和下拉操作。操作滑动事件会涉及到事件分发和拦截，后续博文将详细介绍这部分知识，这里只会简单的概括。

本节为了实现在上滑过程中头部图片与底部内容视图有一个上滑时间差效果，所以自定义的组件不能继承自线性布局`LinearLayout`了。这里我们继承自`FrameLayout`，并完成页面的搭建工作。主要的工作就是操作好自定义视图的`measure`和`layout`的过程。

在自定义父容器中添加两个子视图分别呈现头部图片和底部内容，代码如下
```java
public class StretchScrollView extends FrameLayout {   
    ...
    private ImageView mHeader;
    private ViewGroup mContent;
    ...

    private void init(Context context, AttributeSet attrs) {
        DisplayMetrics dm = new DisplayMetrics();
        ((WindowManager) context.getSystemService(Context.WINDOW_SERVICE))
                .getDefaultDisplay().getMetrics(dm);
        mImageWidth = mScreenWidth = dm.widthPixels;
        mScreenHeight = dm.heightPixels;
        mImageHeight = (int) (mImageWidth * (9.0f / 16.0f));
        mHeader = new ImageView(context, attrs);
        mHeader.setId(R.id.header_id);
        FrameLayout.LayoutParams lp = new LayoutParams(mImageWidth, mImageHeight);
        TypedArray typedArray = getResources().obtainAttributes(attrs, R.styleable.StretchScrollView);
        int headerBackgroundResId = typedArray
                .getResourceId(R.styleable.StretchScrollView_headerViewBackground, BG_HEADER_RES_ID);
        mHeader.setImageDrawable(context.getDrawable(headerBackgroundResId));
        this.addView(mHeader, lp);

        int contentViewResId = typedArray.getResourceId(R.styleable.StretchScrollView_content, -1);
        typedArray.recycle();

        FrameLayout.LayoutParams lp2 = new LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT);
        LayoutInflater inflater = LayoutInflater.from(context);
        mContent = (ViewGroup) inflater.inflate(contentViewResId == -1 ? R.layout.tools_bar : contentViewResId, null);
        mContent.setId(R.id.content_id);
        addView(mContent, lp2);
    }

    ...

}
```

接下来是自定义View的重点以及难点，它就是`measure`和`layout`过程。为了方便演示，这里的头部图片是一个16:9并且铺满屏幕宽度固定大小的一块区域。初始化时图片底部的内容部分是紧挨着图片进行排布的，并且内容部分的高度是依据子控件的高度（wrap_content）。
```java
    @Override
    protected void onMeasure(int widthMeasureSpec, int heightMeasureSpec) {
        final int widthSize = MeasureSpec.getSize(widthMeasureSpec);
        final int heightSize = MeasureSpec.getSize(heightMeasureSpec);
        final int widthMode = MeasureSpec.getMode(widthMeasureSpec);
        final int heightMode = MeasureSpec.getMode(heightMeasureSpec);

        final FrameLayout.LayoutParams lp = (FrameLayout.LayoutParams) mContent.getLayoutParams();
        mHeader.measure(MeasureSpec.makeMeasureSpec(mCurrImgWidth, MeasureSpec.EXACTLY),
                MeasureSpec.makeMeasureSpec(mCurrImgHeight, MeasureSpec.EXACTLY));
        mContent.measure(MeasureSpec.makeMeasureSpec(mScreenWidth, MeasureSpec.EXACTLY),
                MeasureSpec.makeMeasureSpec(lp.height, MeasureSpec.AT_MOST));

        int measureHeight = mCurrImgHeight + mContent.getHeight() + mContent.getPaddingBottom() + mContent.getPaddingTop();
        setMeasuredDimension(widthSize, measureHeight);
    }
```

现在来思考一下，下拉的过程其实就是扩大`headerView`的宽高值的过程，改变`headerView`和`contentView`的布局位置。知道这一点很重要，这个原理就是实现滑动效果的核心思想。下面我们从代码上来实现。
先声明一个下拉操作的方法
```java
    private void smoothScrollDown(final int deltaY) {
        if (mContentTop < mOriginImgHeight) {
            mContentTop += deltaY;
        } else {
            mDeltaImgHeight = deltaY;
            mDeltaImgWidth = (int) (mDeltaImgHeight * (16f / 9f));
            mCurrImgHeight += deltaY;
            mCurrImgWidth += mDeltaImgWidth;
            isScrollUp = false;
        }
        switchToolbar();
        requestLayout();
    }
```
下拉的过程又要从临界点即`headerView`以原始（16:9铺满屏幕宽度）方式呈现的那个状态分为即将下拉来拉伸`headerView`背景图片和`headerView`有一部分或者全部隐藏在屏幕顶部以上区域需要下拉呈现。`else`里的内容就是操作下拉伸展背景图片的过程。每次通过下拉增距离`deltaY`来增加`headerView`的宽高，最后调用`requestLayout()`方法来从新绘制视图。
```java
    @Override
    protected void onLayout(boolean changed, int l, int t, int r, int b) {
        int left = -(mCurrImgWidth - mScreenWidth) / 2;
        setChildFrame(mHeader, left, isScrollUp ? (mContentTop - mCurrImgHeight) / 2 : 0, mCurrImgWidth, mCurrImgHeight);
        setChildFrame(mContent, l, isScrollUp ? mContentTop : mCurrImgHeight, mScreenWidth, mContent.getMeasuredHeight());
    }

    private void setChildFrame(View child, int l, int t, int width, int height) {
        child.layout(l, t, l + width, t + height);
    }
```

重新绘制的过程也要经历`measure` `layout`以及`draw`三个过程，所以在`onMeasure`中重新测量了`headerView`的高度和宽度，并且在`onLayout`方法中进行`headerView`拉伸后的布局。这个过程看似复杂，其实核心思想很简单，无非就是来回折腾View的`measure` `layout`以及`draw`的过程。

下拉的这个过程已经分析完了，其它的操作过程也都一样，上滑过程中`headerView`和`contentView`有一个滑动速度差效果而不是并列一起向上滑。这里利用`contentView`上滑来覆盖一部分`headerView`的原理，可以在布局的时候将头部视图的顶部设为`(mContentTop - mCurrImgHeight) / 2`。

下面简单介绍滑动操作事件序列的监听过程（这里只是简单实现滑动过程，对于手势以及滑动事件拦截等操作将在后续的博文中进行分析）
```java
    @Override
    public boolean onTouchEvent(MotionEvent event) {
        mVelocityTracker.addMovement(event);
        final int x = (int) event.getX();
        final int y = (int) event.getY();
        int deltaY = 0;

        switch (event.getAction()) {
            case MotionEvent.ACTION_DOWN:

                break;
            case MotionEvent.ACTION_MOVE:
                deltaY = y - mLastY;//正数下拉，负数上滑
                if (deltaY > 0) {
                    smoothScrollDown(deltaY);
                } else {
                    smoothScrollUp(deltaY);
                }
                break;
            case MotionEvent.ACTION_UP:
                mVelocityTracker.computeCurrentVelocity(200);
                float velocity = mVelocityTracker.getYVelocity();
                mVelocityTracker.clear();
                scrollAfterGesture((int) velocity);
                smoothToResume();
                break;
        }

        mLastX = x;
        mLastY = y;
        return true;
    }

    private void smoothScrollDown(final int deltaY) {
        if (mContentTop < mOriginImgHeight) {
            mContentTop += deltaY;
        } else {
            mDeltaImgHeight = deltaY;
            mDeltaImgWidth = (int) (mDeltaImgHeight * (16f / 9f));
            mCurrImgHeight += deltaY;
            mCurrImgWidth += mDeltaImgWidth;
            isScrollUp = false;
        }
        switchToolbar();
        requestLayout();
    }

    private void smoothScrollUp(int deltaY) {
        if (mContent.getBottom() <= mScreenHeight) {
            return;
        }
        if (mCurrImgHeight > mOriginImgHeight) {
            mDeltaImgHeight = deltaY;
            mDeltaImgWidth = (int) (mDeltaImgHeight * (16f / 9f));
            int tempWidth = mCurrImgWidth + mDeltaImgWidth;
            mCurrImgWidth = tempWidth < mOriginImgWidth ? mOriginImgWidth : tempWidth;
            int tempHeight = mCurrImgHeight + mDeltaImgHeight;
            mCurrImgHeight = tempHeight < mOriginImgHeight ? mOriginImgHeight : tempHeight;
        } else {
            //上滑header没有伸缩效果
            //为了将header和content产生一个滑动差的效果可以对两个子View使用一个线性关系的deltaY
            isScrollUp = true;
            mContentTop += deltaY;

        }
        switchToolbar();
        requestLayout();
    }

    private void switchToolbar() {
        final View titleBar = mContent.getChildAt(0);
        final View toolBar = mContent.getChildAt(1);
        if (-mContent.getTop() >= titleBar.getHeight() + toolBar.getPaddingTop()) {
            toolBar.setVisibility(INVISIBLE);
            mToolBarVisibility.setOnToolbarVisibility(VISIBLE);
        } else {
            toolBar.setVisibility(VISIBLE);
            mToolBarVisibility.setOnToolbarVisibility(INVISIBLE);
        }
    }

    private void smoothToResume() {
        final int resumeHeight = mCurrImgHeight - mOriginImgHeight;
        if (resumeHeight > 0) {
            mCurrImgHeight = mOriginImgHeight;
            mCurrImgWidth = mOriginImgWidth;
            requestLayout();
        }
    }
```

在`MotionEvent.ACTION_MOVE`的事件序列里可以通过`event.getY()`得到每次滑动的位置通过记录上次位置并且求得它俩的差值就是我们每次滑动的`deltaY`的值了，`deltaY`为正数时代表下拉操作，相反则是上滑的操作。

最终通过底层修改View的宽高并且重新`measure`和`layout`的过程轻松的实现了类似最美应用的滑动效果。

<p style="text-align: center">
    <img src="pic/view_scroll/the_demo.gif"/>
</p>

# 对比
通过以上三种解决方案的论述以及亲身实践，我们发现从底层出发是最根本的解决之道，因为安卓View框架以及安卓提供的原生控件也都是通过最底层的方法实现的。使用这种方案优点就是从对底层就能解决各种问题，但是缺点也很明确，那就是很复杂，对于初学者较难，要处理很多细节的东西例如`measure`过程中要处理每个子控件的`padding`和`margin`以及`MeasureSpec`的模式。所以，如果你本身具备这方面的能力，对各种情形考虑周全并能一一解决的当然推荐使用这种方法。

动画解决方案明显劣势就是版本兼容性问题，其次对于复杂的多控件不规则的滑动效果来说，动画解决方案也捉襟见肘。所以说对于简单的一个view控件来说动画也不失为一个明智的选择，因为它提供了强大的框架和库的支持，只不过对于3.0以下的版本来说若想在滑动结束后还要操作该view的时候就像前文提到的方法增加替身来处理了。

采用`Scroller`辅助`scrollTo`和`scrollBy`往往是我们最先选择的方法，该方案实现简单，代码量少，与修改底层相比要简单的多。但是它的缺点也很明确就是只能滑动控件里的内容。所以，对于操作View内容的滑动，首选该方案。

# 参考
- 最美应用App
- 《Android开发艺术探索》
- [PullZoomView](https://github.com/Frank-Zhu/PullZoomView)