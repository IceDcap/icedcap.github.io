---
title: 深入理解Handler机制
date: 2016-05-12 22:12:49
tags: [android, Handler]
categories: [android]
---
<p style="text-align: center;">
<img src="http://icedcap.github.io/pic/handler_header.jpg">
</p>

## Handler机制概述
Handler是安卓框架中消息机制的核心，在开发中用到最多的就是通过消息传递通知主线程进行UI操作，比如UI更新，view事件等。
<!-- more -->

### 引入Handler机制的原因

安卓应用启动时，系统会创建一个主线程（一个应用的启动入口位于 *frameworks/base/core/java/android/app/ActivityThread.java* 的`main`方法中）。在该线程中会进行UI组件的加载、更新以及事件响应等与UI相关的操作，所以通常情况下该线程也被称为UI线程。那么为什么非得在该线程下进行UI相关的操作呢？其实这与安卓特性和线程安全有关，作为手机界面直接与用户交互的话就要保证每一个UI组件的唯一性和确定性，所以对于UI组件以及相关View类来说，它不是线程安全的。Java在多线程中解决不是线程安全的方法就是加锁，如果将加锁机制引入到Android框架中势必又增加了开发的复杂性并且容易出错。基于上述两点，安卓框架的设计就是在单一线程（主线程或UI线程）中进行UI操作。

到了实际开发中经常要进行耗时操作例如请求网络、从磁盘中加载数据等。为了提高用户体验，这些操作不可能放进UI线程中进行操作，因为这样肯定会阻塞UI线程造成界面的卡顿。这样就要引入多线程将耗时操作放到`work`线程中，等到数据或者网络请求完成后进行UI的更新操作时不能就在当前的线程中进行而要移步到主线程中进行操作，不然都话就要报错了，因为在`ViewRootImpl`类中会进行线程检查。

```java
    void checkThread() {
        if (mThread != Thread.currentThread()) {
            throw new CalledFromWrongThreadException(
                    "Only the original thread that created a view hierarchy can touch its views.");
        }
    }
```

总结一下，安卓中主线程中进行UI操作为了确保用户操作的流畅性，在`work`线程中进行耗时操作不至于让用户在视觉上感觉到程序运行缓慢。为了连接这两种线程之间的通信我们引入消息机制即handler机制。简单的说，Handler机制就是将`work`线程中的消息转发到UI线程中进行操作（当然这是最常用到的，也有其他形式的消息发送与接收的实例）。

### Handler机制的工作原理

Handler机制其实由三个类组成，它们分别是`Handler` `MessageQueue` 和 `Looper`。它们之间的关系就如同工厂车间生产零件和包装零件的过程，工厂中有两个车间一个是零件包装车间一个是零件生产车间它们分别代表两个线程，包装车间的工人只能在该车间中进行零件的包装工作，生产车间的工人进行着耗时的操作（生产零件），在两个车间之间有一条传送带，它每时每刻地都在循环的运转，负责将生产出的零件传送至包装车间供给包装车间的工人进行操作。在这个过程中，零件相当于`Message`，传送带相当于`Looper`，传送带上的所有零件又组成了`MessageQueue`，当传送带上的一个零件传送到包装车间时，该车间的工人取得这个零件并且对该零件进行操作，这个操作动作就是由`Handler`来完成的。由于生产车间工人短缺造成生产一个零件耗时较长，这时候传送带上（`MessageQueue`）没有零件（`Message`），传送带依然在不停的进行循环传送（`Looper`）的工作。当生产车间生产出一个零件（`Message`）时，将它放到传送带上进行传送（`send`），这里传送的目的地是包装车间（`MainThread`），生产车间的工人（`WorkThrad`）不关心其目的地而是全部交由传送带（`Looper`）控制，所以`Looper`对象的初始化很重要。在应用启动的时候我们可以看到已经为主线程初始化了`Looper`并且运转了该`Looper`

