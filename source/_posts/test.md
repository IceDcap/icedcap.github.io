---
title: Android Architecture Collection[转]
date: 2016-04-24 21:58:29
tags: [架构, 合集]
---
> 安卓架构文章合集（a collection of android Architecture）
> 博客原地址：http://www.jianshu.com/p/1f21e1d375aa
> github地址：https://github.com/CameloeAnthony/AndroidArchitectureCollection 
> 欢迎star，fork进行收藏，后续会继续更新。

> 这是从各大平台上参考的android架构文章，主要参考自：
[Juude/Awesome-Android-Architecture](https://github.com/Juude/Awesome-Android-Architecture)

<!-- more -->

# 1 国内各大平台架构：
+ [App工程结构搭建：几种常见Android代码架构分析](http://www.uml.org.cn/mobiledev/201310211.asp)
+ [携程Mobile架构演化(视频)](http://www.infoq.com/cn/presentations/ctrip-mobile-architecture-evolution)
+ [携程Android App插件化和动态加载实践](http://www.infoq.com/cn/articles/ctrip-android-dynamic-loading)
+ [陶钧谈淘宝客户端应用框架实践](http://www.infoq.com/cn/interviews/tj-taobao-client-arch)
+ [QCon旧金山演讲总结：阿里无线技术架构演进](http://www.infoq.com/cn/articles/alibaba-mobile-infrastructure)
+ [手机淘宝构架演化实践](http://www.infoq.com/cn/news/2014/12/taobao-app-evolution)
+ [手机淘宝Android客户端架构](http://www.open-open.com/lib/view/open1436316754208.html)
+ [漫谈移动应用架构设计](http://club.alibabatech.org/resource_detail.htm?topicId=124)
+ [大规模团队的Android开发](http://club.alibabatech.org/resource_detail.htm?topicId=130)
+ [支付宝钱包客户端技术架构](http://club.alibabatech.org/resource_detail.htm?topicId=155)
+ [手机百度Android平台平台化解决方案](http://www.infoq.com/cn/presentations/mobile-baidu-android-platform-solutions)
+ [涅盘新生—Android QQ音乐架构演进](http://www.infoq.com/cn/presentations/evolution-of-android-qq-music-architecture)
+ [微信Android客户端架构演进之路](http://www.infoq.com/cn/articles/wechat-android-app-architecture)
+ [饿了么移动APP的架构演进](https://mp.weixin.qq.com/s?__biz=MzAxNDUwMzU3Mw==&mid=401044540&idx=1&sn=24b7d8fb655ae6dd5d989d0cb3c08e90&scene=2&srcid=0106EtxRjD2jHxzomxVPTwY3&from=timeline&isappinstalled=0&uin=NzgwODIwNDgw&key=&devicetype=webwx&version=70000001&lang=zh_CN&pass_ticket=46hW44w3Hxd7VY9rutz7mgLu1JGe2T1AAKNQpxNoYOSGi8NpmNYr%2BAZj%2BiXtRX2F)

# 2 MVVM & MVP & MVC

+ [ANDROID DATABINDING: GOODBYE PRESENTER, HELLO VIEWMODEL](http://tech.vg.no/2015/07/17/android-databinding-goodbye-presenter-hello-viewmodel/)
（viewmodel，安卓中的databinding）
+ [MVVM-in-Android](http://www.codeproject.com/Articles/166952/MVVM-in-Android)（android中的mvvm）
+ [ ZhiHuMVP github 地址](https://github.com/CameloeAnthony/ZhiHuMVP)（MVP架构思想，Retrofit RESTful API 框架的配合，RxJava 响应式编程）
+ [ androidmvp github地址](https://github.com/antoniolg/androidmvp)（star2000+的MVP实例）
+ [MVP for Android: how to organize the presentation layer](http://antonioleiva.com/mvp-android/)（上面这个github对应的文章）
+ [ Introduction-to-Model-View-Presenter-on-Android](https://github.com/konmik/konmik.github.io/wiki/Introduction-to-Model-View-Presenter-on-Android)（MVP的介绍，MVP必读经典）
+ [Introduction-to-Model-View-Presenter-on-Android 中文翻译版](http://www.jcodecraeer.com/a/anzhuokaifa/androidkaifa/2015/0425/2782.html)
+ [ActivityFragmentMVP github地址](https://github.com/spengilley/ActivityFragmentMVP)（MVP处理Activity和Fragment，使用了Dagger 注入）
+ [ EffectiveAndroidUI github地址](https://github.com/pedrovgs/EffectiveAndroidUI)（star 3000+的mvp，mvvm实例）
+ [ MvpCleanArchitecture github地址](https://github.com/glomadrian/MvpCleanArchitecture)（使用clean architecture 和mvp的实例）
+ [ Material-Movies github地址](https://github.com/saulmm/Material-Movies)（ 使用material design +MVP实现的Material-Movies）
+ [EffectiveAndroid github地址](https://github.com/rallat/EffectiveAndroid)（MVP+clean Architecture 项目）
+ [AndroidMVPDemo github地址](https://github.com/CameloeAnthony/AndroidMVPDemo)（本文作者MVP demo github地址）
+ [MVVM on Android: What You Need to Know](http://willowtreeapps.com/blog/mvvm-on-android-what-you-need-to-know/)(MVVM介绍，这个博客很不错)
+ [data-bingding guide](https://developer.android.com/tools/data-binding/guide.html)（data-binding guide官网）
+ [Web开发的MVVM模式](http://www.cnblogs.com/dxy1982/p/3793895.html)（MVC VS. MVP VS. MVVM）
+ [Android应用开发架构概述](http://www.liuguangli.win/archives/299)
+ [MVVM介绍](http://objccn.io/issue-13-1/)（iOS中MVVM的一种实现，对概念的理解有帮助）
# 3 Clean Architecture
+ [The Clean Architecture](https://blog.8thlight.com/uncle-bob/2012/08/13/the-clean-architecture.html)(clean architecture出处)
+ [Android-CleanArchitecture github地址](https://github.com/android10/Android-CleanArchitecture)（The Clean Architecture文章的例子）
+ [Android Application Architecture原文](https://medium.com/ribot-labs/android-application-architecture-8b6e34acda65#.b29vhtdm2) 
+ [Android Application Architecture中文翻译](http://www.jianshu.com/p/8ca27934c6e6)
+ [Architecting Android…The evolution](http://fernandocejas.com/2015/07/18/architecting-android-the-evolution/)
+ [Architecting Android…The evolution中文翻译](http://www.devtf.cn/?p=1083)

# 4 Flux
* [flux and android](https://armueller.github.io/android/2015/03/29/flux-and-android.html)
* [rxflux android architecture](https://medium.com/swlh/rxflux-android-architecture-94f77c857aa2#.sfjwchwok)
* [why rxflux](https://medium.com/swlh/why-rxflux-5b687f062709#.ltlnlr4cl)
* [android flux todo app](https://github.com/lgvalle/android-flux-todo-app)([中文翻译](http://www.devtf.cn/?p=1028))
* [RxFlux](https://github.com/skimarxall/RxFlux)
* [android-flux](https://github.com/naodroid/android-flux)

# 5 其它
+ [Artchitecture Library](https://github.com/Juude/Awesome-Android-Architecture/blob/master/Library.md)
+ [Design for Offline: Android App Architecture Best Practices](https://plus.google.com/+AndroidDevelopers/posts/3C4GPowmWLb)
+ [Robust and readable architecture for an Android App](http://blog.joanzapata.com/robust-architecture-for-an-android-app/)
+ [Android application architecture](https://events.google.com/io2015/schedule?sid=358c9f91-b6d4-e411-b87f-00155d5066d7#day1/358c9f91-b6d4-e411-b87f-00155d5066d7)
+ [googlesamples/android-architecture](https://github.com/googlesamples/android-architecture)（google官方架构项目）
+ [google官方MVP架构示例项目解析](http://mp.weixin.qq.com/s?__biz=MzA3ODg4MDk0Ng==&mid=403539764&idx=1&sn=d30d89e6848a8e13d4da0f5639100e5f#rd)（上面这个github地址的解析）
+ [jiangqqlmj](https://github.com/jiangqqlmj)/**[FastDev4Android](https://github.com/jiangqqlmj/FastDev4Android)** （android快速开发框架）
+ [Android 开发有什么好的架构么?](https://www.zhihu.com/question/21406685)
+ [如果从0创建一个Android APP，设计思路是什么？（架构、activity、layout等复用性的考虑），感觉无从下手](https://www.zhihu.com/question/28564947)


