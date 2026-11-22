plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

// Release signing: the committed StreamHub keystore keeps every GitHub Actions
// release (and any local assembleRelease) on the same key, so installs and
// updates never hit "app not installed" signature mismatches. The environment
// variables override the committed file for anyone who wants their own key.
val envKeystorePath = System.getenv("STREAMHUB_KEYSTORE_PATH")
val releaseKeystore: java.io.File = if (!envKeystorePath.isNullOrBlank()) {
    file(envKeystorePath)
} else {
    rootProject.file("signing/streamhub.keystore")
}
val releaseKeystorePassword: String =
    System.getenv("STREAMHUB_KEYSTORE_PASSWORD") ?: "streamhub"
val releaseKeyAlias: String =
    System.getenv("STREAMHUB_KEY_ALIAS") ?: "streamhub"
val releaseKeyPassword: String =
    System.getenv("STREAMHUB_KEY_PASSWORD") ?: "streamhub"
val hasReleaseSigning = releaseKeystore.exists()

android {
    namespace = "com.xspeen.streamhub"
    compileSdk = 35

    defaultConfig {
        applicationId = "com.xspeen.streamhub"
        minSdk = 24
        targetSdk = 34
        // CI overrides these from the release tag (-PversionName / -PversionCode)
        versionCode = (project.findProperty("versionCode") as String?)?.toInt() ?: 10004
        versionName = project.findProperty("versionName") as String? ?: "1.0.4"

        vectorDrawables {
            useSupportLibrary = true
        }
    }

    signingConfigs {
        if (hasReleaseSigning) {
            create("release") {
                storeFile = releaseKeystore
                storeType = "PKCS12"
                storePassword = releaseKeystorePassword
                keyAlias = releaseKeyAlias
                keyPassword = releaseKeyPassword
                enableV1Signing = true
                enableV2Signing = true
                enableV3Signing = true
            }
        }
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            isShrinkResources = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
            if (hasReleaseSigning) {
                signingConfig = signingConfigs.getByName("release")
            } else {
                // Keystore missing (e.g. stripped checkout): fall back to the
                // debug key so the APK still builds and stays installable.
                signingConfig = signingConfigs.getByName("debug")
            }
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    kotlinOptions {
        jvmTarget = "17"
    }

    sourceSets {
        getByName("main") {
            // The shared cross-platform web app lives at the repo root so the
            // Android, iOS and web builds all ship the exact same HTML.
            assets.srcDir("${rootProject.projectDir}/web")
        }
    }
}

dependencies {
    implementation("androidx.core:core-ktx:1.15.0")
    implementation("androidx.appcompat:appcompat:1.7.0")
    implementation("androidx.activity:activity-ktx:1.9.3")
    implementation("androidx.webkit:webkit:1.12.1")
}