```java
    public static void main(String[] args) {
        SamplingProfilerIntegration.start();

        // CloseGuard defaults to true and can be quite spammy.  We
        // disable it here, but selectively enable it later (via
        // StrictMode) on debug builds, but using DropBox, not logs.
        CloseGuard.setEnabled(false);

        Environment.initForCurrentUser();

        // Set the reporter for event logging in libcore
        EventLogger.setReporter(new EventLoggingReporter());

        Security.addProvider(new AndroidKeyStoreProvider());

        // Make sure TrustedCertificateStore looks in the right place for CA certificates
        final File configDir = Environment.getUserConfigDirectory(UserHandle.myUserId());
        TrustedCertificateStore.setDefaultUserDirectory(configDir);

        Process.setArgV0("<pre-initialized>");

        Looper.prepareMainLooper(); //初始化主Looper

        ActivityThread thread = new ActivityThread();
        thread.attach(false);

        if (sMainThreadHandler == null) {
            sMainThreadHandler = thread.getHandler();
        }

        if (false) {
            Looper.myLooper().setMessageLogging(new
                    LogPrinter(Log.DEBUG, "ActivityThread"));
        }

        Looper.loop(); //启动该Looper

        throw new RuntimeException("Main thread loop unexpectedly exited");
    }
```

所以这也是为什么我们在主线程中使用Handler时不需要初始化Looper的原因了。如果我们不是在主线程中去应用Handler时，一定要初始化该线程的Looper最后启动Looper来保证Handler能接收到消息。

接下来就从源码角度具体看一看Handler机制的工作原理。首先看一下`Handler`的构造器

```java
    public Handler() {
        this(null, false);
    }

    public Handler(Callback callback) {
        this(callback, false);
    }

    public Handler(Looper looper) {
        this(looper, null, false);
    }

    public Handler(Looper looper, Callback callback) {
        this(looper, callback, false);
    }

    public Handler(boolean async) {
        this(null, async);
    }

    public Handler(Callback callback, boolean async) {
        if (FIND_POTENTIAL_LEAKS) {
            final Class<? extends Handler> klass = getClass();
            if ((klass.isAnonymousClass() || klass.isMemberClass() || klass.isLocalClass()) &&
                    (klass.getModifiers() & Modifier.STATIC) == 0) {
                Log.w(TAG, "The following Handler class should be static or leaks might occur: " +
                        klass.getCanonicalName());
            }
        }

        mLooper = Looper.myLooper();
        if (mLooper == null) {
            throw new RuntimeException(
                    "Can't create handler inside thread that has not called Looper.prepare()");
        }
        mQueue = mLooper.mQueue;
        mCallback = callback;
        mAsynchronous = async;
    }

    public Handler(Looper looper, Callback callback, boolean async) {
        mLooper = looper;
        mQueue = looper.mQueue;
        mCallback = callback;
        mAsynchronous = async;
    }
```

框架中对外提供的API只有前五个最后两个是隐藏的。其实这五个构造器也都是调用最后两个，我们把精力放到最后两个构造方法上就可以了。可以看到在初始化Handler的时候要求我们必须初始`Looper`否则会产生一个`RuntimeException`这正是我们之前分析的`Looper`控制着`Message`接收方向，如果没有`Looper`就不能接收`Message`从而`Handler`就没有意义。纵观这五个构造方法涉及到三个参数`CallBack` `Looper`和标记量`async`。`async`是异步操作的标示而`Callback`是一个回调接口给出代码后大家就很熟悉了它和我们经常使用的Handler中覆写`handlerMessage`的方法同名，其作用也是一样的操作接收到的`Message`消息。

```java
    /**
     * Callback interface you can use when instantiating a Handler to avoid
     * having to implement your own subclass of Handler.
     *
     * @param msg A {@link android.os.Message Message} object
     * @return True if no further handling is desired
     */
    public interface Callback {
        public boolean handleMessage(Message msg);
    }
```

接下来我们将关注的焦点放在`Looper`上，分析完`Looper`之后再回来看`Handler`。
打开`Looper`源码（*frameworks/base/core/java/android/os/Looper.java*）首先看到是注释部分，原话这里就不列出了，它主要讲的是`Looper`的用法，翻译成大白话就是：`Looper`类是用于在线程中循环一个消息队列。默认情况下一个线程是不会主动和一个消息`Looper`进行关联的；为了创建一个`Looper`需要在线程中调用`prepear`并且使用`looper`方法使消息队列运转起来。大多数情况下消息`Looper`和`Handler`直接交互，下面是一个例子展示了`Looper`的创建与`handler`的交互。

