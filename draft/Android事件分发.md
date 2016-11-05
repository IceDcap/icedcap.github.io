<p style="text-align: center;">
    <img src="pic/eventbus/eventbus_header.jpg">
</p>

# Android事件分发
众所周知，android视图框架由`View`和`ViewGroup`构成。`ViewGroup`是`View`的子类，是所有的布局类的父类，`View`是所有控件的父类。如下图所示的关系：

<p style="text-align: center;">
<img src="pic/view&viewgroup.jpg">
</p>

Android事件`MotionAction`作为用户交互的媒介，包括点击，滑动，长按，拖拽等等。用户每次对屏幕操作动作都由三个最基本的动作构成，它们分别是`ACTION_DOWN` `ACTION_MOVE`和`ACTION_UP`。这一系列的动作操作被称为一个事件序列。比如说点击事件可以被分解为`ACTION_DOWN` -> `aCTION_UP`;滑动操作可以被分解为`ACTION_DOWN` -> `ACTION_MOVE` -> `ACTION_MOVE` -> ... ->`ACTION_MOVE` -> `ACTION_UP`。可以肯定的是每一个事件序列都是以`ACTION_DOWN`开始。

我们都知道在手屏幕上呈现的多姿多彩的画面不是由一个或者两个`View`就能构成的，而是由不同的布局视图`ViewGroup`和不同的控件`View`一层一层嵌套形成的视图层级。这么多的`View`是如何接收到事件的呢？具体的事件又该真正的作用于哪个`View`呢？

这就需要Android强大框架支持了。实现解决这些问题恰恰需要Android提供一个强大的View事假分发消费机制。

`View`源码中提供了两个方法分别是`public boolean dispatchTouchEvent(MotionEvent event)`和`public boolean onTouchEvent(MotionEvent event)`而在`ViewGroup`源码中中发现不仅覆写了`public boolean dispatchTouchEvent(MotionEvent event)`而且还提供了一个`public boolean onInterceptTouchEvent(MotionEvent ev)`方法。在`Activity`的源码中也可以找到`dispatchTouchEvent`和`onTouchEvent`两个方法。

通过方法的名字大意上不难看出，它们就是分发事件和消耗事件的关键方法。下面通过实验来观察事件传递的过程。

## View事件分发与处理
为了能在`dispatchTouchEvent`和`onTouchEvent`方法中打印日志，这里写两个类来分别继承`Button`和`FrameLayout`，分别命名为`CustomButton`和`CustomLayout`
```java
public class CustomLayout extends FrameLayout {
    private static final String TAG = "CustomLayout";
    ...

    @Override
    public boolean dispatchTouchEvent(MotionEvent ev) {
        switch (ev.getAction()){
            case MotionEvent.ACTION_DOWN:
                Log.d(TAG, " >>>> dispatchTouchEvent >>>> DOWN");
                break;
            case MotionEvent.ACTION_UP:
                Log.d(TAG, " >>>> dispatchTouchEvent >>>> UP");
                break;
            case MotionEvent.ACTION_MOVE:
                Log.d(TAG, " >>>> dispatchTouchEvent >>>> MOVE");
                break;
        }
        return super.dispatchTouchEvent(ev);
    }

    @Override
    public boolean onTouchEvent(MotionEvent event) {
        switch (event.getAction()){
            case MotionEvent.ACTION_DOWN:
                Log.d(TAG, " >>>> onTouchEvent >>>> DOWN");
                break;
            case MotionEvent.ACTION_MOVE:
                Log.d(TAG, " >>>> onTouchEvent >>>> MOVE");
                break;
            case MotionEvent.ACTION_UP:
                Log.d(TAG, " >>>> onTouchEvent >>>> UP");
                break;
        }
        return super.onTouchEvent(event);
    }
}
```

```java
public class CustomButton extends Button {
    private static final String TAG = "CustomButton";
    ...

    @Override
    public boolean dispatchTouchEvent(MotionEvent event) {
        switch (event.getAction()) {
            case MotionEvent.ACTION_DOWN:
                Log.d(TAG, ">>>> dispatchTouchEvent >>> DOWN");
                break;
            case MotionEvent.ACTION_UP:
                Log.d(TAG, ">>>> dispatchTouchEvent >>> UP");
                break;
        }
        return super.dispatchTouchEvent(event);
    }

    @Override
    public boolean onTouchEvent(MotionEvent event) {
        switch (event.getAction()) {
            case MotionEvent.ACTION_DOWN:
                Log.d(TAG, ">>>> onTouchEvent >>> DOWN");
                break;
            case MotionEvent.ACTION_UP:
                Log.d(TAG, ">>>> onTouchEvent >>> UP");
                break;
        }
        return super.onTouchEvent(event);
    }
}
```

布局文件代码如下：
```xml
<?xml version="1.0" encoding="utf-8"?>
<com.icedcap.viewtestdemo.CustomLayout
    android:id="@+id/customLayout"
    xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent">
    <com.icedcap.viewtestdemo.CustomButton
        android:id="@+id/customButton"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="自定义按钮"/>
</com.icedcap.viewtestdemo.CustomLayout>
```

