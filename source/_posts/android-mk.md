---
title: JNI开发之Android.mk
date: 2016-09-18 21:44:16
tags: [android, jni]
categories: [android]
---

ndk build脚本Android.mk,是c/c++文件和Android NDK直接的粘合剂。

# 综述
Android.mk文件位于项目目录jni/下的首层目录，并且描述了你构建系统中的资源以及共享库。它只是GNUmakefile构建复杂系统中的一个小小片段。Android.mk文件定义了Application.mk中设置的项目范围，构建系统以及你离开时未定义的环境变量。它也可以重新为指定的模块重写项目范围的设置。

<!--more-->
Android.mk解析时可以将项目中的资源以模块来分组。一个模块即是一个静态库，有又可以是共享库，也可以是一个单独可执行的文件。你可以在Android.mk中定义一个或者多个模块，并且在多个模块中使用相同的代码。构建系统只会把共享库（so）放置到你的应用包中（apk）。此外，静态库可以生成共享库。

在打包库文件的时候，构建系统会自动为你构建所有的细节。例如，你不需要在Android.mk中生成的文件里列出头文件或者显示的依赖。NDK构建系统会为你自动计算它们直接的关系和依赖。最后的结果就是在最新发布的NDK中也支新工具链/平台，而不需要触及Android.mk文件。

这种方式的构建模式和AOSP的构建系统非常相似。但是不同的是构建系统的实现是不一样的，他们的相似之处是一个有意的设计来决定要构建的目标，这样会使得应用程序开发人员更容易重用外部库的源代码。

# 基本
在了解复杂语法前有必要先看一看最基本的Android.mk语法，这部分使用Hello-JNI例子来解释最基本的语法。

一个Android.mk必须以LOCAL_PATH变量开始
```Makefile
LOCAL_PATH := $(call my-dir)
```
该变量指示本地源码在整个项目树中的位置。这里，使用宏函数`my-dir`，他是系统内建函数，返回当前目录所在的地址。

下一行声明了CLEAR_VARS变量，它也是系统内建函数。
```Makefile
include $(CLEAR_VARS)
```
`CLEAR_VARS`变量是一个特别的GNU makefile变量，它的作用是清理所有类似于LOCAL_XXX变量。例如`LOCAL_MODULE, LOCAL_SRC_FILES, LOCAL_STATIC_LIBRARIES`。注意，它不会清除LOCAL_PATH变量。CLEAR_VARS必须保持它的变量值，因为系统在解析所有构建GNU makefile控制文件时都会使用这个上下文，也就是说它会做为全局变量被使用。所以在描述每一个模块前需要重新声明该变量。

`LOCAL_MODULE`声明模块的名字，在应用中的每一个模块中只使用一次该变量
```Makefile
LOCAL_MODULE := hello-jni
```
每一个模块的名字必须唯一，并且不能包含空格。构建系统再生成本地共享库之后，会自动为`LOCAL_MODULE`添加前缀和后缀名字。例如，上述的声明最终会生成libhello-jni.so文件。

> 注意：如果你的模块名字已经定义了lib为开头，构建系统不会在添加lib前缀了，只会添加.so后缀。所以在源码原始调用中，例如libfoo.c仍然会产生一个共享对象文件叫做libfoo.so。这种行为是支持Android源码平台以Android.mk编译生成的库；所有这些库的名称都以lib为前缀命名的。

`LOCAL_SRC_FILES`是列举所有要编译的源文件，可以使用空格指定多个源文件：
```Makefile
LOCAL_SRC_FILES := hello-jni.c
```
`LOCAL_SRC_FILES`必须包含一组要编译为当前模块的c/c++源文件

最后一行是帮助系统打包为最终要编译的库
```Makefile
include $(BUILD_SHARED_LIBRARY)
```
`BUILD_SHARED_LIBRARY`变量指示GNU makefile脚本收集从最近一个`include`开始的所有以LOCAL_XXX定义的变量声明的信息，最终构建为一个共享库。

# 变量和宏定义（Variables and Macros）
在Android.mk文件中构建系统提供了很多合适的变量。所有这些变量都来自于预先定义的值中。还有就是你所指定的。
除了这些变量外，你也可以定义自己变量名。如果你这么做了，一定要记住NDK构建系统还保留了如下的变量名：