```java
    class LooperThread extends Thread {
        public Handler mHandler;

        public void run() {
            Looper.prepare();

            mHandler = new Handler() {
                public void handleMessage(Message msg) {
                    // process incoming messages here
                }
            };

            Looper.loop();
        }
    }
```

接下来我们看一看`prepear`方法。

```java
    public static void prepare() {
        prepare(true);
    }

    private static void prepare(boolean quitAllowed) {
        if (sThreadLocal.get() != null) {
            throw new RuntimeException("Only one Looper may be created per thread");
        }
        sThreadLocal.set(new Looper(quitAllowed));
    }
```

`sThreadLocal`是一个静态final成员变量。

```java
static final ThreadLocal<Looper> sThreadLocal = new ThreadLocal<Looper>();
```

`ThreadLocal`是一个存储器，存储了每一个线程下`Looper`对象。对于不同的线程创建`Looper`对象时，那么对于该线程来说这个`Looper`对象要保证唯一性和原始性，这样才能保证消息`message`的传递被该线程下和该`Looper`关联的`Handler`所接收和处理，从而保证了消息接收的正确性。

```java
    private Looper(boolean quitAllowed) {
        mQueue = new MessageQueue(quitAllowed);
        mThread = Thread.currentThread();
    }
```

接着跟进代码，我们发现`Looper`的构造中将初始化`MessageQueue`并且在成员变量`mthread`中存储当前线程。至此，`Looper`的初始化工作就完成了。下面看一下`loop`方法如何循环运转`MessageQueue`。