在`Activity`中重写`dispatchTouchEvent`和`onTouchEvent`这两个方法，并且为`customButton`和`customLayout`添加点击事件和触摸事件。
```java
public class SjActivity extends Activity implements View.OnClickListener, View.OnTouchListener{
    private static final String TAG = "SjActivity";


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_sj);
        findViewById(R.id.customButton).setOnClickListener(this);
        findViewById(R.id.customButton).setOnTouchListener(this);
        findViewById(R.id.customLayout).setOnClickListener(this);
        findViewById(R.id.customLayout).setOnTouchListener(this);

    }

    @Override
    public boolean dispatchTouchEvent(MotionEvent ev) {
        switch (ev.getAction()) {
            case MotionEvent.ACTION_DOWN:
                Log.d(TAG, " >>>> SjActivity >> dispatchTouchEvent >>> DOWN");
                break;
            case MotionEvent.ACTION_MOVE:
                Log.d(TAG, " >>>> SjActivity >> dispatchTouchEvent >>> MOVE");
                break;
            case MotionEvent.ACTION_UP:
                Log.d(TAG, " >>>> SjActivity >> dispatchTouchEvent >>> UP");
                break;
        }
        return super.dispatchTouchEvent(ev);
    }

    @Override
    public boolean onTouchEvent(MotionEvent event) {
        switch (event.getAction()) {
            case MotionEvent.ACTION_DOWN:
                Log.d(TAG, " >>>> SjActivity >> onTouchEvent >>> DOWN");
                break;
            case MotionEvent.ACTION_MOVE:
                Log.d(TAG, " >>>> SjActivity >> onTouchEvent >>> MOVE");
                break;
            case MotionEvent.ACTION_UP:
                Log.d(TAG, " >>>> SjActivity >> onTouchEvent >>> UP");
                break;
        }
        return super.onTouchEvent(event);
    }

    @Override
    public void onClick(View v) {
        switch (v.getId()) {
            case R.id.customButton:
                Log.d(TAG, ">>>> CustomButton >> onClick!");
                break;
            case R.id.customLayout:
                Log.d(TAG, ">>>> CustomLayout >> onClick!");
                break;
        }
    }

    @Override
    public boolean onTouch(View v, MotionEvent event) {
        if (v.getId() == R.id.customButton) {
            switch (event.getAction()){
                case MotionEvent.ACTION_DOWN:
                    Log.d(TAG, "CustomButton >>>> onTouch >>>> DOWN");
                    break;
                case MotionEvent.ACTION_MOVE:
                    Log.d(TAG, "CustomButton >>>> onTouch >>>> MOVE");
                    break;
                case MotionEvent.ACTION_UP:
                    Log.d(TAG, "CustomButton >>>> onTouch >>>> UP");
                    break;
            }
        } else if (v.getId() == R.id.customLayout){
            switch (event.getAction()){
                case MotionEvent.ACTION_DOWN:
                    Log.d(TAG, "CustomLayout >>>> onTouch >>>> DOWN");
                    break;
                case MotionEvent.ACTION_MOVE:
                    Log.d(TAG, "CustomLayout >>>> onTouch >>>> MOVE");
                    break;
                case MotionEvent.ACTION_UP:
                    Log.d(TAG, "CustomLayout >>>> onTouch >>>> UP");
                    break;
            }
        }
        return false;
    }
}
```

启动这个demo后点击`CustomButton`得到的日志如下
```
05-30 15:32:59.304 2310-2310/com.icedcap.viewtestdemo D/SjActivity:  >>>> SjActivity >> dispatchTouchEvent >>> DOWN
05-30 15:32:59.309 2310-2310/com.icedcap.viewtestdemo D/CustomLayout:  >>>> dispatchTouchEvent >>>> DOWN
05-30 15:32:59.309 2310-2310/com.icedcap.viewtestdemo D/CustomButton: >>>> dispatchTouchEvent >>> DOWN
05-30 15:32:59.310 2310-2310/com.icedcap.viewtestdemo D/SjActivity: CustomButton >>>> onTouch >>>> DOWN
05-30 15:32:59.310 2310-2310/com.icedcap.viewtestdemo D/CustomButton: >>>> onTouchEvent >>> DOWN
05-30 15:32:59.362 2310-2310/com.icedcap.viewtestdemo D/SjActivity:  >>>> SjActivity >> dispatchTouchEvent >>> UP
05-30 15:32:59.362 2310-2310/com.icedcap.viewtestdemo D/CustomLayout:  >>>> dispatchTouchEvent >>>> UP
05-30 15:32:59.363 2310-2310/com.icedcap.viewtestdemo D/CustomButton: >>>> dispatchTouchEvent >>> UP
05-30 15:32:59.363 2310-2310/com.icedcap.viewtestdemo D/SjActivity: CustomButton >>>> onTouch >>>> UP
05-30 15:32:59.363 2310-2310/com.icedcap.viewtestdemo D/CustomButton: >>>> onTouchEvent >>> UP
05-30 15:32:59.366 2310-2310/com.icedcap.viewtestdemo D/SjActivity: >>>> CustomButton >> onClick!
```

从日志可以看出，事件`DOWN`首先从`Activity`中的`dispatchTouchEvent`方法中发出，接着到达视图层级的第一层`CustomLayout`，再到下一层`CustomButton`的`dispatchTouchEvent`。由于这一层已经是视图层级的最后一层了，日志中没有看到继续再往下一层分发反而是回调了在`Activity`中添加的`onTouch`事件。之后才调用`CustomButton`中的`onTouchEvent`方法。这样`ACTION_DOWN`事件就结束了，紧接着是`ACTION_UP`事件的传递过程和`ACTION_DOWN`过程一样，到最后才去回调`CustomButton`的`onClick`方法。从日志输出来看，这是一个典型的点击事件的在视图层级和`Activity`之间的传递过程。至于为什么会这样传递，还是要回归源码来找答案。

