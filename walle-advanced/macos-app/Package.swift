// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "WALLE",
    platforms: [
        .macOS(.v13)
    ],
    products: [
        .executable(
            name: "WALLE",
            targets: ["WALLE"]
        )
    ],
    dependencies: [
    ],
    targets: [
        .executableTarget(
            name: "WALLE",
            dependencies: [],
            path: "WALLE"
        )
    ]
)