- 以LOCAL_为开头的变量名，例如LOCAL_MODULE
- 以PRIVATE_, NDK_, 或者 APP为开头的变量名，构建系统会在内部使用这些变量
- 全小写字母组成的，例如my-dir。构建系统也会在内部使用它

如果你需要在你的Android.mk文件中定义自己的方便的变量，我们推荐使用MY_为前缀的变量名。

## NDK-defined 变量
这部分讨论GNU Make变量，它在解析你的Android.mk文件之前由构建系统定义。在某些确定的情况下，NDK有可能会解析你的Android.mk文件很多次，并且每次使用不同的定义的变量来解析。

### CLEAR_VARS
该变量指示构建脚本不要在LOCAL_XXX变量附近定义。通常使用该变量在定义一个模块之前使用include来包含，例如
```Makefile
include $(CLEAR_VARS)
```
### BUILD_SHARED_LIBRARY
该变量表明将所有收集的以`LOCAL_XXX`的变量信息来作为构建环境。并且决定在你列出的资源中如何构建一个目标共享库。注意，在使用该变量前，要至少指定好`LOCAL_MODULE`和`LOCAL_SRC_FILES`两个变量。（详细信息[查看](#module-description)）
该变量语法如下：
```Makefile
include $(BUILD_SHARED_LIBRARY)
```
该变量一旦声明就会构建系统并且生成.so的共享库文件。

### BUILD_STATIC_LIBRARY
`BUILD_SHARED_LIBRARY`的一种变体，用于构建静态库。构建系统不会向你的项目包下拷贝静态库，但是可以使用它们来构建共享库（详细参考下面的`LOCAL_STATIC_LIBRARIES`和`LOCAL_WHOLE_STATIC_LIBRARIES`两个变量）。语法使用如下：
```Makefile
include $(BUILD_STATIC_LIBRARY)
```
该变量一旦声明就会在系统构建中生成.a文件。

### PREBUILT_SHARED_LIBRARY
告诉构建脚本使用指定的预编译的共享库（prebuilt shared library）。不像在`BUILD_SHARED_LIBRARY`和`BUILD_STATIC_LIBRARY`的情况下。在该变量制定后，脚本中的`LOCAL_SRC_FILES`的变量值不是指资源文件了。作为替代，它必须是单一路径来构建预编译的共享库。例如`foo/libfoo.so`。其语法如下所示：
```Makefile
include $(PREBUILT_SHARED_LIBRARY)
```
你也可以参照另外一个变量`LOCAL_PREBUILTS`用于构建预编译共享库，更多关于prebuilts的信息查看[使用Prebuilt Libraries](https://developer.android.com/ndk/guides/prebuilts.html)

### PREBUILT_STATIC_LIBRARY
和`PREBUILT_SHARED_LIBRARY`类似，但是是针对预编译静态库。更多信息查看[使用Prebuilt Libraries](https://developer.android.com/ndk/guides/prebuilts.html)

### TARGET_ARCH
CPU架构类型名称，它由AOSP来指定。对于一些兼容arm构建平台的称为`arm`，它不受CPU架构版本或者ABI（详细查看下面的TARGET_ARCH_ABI）影响。
该变量的值可以从Android.mk文件中定义的APP_ABI变量中取得。

### TARGET_PLATFORM
指定构建Android API Level（版本号）。例如，Android5.1系统图片对应的Android API level为22，即`android-22`。更完整的android版本对应表查看[Android NDK Native APIs](https://developer.android.com/ndk/guides/stable_apis.html)。下面是该变量的语法表示：
```Makefile
TARGET_PLATFORM := android-22
```

### TARGET_ARCH_ABI
该变量存储目标CPU和架构型号，当系统构建时会解析该变量。你可以指定一个或者多个如下biao列出的值，在多个值之间使用空格来分隔。下表就是ABI所支持的各个CPU和架构型号以及所对应的值

|CPU and architecture|Setting|
|:--|:--|
|ARMv5TE|armeabi|
|ARMv7|armeabi-v7a|
|ARMv8 AArch64|arm64-v8a|
|i686|x86|
|x86-64|x86_64|
|mips32 (r1)|mips|
|mips64 (r6)|mips64|
|All|all|

例如`ARMv8 AArch64`的CPU和架构，则声明如下：
```Makefile
TARGET_ARCH_ABI := arm64-v8a
```
> **注意：**，NDK 1.6_r1以上，该变量定义为`arm`

关于架构ABIs以及其兼容性问题，请参考[ABI Management](https://developer.android.com/ndk/guides/abis.html)

未来新的目标ABIs将会带来不同的参数值。

### TARGET_ABI
Android API level和ABI的串联，当以想要为一台真实设备测试指定的目标系统图片（system image）时该变量尤为有用。例如为64位arm设备上跑一个API Level为22的程序须有如下声明：
```Makefile
TARGET_ABI := android-22-arm64-v8a
```
> **注意：**NDK 1.6_r1以上，默认值为android-3-arm.


## Module-Description 变量
本节提到的这些变量是描述构建系统中的一个模块。每个模块的描述应该遵循如下流程：

1. 初始化或者叫未定义这些和模块相关的变量，使用`CLEAR_VARS`变量来完成。
2. 为模块的描述变量赋值。
3. 使用恰当的构建脚本来设置NDK构建系统，使用`BUILD_XXX`变量完成。

### LOCAL_PATH
该变量用于给出当前文件的路径。你必须在你的Android.mk的开头定义它。例如：
```Makefile
LOCAL_PATH := $(call my-dir)
```
在脚本中使用CLEAR_VARS变量是不会清除该变量的值。因此,你只需要定义该变量一次,即使你的Android.mk可文件描述了多个模块也没关系。

### LOCAL_MODULE
该变量存放你所要编译模块的名字。必须在所有的模块名称中唯一，也不能包含任何空格。在包含其他脚本之前（除非设置了`CLEAR_VARS`）必须要定义好该变量。你不需要添加任何的`lib`或者`.so`、`.a`的前缀和后缀，构建系统会自动为你添加合适的前缀和后缀的。纵观你的Android.mk或者Application.mk文件中，都要涉及到该模块名。例如，下行的脚本将会产生一个名为`libfoo.so`的静态共享库。
```Makefile
LOCAL_MODULE := "foo"
```
如果你想获得的静态共享库名不是以lib+上所要设置的名称的话，你可以使用`LOCAL_MODULE_FILENAME`变量来设置，这样生成的共享库即为该变量所设置的值。

### LOCAL_MODULE_FILENAME
这是一个可选的变量用来覆盖上述的`LOCAL_MODULE`变量。例如，使用`LOCAL_MODULE`设置的模块名称为foo，这时你可以使用该变量来强制系统生成的静态共享库名称为libnewfoo，代码如下：
```Makefile
LOCAL_MODULE := foo
LOCAL_MODULE_FILENAME := libnewfoo
```
对于静态共享库生成最终的名称为libnewfoo
> **注意：**你不能覆盖文件路径和文件后缀。

### LOCAL_SRC_FILES
该变量包含一组该模块所要构建的源文件（source file）。只有列出这些源文件才可以在构建系统构建时将这些文件传递到编译器上，因为构建系统会自动计算所有文件的关联以及依赖关系。
注意，你可以使用相对（LOCAL_PATH为根路径）或者绝对路径来指定这源文件。
我们强烈推荐使用相对路径来指定源文件，相对路径使得Android.mk更加轻便。
> **注意：**在构建文件中使用Unix风格的路径分隔符：斜杠（/）。构建系统是不认window风格的反斜杠（\）。

### LOCAL_CPP_EXTENSION
你可以使用该可选择的变量来指定一个文件的除了c++中的`.cpp`之外的扩展名。例如下行中改变扩展名称为.cxx(这里必须包括.<dot>)
```Makefile
LOCAL_CPP_EXTENSION := .cxx
```
从NDK r7开始，你可以指定多个扩展名的文件，例如
```Makefile
LOCAL_CPP_EXTENSION := .cxx .cpp .cc
```

### LOCAL_CPP_FEATURES
你可以使用该可选的变量来指定你的代码所要依赖的具体的C++特性。它可以使在构建过程中使用正确的编译器以及链接标记可用。对于预编译的二进制，也可以使用该变量声明所要依赖的特性，因此为了保证最后的链接工作正确无误，就要声明该变量并且设置相应的C++特性。我们推荐你使用该变量来代替在`LOCAL_CPPFLAGS`中声明`-frtti`和`-fexceptions `。
使用该变量允许构建系统在每一个模块中使用恰当的标记。使用`LOCAL_CPPFLAGS`变量会引起编译器使用所有指定的标记，而不是按照实际需要来进行。
例如，在代码中使用RTTI，可以做如下指定
```Makefile
LOCAL_CPP_FEATURES := rtti
```
在代码中使用C++的异常，可以做如下指定：
```Makefile
LOCAL_CPP_FEATURES := exceptions
```
你也可以为该变量指定多个值，例如：
```Makefile
LOCAL_CPP_FEATURES := rtti features
```
对于这些值的顺序是无关紧要的。

### LOCAL_C_INCLUDES
你可使用这个可选的变量指定一组路径来关联到NDK的`root`，该路径可以就可以指定将要编译的资源（C、C++文件），例如：
```Makefile
LOCAL_C_INCLUDES := sources/foo
```
或者
```Makefile
LOCAL_C_INCLUDES := $(LOCAL_PATH)//foo
```
在设置任何类似于包含标记位为`LOCAL_CFLAGS`或者`LOCAL_CPPFLAGS`之前要定义该变量。
当时用`ndk-gdb`进行native debug时候，构建系统也会自动使用`LOCAL_C_INCLUDES`定义的路径。

### LOCAL_CFLAGS
该可选变量是设置编译器标记位的，当构建C或者C++资源文件的时候会使用该变量定义的标记位进行构建。这样做到目的是指定额外的宏定义和编译选项。

在Android.mk文件中尝试改变优化/调试的级别。在Application.mk文件相关信息中，构建系统也可以自动操纵该标记位进行构建。该方式允许构建系统在调试阶段生成有意义的数据。

> **注意：**在android-ndk-1.5_r1中，相关标记位仅仅应用在C文件中，对于C++不支持。但是现在它们已经支持整个Android构建系统（你现在可以是使用`LOCAL_CPPFLAGS`变量来指定C++文件的标记位）

指定额外的包含路径可以使用下面的定义：
```Makefile
LOCAL_CFLAGS += -I<path>,
```
但是最好还是使用`LOCAL_C_INCLUDES`，因为那样做有可能应用在使用ndk-gdb进行的本地调试上的路径。

### LOCAL_CPPFLAGS
当只是编译C++文件的时候使用该可选的变量来添加标记位。它们一般都出现在`LOCAL_CFLAGS`之后的命令行中。
> **注意：**在android-ndk-1.5_r1中，相关的标记位会应用在C和C++文件中。这也非常正确的匹配到整个安卓构建系统中。为了给C或者C++指定标记位也可以使用`LOCAL_CFLAGS`

### LOCAL_STATIC_LIBRARIES
该变量存放一组静态共享库用于当前模块所要依赖的库。

如果当前模块是一个共享库或者一个可执行文件，那么该变量就会强制这些静态库链接到最终的结果二进制中。

如果当前模块是一个静态库，那么该变量只是简单的包含到其他模块所要依赖的一个或者一组库中。

### LOCAL_SHARED_LIBRARIES
该变量是在运行时模块所要依赖的共享库。这些信息在链接时间是非常必要的，并且在生成的文件中嵌入这些信息

### LOCAL_WHOLE_STATIC_LIBRARIES
该变量是`LOCAL_STATIC_LIBRARIES`一个变种，链接器应该作为整个归档与表达式相关联。更多有关整个归档的详细信息，查看GNU链接器[文档](http://ftp.gnu.org/old-gnu/Manuals/ld-2.9.1/html_node/ld_3.html)中的`--whole-archive`标记。

当在一些静态库中存在环形依赖的时候，该变量是非常有用的。当使用该变量构建一个共享库时，它会强制构建系统将所有的静态库中的对象文件添加到最终的二进制文件中。所以，当要生成可执行文件的时候，是不正确的。

### LOCAL_LDLIBS
该变量为构建你的共享库或者可执行文件提供了一组额外的链接器标记位。可以使用一个`-l`的前缀来传递指定系统库的名字。例如，下面的例子告诉链接器生成的模块在加载时候链接到/system/lib/libz.so
```Makefile
LOCAL_LDLIBS := -lz
```
[Android NDK Native APIs](https://developer.android.com/ndk/guides/stable_apis.html)提供了一组系统库接口。
> **注意：**如果你为静态库定义该变量，那么构建系统会忽略它，并且ndk-build打印警告提示。

### LOCAL_LDFLAGS
当构建你的共享库或者可执行文件时，指定构建系统链接器标记位。例如，下面的例子使用`ld.bfd`链接器在ARM/X86 GCC 4.6+ 上默认使用ld.gold
```Makefile
LOCAL_LDFLAGS += -fuse-ld=bfd
```
> **注意：**如果你为静态库定义该变量，构建系统会忽略它，并且ndk-build会打印警告提示。

### LOCAL_ALLOW_UNDEFINED_SYMBOLS
默认的，当构建系统遇到一个未定义的引用并且尝试构建共享库的时候，它就会抛出一个未定义的符号错误（undefined symbol error）。该错误可以帮你捕获你代码中的bugs

为了禁用该检查，设置该变量为true，注意该设置可能导致在运行时会加载共享可。
> **注意：**如果你为静态库定义了该变量，那么构建系统会忽略它，并且ndk-build会打印一个警告提示。

### LOCAL_ARM_MODE
默认的，构建系统会在*thumb*模式下生成ARM目标的二进制文件，该模式每条指令是16位宽,并且在thumb/目录下和STL库进行链接。为该变量定义相应的值会导致构建系统强制生成32位模式下的模块对象文件。例如：
```Makefile
LOCAL_ARM_MODE := arm
```
当然也可以命令构建系统在arm模式下只是构建指定的c文件，例如以.arm为后缀的文件。例如，下面的例子是告诉构建系统在ARM模式下总是编译bar.c，但是为了构建foo.c需要按照`LOCAL_ARM_MODE`所定义的值。
```Makefile
LOCAL_SRC_FILES := foo.c bar.c.arm
```
> **注意：**你也可以在Application.mk文件中定义`APP_OPTION`来强制构建系统生成ARM的二进制文件来进行调试。由于调试的工具链（toolchain debugger）不会去操作Thumb代码，所以需要为调试指定ARM的模式。

### LOCAL_ARM_NEON
该变量只要匹配你指定的armabi-v7a的ABI就会允许你在C或者C++代码中使用ARM高级的SIMD（NEON）GCC。

注意不是所有基于ARMv7的CPU都支持NEON来设置其扩展。基于这个原因，你必须在运行时进行安全检查。更多详细信息查看[NEON支持](https://developer.android.com/ndk/guides/cpu-arm-neon.html)和[cpu库](https://developer.android.com/ndk/guides/cpu-features.html)

可选地，你可以使用.neon后缀来指定构建系统只是编译特殊的支持NEON的资源文件。在下面的例子中，构建系统编译foo.c使用thumb和neon支持，bar.c使用thumb支持，zoo.c使用ARM和NEON的支持：
```Makefile
LOCAL_SRC_FILES = foo.c.neon bar.c zoo.c.arm.neon
```
如果使用后缀的方式，那么.arm必须再添加.neon的后缀。

### LOCAL_DISABLE_NO_EXECUTE
Android NDK r4添加了一个支持“NX比特”的安全特性。它在默认情况下是开启的，但是你可以通过该变量设置为`true`来禁用掉该特性。在没有充分的理由下我们不推荐这样做。

该特性不会修改ABI，并且只会在内核目标为ARMv6+的CPU设备上开启。在早些的CPU架构的机器上会运行未修改代码。

更多详细信息，查看[Wikipedia：NX bit](http://en.wikipedia.org/wiki/NX_bit)和[The GNU stack kickstart](http://www.gentoo.org/proj/en/hardened/gnu-stack.xml)

### LOCAL_DISABLE_RELRO
默认的，NDK所编译的代码会带有只读的重定位和GOT防护。该变量指示在运行时的链接器来标记一个确定的内存区域作为只读重定位，标记确定的安全属性（security exploits）例如重写GOT。注意这些保护措施只在ANdroid API 16或者更高版本上奏效。在低于API 16的平台上，这些代码依旧可以运行但是不会具有内存防护功能。

该变量默认也是开启的，但是你可以通过设置`true`来禁用该功能。同样没有充足的理由的话我们不推荐禁用它。

更多详细信息，查看 [RELRO: RELocation Read-Only](http://isisblogs.poly.edu/2011/06/01/relro-relocation-read-only/) 和 [Security enhancements in RedHat Enterprise Linux (section 6)](http://www.akkadia.org/drepper/nonselsec.pdf)。

### LOCAL_DISABLE_FORMAT_STRING_CHECKS
默认的，构建系统编译代码时后进行格式化字符串保护。如果非常量格式化的字符串被用于打印功能的时候会导致编译器错误。

该保护措施默认是开启的，当然设置为`true`会禁用该功能，同样我们不推荐禁用该功能。

### LOCAL_EXPORT_CFLAGS
该变量记录一组C/C++编译器标记位并且将其添加到`LOCAL_CFLAGS`为模块所定义的标记位。使用该变量配合使用`LOCAL_STATIC_LIBRARIES`或者`LOCAL_SHARED_LIBRARIES`变量。

例如，考虑下面一对模块：foo和bar，其中bar依赖foo模块：
```Makefile
include $(CLEAR_VARS)
LOCAL_MODULE := foo
LOCAL_SRC_FILES := foo/foo.c
LOCAL_EXPORT_CFLAGS := -DFOO=1
include $(BUILD_STATIC_LIBRARY)


include $(CLEAR_VARS)
LOCAL_MODULE := bar
LOCAL_SRC_FILES := bar.c
LOCAL_CFLAGS := -DBAR=2
LOCAL_STATIC_LIBRARIES := foo
include $(BUILD_SHARED_LIBRARY)
```
这里，当构建bar.c时候构建系统传递一个标记位为 -DFOO=1和 -DBAR=2给编译器。它也会预先考虑在当前模块的LOCAL_CFLAGS中导出标记位，所以你只需要简单的覆盖它就可以了。

除此之外，模块之间的关系是一个过渡关系：如果zoo依赖bar，而bar又依赖foo，那么zoo也要继承foo中导出的所有标记位。

最后，当在局部构建时，构建系统不会使用导出的标记位。因此，在上面的例子中，当构建foo/foo.c时不会将-DFOO=1的标记位传递给编译器。本地构建时，使用LOCAL_CFLAGS变量来替代。

### LOCAL_EXPORT_CPPFLAGS
该变量功能和`LOCAL_EXPORT_CFLAGS`一样，但是只对C++代码奏效。

### LOCAL_EXPORT_C_INCLUDES
该变量和`LOCAL_EXPORT_CFLAGS`功能一样，但是只针对C include路径。它也是非常有用的变量，例如，bar.c需要包含一个从foo模块而来的头文件。

### LOCAL_EXPORT_LDFLAGS
该变量和`LOCAL_EXPORT_CFLAGS`功能一样，但是只是针对链接器标记位。

### LOCAL_EXPORT_LDLIBS
该变量和`LOCAL_EXPORT_CFLAGS`变量功能类似，告诉构建系统传递一个指定一个具体系统库的名字给编译器。预先考虑`-l`指定每一个库的名字。

注意构建系统会附加导入链接器标记位给你的模块的`LOCAL_LDLIBS`变量。这样做的目的是由于Unix链接器的工作特性导致。

当模块foo是静态库并且有代码依赖于一个系统库时，该变量是非常有用的。你可以使用`LOCAL_EXPORT_LDLIBS`来导出一个依赖项，例如：
```Makefile
include $(CLEAR_VARS)
LOCAL_MODULE := foo
LOCAL_SRC_FILES := foo/foo.c
LOCAL_EXPORT_LDLIBS := -llog
include $(BUILD_STATIC_LIBRARY)

include $(CLEAR_VARS)
LOCAL_MODULE := bar
LOCAL_SRC_FILES := bar.c
LOCAL_STATIC_LIBRARIES := foo
include $(BUILD_SHARED_LIBRARY)
```
在该例子中，当构建libbar.so时，构建系统在链接器命令末端放置`-llog`参数。这样做会告诉连接器libbar.so依赖foo，并且也要依赖系统库logging。

### LOCAL_SHORT_COMMANDS
当你的模块有大量的源代码文件或者依赖大量的静态或者共享库时，就要设置该变量为true。这样做的目的也是强制构建系统使用@语法来归档包含中间对象文件或者链接库。

这个特性在Windows上是非常有用的，因为命令行接收最大的值为8191个字符，这个数对于一个复杂的项目是非常渺小的。它还影响单个源文件的编译,也会将几乎所有的编译器标志放置到内部列表文件中。

注意，除了true之外的任何值都将恢复默认行为。你也可以在Application.mk中定义`APP_SHORT_COMMANDS`变量来强制该行为。

我们不建议默认开启该特性，因为它将导致构建系统速度极具下降。

### LOCAL_THIN_ARCHIVE
当构建静态库的时候应该设置该变量为true。这样做将生成一个轻量级的归档，该归档不包含对象文件，但是代替它的是这些对象文件的路径。

这个变量对于构建输出尤其为输出文件瘦身来说是非常有用的。缺点就是不能随便挪动文件位置也就是改变文件路径。

合法的值为true，false或者空。默认值可以在Application.mk文件中通过`APP_THIN_ARCHIVE`变量设置。

> **注意：**该变量会忽略非静态库的模块或者预编译静态库的模块。

### LOCAL_FILTER_ASM
该变量作为构建系统中的一个shell命令被定义。构建系统使用它来过滤装配文件的提取或者从`LOCAL_SRC_FILES`指定的文件中生成。

定义该变量会引起以下事情的发生：

1. 构建系统会在C和C++文件中生成临时的装配文件，而不是由编译器生成的对象文件（.o）
2. 构建系统在临时的装配文件上或者其他由`LOCAL_SRC_FILES`生成的任何装配文件上执行`LOCAL_FILTER_ASM`声明的shell命令，因此会生成其他的临时装配文件。
3. 构建系统将这些装配文件编译为一个对象文件。

例如：
```Makefile
LOCAL_SRC_FILES  := foo.c bar.S
LOCAL_FILTER_ASM :=

foo.c --1--> $OBJS_DIR/foo.S.original --2--> $OBJS_DIR/foo.S --3--> $OBJS_DIR/foo.o
bar.S                                 --2--> $OBJS_DIR/bar.S --3--> $OBJS_DIR/bar.o
```
"1"对应的是编译器，"2"对应的是过滤器，"3"对应的是汇编器（assembler）。过滤器必须是一个独立的shell命令,输入文件的名称作为其第一个参数,输出文件作为第二个参数，例如：
```Makefile
myasmfilter $OBJS_DIR/foo.S.original $OBJS_DIR/foo.S
myasmfilter bar.S $OBJS_DIR/bar.S
```


## NDK提供的宏指令函数
这部分解释NDK中提供的GNU Make宏指令函数。使用`$(call <function>)`格式来激活命令。

### my-dir
该指令返回当前Android.mk所在的目录位置。`my-dir`对于在Android.mk中定义`LOCAL_PATH`非常有用。例如：
```Makefile
LOCAL_PATH := $(call my-dir)
```
由于使用的是GNU Make构建原理，宏指令实际返回的是上一个makefile所在的目录路径，基于这个原因，我们不应该在包含其他文件的源码下调用my-dir。

例如，考虑下面的例子
```Makefile
LOCAL_PATH := $(call my-dir)

# ... declare one module

include $(LOCAL_PATH)/foo/`Android.mk`

LOCAL_PATH := $(call my-dir)

# ... declare another module
```

这里存在的问题就是第二次调用`my-dir`并定义为`LOCAL_PATH`作为 `$PATH/foo`来替换`$PATH`

可以在最后使用额外的include来避免上述问题，例如
```Makefile
LOCAL_PATH := $(call my-dir)

# ... declare one module

LOCAL_PATH := $(call my-dir)

# ... declare another module

# extra includes at the end of the Android.mk file
include $(LOCAL_PATH)/foo/Android.mk

```
如果使用这种方式破坏了项目调用结构，那么可以使用一个其他的变量来存储第一个my-dir的值，例如：
```Makefile
MY_LOCAL_PATH := $(call my-dir)

LOCAL_PATH := $(MY_LOCAL_PATH)

# ... declare one module

include $(LOCAL_PATH)/foo/`Android.mk`

LOCAL_PATH := $(MY_LOCAL_PATH)

# ... declare another module
```

### all-subdir-makefiles
返回所有含有Android.mk文件子目录路径。

你可以使用该函数为一个深层嵌套的构建项目提供帮助。默认情况下，NDK构建只会寻找目录下的包含Android.mk文件。

### this-makefile
返回当前makefile的路径
### parent-makefile
返回当前makefile文件所在的目录树的父节点位置
### grand-parent-makefile
返回当前makefile文件所在的目录树的祖父节点位置

### import-module
该函数会寻找项目中的模块并且包含该模块的makefile文件（Android.mk）,例如
```Makefile
$(call import-module,<name>)
```
在上述例子中，构建系统首先在你的`NDK_MODULE_PATH`环境变量所引用的目录下寻找以<name>命名的模块，找到后自动包含它的Android.mk文件。