## 源码分析
先从`Activity`的`dispatchTouchEvent`方法入手：
```java
    /**
     * Called to process touch screen events.  You can override this to
     * intercept all touch screen events before they are dispatched to the
     * window.  Be sure to call this implementation for touch screen events
     * that should be handled normally.
     *
     * @param ev The touch screen event.
     *
     * @return boolean Return true if this event was consumed.
     */
    public boolean dispatchTouchEvent(MotionEvent ev) {
        if (ev.getAction() == MotionEvent.ACTION_DOWN) {
            onUserInteraction();
        }
        if (getWindow().superDispatchTouchEvent(ev)) {
            return true;
        }
        return onTouchEvent(ev);
    }
```

从注释可以看出，该方法是屏幕事件的入口。如果想需要在将事件分发到`window`之前就拦截该事件，可以在子类中重写该方法。返回`true`就可以消费掉该事件，也就成功的拦截了该事件。
那么我们就试试在该方法下返回`true`，看看日志会怎么打印。
```java
public class SjActivity extends Activity implements View.OnClickListener, View.OnTouchListener{
    private static final String TAG = "SjActivity";
    ...

    @Override
    public boolean dispatchTouchEvent(MotionEvent ev) {
        switch (ev.getAction()) {
            case MotionEvent.ACTION_DOWN:
                Log.d(TAG, " >>>> SjActivity >> dispatchTouchEvent >>> DOWN");
                break;
            case MotionEvent.ACTION_MOVE:
                Log.d(TAG, " >>>> SjActivity >> dispatchTouchEvent >>> MOVE");
                break;
            case MotionEvent.ACTION_UP:
                Log.d(TAG, " >>>> SjActivity >> dispatchTouchEvent >>> UP");
                break;
        }
        return true;
    }

    ...
}
```

```
05-30 15:57:57.028 2310-2310/com.icedcap.viewtestdemo D/SjActivity:  >>>> SjActivity >> dispatchTouchEvent >>> DOWN
05-30 15:57:57.084 2310-2310/com.icedcap.viewtestdemo D/SjActivity:  >>>> SjActivity >> dispatchTouchEvent >>> UP
```
和注释中说的一模一样，后续视图层级不会收到事件，而视图的`onClick`和`onTouch`事件也得不到回调的机会。所以在开发中如果覆写了该方法还是要注意正常返回是否要拦截事件的逻辑。

继续分析源码，首先由`ACTION_DOEN`事件会调用`onUserInteraction()`方法，该方法是一个空实现，可以由子类来覆写，并且在接收到`ACTION_DOWN`事件后进行相应的操作。

`getWindow().superDispatchTouchEvent(ev)`方法主要是进行自定义`window`的事件分发过程，例如`Dialog`。

最后调用`onTouchEvent`方法。
```java
    /**
     * Called when a touch screen event was not handled by any of the views
     * under it.  This is most useful to process touch events that happen
     * outside of your window bounds, where there is no view to receive it.
     *
     * @param event The touch screen event being processed.
     *
     * @return Return true if you have consumed the event, false if you haven't.
     * The default implementation always returns false.
     */
    public boolean onTouchEvent(MotionEvent event) {
        if (mWindow.shouldCloseOnTouch(this, event)) {
            finish();
            return true;
        }

        return false;
    }
```
从注释来看，如果视图层级中没有任何视图去操作该事件，该方法是非常有用的，主要用于不在`window`范围内的视图。并且它默认都是返回`false`。

当返回`false`时将把事件继续往下一层进行分发。这里直接看`View`的`dispatchTouchEvent`方法。
```java
    /**
     * Pass the touch screen motion event down to the target view, or this
     * view if it is the target.
     *
     * @param event The motion event to be dispatched.
     * @return True if the event was handled by the view, false otherwise.
     */
    public boolean dispatchTouchEvent(MotionEvent event) {
        // If the event should be handled by accessibility focus first.
        if (event.isTargetAccessibilityFocus()) {
            // We don't have focus or no virtual descendant has it, do not handle the event.
            if (!isAccessibilityFocusedViewOrHost()) {
                return false;
            }
            // We have focus and got the event, then use normal event dispatch.
            event.setTargetAccessibilityFocus(false);
        }

        boolean result = false;

        if (mInputEventConsistencyVerifier != null) {
            mInputEventConsistencyVerifier.onTouchEvent(event, 0);
        }

        final int actionMasked = event.getActionMasked();
        if (actionMasked == MotionEvent.ACTION_DOWN) {
            // Defensive cleanup for new gesture
            stopNestedScroll();
        }

        if (onFilterTouchEventForSecurity(event)) {
            //noinspection SimplifiableIfStatement
            ListenerInfo li = mListenerInfo;
            if (li != null && li.mOnTouchListener != null
                    && (mViewFlags & ENABLED_MASK) == ENABLED
                    && li.mOnTouchListener.onTouch(this, event)) {
                result = true;
            }

            if (!result && onTouchEvent(event)) {
                result = true;
            }
        }

        if (!result && mInputEventConsistencyVerifier != null) {
            mInputEventConsistencyVerifier.onUnhandledEvent(event, 0);
        }

        // Clean up after nested scrolls if this is the end of a gesture;
        // also cancel it if we tried an ACTION_DOWN but we didn't want the rest
        // of the gesture.
        if (actionMasked == MotionEvent.ACTION_UP ||
                actionMasked == MotionEvent.ACTION_CANCEL ||
                (actionMasked == MotionEvent.ACTION_DOWN && !result)) {
            stopNestedScroll();
        }

        return result;
    }
```
从代码中可以看到，先是进行聚焦检查，再通过事件`DOWN`的检查来停止当前的滑动效果，这些都不是重点。接下来`onFilterTouchEventForSecurity(event)`进行检查当前`window`是否被覆盖，若没有的话就切入重点了。首先是进行很多条件的判断，`ListenerInfo`类是一个包装了很多监听事件的内部类，其中就包括了`OnTouchListener`和`OnClickListener`，所以一旦为`View`设置了`setOnTouchListener`监听事件的话，`li != null && li.mOnTouchListener != null && (mViewFlags & ENABLED_MASK) == ENABLED && li.mOnTouchListener.onTouch(this, event)`前三个条件都会成立，故该`View`的`onTouch`会被回调的。若在该回调函数中返回`true`就不会再去调用当前的`onTouchEvent`方法了。而在`onTouchEvent`方法中我们有可以看到什么呢？继续追踪源代码。