```java
    /**
     * Run the message queue in this thread. Be sure to call
     * {@link #quit()} to end the loop.
     */
    public static void loop() {
        final Looper me = myLooper();
        if (me == null) {
            throw new RuntimeException("No Looper; Looper.prepare() wasn't called on this thread.");
        }
        final MessageQueue queue = me.mQueue;

        // Make sure the identity of this thread is that of the local process,
        // and keep track of what that identity token actually is.
        Binder.clearCallingIdentity();
        final long ident = Binder.clearCallingIdentity();

        for (;;) {
            Message msg = queue.next(); // might block
            if (msg == null) {
                // No message indicates that the message queue is quitting.
                return;
            }

            // This must be in a local variable, in case a UI event sets the logger
            Printer logging = me.mLogging;
            if (logging != null) {
                logging.println(">>>>> Dispatching to " + msg.target + " " +
                        msg.callback + ": " + msg.what);
            }

            msg.target.dispatchMessage(msg);

            if (logging != null) {
                logging.println("<<<<< Finished to " + msg.target + " " + msg.callback);
            }

            // Make sure that during the course of dispatching the
            // identity of the thread wasn't corrupted.
            final long newIdent = Binder.clearCallingIdentity();
            if (ident != newIdent) {
                Log.wtf(TAG, "Thread identity changed from 0x"
                        + Long.toHexString(ident) + " to 0x"
                        + Long.toHexString(newIdent) + " while dispatching to "
                        + msg.target.getClass().getName() + " "
                        + msg.callback + " what=" + msg.what);
            }

            msg.recycleUnchecked();
        }
    }
```
很明显，在代码中一个大写的死循环，只有当`msg=null`的情况下才能退出循环。`Message`通过`MessageQueue`获得（稍后再看）该过程有可能被阻塞因为这要取决于消息队列是否有消息，一旦发送了消息就会立即获得`msg`对象并且通过`msg.target.dispatchMessage(msg)`进行转发`msg.target`是一个`Handler`对象，调用`dispatchMessage`方法，在目标线程中进行派发。
```java
    /**
     * Handle system messages here.
     */
    public void dispatchMessage(Message msg) {
        if (msg.callback != null) {
            handleCallback(msg);
        } else {
            if (mCallback != null) {
                if (mCallback.handleMessage(msg)) {
                    return;
                }
            }
            handleMessage(msg);
        }
    }
```
看到这里是不是有一种豁然开朗的感觉呢？我们每次使用`Handler`的时候都会覆写`handleMessage`方法，然而在`Looper`中取得消息后即交由`Handler`的`handleMessage`进行处理。接着核心的东西来了，我们来研究下消息队列存取消息的原理，这里移步到`MessageQueue`类来看。
```java
    Message next() {
        // Return here if the message loop has already quit and been disposed.
        // This can happen if the application tries to restart a looper after quit
        // which is not supported.
        final long ptr = mPtr;
        if (ptr == 0) {
            return null;
        }

        int pendingIdleHandlerCount = -1; // -1 only during first iteration
        int nextPollTimeoutMillis = 0;
        for (;;) {
            if (nextPollTimeoutMillis != 0) {
                Binder.flushPendingCommands();
            }

            nativePollOnce(ptr, nextPollTimeoutMillis);

            synchronized (this) {
                // Try to retrieve the next message.  Return if found.
                final long now = SystemClock.uptimeMillis();
                Message prevMsg = null;
                Message msg = mMessages;
                if (msg != null && msg.target == null) {
                    // Stalled by a barrier.  Find the next asynchronous message in the queue.
                    do {
                        prevMsg = msg;
                        msg = msg.next;
                    } while (msg != null && !msg.isAsynchronous());
                }
                if (msg != null) {
                    if (now < msg.when) {
                        // Next message is not ready.  Set a timeout to wake up when it is ready.
                        nextPollTimeoutMillis = (int) Math.min(msg.when - now, Integer.MAX_VALUE);
                    } else {
                        // Got a message.
                        mBlocked = false;
                        if (prevMsg != null) {
                            prevMsg.next = msg.next;
                        } else {
                            mMessages = msg.next;
                        }
                        msg.next = null;
                        if (DEBUG) Log.v(TAG, "Returning message: " + msg);
                        msg.markInUse();
                        return msg;
                    }
                } else {
                    // No more messages.
                    nextPollTimeoutMillis = -1;
                }

                // Process the quit message now that all pending messages have been handled.
                if (mQuitting) {
                    dispose();
                    return null;
                }

                // If first time idle, then get the number of idlers to run.
                // Idle handles only run if the queue is empty or if the first message
                // in the queue (possibly a barrier) is due to be handled in the future.
                if (pendingIdleHandlerCount < 0
                        && (mMessages == null || now < mMessages.when)) {
                    pendingIdleHandlerCount = mIdleHandlers.size();
                }
                if (pendingIdleHandlerCount <= 0) {
                    // No idle handlers to run.  Loop and wait some more.
                    mBlocked = true;
                    continue;
                }

                if (mPendingIdleHandlers == null) {
                    mPendingIdleHandlers = new IdleHandler[Math.max(pendingIdleHandlerCount, 4)];
                }
                mPendingIdleHandlers = mIdleHandlers.toArray(mPendingIdleHandlers);
            }

            // Run the idle handlers.
            // We only ever reach this code block during the first iteration.
            for (int i = 0; i < pendingIdleHandlerCount; i++) {
                final IdleHandler idler = mPendingIdleHandlers[i];
                mPendingIdleHandlers[i] = null; // release the reference to the handler

                boolean keep = false;
                try {
                    keep = idler.queueIdle();
                } catch (Throwable t) {
                    Log.wtf(TAG, "IdleHandler threw exception", t);
                }

                if (!keep) {
                    synchronized (this) {
                        mIdleHandlers.remove(idler);
                    }
                }
            }

            // Reset the idle handler count to 0 so we do not run them again.
            pendingIdleHandlerCount = 0;

            // While calling an idle handler, a new message could have been delivered
            // so go back and look again for a pending message without waiting.
            nextPollTimeoutMillis = 0;
        }
    }
```
首先来看`MessageQueue`的出队列即取消息，这里也是一个大写的死循环，队列中只要有消息就会取出并且将指针向前移动直到将所有的消息都取出来为止。接着再来看一看消息的入队列的过程。
```java
    boolean enqueueMessage(Message msg, long when) {
        if (msg.target == null) {
            throw new IllegalArgumentException("Message must have a target.");
        }
        if (msg.isInUse()) {
            throw new IllegalStateException(msg + " This message is already in use.");
        }

        synchronized (this) {
            if (mQuitting) {
                IllegalStateException e = new IllegalStateException(
                        msg.target + " sending message to a Handler on a dead thread");
                Log.w(TAG, e.getMessage(), e);
                msg.recycle();
                return false;
            }

            msg.markInUse();
            msg.when = when;
            Message p = mMessages;
            boolean needWake;
            if (p == null || when == 0 || when < p.when) {
                // New head, wake up the event queue if blocked.
                msg.next = p;
                mMessages = msg;
                needWake = mBlocked;
            } else {
                // Inserted within the middle of the queue.  Usually we don't have to wake
                // up the event queue unless there is a barrier at the head of the queue
                // and the message is the earliest asynchronous message in the queue.
                needWake = mBlocked && p.target == null && msg.isAsynchronous();
                Message prev;
                for (;;) {
                    prev = p;
                    p = p.next;
                    if (p == null || when < p.when) {
                        break;
                    }
                    if (needWake && p.isAsynchronous()) {
                        needWake = false;
                    }
                }
                msg.next = p; // invariant: p == prev.next
                prev.next = msg;
            }

            // We can assume mPtr != 0 because mQuitting is false.
            if (needWake) {
                nativeWake(mPtr);
            }
        }
        return true;
    }
```
这里也是很清楚的看到`msg`的入队列的过程，没什么好说的。下面我们寻找所有的入队列的操作，在`Handler`类中
```java
    private boolean enqueueMessage(MessageQueue queue, Message msg, long uptimeMillis) {
        msg.target = this;
        if (mAsynchronous) {
            msg.setAsynchronous(true);
        }
        return queue.enqueueMessage(msg, uptimeMillis);
    }
```
所有的消息发送无论是`sendMessage`还是`postXXX`形式的消息发送最终都是调用`enqueueMessage`入队列方法，交给`Looper`和`MessageQueue`进行消息的递交工作，并且最后派发给`Handler`所在的类中进行消息的消费工作。至此，安卓框架的消息机制就由`Handler` `MessageQueue`和`Looper`完美配合下完成了。通过上述的源码分析可以得出如下图所示的Handler的工作原理。

