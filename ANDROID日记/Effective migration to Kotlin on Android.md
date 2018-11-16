# Effective migration to Kotlin on Android



![img](https://cdn-images-1.medium.com/max/1600/0*fmIfWMQTJlwc6r56)

There are countless resources available to help you jumpstart on Kotlin: official documentation from [Google](https://developer.android.com/kotlin/get-started) and [JetBrains](https://kotlinlang.org/docs/tutorials/kotlin-android.html), [Google-IO](https://www.youtube.com/watch?v=6P20npkvcb8) [talks](https://www.youtube.com/watch?v=X1RVYt2QKQE), [codelabs](https://codelabs.developers.google.com/codelabs/build-your-first-android-app-kotlin/index.html#0), and an endless supply of blogpost and tutorial provided by the community. All these resources can introduce you to Kotlin’s type system, null-safety, extension functions, data classes, high order functions and all the other cool features that Kotlin provides.

However, when you start applying all this to a real Android codebase, not everything turns out to be as simple as it appears. Although Kotlin’s syntax is easy to pick up for a Java developer, it takes some time and practice in order to be able to write idiomatic code and effectively translate some of the widely-used patterns on Android development to Kotlin. Furthermore, many libraries are made redundant or at least require some adaptations to be made on how they are used, due to the features that Kotlin offers out of the box.

This article presents a collection of practical advice and tricks to help you out in the transition to Kotlin.

------

#### Custom view constructors

When creating a Custom View in Java, we have to override the 4 constructors that the `View` class defines. This is quite a bit of boilerplate.



<iframe width="700" height="250" data-src="/media/90b83c5a2cd4869445cdc0178142d24c?postId=cfb92bfaa49b" data-media-id="90b83c5a2cd4869445cdc0178142d24c" data-thumbnail="https://i.embed.ly/1/image?url=https%3A%2F%2Favatars0.githubusercontent.com%2Fu%2F15818524%3Fs%3D400%26v%3D4&amp;key=a19fcc184b9711e1b4764040d3dc5c07" class="progressiveMedia-iframe js-progressiveMedia-iframe" allowfullscreen="" frameborder="0" src="https://android.jlelse.eu/media/90b83c5a2cd4869445cdc0178142d24c?postId=cfb92bfaa49b" style="display: block; position: absolute; margin: auto; max-width: 100%; box-sizing: border-box; transform: translateZ(0px); top: 0px; left: 0px; width: 700px; height: 451.984px;"></iframe>

One of the first things we learn about defining classes in Kotlin is that we can use the implicit constructor that is part of the class header and it also allows us to define the class’s fields in one line.



<iframe width="700" height="250" data-src="/media/f813d29607deb09bb823f104dbb1bf63?postId=cfb92bfaa49b" data-media-id="f813d29607deb09bb823f104dbb1bf63" data-thumbnail="https://i.embed.ly/1/image?url=https%3A%2F%2Favatars0.githubusercontent.com%2Fu%2F15818524%3Fs%3D400%26v%3D4&amp;key=a19fcc184b9711e1b4764040d3dc5c07" class="progressiveMedia-iframe js-progressiveMedia-iframe" allowfullscreen="" frameborder="0" src="https://android.jlelse.eu/media/f813d29607deb09bb823f104dbb1bf63?postId=cfb92bfaa49b" style="display: block; position: absolute; margin: auto; max-width: 100%; box-sizing: border-box; transform: translateZ(0px); top: 0px; left: 0px; width: 700px; height: 82.9844px;"></iframe>

We then learn that it’s possible to define secondary constructors, using the `constructor` keyword. With secondary constructors, `MyCustomView` would look like this: (this is actually very similar to the code that Android Studio’s automatic conversion to Kotlin generates).



<iframe width="700" height="250" data-src="/media/ebf7a13363848b87b128ab4926c893fb?postId=cfb92bfaa49b" data-media-id="ebf7a13363848b87b128ab4926c893fb" data-thumbnail="https://i.embed.ly/1/image?url=https%3A%2F%2Favatars0.githubusercontent.com%2Fu%2F15818524%3Fs%3D400%26v%3D4&amp;key=a19fcc184b9711e1b4764040d3dc5c07" class="progressiveMedia-iframe js-progressiveMedia-iframe" allowfullscreen="" frameborder="0" src="https://android.jlelse.eu/media/ebf7a13363848b87b128ab4926c893fb?postId=cfb92bfaa49b" style="display: block; position: absolute; margin: auto; max-width: 100%; box-sizing: border-box; transform: translateZ(0px); top: 0px; left: 0px; width: 700px; height: 325px;"></iframe>

While this is valid Kotlin syntax, we can do better than that and reduce the boilerplate. By using the `@JvmOverloads` annotation, we can just define one constructor with the full argument list and provide default values for the optional ones. The annotation instructs the Kotlin compiler to generate the overloaded constructors.



<iframe width="700" height="250" data-src="/media/d5088824a574fcfe0d1c0c1809c2bdb7?postId=cfb92bfaa49b" data-media-id="d5088824a574fcfe0d1c0c1809c2bdb7" data-thumbnail="https://i.embed.ly/1/image?url=https%3A%2F%2Favatars0.githubusercontent.com%2Fu%2F15818524%3Fs%3D400%26v%3D4&amp;key=a19fcc184b9711e1b4764040d3dc5c07" class="progressiveMedia-iframe js-progressiveMedia-iframe" allowfullscreen="" frameborder="0" src="https://android.jlelse.eu/media/d5088824a574fcfe0d1c0c1809c2bdb7?postId=cfb92bfaa49b" style="display: block; position: absolute; margin: auto; max-width: 100%; box-sizing: border-box; transform: translateZ(0px); top: 0px; left: 0px; width: 700px; height: 171px;"></iframe>

#### Static factory methods for Fragments and Activities

One very popular pattern on Android is the use of static factory method for creating Fragments and Activities (actually in the case of Activities, the factory methods generate the Intent that is used to launch the Activity). Since Activities and Fragments are created by the Android framework, which means that we can’t pass arguments to the constructors of these classes, with the use of factory methods, we can encapsulate the creation code inside the actual class that we are instantiating, so that on the creation site we don’t have to worry about the extras names or other details related to the creation of the Fragment or Activity.



<iframe width="700" height="250" data-src="/media/5e90741b907888b5a78f36c9c08856b7?postId=cfb92bfaa49b" data-media-id="5e90741b907888b5a78f36c9c08856b7" data-thumbnail="https://i.embed.ly/1/image?url=https%3A%2F%2Favatars0.githubusercontent.com%2Fu%2F15818524%3Fs%3D400%26v%3D4&amp;key=a19fcc184b9711e1b4764040d3dc5c07" class="progressiveMedia-iframe js-progressiveMedia-iframe" allowfullscreen="" frameborder="0" src="https://android.jlelse.eu/media/5e90741b907888b5a78f36c9c08856b7?postId=cfb92bfaa49b" style="display: block; position: absolute; margin: auto; max-width: 100%; box-sizing: border-box; transform: translateZ(0px); top: 0px; left: 0px; width: 700px; height: 390.984px;"></iframe>

Since Kotlin doesn’t have static methods, converting this code requires the use of the Activity’s `companion object`.



<iframe width="700" height="250" data-src="/media/b105cff590278145167aa98a41c1739a?postId=cfb92bfaa49b" data-media-id="b105cff590278145167aa98a41c1739a" data-thumbnail="https://i.embed.ly/1/image?url=https%3A%2F%2Favatars0.githubusercontent.com%2Fu%2F15818524%3Fs%3D400%26v%3D4&amp;key=a19fcc184b9711e1b4764040d3dc5c07" class="progressiveMedia-iframe js-progressiveMedia-iframe" allowfullscreen="" frameborder="0" src="https://android.jlelse.eu/media/b105cff590278145167aa98a41c1739a?postId=cfb92bfaa49b" style="display: block; position: absolute; margin: auto; max-width: 100%; box-sizing: border-box; transform: translateZ(0px); top: 0px; left: 0px; width: 700px; height: 435px;"></iframe>

There are [articles](https://medium.com/@passsy/starting-activities-with-kotlin-my-journey-8b7307f1e460) that describe ways to try and make this more generic and extract it into a base activity, but I don’t think its worth the fuss.

Note that we can improve the code above by writing it in a more idiomatic way. First we can use the `apply` method, that allows us to chain a constructor call with method calls on the newly-created object. Then we can also use the `bundleOf` method of `android-ktx` [library](https://developer.android.com/kotlin/ktx) to simplify the creation of the extras.



<iframe width="700" height="250" data-src="/media/e339c3fa58b5296745eefb1a5932222c?postId=cfb92bfaa49b" data-media-id="e339c3fa58b5296745eefb1a5932222c" data-thumbnail="https://i.embed.ly/1/image?url=https%3A%2F%2Favatars0.githubusercontent.com%2Fu%2F15818524%3Fs%3D400%26v%3D4&amp;key=a19fcc184b9711e1b4764040d3dc5c07" class="progressiveMedia-iframe js-progressiveMedia-iframe" allowfullscreen="" frameborder="0" src="https://android.jlelse.eu/media/e339c3fa58b5296745eefb1a5932222c?postId=cfb92bfaa49b" style="display: block; position: absolute; margin: auto; max-width: 100%; box-sizing: border-box; transform: translateZ(0px); top: 0px; left: 0px; width: 700px; height: 171px;"></iframe>

#### Dagger

Dagger is an annotation library written for Java, that generates Java code. Its API and usage patterns contain some idioms that do not translate well to Kotlin. Migrating dagger code to Kotlin sometimes requires extra effort, and actually the resulting code seems a bit unnatural. Here’s a small collection of gotchas and tricks that we are forced to follow when dealing with Dagger in Kotlin.

- Field injection

The first struggle when introducing Dagger in a Kotlin project is how to define injected fields, complying with Kotlin’s nullability system. The solution is to define the field with `lateinit var`. So this (in Java):



<iframe width="700" height="250" data-src="/media/99f18f9636d887e041a20c81852f82ca?postId=cfb92bfaa49b" data-media-id="99f18f9636d887e041a20c81852f82ca" data-thumbnail="https://i.embed.ly/1/image?url=https%3A%2F%2Favatars0.githubusercontent.com%2Fu%2F15818524%3Fs%3D400%26v%3D4&amp;key=a19fcc184b9711e1b4764040d3dc5c07" class="progressiveMedia-iframe js-progressiveMedia-iframe" allowfullscreen="" frameborder="0" src="https://android.jlelse.eu/media/99f18f9636d887e041a20c81852f82ca?postId=cfb92bfaa49b" style="display: block; position: absolute; margin: auto; max-width: 100%; box-sizing: border-box; transform: translateZ(0px); top: 0px; left: 0px; width: 700px; height: 171px;"></iframe>

becomes:



<iframe width="700" height="250" data-src="/media/fe2f25d7b750e354cfe831c33f09110b?postId=cfb92bfaa49b" data-media-id="fe2f25d7b750e354cfe831c33f09110b" data-thumbnail="https://i.embed.ly/1/image?url=https%3A%2F%2Favatars0.githubusercontent.com%2Fu%2F15818524%3Fs%3D400%26v%3D4&amp;key=a19fcc184b9711e1b4764040d3dc5c07" class="progressiveMedia-iframe js-progressiveMedia-iframe" allowfullscreen="" frameborder="0" src="https://android.jlelse.eu/media/fe2f25d7b750e354cfe831c33f09110b?postId=cfb92bfaa49b" style="display: block; position: absolute; margin: auto; max-width: 100%; box-sizing: border-box; transform: translateZ(0px); top: 0px; left: 0px; width: 700px; height: 171px;"></iframe>

- Injecting named fields

Injecting a named field is quite easy in Java, you just annotate the field and the provision (`@Provides` or `@Binds`) method and you are done.



<iframe width="700" height="250" data-src="/media/6cdcbd32612fbfd6d214f8ebb882eb29?postId=cfb92bfaa49b" data-media-id="6cdcbd32612fbfd6d214f8ebb882eb29" data-thumbnail="https://i.embed.ly/1/image?url=https%3A%2F%2Favatars0.githubusercontent.com%2Fu%2F15818524%3Fs%3D400%26v%3D4&amp;key=a19fcc184b9711e1b4764040d3dc5c07" class="progressiveMedia-iframe js-progressiveMedia-iframe" allowfullscreen="" frameborder="0" src="https://android.jlelse.eu/media/6cdcbd32612fbfd6d214f8ebb882eb29?postId=cfb92bfaa49b" style="display: block; position: absolute; margin: auto; max-width: 100%; box-sizing: border-box; transform: translateZ(0px); top: 0px; left: 0px; width: 700px; height: 105px;"></iframe>

In Kotlin simply annotating the field like this will not work. You need to set the correct [use-site target](https://kotlinlang.org/docs/reference/annotations.html#annotation-use-site-targets) for the annotation:



<iframe width="700" height="250" data-src="/media/969354b7151ceec8c293a5065bb18a65?postId=cfb92bfaa49b" data-media-id="969354b7151ceec8c293a5065bb18a65" data-thumbnail="https://i.embed.ly/1/image?url=https%3A%2F%2Favatars0.githubusercontent.com%2Fu%2F15818524%3Fs%3D400%26v%3D4&amp;key=a19fcc184b9711e1b4764040d3dc5c07" class="progressiveMedia-iframe js-progressiveMedia-iframe" allowfullscreen="" frameborder="0" src="https://android.jlelse.eu/media/969354b7151ceec8c293a5065bb18a65?postId=cfb92bfaa49b" style="display: block; position: absolute; margin: auto; max-width: 100%; box-sizing: border-box; transform: translateZ(0px); top: 0px; left: 0px; width: 700px; height: 105px;"></iframe>

If the injected type is a primitive, an extra step is required: you also need to add the `@JvmField` annotation to instruct the Kotlin compiler to create a public field, so that Dagger can inject it.



<iframe width="700" height="250" data-src="/media/8035a53a8675e6c426c1c4076bf76fe8?postId=cfb92bfaa49b" data-media-id="8035a53a8675e6c426c1c4076bf76fe8" data-thumbnail="https://i.embed.ly/1/image?url=https%3A%2F%2Favatars0.githubusercontent.com%2Fu%2F15818524%3Fs%3D400%26v%3D4&amp;key=a19fcc184b9711e1b4764040d3dc5c07" class="progressiveMedia-iframe js-progressiveMedia-iframe" allowfullscreen="" frameborder="0" src="https://android.jlelse.eu/media/8035a53a8675e6c426c1c4076bf76fe8?postId=cfb92bfaa49b" style="display: block; position: absolute; margin: auto; max-width: 100%; box-sizing: border-box; transform: translateZ(0px); top: 0px; left: 0px; width: 700px; height: 127px;"></iframe>

Note that since we cannot use `lateinit` with primitives, we have to initialize the field with a default value.

- Static `@Provides` methods

It is a [recommended practice](https://medium.com/square-corner-blog/keeping-the-daggers-sharp-%EF%B8%8F-230b3191c3f) to use static `@Provides` methods whenever possible. But in Kotlin static methods do not exist. The replacement for static methods is to define a method in the class’s companion object, but in the case of a `@Provides` method, just doing so isn’t enough.
As shown in the complete solution below, we also need to add the `@JvmStatic`annotation to the method, in order to indicate to the compiler that it has to generate a static method that dagger can locate. Apart from that, we also need to annotate not only the module, but also the companion object with `@Module`.



<iframe width="700" height="250" data-src="/media/d904c13763a3bf36cd3a0de38f91e6ee?postId=cfb92bfaa49b" data-media-id="d904c13763a3bf36cd3a0de38f91e6ee" data-thumbnail="https://i.embed.ly/1/image?url=https%3A%2F%2Favatars0.githubusercontent.com%2Fu%2F15818524%3Fs%3D400%26v%3D4&amp;key=a19fcc184b9711e1b4764040d3dc5c07" class="progressiveMedia-iframe js-progressiveMedia-iframe" allowfullscreen="" frameborder="0" src="https://android.jlelse.eu/media/d904c13763a3bf36cd3a0de38f91e6ee?postId=cfb92bfaa49b" style="display: block; position: absolute; margin: auto; max-width: 100%; box-sizing: border-box; transform: translateZ(0px); top: 0px; left: 0px; width: 700px; height: 303px;"></iframe>

#### Butterknife

[Butterknife](http://jakewharton.github.io/butterknife/) is a very convenient and popular library that was used in the Java days to reduce the boilerplate required to get references to the Views from an inflated layout.

The [Android extensions plugin](https://kotlinlang.org/docs/tutorials/android-plugin.html) leaves us with no good reason to use Butterknife any more on Kotlin. The plugin generates extension properties for Activities, Fragments and other targets (including custom targets — check the [documentation](https://kotlinlang.org/docs/tutorials/android-plugin.html#layoutcontainer-support)), and Android Studio directly imports them, so you can seamlessly access the Views by just using their ids.

With the use of the plugin, this code:



<iframe width="700" height="250" data-src="/media/9e86c385102744e02a3d2965437513dc?postId=cfb92bfaa49b" data-media-id="9e86c385102744e02a3d2965437513dc" data-thumbnail="https://i.embed.ly/1/image?url=https%3A%2F%2Favatars0.githubusercontent.com%2Fu%2F15818524%3Fs%3D400%26v%3D4&amp;key=a19fcc184b9711e1b4764040d3dc5c07" class="progressiveMedia-iframe js-progressiveMedia-iframe" allowfullscreen="" frameborder="0" src="https://android.jlelse.eu/media/9e86c385102744e02a3d2965437513dc?postId=cfb92bfaa49b" style="display: block; position: absolute; margin: auto; max-width: 100%; box-sizing: border-box; transform: translateZ(0px); top: 0px; left: 0px; width: 700px; height: 368.984px;"></iframe>

can be simplified to this:



<iframe width="700" height="250" data-src="/media/e7d3159e93cbf2d429effe4af1f34333?postId=cfb92bfaa49b" data-media-id="e7d3159e93cbf2d429effe4af1f34333" data-thumbnail="https://i.embed.ly/1/image?url=https%3A%2F%2Favatars0.githubusercontent.com%2Fu%2F15818524%3Fs%3D400%26v%3D4&amp;key=a19fcc184b9711e1b4764040d3dc5c07" class="progressiveMedia-iframe js-progressiveMedia-iframe" allowfullscreen="" frameborder="0" src="https://android.jlelse.eu/media/e7d3159e93cbf2d429effe4af1f34333?postId=cfb92bfaa49b" style="display: block; position: absolute; margin: auto; max-width: 100%; box-sizing: border-box; transform: translateZ(0px); top: 0px; left: 0px; width: 700px; height: 259px;"></iframe>

Note that in order to be able to use the feature, you need to add the `kotlin-android-extension` plugin to your module’s `build.gradle` file, and for certain features, you also need to enable the `experimental` flag.



<iframe width="700" height="250" data-src="/media/8f989a11d04fbd89e6e273c42881657d?postId=cfb92bfaa49b" data-media-id="8f989a11d04fbd89e6e273c42881657d" data-thumbnail="https://i.embed.ly/1/image?url=https%3A%2F%2Favatars0.githubusercontent.com%2Fu%2F15818524%3Fs%3D400%26v%3D4&amp;key=a19fcc184b9711e1b4764040d3dc5c07" class="progressiveMedia-iframe js-progressiveMedia-iframe" allowfullscreen="" frameborder="0" src="https://android.jlelse.eu/media/8f989a11d04fbd89e6e273c42881657d?postId=cfb92bfaa49b" style="display: block; position: absolute; margin: auto; max-width: 100%; box-sizing: border-box; transform: translateZ(0px); top: 0px; left: 0px; width: 700px; height: 500.984px;"></iframe>

#### AutoValue

[AutoValue](https://github.com/google/auto/tree/master/value) is very useful for defining value-classes in Java: it helps eliminate all the boilerplate related to overriding the `equals`, `hashCode` and `toString`methods. 
However, Kotlin’s out-of-the-box support for [data classes](https://kotlinlang.org/docs/reference/data-classes.html) renders it redundant. And it does so by also offering a lower maintenance cost: when adding/removing a field to an AutoValue class, you have to manually update the factory method or the Builder, and although the IDE can help you with that it’s still an extra step that you need to follow. In Kotlin you just add the property in the constructor, and the compiler takes care of the rest.

Note that [AutoValue builders](https://github.com/google/auto/blob/master/value/userguide/builders.md) are also made obsolete with Kotlin, as they can be replaced by constructors with optional and named arguments.

#### Parcelable

Another source of boilerplate for Android is implementing the `Parcelable`interface. In Java-land there are numerous options available to help you out with the generation of this boilerplate, from Android Studio [plugins](https://plugins.jetbrains.com/plugin/7332-android-parcelable-code-generator), to [AutoValue](https://github.com/rharter/auto-value-parcel) [extensions](https://github.com/frankiesardo/auto-parcel) and [various](https://github.com/grandstaish/paperparcel) [libraries](https://github.com/johncarl81/parceler). There are actually so many options available, that even [articles](https://hk.saowen.com/a/b5060cf225768c0464e69c90624eeaa9f0a25a3a72ebc3e2f7ae88273627e467) that compare their advantages and disadvantages are available.

In Kotlin, the situation is simpler: the Kotlin android extension offers a zero-maintenance and low-overhead solution. You can just annotate your class with `@Parcelize` and the Kotlin compiler will generate the Parcelable implementation.



<iframe width="700" height="250" data-src="/media/acfd17e263a0ca41892123e978ac2918?postId=cfb92bfaa49b" data-media-id="acfd17e263a0ca41892123e978ac2918" data-thumbnail="https://i.embed.ly/1/image?url=https%3A%2F%2Favatars0.githubusercontent.com%2Fu%2F15818524%3Fs%3D400%26v%3D4&amp;key=a19fcc184b9711e1b4764040d3dc5c07" class="progressiveMedia-iframe js-progressiveMedia-iframe" allowfullscreen="" frameborder="0" src="https://android.jlelse.eu/media/acfd17e263a0ca41892123e978ac2918?postId=cfb92bfaa49b" style="display: block; position: absolute; margin: auto; max-width: 100%; box-sizing: border-box; transform: translateZ(0px); top: 0px; left: 0px; width: 700px; height: 171px;"></iframe>

#### Testing/Mockito

In Kotlin all classes are final/`closed` to inheritance by default, and this causes problems with Mockito, which creates mocks by subclassing the class to be mocked. There are three main solutions for this:

1. Use interfaces, and define your mocks to be of the interface type — then Mockito can create the mocks without problems. Extracting an interface for all classes, though, might be a bit of an overkill for certain projects.
2. Mockito does [offers a mechanism](https://github.com/mockito/mockito/wiki/What%27s-new-in-Mockito-2#mock-the-unmockable-opt-in-mocking-of-final-classesmethods) for allowing mocks of final classes. In order to enable it you just need to create the file `src/test/resources/mockito-extensions/org.mockito.plugins.MockMaker`containing the single line:
   `mock-maker-inline`
   Note that this comes with a performance penalty of up to 3x according to the official documentation.
3. Finally, the kotlin compiler [offers a plugin](https://kotlinlang.org/docs/reference/compiler-plugins.html) that treats all classes that are marked with a specific annotation as open by default. To enable it, you just need to add this to your gradle file
   `apply plugin: "kotlin-allopen"` 
   and then specify the annotation that you will use to mark the classes that should be treated as open.



<iframe width="700" height="250" data-src="/media/4964781aa991b638e585b2360d0ba98d?postId=cfb92bfaa49b" data-media-id="4964781aa991b638e585b2360d0ba98d" data-thumbnail="https://i.embed.ly/1/image?url=https%3A%2F%2Favatars0.githubusercontent.com%2Fu%2F15818524%3Fs%3D400%26v%3D4&amp;key=a19fcc184b9711e1b4764040d3dc5c07" class="progressiveMedia-iframe js-progressiveMedia-iframe" allowfullscreen="" frameborder="0" src="https://android.jlelse.eu/media/4964781aa991b638e585b2360d0ba98d?postId=cfb92bfaa49b" style="display: block; position: absolute; margin: auto; max-width: 100%; box-sizing: border-box; transform: translateZ(0px); top: 0px; left: 0px; width: 700px; height: 105px;"></iframe>

So, now that we’ve covered how we can empower mockito with the ability to create mocks, we will go through how we can actually create and use them in code. In Java, the standard Mockito usage would look like this:



<iframe width="700" height="250" data-src="/media/7df9e6020f3d9f77fcedbe85f218f6b6?postId=cfb92bfaa49b" data-media-id="7df9e6020f3d9f77fcedbe85f218f6b6" data-thumbnail="https://i.embed.ly/1/image?url=https%3A%2F%2Favatars0.githubusercontent.com%2Fu%2F15818524%3Fs%3D400%26v%3D4&amp;key=a19fcc184b9711e1b4764040d3dc5c07" class="progressiveMedia-iframe js-progressiveMedia-iframe" allowfullscreen="" frameborder="0" src="https://android.jlelse.eu/media/7df9e6020f3d9f77fcedbe85f218f6b6?postId=cfb92bfaa49b" style="display: block; position: absolute; margin: auto; max-width: 100%; box-sizing: border-box; transform: translateZ(0px); top: 0px; left: 0px; width: 700px; height: 346.984px;"></iframe>

If we want to translate directly this to Kotlin, we have two options:

- We can define the `collaborator` variable as nullable (`val collaborator: Dependency?`) so that it can be assigned by `MockitoAnnotations.initMocks`. Then we would have to always reference it with `?.` or `!!`
- Or we could alternatively define it as 
  `lateinit var collaborator: Collaborator` 
  which is not perfect either.

The [mockito-kotlin library](https://github.com/nhaarman/mockito-kotlin) offers a shorthand to create mocks, that at the same time doesn’t require to call `initMocks`, so we can initialize our mocks in just one line:



<iframe width="700" height="250" data-src="/media/513447003ce58fd6ea2c669abe4db35c?postId=cfb92bfaa49b" data-media-id="513447003ce58fd6ea2c669abe4db35c" data-thumbnail="https://i.embed.ly/1/image?url=https%3A%2F%2Favatars0.githubusercontent.com%2Fu%2F15818524%3Fs%3D400%26v%3D4&amp;key=a19fcc184b9711e1b4764040d3dc5c07" class="progressiveMedia-iframe js-progressiveMedia-iframe" allowfullscreen="" frameborder="0" src="https://android.jlelse.eu/media/513447003ce58fd6ea2c669abe4db35c?postId=cfb92bfaa49b" style="display: block; position: absolute; margin: auto; max-width: 100%; box-sizing: border-box; transform: translateZ(0px); top: 0px; left: 0px; width: 700px; height: 259px;"></iframe>

Another annoying thing when starting writing tests in Kotlin is that since `when` is a keyword, it causes a conflict with the method `Mockito.when` which is necessary for setting up our mocks. You have to use backticks to signal the compiler that it’s the method that you want to use and not the keyword.



<iframe width="700" height="250" data-src="/media/7666e91eb469bfe2860cadba8cc364c5?postId=cfb92bfaa49b" data-media-id="7666e91eb469bfe2860cadba8cc364c5" data-thumbnail="https://i.embed.ly/1/image?url=https%3A%2F%2Favatars0.githubusercontent.com%2Fu%2F15818524%3Fs%3D400%26v%3D4&amp;key=a19fcc184b9711e1b4764040d3dc5c07" class="progressiveMedia-iframe js-progressiveMedia-iframe" allowfullscreen="" frameborder="0" src="https://android.jlelse.eu/media/7666e91eb469bfe2860cadba8cc364c5?postId=cfb92bfaa49b" style="display: block; position: absolute; margin: auto; max-width: 100%; box-sizing: border-box; transform: translateZ(0px); top: 0px; left: 0px; width: 700px; height: 60.9844px;"></iframe>

The mockito-kotlin library offers an alias for the `Mockito.when` method, called `whenever` to avoid the name clash.



<iframe width="700" height="250" data-src="/media/c18d96e8746bd2be7edd1ad3ef7b0433?postId=cfb92bfaa49b" data-media-id="c18d96e8746bd2be7edd1ad3ef7b0433" data-thumbnail="https://i.embed.ly/1/image?url=https%3A%2F%2Favatars0.githubusercontent.com%2Fu%2F15818524%3Fs%3D400%26v%3D4&amp;key=a19fcc184b9711e1b4764040d3dc5c07" class="progressiveMedia-iframe js-progressiveMedia-iframe" allowfullscreen="" frameborder="0" src="https://android.jlelse.eu/media/c18d96e8746bd2be7edd1ad3ef7b0433?postId=cfb92bfaa49b" style="display: block; position: absolute; margin: auto; max-width: 100%; box-sizing: border-box; transform: translateZ(0px); top: 0px; left: 0px; width: 700px; height: 60.9844px;"></iframe>

### Conclusions

Kotlin’s features and idiomatic syntax can help us remove large amounts of boilerplate. At the same time, these powerful feature have made some of the libraries that belonged until now to the standard toolset of android developers, look almost redundant nowadays. Other libraries (like Dagger) seem a bit awkward and require extra effort when used with Kotlin: these libraries will either have to provide more Kotlin-friendly APIs, or they will be replaced by new Kotlin-first libraries that have started popping up.


  