```java
/**
     * Implement this method to handle touch screen motion events.
     * <p>
     * If this method is used to detect click actions, it is recommended that
     * the actions be performed by implementing and calling
     * {@link #performClick()}. This will ensure consistent system behavior,
     * including:
     * <ul>
     * <li>obeying click sound preferences
     * <li>dispatching OnClickListener calls
     * <li>handling {@link AccessibilityNodeInfo#ACTION_CLICK ACTION_CLICK} when
     * accessibility features are enabled
     * </ul>
     *
     * @param event The motion event.
     * @return True if the event was handled, false otherwise.
     */
    public boolean onTouchEvent(MotionEvent event) {
        ...

        if (((viewFlags & CLICKABLE) == CLICKABLE ||
                (viewFlags & LONG_CLICKABLE) == LONG_CLICKABLE)) {
            switch (event.getAction()) {
                case MotionEvent.ACTION_UP:
                    boolean prepressed = (mPrivateFlags & PFLAG_PREPRESSED) != 0;
                    if ((mPrivateFlags & PFLAG_PRESSED) != 0 || prepressed) {
                        // take focus if we don't have it already and we should in
                        // touch mode.
                        boolean focusTaken = false;
                        if (isFocusable() && isFocusableInTouchMode() && !isFocused()) {
                            focusTaken = requestFocus();
                        }

                        if (prepressed) {
                            // The button is being released before we actually
                            // showed it as pressed.  Make it show the pressed
                            // state now (before scheduling the click) to ensure
                            // the user sees it.
                            setPressed(true, x, y);
                       }

                        if (!mHasPerformedLongPress) {
                            // This is a tap, so remove the longpress check
                            removeLongPressCallback();

                            // Only perform take click actions if we were in the pressed state
                            if (!focusTaken) {
                                // Use a Runnable and post this rather than calling
                                // performClick directly. This lets other visual state
                                // of the view update before click actions start.
                                if (mPerformClick == null) {
                                    mPerformClick = new PerformClick();
                                }
                                if (!post(mPerformClick)) {
                                    performClick();
                                }
                            }
                        }

                        if (mUnsetPressedState == null) {
                            mUnsetPressedState = new UnsetPressedState();
                        }

                        if (prepressed) {
                            postDelayed(mUnsetPressedState,
                                    ViewConfiguration.getPressedStateDuration());
                        } else if (!post(mUnsetPressedState)) {
                            // If the post failed, unpress right now
                            mUnsetPressedState.run();
                        }

                        removeTapCallback();
                    }
                    break;

                case MotionEvent.ACTION_DOWN:
                    ...
                    break;

                case MotionEvent.ACTION_CANCEL:
                    setPressed(false);
                    removeTapCallback();
                    removeLongPressCallback();
                    break;

                case MotionEvent.ACTION_MOVE:
                    ...
                    break;
            }

            return true;
        }

        return false;
    }        
```

这里代码很长，选取了其中的一部分来分析。这里监听到`ACTION_UP`事件后会调用`performClick`方法。
```java
    /**
     * Call this view's OnClickListener, if it is defined.  Performs all normal
     * actions associated with clicking: reporting accessibility event, playing
     * a sound, etc.
     *
     * @return True there was an assigned OnClickListener that was called, false
     *         otherwise is returned.
     */
    public boolean performClick() {
        final boolean result;
        final ListenerInfo li = mListenerInfo;
        if (li != null && li.mOnClickListener != null) {
            playSoundEffect(SoundEffectConstants.CLICK);
            li.mOnClickListener.onClick(this);
            result = true;
        } else {
            result = false;
        }

        sendAccessibilityEvent(AccessibilityEvent.TYPE_VIEW_CLICKED);
        return result;
    }
```
到这里就真相大白了，`performClick`方法就是进行`onClick`事件回调的入口（当然前提是设置了`OnClickListener`）。

在最开始的demo中，我们为每一个视图层级的和`Activity`的`dispatchTouchEvent`只进行了日志打印工作没有改变其返回的值，直接是默认的调用其父类的`dispatchTouchEvent`方法返回其父类的值。而在分析`Activity`的`dispatchTouchEvent`方法的时候我们在demo中返回了`true`后直接导致了View视图层级没有收到事件也接收不到`onTouch`和`onClick`的回调操作。