<p style="text-align: center;">
<img src="pic/handler_structure.png">
</p>

在实际开发中运用该机制在不同线程中进行消息的派发和消耗是一件很惬意的事情。哈哈，主要还是致力于解决在第二节中提到的UI线程和工作线程之间的矛盾冲突，这才是`Handler`真正的用武之地！

## HandlerThread
`HandlerThread`是安卓框架提供的一个自带`Looper`具有循环递交`Message`功能的线程，它位于*frameworks/base/core/java/android/os/HandlerThread.java*下。因为默认（除了主线程，前文已经说明原因）线程是不会绑定`Looper`需要我们手动初始化和启动`Looper`对象。
```java
    @Override
    public void run() {
        mTid = Process.myTid();
        Looper.prepare();
        synchronized (this) {
            mLooper = Looper.myLooper();
            notifyAll();
        }
        Process.setThreadPriority(mPriority);
        onLooperPrepared();
        Looper.loop();
        mTid = -1;
    }
```
`HandlerThread`通过覆写`run`方法并且在其中进行`Looper`初始化和启动工作。并且提供一个`onLooperPrepared`接口方便子类进行`Looper`启动前的工作。

`HandlerThread`的出现使我们很方便进行消息的传递和消费工作，而不需要手动添加`Looper`创建与启动的代码。

## 参考
- [Android的Handler机制原理](http://www.feeyan.cn/?p=17)
- [Handler和他的小伙伴们（上）](http://www.jianshu.com/p/e04698eaba88)
- [Handler和他的小伙伴们（中）](http://www.jianshu.com/p/1d03fe0b285c)