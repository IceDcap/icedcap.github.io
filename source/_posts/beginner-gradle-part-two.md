---
title: Gradle基础篇
date: 2016-12-10 21:10:33
tags: [构建工具, Android]
categories: [构建工具]
---

# Gradle构建基础
在AndroidStudio创建一个安卓项目时会自动生成三个Gradle文件，其中两个build.gradle和一个settings.gradle文件。他们的后缀都是.gradle，并且如果在项目中创建一个module也会随之生成一个build.gradle文件。初始化后的这三个gradle文件结构如下所示：
<!--more-->
<p style="text-align: center;">
    <img src="http://icedcap.github.io/2016/12/10/beginner-gradle-part-two/pic/gradle-file-location.png" width="35%">
</p>

- 根目录下的settings.build文件在初始化阶段被执行，并且定义了那些模块应该包含在构建内
    + 本例中只有一个app模块，故只有一行`include ':app'`
    + 若还有其他一些模块，比如mylibrary库，应该为`include ':app', ':mylibrary'`
- 根目录下的build.gradle文件默认会包含两个代码块，分别如下：

```php
buildscript {
    repositories {
        jcenter()
    }
    dependencies {
        classpath 'com.android.tools.build:gradle:2.2.2'

        // NOTE: Do not place your application dependencies here; they belong
        // in the individual module build.gradle files
    }
}

allprojects {
    repositories {
        jcenter()
    }
}
```

实际构建配置在`buildscript`代码块中，`repositories`将jcenter配置为一个仓库，和编译有关的依赖库都是从jcenter仓库中拉取；`dependencies`将配置构建过程中的gradle插件的依赖包，默认情况下只定义Android插件（有了`classpath 'com.android.tools.build:gradle:2.2.2'`这句话后随后的app中的build.gradle文件才可以使用android代码块变量以及一些有关Android的属性）。

`allprojects`代码块可用来声明那些需要用于所有模块的属性，甚至可以在该代码块下创建任务，这些任务最终会被运用到所有模块中。


- app模块下的build.gradle文件所定义的属性或者任务只能应用在该app模块下，它可以覆盖根下的build.gradle文件所声明属性。

默认的AndroidStudio会生成如下代码：

```php
# Android应用插件，根下的build.gradle文件要配置安卓构建工具`classpath 'com.android.tools.build:gradle:2.2.2'`的依赖才能使用
apply plugin: 'com.android.application'

android {
    compileSdkVersion 25 #用来编译应用的Android API版本
    buildToolsVersion "25.0.0" #构建工具和编译器使用的版本号
    #改代码块下的属性会覆盖AndroidManifest中声明的相关属性
    defaultConfig { 
        #覆盖manifest中的packagename，但是它和package name还有不同，它应用在
        #variants多版本构建时至关重要（多版本要有不同的包名才能安装到同一设备上）
        applicationId "com.icedcap.myapplication" 
        minSdkVersion 22 #对应manifest <uses-sdk>
        targetSdkVersion 25 #对应manifest <uses-sdk>
        versionCode 1 #和manifest的该属性意义相同
        versionName "1.0" #和manifest的该属性意义相同
        testInstrumentationRunner "android.support.test.runner.AndroidJUnitRunner"
    }

    # 该代码块用来定义如何构建和打包不同类型的应用，这将在后续详细指出
    buildTypes { 
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
        }
    }
}

# app项目所要依赖的库要在该出声明
dependencies { 
    compile fileTree(dir: 'libs', include: ['*.jar'])
    androidTestCompile('com.android.support.test.espresso:espresso-core:2.2.2', {
        exclude group: 'com.android.support', module: 'support-annotations'
    })
    compile 'com.android.support:appcompat-v7:25.0.1'
    testCompile 'junit:junit:4.12'
}
```