这时我们在回过头来看一下`View`的`onTouchEvent`代码，在if判断语句中，只要当前的操作是`CLICKABLE`点击或者`LONG_CLICKABLE`长按最后都会返回`true`继而其对应的`dispatchTouchEvent`就会返回`true`这也意味着该事件不会继续向下传递。

为了验证这个结果，我们在demo中为`CustomLayout`的`dispatchTouchEvent`返回一个`true`，再去看看打印结果。下面给出修改后的代码以及日志输出情况：
```java
public class CustomLayout extends FrameLayout {
    private static final String TAG = "CustomLayout";
    ...

    @Override
    public boolean dispatchTouchEvent(MotionEvent ev) {
        switch (ev.getAction()){
            case MotionEvent.ACTION_DOWN:
                Log.d(TAG, " >>>> dispatchTouchEvent >>>> DOWN");
                break;
            case MotionEvent.ACTION_UP:
                Log.d(TAG, " >>>> dispatchTouchEvent >>>> UP");
                break;
            case MotionEvent.ACTION_MOVE:
                Log.d(TAG, " >>>> dispatchTouchEvent >>>> MOVE");
                break;
        }
//        return super.dispatchTouchEvent(ev);
        return onTouchEvent(ev);
    }

    @Override
    public boolean onTouchEvent(MotionEvent event) {
        switch (event.getAction()){
            case MotionEvent.ACTION_DOWN:
                Log.d(TAG, " >>>> onTouchEvent >>>> DOWN");
                break;
            case MotionEvent.ACTION_MOVE:
                Log.d(TAG, " >>>> onTouchEvent >>>> MOVE");
                break;
            case MotionEvent.ACTION_UP:
                Log.d(TAG, " >>>> onTouchEvent >>>> UP");
                break;
        }
//        return super.onTouchEvent(event);
        return true;
    }
}
```
```
05-30 17:09:30.829 5953-5953/com.icedcap.viewtestdemo D/SjActivity:  >>>> SjActivity >> dispatchTouchEvent >>> DOWN
05-30 17:09:30.829 5953-5953/com.icedcap.viewtestdemo D/CustomLayout:  >>>> dispatchTouchEvent >>>> DOWN
05-30 17:09:30.829 5953-5953/com.icedcap.viewtestdemo D/CustomLayout:  >>>> onTouchEvent >>>> DOWN
05-30 17:09:30.896 5953-5953/com.icedcap.viewtestdemo D/SjActivity:  >>>> SjActivity >> dispatchTouchEvent >>> UP
05-30 17:09:30.896 5953-5953/com.icedcap.viewtestdemo D/CustomLayout:  >>>> dispatchTouchEvent >>>> UP
05-30 17:09:30.896 5953-5953/com.icedcap.viewtestdemo D/CustomLayout:  >>>> onTouchEvent >>>> UP
```
和分析的结果一样，如果在`CustomLayout`的`dispatchTouchEvent`方法中返回`true`（这也意味着在该视图层级的`onTouchEvent`中消费了这个事件，否则这是无意义的事情）时，事件将不会继续向下传递。

## ViewGroup事件分发与处理
现在我们假设在`CustomLayout`类的`dispatchTouchEvent`方法中接收到`ACTION_DOWN`事件后直接返回`true`接收其他的动作还是继续派发。如下代码所示
```java
    @Override
    public boolean dispatchTouchEvent(MotionEvent ev) {
        switch (ev.getAction()){
            case MotionEvent.ACTION_DOWN:
                Log.d(TAG, " >>>> dispatchTouchEvent >>>> DOWN");
            return true;
//                break;
            case MotionEvent.ACTION_UP:
                Log.d(TAG, " >>>> dispatchTouchEvent >>>> UP");
                break;
            case MotionEvent.ACTION_MOVE:
                Log.d(TAG, " >>>> dispatchTouchEvent >>>> MOVE");
                break;
        }
        return super.dispatchTouchEvent(ev);
    }
```

按照常理来说事件传递顺序应该是这样的：Activity（d : D） -> CustomLayout(d : D);Activity(d : U) -> CustomLayout(d : U) -> CustomButton(d : U) -> Activity(onTouch : U) -> CustomButton(t : U) -> Activity(onClick)
> (d : D) 代表 `dispatchTouchEvent`和`ACTION_DOWN`
> (t : U) 代表`onTouchEvent`和`ACTION_UP`

那么我们看一下日志，事件到底是怎么传递的呢？
```
05-30 17:29:11.636 32280-32280/com.icedcap.viewtestdemo D/SjActivity:  >>>> SjActivity >> dispatchTouchEvent >>> DOWN
05-30 17:29:11.636 32280-32280/com.icedcap.viewtestdemo D/CustomLayout:  >>>> dispatchTouchEvent >>>> DOWN
05-30 17:29:11.694 32280-32280/com.icedcap.viewtestdemo D/SjActivity:  >>>> SjActivity >> dispatchTouchEvent >>> UP
05-30 17:29:11.694 32280-32280/com.icedcap.viewtestdemo D/CustomLayout:  >>>> dispatchTouchEvent >>>> UP
05-30 17:29:11.695 32280-32280/com.icedcap.viewtestdemo D/SjActivity: CustomLayout >>>> onTouch >>>> UP
05-30 17:29:11.695 32280-32280/com.icedcap.viewtestdemo D/CustomLayout:  >>>> onTouchEvent >>>> UP
```
`ACTION_DOWN`事件和想象的一样，但是对于`ACTION_UP`事件来说，它没有传递到下一个视图层级而是直接由`CustomLayout`的`onTouchEvent`消费掉。这又是为什么呢？看来真相还得去看源代码。`ViewGroup`覆写了`View`的`dispatchTouchEvent`方法，我们就看看到底在这里搞了什么鬼。

```java
    @Override
    public boolean dispatchTouchEvent(MotionEvent ev) {
        if (mInputEventConsistencyVerifier != null) {
            mInputEventConsistencyVerifier.onTouchEvent(ev, 1);
        }

        // If the event targets the accessibility focused view and this is it, start
        // normal event dispatch. Maybe a descendant is what will handle the click.
        if (ev.isTargetAccessibilityFocus() && isAccessibilityFocusedViewOrHost()) {
            ev.setTargetAccessibilityFocus(false);
        }

        boolean handled = false;
        if (onFilterTouchEventForSecurity(ev)) {
            final int action = ev.getAction();
            final int actionMasked = action & MotionEvent.ACTION_MASK;

            // Handle an initial down.
            if (actionMasked == MotionEvent.ACTION_DOWN) {
                // Throw away all previous state when starting a new touch gesture.
                // The framework may have dropped the up or cancel event for the previous gesture
                // due to an app switch, ANR, or some other state change.
                cancelAndClearTouchTargets(ev);
                resetTouchState();
            }

            // Check for interception.
            final boolean intercepted;
            if (actionMasked == MotionEvent.ACTION_DOWN
                    || mFirstTouchTarget != null) {
                final boolean disallowIntercept = (mGroupFlags & FLAG_DISALLOW_INTERCEPT) != 0;
                if (!disallowIntercept) {
                    intercepted = onInterceptTouchEvent(ev);
                    ev.setAction(action); // restore action in case it was changed
                } else {
                    intercepted = false;
                }
            } else {
                // There are no touch targets and this action is not an initial down
                // so this view group continues to intercept touches.
                intercepted = true;
            }

            // If intercepted, start normal event dispatch. Also if there is already
            // a view that is handling the gesture, do normal event dispatch.
            if (intercepted || mFirstTouchTarget != null) {
                ev.setTargetAccessibilityFocus(false);
            }

            // Check for cancelation.
            final boolean canceled = resetCancelNextUpFlag(this)
                    || actionMasked == MotionEvent.ACTION_CANCEL;

            // Update list of touch targets for pointer down, if needed.
            final boolean split = (mGroupFlags & FLAG_SPLIT_MOTION_EVENTS) != 0;
            TouchTarget newTouchTarget = null;
            boolean alreadyDispatchedToNewTouchTarget = false;
            if (!canceled && !intercepted) {

                // If the event is targeting accessiiblity focus we give it to the
                // view that has accessibility focus and if it does not handle it
                // we clear the flag and dispatch the event to all children as usual.
                // We are looking up the accessibility focused host to avoid keeping
                // state since these events are very rare.
                View childWithAccessibilityFocus = ev.isTargetAccessibilityFocus()
                        ? findChildWithAccessibilityFocus() : null;

                if (actionMasked == MotionEvent.ACTION_DOWN
                        || (split && actionMasked == MotionEvent.ACTION_POINTER_DOWN)
                        || actionMasked == MotionEvent.ACTION_HOVER_MOVE) {
                    final int actionIndex = ev.getActionIndex(); // always 0 for down
                    final int idBitsToAssign = split ? 1 << ev.getPointerId(actionIndex)
                            : TouchTarget.ALL_POINTER_IDS;

                    // Clean up earlier touch targets for this pointer id in case they
                    // have become out of sync.
                    removePointersFromTouchTargets(idBitsToAssign);

                    final int childrenCount = mChildrenCount;
                    if (newTouchTarget == null && childrenCount != 0) {
                        final float x = ev.getX(actionIndex);
                        final float y = ev.getY(actionIndex);
                        // Find a child that can receive the event.
                        // Scan children from front to back.
                        final ArrayList<View> preorderedList = buildOrderedChildList();
                        final boolean customOrder = preorderedList == null
                                && isChildrenDrawingOrderEnabled();
                        final View[] children = mChildren;
                        for (int i = childrenCount - 1; i >= 0; i--) {
                            final int childIndex = customOrder
                                    ? getChildDrawingOrder(childrenCount, i) : i;
                            final View child = (preorderedList == null)
                                    ? children[childIndex] : preorderedList.get(childIndex);

                            // If there is a view that has accessibility focus we want it
                            // to get the event first and if not handled we will perform a
                            // normal dispatch. We may do a double iteration but this is
                            // safer given the timeframe.
                            if (childWithAccessibilityFocus != null) {
                                if (childWithAccessibilityFocus != child) {
                                    continue;
                                }
                                childWithAccessibilityFocus = null;
                                i = childrenCount - 1;
                            }

                            if (!canViewReceivePointerEvents(child)
                                    || !isTransformedTouchPointInView(x, y, child, null)) {
                                ev.setTargetAccessibilityFocus(false);
                                continue;
                            }

                            newTouchTarget = getTouchTarget(child);
                            if (newTouchTarget != null) {
                                // Child is already receiving touch within its bounds.
                                // Give it the new pointer in addition to the ones it is handling.
                                newTouchTarget.pointerIdBits |= idBitsToAssign;
                                break;
                            }

                            resetCancelNextUpFlag(child);
                            if (dispatchTransformedTouchEvent(ev, false, child, idBitsToAssign)) {
                                // Child wants to receive touch within its bounds.
                                mLastTouchDownTime = ev.getDownTime();
                                if (preorderedList != null) {
                                    // childIndex points into presorted list, find original index
                                    for (int j = 0; j < childrenCount; j++) {
                                        if (children[childIndex] == mChildren[j]) {
                                            mLastTouchDownIndex = j;
                                            break;
                                        }
                                    }
                                } else {
                                    mLastTouchDownIndex = childIndex;
                                }
                                mLastTouchDownX = ev.getX();
                                mLastTouchDownY = ev.getY();
                                newTouchTarget = addTouchTarget(child, idBitsToAssign);
                                alreadyDispatchedToNewTouchTarget = true;
                                break;
                            }

                            // The accessibility focus didn't handle the event, so clear
                            // the flag and do a normal dispatch to all children.
                            ev.setTargetAccessibilityFocus(false);
                        }
                        if (preorderedList != null) preorderedList.clear();
                    }

                    if (newTouchTarget == null && mFirstTouchTarget != null) {
                        // Did not find a child to receive the event.
                        // Assign the pointer to the least recently added target.
                        newTouchTarget = mFirstTouchTarget;
                        while (newTouchTarget.next != null) {
                            newTouchTarget = newTouchTarget.next;
                        }
                        newTouchTarget.pointerIdBits |= idBitsToAssign;
                    }
                }
            }

            // Dispatch to touch targets.
            if (mFirstTouchTarget == null) {
                // No touch targets so treat this as an ordinary view.
                handled = dispatchTransformedTouchEvent(ev, canceled, null,
                        TouchTarget.ALL_POINTER_IDS);
            } else {
                // Dispatch to touch targets, excluding the new touch target if we already
                // dispatched to it.  Cancel touch targets if necessary.
                TouchTarget predecessor = null;
                TouchTarget target = mFirstTouchTarget;
                while (target != null) {
                    final TouchTarget next = target.next;
                    if (alreadyDispatchedToNewTouchTarget && target == newTouchTarget) {
                        handled = true;
                    } else {
                        final boolean cancelChild = resetCancelNextUpFlag(target.child)
                                || intercepted;
                        if (dispatchTransformedTouchEvent(ev, cancelChild,
                                target.child, target.pointerIdBits)) {
                            handled = true;
                        }
                        if (cancelChild) {
                            if (predecessor == null) {
                                mFirstTouchTarget = next;
                            } else {
                                predecessor.next = next;
                            }
                            target.recycle();
                            target = next;
                            continue;
                        }
                    }
                    predecessor = target;
                    target = next;
                }
            }

            // Update list of touch targets for pointer up or cancel, if needed.
            if (canceled
                    || actionMasked == MotionEvent.ACTION_UP
                    || actionMasked == MotionEvent.ACTION_HOVER_MOVE) {
                resetTouchState();
            } else if (split && actionMasked == MotionEvent.ACTION_POINTER_UP) {
                final int actionIndex = ev.getActionIndex();
                final int idBitsToRemove = 1 << ev.getPointerId(actionIndex);
                removePointersFromTouchTargets(idBitsToRemove);
            }
        }

        if (!handled && mInputEventConsistencyVerifier != null) {
            mInputEventConsistencyVerifier.onUnhandledEvent(ev, 1);
        }
        return handled;
    }
```