# Gradle任务和简单的自定义构建
谷歌的工程师在开发Android的Gradle插件时也是利用依赖进行开发的。首先Gradle的Android插件使用了Java的基础插件，而Java基础插件又使用了Gradle基础插件，基础插件中定义了任务的标准生命周期和一些共同约定的属性。基础插件中定义了`assemble`和`clean`任务，Java插件定义了`check`和`build`任务。在基础插件中`assemble`和`clean`任务既不被实现，也不执行任何操作，它类似于编程语言中的接口或者是抽象类由依赖该任务的其他插件来具体实现，例如在[Gradle 前传---- Gradle Wrapper](http://icedcap.github.io/2016/12/07/beginner-gradle-part-one/)列出的所有Gradle任务以及它的依赖，其中`app:assemble`要依赖`app:assembleDebug`和`app:assembleRelease`而`app:installDebug`要依赖`app:assembleDebug`。

对于底层插件定义的任务约定如下：

- assemble：集合项目的输出
- clean：清理项目的输出
- check：运行所有的检查，通常是单元测试和集成测试
- build：同时运行assemble和check

而对于安卓Gradle插件来说是在上述约定的基础扩展而来，具体任务约定如下：

- assemble：为每一个构建版本创建一个APK文件
- clean：删除所有的构建内容，例如APK文件以及编译时产生的资源R文件等
- check：运行Lint检查，如果Lint发现问题则停止构建
- build：同时运行assemble和check任务

Android的Gradle插件除了扩展了这四个基础任务之外，还自定义了很多有用的任务，在[Gradle 前传---- Gradle Wrapper](http://icedcap.github.io/2016/12/07/beginner-gradle-part-one/)中也列出了一个Android项目所有的任务以及详细描述和依赖情况。

这里列出几个平时用的比较多的任务：

- connectedCheck：在连接设备或者模拟器上运行测试
- deviceCheck：一个占位任务，专为其他插件在远端设备上运行测试
- installDebug和installRelease：在连接设备上或模拟器上安装特定版本
- uninstallDebug和uninstallRelease：卸载相应的版本

好了，说完了基本的构建任务外再来谈谈简单的自定义构建。

简单的自定义构建也是平时项目中常常用到的比较有灵气的Gradle小技巧，主要包括以下几块内容：

- BuildConfig设置
- 项目范围设置
- 项目属性设置
- 默认任务设置

## BuildConfig设置
从SDK工具升级到17以后，构建工具会在项目中生成一个叫`BuildConfig`的类，默认的使用`generateDebugSources`（点击AndroidStudio的Gradle同步按钮也会执行该任务）构建时，会生成如下信息：

```java
/**
 * Automatically generated file. DO NOT MODIFY
 */
package com.icedcap.myapplication;

public final class BuildConfig {
  public static final boolean DEBUG = Boolean.parseBoolean("true");
  public static final String APPLICATION_ID = "com.icedcap.myapplication";
  public static final String BUILD_TYPE = "debug";
  public static final String FLAVOR = "";
  public static final int VERSION_CODE = 1;
  public static final String VERSION_NAME = "1.0";
}
```

包括`DEBUG` `APPLICATION_ID` `BUILD_TYPE` `FLAVOR` `VERSION_CODE` `VERSION_NAME`所以我们在使用Debug版本时可以引用到该类中的属性。应用在实际场景中，比如构建debug版应用时项目内访问测试服务器，当发布正式版本时要访问正式的服务器，这时候就可以定义两个版本的服务器URL从而在不同版本上使用不同的URL，同理，对于http请求的日志只想在debug版本中看到。

```php
buildTypes {
        debug {
            buildConfigField "String", "APP_URL", "\"http://debug.test.com\""
            buildConfigField "boolean", "LOG_HTTP_CALLS", "true"
            ...
        }
        release {
            buildConfigField "String", "APP_URL", "\"http://release.test.com\""
            buildConfigField "boolean", "LOG_HTTP_CALLS", "false"
            ...
        }
    }
```

**注意：**这里的url地址要使用转移符号将双引号连带地址一并传入BuildConfig类中。

可以看到分别使用assembleDebug和assembleRelease构架时生成的BuildConfig类内容分别如下：

```java
/**
 * Automatically generated file. DO NOT MODIFY
 */
package com.icedcap.myapplication;

public final class BuildConfig {
  public static final boolean DEBUG = Boolean.parseBoolean("true");
  public static final String APPLICATION_ID = "com.icedcap.myapplication";
  public static final String BUILD_TYPE = "debug";
  public static final String FLAVOR = "";
  public static final int VERSION_CODE = 1;
  public static final String VERSION_NAME = "1.0";
  // Fields from build type: debug
  public static final String APP_URL = "http://debug.test.com";
  public static final boolean LOG_HTTP_CALLS = true;
}
```

```java
/**
 * Automatically generated file. DO NOT MODIFY
 */
package com.icedcap.myapplication;

public final class BuildConfig {
  public static final boolean DEBUG = false;
  public static final String APPLICATION_ID = "com.icedcap.myapplication";
  public static final String BUILD_TYPE = "release";
  public static final String FLAVOR = "";
  public static final int VERSION_CODE = 1;
  public static final String VERSION_NAME = "1.0";
  // Fields from build type: release
  public static final String APP_URL = "http://release.test.com";
  public static final boolean LOG_HTTP_CALLS = false;
}
```

## 项目范围设置
针对多模块的Android项目，通常在根目录下的build.gradle文件的`allprojects`代码块进行配置时，它将应用在各个子模块中。

```php
allprojects {
    apply plugin: 'com.android.application'
    android {
        compileSdkVersion 23
        buildToolsVersion "25.0.0"
    }
}
```
因为Gradle允许在Project对象上添加额外的属性，这就意味着任何gradle.build文件都能定义额外的属性，添加额外的属性需要使用`ext`代码块

```php
ext {
    local = "hello world, from buid.gradle"
    compileSdkVersion = 22
    buildToolsVersion = "22.0.1"
}
```

在各个模块的build.gradle文件中可以引用根下build.gradle使用ext声明的变量：

```php
android {
    compileSdkVersion rootProject.ext.compileSdkVersion
    buildToolsVersion rootProject.ext.buildToolsVersion
}
```

## 项目属性
当然上述在根下的build.gradle文件下使用`ext`声明变量外，还有一些其他方法声明属性变量为模块中的build.gradle来引用：

- ext代码块
- gradle.properties文件
- -P命令行参数

ext在前文中声明了一个local变量，同理在`gradle.properties`文件下也声明一个`propertiesFile`变量并赋值，`propertiesFile=hello world from properties`然后我们在根下的build.gradle文件中定义一个打印任务来把这些变量输出出来，具体如下代码

```php
task printProperties << {
    println local
    println propertiesFile
    if (project.hasProperty('cmd')) {
        println cmd
    }
}
```

使用命令`gradle printProperties -P cmd="hello world from cmd"`输出如下：
```
:printProperties
hello world, from buid.gradle
hello world from properties
hello world from cmd
```

## 默认任务配置
通常在根下的build.gradle文件中使用`defaultTask`来定义默认任务：

```
defaultTasks 'clean', 'iD'
```
这里我配置了`clean`和`installDebug`为默认的任务，每次命令行输入gradle或者./gradlew不加任何任务名时会默认构建`clean`和`installDebug`两个任务。