当接收事件为`actionMasked == MotionEvent.ACTION_DOWN`时会调用`cancelAndClearTouchTargets`和`resetTouchState`分别用于清除touch目标和重置touch状态。这里维护了一个`mFirstTouchTarget`成员变量来用于清除touch目标和touch状态。

接下来会通过`actionMasked == MotionEvent.ACTION_DOWN || mFirstTouchTarget != null`两个条件判断是否拦截当前的事件，第一个条件很好理解但是对于`mFirstTouchTarget != null`是什么意思呢？现在暂时看不出来，那么我们继续往下看。

先略过中间这大段，直接看判断语句`if (mFirstTouchTarget == null) {...} else {...}`这段是将事件向子视图进行分发的逻辑，可以看到当事件由`ViewGroup`子元素成功处理时，`mFirstTouchTarget`会被赋值。这时候在回过头看，如果一旦由`ViewGroup`将事件拦截了`mFirstTouchTarget`必然不会被赋值因此就不会满足`mFirstTouchTarget != null`条件。当除`ACTION_DOWN`之外的事件传进来的时候就不会去调用`onInterceptTouchEvent`方法。该方法正式`ViewGroup`进行拦截事件的重要方法，但是从上面的分析中得出：如果在`ACTION_DOWN`事件中就返回`true`那么接下来的事件序列将不会在调用`onInterceptTouchEvent`方法，而是直接默认拦截该事件。所以在开发中，如果要判断滑动事件满足某一条件时进行拦截操作的话，一定不能在`onInterceptTouchEvent`方法的`ACTION_DOWN`事件的时候就返回`true`。

在`ViewGroup`中默认的`onInterceptTouchEvent`方法至返回`false`。拦截操作要在子类中完成。
```java
    public boolean onInterceptTouchEvent(MotionEvent ev) {
        return false;
    }
```
上述分析的结果也正好吻合我们日志中打印的结果，我们在`CustomLayout`中`dispatchTouchEvent`的`ACTION_DOWN`事件下返回了`true`，这就意味着要拦截当前的事件，导致`mFirstTouchTarget == null`，在之后的事件序列中也默认的走`else { intercepted = true; }`的代码块，也就是拦截了。

接下来看一看`ViewGroup`不拦截事件的时候，它是怎么交给子`View`进行处理的。首先通过遍历拿到子元素`for (int i = childrenCount - 1; i >= 0; i--) {...}`在循环代码块中进行一系列的判断包括子元素是否在播放动画或者点击坐标是否在子元素区域内。如果子元素满足了这两个条件，就会将事件传递给该子元素。

`dispatchTransformedTouchEvent`方法是将事件传递给子元素的入口，我们看一下具体代码：
```java
    /**
     * Transforms a motion event into the coordinate space of a particular child view,
     * filters out irrelevant pointer ids, and overrides its action if necessary.
     * If child is null, assumes the MotionEvent will be sent to this ViewGroup instead.
     */
    private boolean dispatchTransformedTouchEvent(MotionEvent event, boolean cancel,
            View child, int desiredPointerIdBits) {
        final boolean handled;

        ...

        // Perform any necessary transformations and dispatch.
        if (child == null) {
            handled = super.dispatchTouchEvent(transformedEvent);
        } else {
            final float offsetX = mScrollX - child.mLeft;
            final float offsetY = mScrollY - child.mTop;
            transformedEvent.offsetLocation(offsetX, offsetY);
            if (! child.hasIdentityMatrix()) {
                transformedEvent.transform(child.getInverseMatrix());
            }

            handled = child.dispatchTouchEvent(transformedEvent);
        }

        // Done.
        transformedEvent.recycle();
        return handled;
    }
```

经过以上源码+Demo的分析我们知道了View事件分发机制，接下来就[上篇博客](http://icedcap.github.io/2016/05/21/%E9%80%9A%E8%BF%87%E6%A8%A1%E4%BB%BF%E6%9C%80%E7%BE%8E%E5%BA%94%E7%94%A8%E8%AF%A6%E6%83%85%E9%A1%B5%E6%9D%A5%E8%B0%88%E8%B0%88%E5%AE%89%E5%8D%93%E4%B8%ADView%E6%BB%91%E5%8A%A8%E8%A7%A3%E5%86%B3%E6%96%B9%E6%A1%88/)中的自定义滑动控件的bug进行修复。

## 实践开发
上篇博客中自定义滑动View存在这样一个bug，当手指按到中间的按钮区域的时候在进行滑动将会出现滑不动的情况。经过上述对View事件分发机制的了解，很容易就知道产生这个bug的原因。

由于没有在自定义`ViewGroup`进行事件拦截操作，当手指点击到按钮区域时候将会被按钮的`onTouchEvent`消费该事件，故在传入`ACTION_UP`事件的时候也会被按钮区域的`View`消费掉。所以我们在`StretchScrollView`类中完善`onInterceptTouchEvent`方法。
```java
    @Override
    public boolean onInterceptTouchEvent(MotionEvent ev) {
        boolean intercept = false;
        switch (ev.getAction()) {
            case MotionEvent.ACTION_DOWN:
                intercept = false;
                if (!mOverScroller.isFinished()) {
                    mOverScroller.abortAnimation();
                    intercept = true;
                }
                break;
            case MotionEvent.ACTION_MOVE:
                int x = (int) ev.getX();
                int y = (int) ev.getY();
                int deltaX = mLastX - x;
                int deltaY = mLastY - y;
                intercept = Math.abs(deltaX) < Math.abs(deltaY);
                break;
            case MotionEvent.ACTION_CANCEL:
            case MotionEvent.ACTION_UP:
                intercept = false;
                break;
        }
        mLastX = (int) ev.getX();
        mLastY = (int) ev.getY();
        return intercept;
    }
```
在`MotionEvent.ACTION_MOVE`事件中，判断是否上下滑动，如果是就拦截该事件进行上下滑动的操作。这样就解决了手指按住按钮区域时无法滑动的bug。

#总结
以上就是android中View事件分发机制的过程分析，由于代码繁多且复杂，有些方法以及逻辑还是不能全部搞懂。但是通过以上的分析对于实践开发已经足够了。
1. Android事件分发首先由`Activity`开始到`window`的视图层级，进行一层一层的分发。
2. 事件通过`dispatchTouchEvent`方法进行分发，可以通过`onTouchEvent`进行消费工作，对于`ViewGroup`来说可以通过`onInterceptTouchEvent`进行事件拦截操作。
3. 如果在`ViewGroup`把`ACTION_DOWN`事件拦截了，那么后续的事件序列默认都将被该`ViewGroup`拦截并且不会再去调用`onInterceptTouchEvent`方法来判断是否拦截。
4. `onTouch`回调要先于`onTouchEvent`被调用，它是在`dispatchTouchEvent`方法体中被调用的。而`onClick`事件是在最后才被调用，它的调用时机是在`onTouchEvent`方法体中。

# 参考
- [PRE_andevcon_mastering-the-android-touch-system.pdf](http://trinea.github.io/download/pdf/android/PRE_andevcon_mastering-the-android-touch-system.pdf)
- [http://www.infoq.com/cn/articles/android-event-delivery-mechanism/](http://www.infoq.com/cn/articles/android-event-delivery-mechanism/)
